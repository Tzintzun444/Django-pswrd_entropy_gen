document.addEventListener("DOMContentLoaded", function() {
    const inputs = document.querySelectorAll(".code-input");
    const form = document.getElementById("verification-form");

    inputs.forEach((input, index) => {

        input.addEventListener("input", (e) => {

            e.target.value = e.target.value.replace(/\D/g, '');

            if (e.target.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }

            const allFilled = Array.from(inputs).every(i => i.value.length === 1);
            if (allFilled) form.submit();
        });

        input.addEventListener("keydown", (e) => {
            const allowedKeys = [
                'Backspace', 'Delete', 'ArrowLeft', 'ArrowRight',
                'ArrowUp', 'ArrowDown', 'Tab', 'Home', 'End'
            ];

            if (allowedKeys.includes(e.key)) {
                if (e.key === 'Backspace' && !e.target.value && index > 0) {
                    inputs[index - 1].focus();
                    inputs[index - 1].select();
                }
                return;
            }

            if (e.ctrlKey || e.metaKey) {
                return;
            }

            if (!/^\d$/.test(e.key)) {
                e.preventDefault();
            }
        });

        input.addEventListener("paste", (e) => {
            e.preventDefault();
            const pasteData = e.clipboardData.getData('text').replace(/\D/g, '');

            if (pasteData.length >= 6) {
                for (let i = 0; i < 6; i++) {
                    inputs[i].value = pasteData[i] || '';
                }
                form.submit();
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const cooldownActive = document.getElementById("resend-data").dataset.blocked === "true";
    const btn = document.getElementById("resend-btn");
    const timer = document.getElementById("resend-timer");
    const timerDiv = document.getElementById("timer-div");
    let remaining = document.getElementById("remaining").dataset.remaining;

    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
    }

    if (cooldownActive) {
        btn.disabled = true;
        btn.classList.toggle('btn-disabled')
        timerDiv.style.display = "block"
        timer.textContent = `${formatTime(remaining)}`;

        const interval = setInterval(() => {
            remaining -= 1;
            if (remaining <= 0) {
                clearInterval(interval);
                btn.disabled = false;
                btn.classList.toggle('btn-disabled')
                timerDiv.style.display = "none"
                timer.textContent = "";
            } else {
                timer.textContent = `${formatTime(remaining)}`;
            }
        }, 1000);
    } else {
        btn.disabled = false;
        timer.textContent = "";
    }
});
