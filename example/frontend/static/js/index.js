let baseUrl = 'http://127.0.0.1:4334'; //captcha host (not always necessary)

sleep = (milliseconds) => {return new Promise(resolve => setTimeout(resolve, milliseconds))}

// global
let text2;

// 5s countdown
async function timerIn() {
    for(let i = 5; i>0; i--){
        text2.innerText = `Restart in ${i}s!`
        await sleep(1000)
    }
    location.reload();
}

;(async () => {
    async function css(element, style){for (const property in style){element.style[property] = style[property];}}

    //maik captcha window
    let win = document.createElement('div');
    let img = document.createElement('img');
    let prompt = document.createElement('input');

    //css
    await css(win, {
        "position": "absolute",
        "top": "20%",
        "right": "50%",
        "transform": "translate(55%,-20%)",
    });

    await css(img, {
        "border-radius": "5px",
        "width": "50vh",
        "height": "50vh",
    });

    await css(prompt, {
        "position": "relative",
        "background-color": "#111",
        "border": "none",
        "border-radius": "5px",
        "width": "5vh",
        "height": "3vh",
        "left": "-50%",
        "top": "50px",
    });

    // make a request to the background generator

    let getCap = await fetch(baseUrl+"/captcha/generate", {"method": "POST"});

    // backend return values are {"tag": snowflake , "img": base64}
    let text = JSON.parse(await getCap.text());
    let tag = text['tag']

    img.src = "data:image/png;base64, "+text['img']

    win.appendChild(img);
    win.appendChild(prompt);
    document.body.appendChild(win);

    prompt.addEventListener("keydown", async (e) => {
        if(e.key === "Enter") {

            // make a request to validate captcha "answer"
            let sCap = await fetch(baseUrl+"/captcha/solve", {
                "headers": {"content-type": "application/json"},
                "body": JSON.stringify({"tag": tag, "answer": prompt.value}),
                "method": "POST"
            });

            let text = JSON.parse(await sCap.text());

            // make a simple notification

            let noti = document.createElement('div');
            let statustext = document.createElement('h1');
            text2 = document.createElement('h3');

            let cu = "green"

            if(text.responseCode != 0){
                cu = "red"
                statustext.innerText = "Wrong!";
                timerIn()
            } else {
                statustext.innerText = "Correct";
                text2.innerText = "Click to retry!"
            }

            await css(noti, {
                "position": "absolute",
                "border-radius": "5px",
                "top": "20%",
                "right": "50%",
                "transform": "translate(50%,-50%)",
                "width": "20vh",
                "height": "12vh",
                "background-color": cu,
                "cursor": "pointer",
            });

            noti.appendChild(statustext)
            noti.appendChild(text2)
            document.body.appendChild(noti)

            noti.addEventListener("mousedown", async (e) => {
                if(e.button == 0)
                    location.reload();
            })
        }
    })
})();
