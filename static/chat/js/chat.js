var labelUsername = document.getElementById("label-username")
var usernameInput = document.getElementById("username")
var btnJoin = document.getElementById("btn-join")

var username;
var webSocket;

function webSocketOnMessage(event){
    var parsedData = JSON.parse(event.data)
    var message = parsedData['message'];
    console.log('message:' , message);
    console.log(event , "eventtttttt");

}

btnJoin.addEventListener('click' , () => {
    
    username = usernameInput.value;
    
    console.log( "username:" , username)



    if(username == ""){
        return;
    }
    usernameInput.value = '';
    usernameInput.value = true;
    usernameInput.value = 'hidden';

    btnJoin.disabled = true;
    btnJoin.style.visibility = 'hidden';

    var labelUsername = document.getElementById("label-username")
    labelUsername.innerHTML = username

    var loc = window.location;
    var wsStart = "ws://";

    if (loc.protocol == 'https:'){
        wsStart = 'wss://';
    }

    var endPoint = wsStart + loc.host + loc.pathname;
    console.log('endPoint:' , endPoint)

    webSocket = new WebSocket(endPoint);
    webSocket.addEventListener("open", (e) => {
        console.log("Connection Opend!")
    } )
    webSocket.addEventListener("message", webSocketOnMessage);
    
    webSocket.addEventListener("close", (e) => {
        console.log("Connection closed!")

    } )
    webSocket.addEventListener("error", (e) => {
        console.log("error Occurred!")

    } )
})