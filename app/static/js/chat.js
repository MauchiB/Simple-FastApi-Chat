document.addEventListener('DOMContentLoaded', event => {
  let socket = null;
  let a = document.querySelectorAll('a[chat_id]')
  console.log(a)
  let cont = document.getElementsByClassName('mecontainer')[0]
  let chatin = document.getElementsByClassName('chat')[0]
  a.forEach(tag => {
    tag.addEventListener('click', (event) => {
      event.preventDefault()
      const link = event.currentTarget
      const chat_id = link.getAttribute('chat_id')

      const query = fetch(`/chat/get-chat/${chat_id}`)
        .then(response => {
          if (response.ok) {
            return response.json()
          }
        }
        )
        .then(data => {
          if (data.need) {
            console.log('password need')
          }
          if (data.chat) {
            chatin.innerHTML = ''
            chatin.innerHTML = data.chat

            WSchat()

          } else {
            throw new Error('404 chat')
          }
        })
        .catch(error => {
          console.log(error)
        })
    })

  })
  function WSchat() {

    const button = document.getElementById('button-id')
    const message = document.getElementById('message-to-send')
    const chat = document.getElementById('chat_id')
    const chat_history = document.getElementsByClassName('chat-history')[0]
    const id = chat.getAttribute('chat_id')
    const username = chat.getAttribute('username')
    const delete_chat = document.getElementById('delete-id')

    delete_chat.addEventListener('click', () => {
      fetch(`/chat/logout-chat/${id}`, {
        method: 'POST'
      }).then(response => {
        if (response.ok) {
          alert('You logout from chat')
          window.location.reload()
        } else { alert('error 404') }
      })
    })


    if (socket) {
      socket.onopen = null;
      socket.onmessage = null;
      socket.onerror = null;
      socket.onclose = null;
      socket.close();
      socket = null;
      console.log('WebSocket closed');
    }
    scroll()

    socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${id}`)
    socket.onopen = event => {
      console.log('connect WS')
    }
    socket.onerror = error => {
      socket.close()
      console.log('error - ' + error)
    }
    socket.onclose = event => {
      socket.close()
    }
    socket.onmessage = message => {
      console.log(username)
      parse_message = JSON.parse(message.data)
      if (parse_message.username == username) {
        html =         `<li class="clearfix">
                        <div class="message-data align-right">
                            <span class="message-data-time" >${parse_message.created_at}</span> &nbsp; &nbsp;
                            <span class="message-data-name" >${parse_message.username}</span> <i class="fa fa-circle me"></i>
                            
                        </div>
                        <div class="message other-message float-right">
                            ${parse_message.message}
                        </div>
                        </li>
                        ` } 
                        else {
        html =                 `<li>
                                    <div class="message-data">
                                        <span class="message-data-name"><i class="fa fa-circle online"></i>${parse_message.username}</span>
                                        <span class="message-data-time">${parse_message.created_at}</span>
                                    </div>
                                    <div class="message my-message">
                                        ${parse_message.message}
                                    </div>
                                  </li>
                                `
      }
      chat.innerHTML += html
      scroll()

    }

    button.addEventListener('click', event => {

      event.preventDefault()
      const obj = {
        'message': message.value
      }
      socket.send(JSON.stringify(obj))

      message.value = ''
    })

    function scroll() {
      chat_history.scrollTop = chat_history.scrollHeight
    }

  }

})