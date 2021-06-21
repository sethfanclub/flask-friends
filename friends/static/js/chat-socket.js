var socket
document.addEventListener('DOMContentLoaded', function() {
   socket = io.connect('http://'+document.domain+':'+location.port+'/chatroom')
   socket.on('message', function(data) {
      console.log(data)
      sendMessage(data.text, data.imgURL)
   })
})

let messages = document.getElementById('messages')
let sendButton = document.getElementById('message-send')
let textInput = document.getElementById('message-input')
sendButton.onclick = function() {
   prepareMessage()
}
textInput.addEventListener('keypress', function(e) {
   if (e.which == 13) {
      prepareMessage()
   }
})
function prepareMessage() {
   text = textInput.value 
   socket.emit('send_message', text)
   textInput.value = ''
}
function sendMessage(text, imgURL) {
   newMessage = document.createElement('li') 
   newMessage.classList.add('d-flex')
   newMessage.classList.add('gap-2')
   newMessage.classList.add('my-1')

   messageText = document.createElement('div')
   messageText.innerHTML = text
   if (imgURL) {
      messageImage = document.createElement('img')
      messageImage.src = imgURL
      messageImage.classList.add('icon-sm')
      newMessage.appendChild(messageImage)
   }
   newMessage.appendChild(messageText)
   messages.appendChild(newMessage)
}