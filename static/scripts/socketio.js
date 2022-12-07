document.addEventListener('DOMContentLoaded', () => {
    // Connecting to socket server
//    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var socket = io.connect('https://tru-connect.herokuapp.com')
    let room = "Lounge";
    joinRoom("Lounge");

    // Display Incoming Messages
    socket.on('message', data => {
        const p = document.createElement('p');
        p.className = "text";
        const span_username = document.createElement("span");
        const br = document.createElement('br');

        if(data.username){
            span_username.innerHTML = data.username;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML;
            document.getElementById("display-message-section").append(p);
        }else{
            printSysMsg(data.msg);
        }
    });

    // Send Message
    document.getElementById("send_message").onclick = () => {
        socket.send({'msg':document.querySelector("#user_message").value,
    'username': userName, 'room': room});
    // Clear Input Box
    document.querySelector("#user_message").value = "";
    }

    // Making Enter key send message
    let msg = document.querySelector("#user_message");
    msg.addEventListener('keyup', event => {
        if(event.keyCode == 13){
            document.querySelector('#send_message').click();
        }
    })

    // Room Selection
    document.querySelectorAll(".select-room").forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `You are already in ${room} room.`
                printSysMsg(msg);
            }else{
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });

    // Leave Room
    function leaveRoom(room){
        socket.emit('leave', {'username': userName, 'room': room});
    }

    // Join Room
    function joinRoom(room){
        socket.emit('join', {'username': userName, 'room': room});
        // Clear Message Area
        document.querySelector('#display-message-section').innerHTML = '';
        // Autofocus on text box
        document.querySelector('#user_message').focus();
    }

    // Print System Message
    function printSysMsg(msg){
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }
})