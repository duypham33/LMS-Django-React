import React, { useState, useContext } from "react";
import WebSocketInstance from '../websocket';
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";


export default function SendMsg(props){

    const [newSend, setNewSend] = useState({message: ''});
    const nav = useNavigate();
    
    const messageChangeHandler = (event) =>  {
        setNewSend({
            message: event.target.value
        })
    }
    
    const sendMessageHandler = (event) => {
        event.preventDefault();
        
        let messageObject = {
            userID: props.userID,
            chatID: props.chatID,
            content: newSend.message,
        };

        if(props.chatID.includes('0_') === false){
            WebSocketInstance.newChatMessage(messageObject);
        }
            
        else{
            messageObject = {...messageObject, friendID: props.chatID.split("_").slice(-1)[0]}

            const requestContent = {
                method: "POST",
                withCredentials: true,
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(messageObject)
            }
            
            fetch('/chatapi/send_first_time/', requestContent).then(res=>{
                if (res.ok)
                    return res.json();
                nav("/chat/");
                
            }).then(data=>{
                nav(`/chat/${data.new_chat.chatid}/`);
            })
        }
        
        setNewSend({
            message: ''
        })
    }

    

    return (
        
        <div className="message-input" style={{marginTop: "300px"}}>
            <form onSubmit={sendMessageHandler}>
                <div className="wrap">
                    <input 
                        onChange={messageChangeHandler}
                        value={newSend.message}
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
    )
}