var socket = io();
var buttons = document.querySelectorAll("button");


buttons.forEach((e,i)=>{
    e.onclick = (event)=>{
        event.preventDefault();
        socket.emit('login',i);
    }
});