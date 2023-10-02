// JavaScript for toggling the user dropdown menu
const userDropdown = document.getElementById("userDropdown");

// Close the dropdown if the user clicks outside of it
window.addEventListener("click", (event) => {
    if (!event.target.matches(".username-button")) {
        if (userDropdown.classList.contains("show")) {
            userDropdown.classList.remove("show");
        }
    }
});
