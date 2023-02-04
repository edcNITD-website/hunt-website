function toggleMenu() {
    let menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
    menu.classList.toggle('flex');
}

// document.addEventListener('DOMContentLoaded', function () {
//     const faviconTag = document.getElementById("edc-icon");
//     const isDark = window.matchMedia("(prefers-color-scheme: dark)");

//     const changeFavicon = () => {
//         if(isDark.matches){
//             faviconTag.src = "/static/base/images/favicon_dark.ico";
//         }
//         else {
            
//             faviconTag.href = "/static/base/images/favicon.ico";
//         }
//     };
//     setInterval(changeFavicon,1000)
// });