
let login_signup = document.getElementById("login_signup");
let logout = document.getElementById("logout");

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

login_mark.addEventListener("click", event => {
    let et = event.target;
    if (!login.contains(et) && !signup.contains(et)) {
        login.style.display = "none";
        signup.style.display = "none";
        login_mark.style.display = "none";
    }
});

// user_api
const user_url = "/api/user";

// GET
user_get()

function user_get(){
    fetch(user_url).then((res) => res.json())
    .then((data) => {
        if (data.data != null) {
            // login_signup.innerText = "登出系統";
            // login_signup.textContent = "登出系統";
            login_signup.classList.add("hide");
            logout.classList.remove("hide");
            console.log(data);
        } else {
            console.log(data);
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });
}

// POST


// PATCH


// DELECT
logout.addEventListener("click", user_logout)

function user_logout(){
    fetch(user_url,{method:'DELETE'}).then((res) => res.json())
    .then((data) => {
        if (data.ok) {
            logout.classList.add("hide");
            login_signup.classList.remove("hide");
            console.log(data);
        } 
    })
    .catch((error) => {
        console.log("err:", error)
    });
}
