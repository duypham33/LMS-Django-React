
import React, { useEffect, useState } from 'react';
import WebSocketInstance from '../websocket';
import { useParams } from "react-router-dom";

export default function Chat(props) {
    const {chatID} = useParams();
    const [messages, setMessages] = useState({message: ""})

    const addMessage = (new_message) => {
        setMessages({ messages: [...messages, new_message]});
    }
    
    const set_messages = (messages) => {
        setMessages({ messages: messages.reverse()});
    }

    const waitForSocketConnection = (callback)=>{
        setTimeout(function(){
            if (WebSocketInstance.state() === 1){
                console.log("Connection is made");
                callback();
                return;
            }
            else{
                console.log("wait for connection...");
                waitForSocketConnection(callback);
            }
        }, 100)
    }


    useEffect(() => {
        console.log(chatID)
        waitForSocketConnection(()=>{
            WebSocketInstance.addCallbacks(
                set_messages, addMessage
            )
        });

        WebSocketInstance.connect(chatID);
    })
    
    
    const messageChangeHandler = (event) =>  {
        setMessages({
            message: event.target.value
        })
    }
    
    const sendMessageHandler = (e) => {
        e.preventDefault();
        const messageObject = {
            from: "admin",
            content: messages,
        };

        WebSocketInstance.newChatMessage(messageObject);
        setMessages({
            message: ''
        })
    }
    
    // const renderMessages = (messages) => {
    //     const currentUser = "admin";
    //     return messages.map((message, i) => (
    //         // <li 
    //         //     key={message.id} 
    //         //     className={message.author === currentUser ? 'sent' : 'replies'}>
    //         //     <img src="http://emilcarlsson.se/assets/mikeross.png" />
    //         //     <p> {message.content} <br/> </p>
    //         // </li>
    //         Hello
    //     ));
    // };

    
    const msgs = messages;
    return (
        <>
            <div className="messages">
                <ul id="chat-log">
                { 
                    // msgs && 
                    // renderMessages(msgs) 
                }
                </ul>
            </div>
            <div className="message-input">
                <form onSubmit={sendMessageHandler}>
                    <div className="wrap">
                        <input 
                            onChange={messageChangeHandler}
                            required 
                            id="chat-message-input" 
                            type="text" 
                            placeholder="Write your message..." />
                        <i className="fa fa-paperclip attachment" aria-hidden="true"></i>
                        <button id="chat-message-submit" className="submit">
                            <i className="fa fa-paper-plane" aria-hidden="true"></i>
                        </button>
                    </div>
                </form>
            </div>
        </>
    );

}

