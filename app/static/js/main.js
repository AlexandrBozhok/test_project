window.addEventListener("load", function(){
    function sendData(form){
        const XHR = new XMLHttpRequest();
        const FD = new FormData(form);
        var formDataObj = Object.fromEntries(new FormData(form));
        XHR.addEventListener("load", function(event){
            if(formDataObj.currency == 'eur'){
                redirectToPayPage(event.target.responseText);
            }
            else if(formDataObj.currency == 'usd'){
                window.location = event.target.responseText;
            }
            else if(formDataObj.currency == 'rub'){
                redirectToPayPage(event.target.responseText);
            }
        });
        XHR.addEventListener("error", function(event){
            alert('Oops! Something went wrong.');
        });
        XHR.open("POST", "/");
        XHR.send(FD);
    }

    function redirectToPayPage(obj){
        obj = JSON.parse(obj);
        var form = document.createElement('form');
        form.method = 'post';
        form.action = obj.url;
        form.acceptCharset = 'UTF-8';
        for (const [key, value] of Object.entries(obj.data)){
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = key;
            input.value = value;
            form.appendChild(input);
        }
        document.body.appendChild(form);
        form.submit();
    }

    const form = document.querySelector(".original-form");
    form.addEventListener("submit", function(event){
        sendData(this);
        event.preventDefault();
    });
});
