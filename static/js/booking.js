
// booking
let username = document.getElementById("username");
let message_name = document.getElementById("message-name");
let message_date = document.getElementById("message-date");
let message_time = document.getElementById("message-time");
let message_cost = document.getElementById("message-cost");
let message_address = document.getElementById("message-address");
let booking_image = document.querySelector(".booking-image");
let booking_cost = document.getElementById("booking-cost");

let booking_name = document.getElementById("booking_name");
let booking_email = document.getElementById("booking_email");
let booking_phone = document.getElementById("booking_phone");

let booking_delect = document.getElementById("booking-delect");

let booking_n = document.querySelector(".booking-no");
let booking_y = document.querySelector(".booking-yes");
let booking_c = document.querySelector(".booking-check");

const booking_url = "/api/booking";

// GET
booking_usercheck()

function booking_usercheck() {
    fetch(user_url).then((res) => res.json())
    .then((data) => {
        if (data.data != null) {
            username.textContent = data.data.name;
            booking_get();
            booking_name.value = data.data.name;
            booking_email.value = data.data.email;
        } else {
            document.location.href="/";
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });
}

function booking_get() {
    fetch(booking_url).then((res) => res.json())
    .then((data) => {
        if (data.data != null) {
            console.log(data);
            booking_data(data);
            booking_n.classList.add("bookinghide");
            booking_y.classList.remove("bookinghide");
            booking_c.classList.remove("bookinghide");
        } else {
            booking_n.classList.remove("bookinghide");
            booking_y.classList.add("bookinghide");
            booking_c.classList.add("bookinghide");
            console.log(data);
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });
}

function booking_data(data) {
    data = data.data;
    let time_choice = ["早上 9 點到下午 4 點","下午 2 點到晚上 9 點"];
    booking_image.style.backgroundImage = `url("${data.attraction.image}")`;
    message_name.textContent = data.attraction.name;
    message_date.textContent = data.date;
    if (data.time === "morning"){
        message_time.textContent = time_choice[0];
    } else if (data.time === "afternoon"){
        message_time.textContent = time_choice[1];
    }
    message_cost.textContent = data.price;
    message_address.textContent = data.attraction.address;
    booking_cost.textContent = data.price;
}


// DELECT
booking_delect.addEventListener("click", booking_del);

function booking_del() {
    fetch(booking_url,{method:'DELETE'}).then((res) => res.json())
    .then((data) => {
        if (data.ok) {
            console.log(data);
            booking_n.classList.add("bookinghide");
            booking_y.classList.remove("bookinghide");
            booking_c.classList.remove("bookinghide");
            document.location.href="/booking";
        } 
    })
    .catch((error) => {
        console.log("err:", error)
    });
}