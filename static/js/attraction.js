
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
    let img_first = document.querySelector(".hide");
    img_first.className = "action";
    // img_first.classList.add("action");
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

function next_img (){

}

function previous_img (){

}


