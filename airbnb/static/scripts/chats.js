
    $(()=>{
        const authId = '{{user.id}}'
        const authFirstName = '{{user.first_name}}'
        const authLastName = '{{user.last_name}}'
        const urlParams = getUrlParams(location.search);
        let openedChatId = null
        openChat(urlParams.open_chat)

        $('.chat-item').on('click', handleChatItemClick)
        $('form').on('submit', handleFormSubmit)
        $('input[name="message"]').on('keyup', handleMessageFieldKeyUp)

        function handleFormSubmit(event) {
            event.preventDefault()
            sendMessage()
        }
        function handleChatItemClick(event) {
            const chatItemElem = $(this)
            const chatId = chatItemElem.data('chat-id')
            openChat(chatId)
        }
        function clearMessageField() {
            $('input[name="message"]').val(null)
        }
        function sendMessage() {
            const messageField = $('input[name="message"]')
            const message = messageField.val().trim()
            const csrfmiddlewaretoken = getCookie('csrftoken')
            disableSendMessageButton()
            if(openedChatId && message){
                $.post("{% url 'messages' %}", { csrfmiddlewaretoken, message, chat_id:openedChatId, chat:openedChatId,  }).then((res) => {
                    handleSendMessageResponse(res)
                    enableSendMessageButton()
                }).catch((err) => {
                    enableSendMessageButton()
                    console.log(err);
                })
            }
        }
        function handleSendMessageResponse(res) {
            if(typeof res.chat === 'object'){
                alert('Something went wrong!')
            }else{
                appendMessage({
                    sender__first_name: authFirstName,
                    sender__last_name: authLastName,
                    created_on: new Date(),
                    message: res.message
                }, true)
                clearMessageField()
                enableSendMessageButton()
            }
        }
        function appendMessage(message, iSent=false) {
            const continer = $('.direct-chat-messages')
            continer.append(`
                <div class="direct-chat-msg ${iSent?'right':''}">
                    <div class="direct-chat-infos clearfix">
                        <span class="direct-chat-name float-left">${message.sender__first_name} ${message.sender__last_name}</span>
                        <span class="direct-chat-timestamp float-right">${message.created_on}</span>
                    </div>
                    <img class="direct-chat-img" src="{% static 'icons/avatar-1.png' %}" alt="Message User Image">
                    <div class="direct-chat-text">
                        ${message.message}
                    </div>
                </div>
            `)
        }
        function openChat(chatId) {
            disableSendMessageButton()
            if(chatId){
                openedChatId = chatId
                const chatElem = $(`.chat-item-${openedChatId}`)
                if(chatElem.length){
                    activateChat(`.chat-item-${openedChatId}`)
                    const csrfmiddlewaretoken = getCookie('csrftoken')
                    showMessageSkeleton()
                    $.post(`/messages/${openedChatId}`, { csrfmiddlewaretoken }).then((res) => {
                        replaceMessages(res)
                        enableSendMessageButton()
                    }).catch((err) => {
                        enableSendMessageButton()
                        console.log(err);
                    })
                }
            }
        }
        function disableSendMessageButton() {
            const sendMessageButton = $('button[type="submit"]')
            sendMessageButton.attr('disabled','disabled')
        }
        function enableSendMessageButton() {
            const sendMessageButton = $('button[type="submit"]')
            const messageField = $('input[name="message"]')
            if(openedChatId && messageField.val().trim()){
                sendMessageButton.removeAttr('disabled')
            }
        }
        function handleMessageFieldKeyUp(){
            if($(this).val().trim()){
                enableSendMessageButton()
            }else{
                disableSendMessageButton()
            }
        }
        function showMessageSkeleton() {
            const continer = $('.direct-chat-messages')
            continer.html(`
            <div class="message-skeleton">
                <span class="skeleton avatar"></span>
                <span class="skeleton text"></span>
            </div>
            <div class="message-skeleton right">
                <span class="skeleton avatar"></span>
                <span class="skeleton text"></span>
            </div>
            <div class="message-skeleton">
                <span class="skeleton avatar"></span>
                <span class="skeleton text"></span>
            </div>
            <div class="message-skeleton right">
                <span class="skeleton avatar"></span>
                <span class="skeleton text"></span>
            </div>
            <div class="message-skeleton">
                <span class="skeleton avatar"></span>
                <span class="skeleton text"></span>
            </div>
            `)
        }
        function activateChat(chatSelector){
            const chatElem =  $(chatSelector)
            const openedChatTopicElem = $('.opened-chat-topic')
            const openedChatParticipantsElem = $('.opened-chat-participants')
            const topic = chatElem.find('.chat-topic').attr('title')
            const participants = chatElem.find('.chat-participants').attr('title')
            openedChatTopicElem.text(topic)
            openedChatParticipantsElem.text(participants)
            $('.bg-danger').removeClass('bg-danger')
            chatElem.addClass('bg-danger')
        }
        function replaceMessages(messages) {
            const continer = $('.direct-chat-messages')
            if(!messages.length){
                continer.html(`<p class="empty-chat-body-message">No messages.</p>`)
                return 
            }
            continer.html(null)
            messages.forEach(message => {
                appendMessage(message, authId==message.sender__pk)
            });
        }
        /**
         * Accepts either a URL or querystring and returns an object associating 
         * each querystring parameter to its value. 
         *
         * Returns an empty object if no querystring parameters found.
         */
        function getUrlParams(urlOrQueryString) {
            if ((i = urlOrQueryString.indexOf('?')) >= 0) {
                const queryString = urlOrQueryString.substring(i+1);
                if (queryString) {
                return _mapUrlParams(queryString);
                } 
            }
            return {};
        }

        /**
         * Helper function for `getUrlParams()`
         * Builds the querystring parameter to value object map.
         *
         * @param queryString {string} - The full querystring, without the leading '?'.
         */
        function _mapUrlParams(queryString) {
            return queryString    
                .split('&') 
                .map(function(keyValueString) { return keyValueString.split('=') })
                .reduce(function(urlParams, [key, value]) {
                if (Number.isInteger(parseInt(value)) && parseInt(value) == value) {
                    urlParams[key] = parseInt(value);
                } else {
                    urlParams[key] = decodeURI(value);
                }
                return urlParams;
                }, {});
        }

    })