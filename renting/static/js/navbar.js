const loginLink =
    document.getElementById("login-link");

const logoutButton =
    document.getElementById("logout-button");

const accessToken =
    localStorage.getItem("access_token");


if (accessToken) {

    loginLink.style.display = "none";

    logoutButton.style.display = "inline-block";

}


logoutButton.addEventListener("click", () => {

    localStorage.removeItem("access_token");

    localStorage.removeItem("refresh_token");

    window.location.href = "/login/";

});