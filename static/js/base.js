
let login_signup = document.getElementById("login_signup");

let login_mark = document.querySelector(".login_mark");
let login = document.querySelector("#login");
let login_close = document.querySelector("#login_close");
let signup = document.querySelector("#signup");
let signup_close = document.querySelector("#signup_close");
let signup_link = document.querySelector("#signup_link")
let login_link = document.querySelector("#login_link")

login_signup.addEventListener("click", show_1)
login_close.addEventListener("click",close_1)
signup_close.addEventListener("click",close_2)

signup_link.addEventListener("click",show_2)
login_link.addEventListener("click",show_1)

function show_1() {
    login_mark.style.display = "block";
    login.style.display = "flex";
    signup.style.display = "none";
}

function show_2() {
    login_mark.style.display = "block";
    signup.style.display = "flex";
    login.style.display = "none";
}

function close_1() {
    login_mark.style.display = "none";
    login.style.display = "none";
}

function close_2() {
    login_mark.style.display = "none";
    signup.style.display = "none";
}
