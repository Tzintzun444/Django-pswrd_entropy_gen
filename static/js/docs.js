document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("pre code").forEach((el) => {
        hljs.highlightElement(el);
    });
});

function navigateVersion(select) {
    const selected = select.value;
    window.location.href = `/docs/${selected}/`;
}