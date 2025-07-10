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