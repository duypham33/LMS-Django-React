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
  
    connect(type, id) {
        const path = (type === 'chat') ? `ws://${window.location.host}/ws/chat/${id}/`
                                       : `ws://${window.location.host}/ws/notice/${id}/`;
        this.socketRef = new WebSocket(path);
        this.socketRef.onopen = () => {
            console.log('WebSocket open');
        };
        
        this.socketRef.onmessage = e => {
            this.socketNewMessage(e.data);
        };
        this.socketRef.onerror = e => {
            console.log(e.message);
        };
        this.socketRef.onclose = () => {
            //console.log(ev);
            console.log("WebSocket closed let's reopen");
            this.connect(type, id);
        };
    }
  
    socketNewMessage(data) {
        let parsedData = JSON.parse(data);
        let command = parsedData.command;

        if (Object.keys(this.callbacks).length === 0) {
            return;
        }

        if (command === 'messages' || command === 'notices') {
            this.callbacks[command](parsedData);
        }
    }

    addCallbacks(type, funcCallback) {
        if (type === 'chat')
            this.callbacks['messages'] = funcCallback;
        else
            this.callbacks['notices'] = funcCallback;
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