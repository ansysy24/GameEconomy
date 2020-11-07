// const balance = JSON.parse(document.getElementById('balance').textContent);

const chatSocket = new WebSocket(
    'wss://'
    + window.location.host
    + '/ws/socket/'
);

chatSocket.onmessage = function(e) {
    var bal = JSON.parse(e.data).balance;
    var show = JSON.parse(e.data).show_messages
    if (show){
    alert('winner, new balace is ' + bal + 'f');
    }
    $('#balance').text(bal + 'f');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
