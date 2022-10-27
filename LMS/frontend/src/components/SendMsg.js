import React, { useState, useContext } from "react";
import WebSocketInstance from '../websocket';
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";
import { chatsContext } from "./Messenger";


export default function SendMsg(props){

    const [newSend, setNewSend] = useState({message: ''});
    const nav = useNavigate();
    const [chats, setChats, chatsOrderChg, setOrderChg] = useContext(chatsContext);
    
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
            //updateChats(newSend.message);
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
                addNewChat(data.new_chat);
                nav(`/chat/${data.new_chat.chatid}/`);
            })
        }
        
        setNewSend({
            message: ''
        })
    }

    const updateChats = (newMsg)=>{
        let index = chats.indexOf(chats.filter((c)=>c.chatid == props.chatID)[0]);
        let cs = chats;
        let c = cs[index];
        cs.splice(index, 1);
        c.lastest_msg = newMsg;
        cs.unshift(c);

        setChats(cs);
        setOrderChg(true);
    }

    const addNewChat = (newChat) => {
        let cs = chats;
        cs.unshift(newChat);
        setChats(cs);
        setOrderChg(true);
    }

    return (
        
        <div className="message-input">
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