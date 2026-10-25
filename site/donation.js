"use strict";
// Amount/account display and copy only. No bank login, network calls or donor storage.
(() => {
  const allowedAmounts = new Set([1000, 5000, 10000, 30000, 50000, 100000, 200000, 500000, 1000000]);
  const choices = [...document.querySelectorAll(".amount-choice")];
  const display = document.getElementById("selected-amount");
  const guide = document.getElementById("transfer-guide");
  const copy = document.getElementById("copy-amount");
  const status = document.getElementById("copy-status");
  const accountCopy = document.getElementById("copy-account");
  accountCopy.disabled = false;
  accountCopy.addEventListener("click", async () => {
    accountCopy.disabled = true;
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText("9002171898325");
      status.textContent = "계좌번호를 복사했습니다. 은행 앱에서 새마을금고와 예금주 동강대학교(발전기금관리위원회)를 확인해 주세요.";
    } catch {
      status.textContent = "복사를 사용할 수 없습니다. 계좌번호 9002-1718-9832-5를 길게 눌러 직접 복사해 주세요.";
    } finally { accountCopy.disabled = false; }
  });
  let selectedAmount = null;
  const format = amount => new Intl.NumberFormat("ko-KR").format(amount) + "원";
  for (const button of choices) {
    const amount = Number(button.dataset.amount);
    if (!allowedAmounts.has(amount)) continue;
    button.disabled = false;
    button.addEventListener("click", () => {
      selectedAmount = amount;
      choices.forEach(choice => choice.setAttribute("aria-pressed", String(choice === button)));
      display.textContent = format(amount);
      status.textContent = "";
      copy.disabled = false;
      // Keep keyboard focus on the amount button for choosing another amount.
      // Scroll only when the transfer guide is below the visible viewport.
      const rect = guide.getBoundingClientRect();
      if (rect.top >= window.innerHeight) {
        guide.scrollIntoView({block: "start", behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth"});
      }
    });
  }
  copy.addEventListener("click", async () => {
    if (!allowedAmounts.has(selectedAmount)) return;
    const amount = selectedAmount;
    copy.disabled = true;
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(String(amount));
      if (selectedAmount === amount) status.textContent = format(amount) + "을 복사했습니다. 아직 송금되지 않았습니다.";
    } catch {
      if (selectedAmount === amount) status.textContent = "복사를 사용할 수 없습니다. 선택한 금액 " + format(amount) + "을 직접 입력해 주세요.";
    } finally {
      copy.disabled = !allowedAmounts.has(selectedAmount);
    }
  });
})();
