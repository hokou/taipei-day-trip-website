
// 串接 API
const locationurl = location.href;

let attraction_name = document.querySelector("#name");
let attraction_category = document.querySelector("#category");
let attraction_mrt = document.querySelector("#mrt");
let attraction_description = document.querySelector("#description");
let attraction_address = document.querySelector("#address");
let attraction_transport = document.querySelector("#transport");
let attraction_images = document.querySelector(".images");
let attraction_po = document.querySelector(".po");

attraction_fetch(locationurl);

function attraction_fetch(attractionurl) {
    let attractionarray = attractionurl.split("/");
    let id = attractionarray[attractionarray.length-1];
    let url = `/api/attraction/${id}`;
    fetch(url).then(response => response.json())
        .then((result) => {
            console.log(result.data);
            attraction_create(result.data);
            setdate();
        }).catch(error => console.log("err:", error));        
}

function attraction_create(data){
    let name = data.name;
    document.title = `台北一日遊-${name}`;
    attraction_name.innerText = name;
    attraction_category.innerText = data.category;
    attraction_mrt.innerText = data.mrt;
    attraction_description.innerText = data.description;
    attraction_address.innerText = data.address;
    attraction_transport.innerText = data.transport;
    let imgs = data.images;
    for (let img of imgs) {
        let imgelement = document.createElement('img');
        let poelement = document.createElement('div');
        imgelement.src = img;
        attraction_images.appendChild(imgelement);
        attraction_po.appendChild(poelement);
        imgelement.classList.add('hide');
        poelement.classList.add('p');
    }
    // 只會選第 1 個;
    let img_first = document.querySelector(".hide");
    img_first.classList.add("action");
    // img_first.className = "action";
    let po_first = document.querySelector(".p");
    po_first.classList.add("p_action");
    // po_first.className += " p_action";
}

// == 更換上半天、下半天

let timeselection = document.getElementsByClassName('time-selection')[0];
// console.log(timeselection);
timeselection.addEventListener("change",timechange);

// 使用 id
function timechange(){
    let AM = document.querySelector('#AM');
    let PM = document.querySelector('#PM');
    let price = document.querySelector('#price');
    if (AM.checked) {
        price.innerText = 2000;
    } else if (PM.checked) {
        price.innerText = 2500;
    }
}

// 使用 name
// function timechange(){
//     let select = document.querySelector('[name=time]:checked');
//     let price = document.querySelector("#price");
//     if (select.value === "AM") {
//         price.innerText = 2000;
//     } else if (select.value === "PM") {
//         price.innerText = 2500;
//     }
// }


// == 影像輪播切換

let slideindex = 0;
let timeout = 4000;
let prevBtn = document.querySelector("#prevBtn");
let nextBtn = document.querySelector("#nextBtn");
let img_all = document.getElementsByClassName("hide");
let po_all = document.getElementsByClassName("p");

prevBtn.addEventListener("click", previous_img)
nextBtn.addEventListener("click", next_img)

function next_img(){
    let img_num = img_all.length;
    let nextindex = slideindex + 1;
    if (nextindex >= img_num) {
        nextindex = 0;
    }
    img_all[nextindex].classList.add('action');
    img_all[slideindex].classList.remove('action');
    po_all[nextindex].classList.add('p_action');
    po_all[slideindex].classList.remove('p_action');
    if (slideindex >= img_num -1 ) {
        slideindex = 0;
    } else {
        slideindex ++;
    }
}

function previous_img(){
    let img_num = img_all.length;
    let previndex = slideindex - 1;
    if (previndex <= -1) {
        previndex = img_num-1;
    }
    img_all[previndex].classList.add('action');
    img_all[slideindex].classList.remove('action');
    po_all[previndex].classList.add('p_action');
    po_all[slideindex].classList.remove('p_action');
    if (slideindex <= 0 ) {
        slideindex = img_num-1;
    } else {
        slideindex --;
    }
}

setInterval('next_img()',timeout);

// document.write('<script src="js/base.js"></script>');
// 設定日期 min

function setdate(){
    let today = new Date();
    let year = today.getFullYear();
    let month = today.getMonth();
    let date = today.getDate();
    let tommorow = `${year}-${(month+1).toString().padStart(2, "0")}-${(date+1).toString().padStart(2, "0")}`;
    let bookingDate = document.getElementById("bookingDate");
    bookingDate.setAttribute('min', tommorow);
    console.log(tommorow);
}

const booking_url = "/api/booking";

let booking_form = document.getElementById("booking-form");
let booking_message = document.getElementById("booking_message");

booking_form.addEventListener("submit", e => {
    e.preventDefault();
    user_check();
})

booking_form.addEventListener("click", () => {
    booking_message.textContent="";
});

function user_check() {
    fetch(user_url).then((res) => res.json())
    .then((data) => {
        if (data.data != null) {
            login_signup.classList.add("menuhide");
            logout.classList.remove("menuhide");
            console.log("true",data);
            booking_check();
        } else {
            show_1();
            console.log("false",data);
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });
}

function booking_check() {
    let attractionarray = locationurl.split("/");
    let id = attractionarray[attractionarray.length-1];
    let bookingDate = document.getElementById("bookingDate");
    let checkedValue = document.querySelector(".booking-time:checked").value;
    let price = document.getElementById("price");
    let booking_data = {
        "attractionId": Number(id),
        "date": bookingDate.value,
        "time": checkedValue,
        "price": Number(price.innerText)
    };
    console.log(booking_data);

    fetch(booking_url,{
        method:'POST',
        body:JSON.stringify(booking_data),
        headers: {
            'Content-Type': 'application/json'
          }
    }).then((res) => res.json())
    .then((data) => {
        if (data.ok) {
            console.log(data);
            booking_message.textContent = "預訂成功，5 秒後進入預訂頁面或直接點擊進入";
            setTimeout('document.location.href="/booking"', 5000);
        } else if (data.error) {
            console.log(data);
            booking_message.textContent = data.message;
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });

}
