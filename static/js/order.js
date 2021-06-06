// order
let appID = 20483;
let appKey = 'app_QLFiqzrrn2UCRz37LDZ3vBwNW7A5RdXoLifptkVFd8j9HPialfsBOD5kkwwz';
let serverType = "sandbox";
let bookingbtn = document.getElementById("bookingbtn");
let booking_form = document.getElementById("booking-form");
let check_message = document.getElementById("check-message");

const order_url = "/api/orders";

TPDirect.setupSDK(appID, appKey, serverType);

let fields = {
    number: {
        // css selector
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        // DOM object
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'ccv'
    }
}

TPDirect.card.setup({
    // Display ccv field
    fields: fields,
    styles: {
        // Style all elements
        'input': {
            'color': 'gray'
        },
        // Styling ccv field
        'input.ccv': {
            // 'font-size': '16px'
        },
        // Styling expiration-date field
        'input.expiration-date': {
            // 'font-size': '16px'
        },
        // Styling card-number field
        'input.card-number': {
            // 'font-size': '16px'
        },
        // style focus state
        ':focus': {
            // 'color': 'black'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        },
        // Media queries
        // Note that these apply to the iframe, not the root window.
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    }
})

booking_form.addEventListener("submit", e => {
    e.preventDefault();
    check_message.textContent = "";
    tappay_prime();
})

function tappay_prime() {

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus();

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        check_message.textContent = "TapPay 驗證錯誤";
        console.log('can not get prime');
        return
    }

    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            check_message.textContent = "TapPay 驗證錯誤";
            console.log('get prime error');
            console.log(result.msg);
            return
        }
        check_message.textContent = "TapPay 驗證成功";
        console.log('get prime success');
        console.log(result.card.prime);
        let prime = result.card.prime;
        order_post(prime);
    })
}

async function order_post(prime) {
    let data = await order_json(prime);
    fetch(order_url,{
        method:'POST',
        body:JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
          }
    }).then((res) => res.json())
    .then((data) => {
        console.log(data);
        if (data.data.payment.status === 0 ) {
            console.log(data);
            let orderNumber = data.data.number;
            check_message.textContent = data.data.payment.message;
            document.location.href = `/thankyou?number=${orderNumber}`;
        } else if (data.data.payment.status !== 0) {
            console.log(data);
            check_message.textContent = data.data.payment.message;
        } else if (data.error) {
            console.log(data);
            check_message.textContent = data.message;
        }
    })
    .catch((error) => {
        console.log("err:", error)
    });

}


async function order_json(prime) {
    let res = await fetch(booking_url);
    let booking_data = await res.json();
    booking_data = booking_data.data;
    let price = booking_data.price;
    delete booking_data.price;
    let contact = contact_data();
    let data = {
        "prime": prime,
        "order": {
            "price": price,
            "trip": booking_data,
        },
        "contact": contact
    }
    return data
}

function contact_data() {
    let booking_name = document.getElementById("booking_name")
    let booking_email = document.getElementById("booking_email")
    let booking_phone = document.getElementById("booking_phone")
    let data = {
        "name": booking_name.value,
        "email": booking_email.value,
        "phone": booking_phone.value
    };
    return data
}