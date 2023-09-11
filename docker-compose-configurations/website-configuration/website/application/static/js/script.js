// JavaScript for toggling the user dropdown menu
const loginBtn = document.getElementById("loginBtn");
const userDropdown = document.getElementById("userDropdown");

loginBtn.addEventListener("click", () => {
    userDropdown.classList.toggle("show");
});

// Close the dropdown if the user clicks outside of it
window.addEventListener("click", (event) => {
    if (!event.target.matches(".username-button")) {
        if (userDropdown.classList.contains("show")) {
            userDropdown.classList.remove("show");
        }
    }
});

// Toggle the menu icon for small screens
const menuIcon = document.querySelector(".menu-icon");
const navbar = document.querySelector(".navbar");

menuIcon.addEventListener("click", () => {
    navbar.classList.toggle("active");
});