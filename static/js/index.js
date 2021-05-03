
const attractions_url = "/api/attractions";

let now_page = 0;
let next_page = now_page +1;
let load_state = false;
let searchkeyword = document.getElementById("searchkeyword");


function attractions_fetch(url, now_page, keyword=null){
    if (now_page !== null) {
        if (keyword === null) {
            url = url + "?page=" + now_page;
            // console.log("n=",url);
        }else {
            url = url + "?page=" + now_page + "&keyword=" + keyword;
            // console.log("y=",url);
        }
        // console.log("now=",now_page);
        fetch(url).then(function(response){
            return response.json();
        }).then(function(result){
            // console.log(result);
            if (result.error !== true){
                next_page = result.nextPage;
                // console.log("next",next_page);
                let data = result.data;
                // console.log(data);
                attractions_create(data);
            }else {
                let message = result.message;
                show_message(message);
                alert(message);
            }
        }).catch(function(err){
            console.log("err:",err);
        });
    }
};

function attractions_create(result){
    let attraction = document.querySelector(".attraction-row");
    for (let i=0;i<result.length;i++){
        let title = result[i].name;
        let mrt = result[i].mrt;
        let cat = result[i].category;
        let img = result[i].images[0];

        let div_box = document.createElement("article");
        let div_img = document.createElement("div");
        let att_img = document.createElement("img");
        let div_text = document.createElement("div");
        let div_title = document.createElement("div");
        let div_data = document.createElement("div");
        let div_mrt = document.createElement("div");
        let div_cat = document.createElement("div");

        div_box.className = "attraction-box";
        div_img.className = "attraction-img";
        att_img.src = img;
        div_text.className = "attraction-text";
        div_title.className = "attraction-title";
        div_title.textContent = title;
        div_data.className = "attraction-data";
        div_mrt.className = "attraction-mrt";
        div_mrt.textContent = mrt;
        div_cat.className = "attraction-cat";
        div_cat.textContent = cat;

        attraction.appendChild(div_box);
        div_box.appendChild(div_img);
        div_img.appendChild(att_img);
        div_box.appendChild(div_text);
        div_text.appendChild(div_title);
        div_text.appendChild(div_data);
        div_data.appendChild(div_mrt);
        div_data.appendChild(div_cat);
    }
    load_state = true;
};


attractions_fetch(attractions_url,now_page);


// let i = 1;
if (next_page !== null){
    // console.log("next=",next_page);
    window.addEventListener('scroll',()=>{
        if(((window.innerHeight + window.scrollY) > (document.body.getBoundingClientRect().bottom)) && load_state) {
            now_page = next_page;
            attractions_fetch(attractions_url,next_page,searchkeyword.value);
            load_state = false;
            // console.log("---->",i);
            // i++;
        }
      });
}

function search() {
    let attractionrow = document.querySelector(".attraction-row");
    attractionrow.innerHTML = '';
    now_page = 0;
    console.log("search=",searchkeyword.value);
    attractions_fetch(attractions_url,now_page,searchkeyword.value);
}

function show_message(message) {
    let attraction = document.querySelector(".attraction-row");
    let mes = document.createElement("span");
    mes.style.margin = "20px auto";
    mes.textContent = message;
    attraction.appendChild(mes);
}