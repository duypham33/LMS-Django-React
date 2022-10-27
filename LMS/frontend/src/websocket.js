class WebSocketService {
    static instance = null;
    callbacks = {};
  
    static getInstance() {
        if (!WebSocketService.instance) {
        WebSocketService.instance = new WebSocketService();
        }
        return WebSocketService.instance;
    }
  
    constructor() {
        this.socketRef = null;
    }
  
    connect(chatID) {
        const path = `ws://${window.location.host}/ws/chat/${chatID}/`;
        this.socketRef = new WebSocket(path);
        this.socketRef.onopen = () => {
            console.log('WebSocket open');
        };
        // this.socketNewMessage(JSON.stringify({
        //     command: 'fetch_messages'
        // }));
        this.socketRef.onmessage = e => {
            this.socketNewMessage(e.data);
        };
        this.socketRef.onerror = e => {
            console.log(e.message);
        };
        this.socketRef.onclose = () => {
            //console.log(ev);
            console.log("WebSocket closed let's reopen");
            this.connect();
        };
    }
  
    socketNewMessage(data) {
        let parsedData = JSON.parse(data);
        let command = parsedData.command;

        if (Object.keys(this.callbacks).length === 0) {
            return;
        }
        if (command === 'messages') {
            this.callbacks[command](parsedData);
        }
        // if (command === 'new_message') {
        //     this.callbacks[command](parsedData.message);
        // }
    }

    addCallbacks(messagesCallback) {
        this.callbacks['messages'] = messagesCallback;
        //this.callbacks['new_message'] = newMessageCallback;
    }
  
    fetchMessages(chatID) {
        this.sendMessage({ command: 'fetch_messages', chat_id: chatID });
    }
  
    newChatMessage(message) {
        this.sendMessage({ ...message, command: 'new_message' }); 
    }
    
    sendMessage(data) {
        try {
            this.socketRef.send(JSON.stringify({ ...data }));
        }
        catch(err) {
            console.log(err.message);
        }  
    }
  
    state() {
      return this.socketRef.readyState;
    }
    
    // close() {
    //     this.socketRef.close(reason='discard');
    // }
  }
  
const WebSocketInstance = WebSocketService.getInstance();

export default WebSocketInstance;