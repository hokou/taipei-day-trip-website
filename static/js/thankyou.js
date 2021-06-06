// order
let username = document.getElementById("username");
let message_error = document.getElementById("message-error");
let message_number = document.getElementById("message-number");
let message_status = document.getElementById("message-status");
let message_price = document.getElementById("message-price");
let message_name = document.getElementById("message-name");
let message_date = document.getElementById("message-date");
let message_time = document.getElementById("message-time");

let order_n = document.querySelector(".order-no");
let order_y = document.querySelector(".order-yes");

let params = (new URL(document.location)).searchParams;
let number = params.get('number');

const order_url = "/api/order";

order_usercheck()

function order_usercheck() {
    fetch(user_url).then((res) => res.json())
    .then((data) => {
        if (data.data != null) {
            username.textContent = data.data.name;
            order_get();
        } else {
            document.location.href="/";
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });
}

// GET
function order_get() {
    let url = `${order_url}/${number}`;
    fetch(url).then((res) => res.json())
    .then((data) => {
        if (data.data != null) {
            console.log(data);
            order_data(data);
            // order_n.classList.add("orderhide");
            order_y.classList.remove("orderhide");
        } else {
            order_n.classList.remove("orderhide");
            // order_y.classList.add("orderhide");
            console.log(data);
            message_error.textContent = "沒有訂單資料";
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });
}


function order_data(data) {
    let data_json = data.data;
    let trip = data_json.trip;
    console.log(trip);
    let time_choice = ["早上 9 點到下午 4 點","下午 2 點到晚上 9 點"];
    let status_choice = ["付款成功","付款失敗"];
    console.log(data_json.number);
    message_number.textContent = data_json.number;
    if (data_json.status === 0){
        message_status.textContent = status_choice[0];
    } else {
        message_status.textContent = status_choice[1];
    }
    message_price.textContent = data_json.price;
    message_name.textContent = trip.attraction.name;
    message_date.textContent = trip.date;
    if (trip.time === "morning"){
        message_time.textContent = time_choice[0];
    } else if (trip.time === "afternoon"){
        message_time.textContent = time_choice[1];
    }
}