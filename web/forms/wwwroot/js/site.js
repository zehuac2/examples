// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.
window.onload = () => {
    const prefersDark = matchMedia('(prefers-color-scheme: dark)');

    if (prefersDark.matches) {
        document.body.setAttribute('data-bs-theme', 'dark');
    }
};