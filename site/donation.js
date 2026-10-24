"use strict";
// Amount selection only. No payments, bank login, network calls or stored pledges.
(() => {
  const allowedAmounts = new Set([1000, 5000, 10000, 30000, 50000, 100000, 200000, 500000, 1000000]);
  const choices = [...document.querySelectorAll(".amount-choice")];
  const display = document.getElementById("selected-amount");
  const guide = document.getElementById("transfer-guide");
  const copy = document.getElementById("copy-amount");
  const status = document.getElementById("copy-status");
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
