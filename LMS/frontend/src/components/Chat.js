
import React, { useContext, useEffect, useState } from 'react';
import WebSocketInstance from '../websocket';
import { useParams } from "react-router-dom";
import { chatsContext, userContext } from './Messenger';
import { socketContext } from "../App";
import SendMsg from './SendMsg';

export default function Chat(props) {
    const {chatID} = useParams();
    const [messages, setMessages] = useState(null);
    const user = useContext(userContext);
    const [chats, setChats, chatsOrderChg, setOrderChg] = useContext(chatsContext);
    const waitForSocketConnection = useContext(socketContext);
    //let messagesEnd;
    
    const newNessages = (parsedData) => {
        if (parsedData.chatID === chatID){
            // if (!parsedData.action)
            //     updateChats(parsedData);
            
            setMessages(parsedData.messages.reverse());
        }

        // else
        //     updateChats(parsedData);
    }


    useEffect(() => {
        if(chatID.includes('0_') === false) {
            WebSocketInstance.connect("chat", chatID);
            waitForSocketConnection(()=>{
                WebSocketInstance.addCallbacks("chat", newNessages);
                WebSocketInstance.fetchMessages(chatID);
            });
        }

        else
            setMessages([]);

        //scrollToBottom();
    }, [chatID])


    const renderTimestamp = timestamp => {
        let prefix = "";
        const timeDiff = Math.round(
          (new Date().getTime() - new Date(timestamp).getTime()) / 60000
        );
        if (timeDiff < 1) {
          // less than one minute ago
          prefix = "just now...";
        } else if (timeDiff < 60 && timeDiff > 1) {
          // less than sixty minutes ago
          prefix = `${timeDiff} ` + ((timeDiff > 1) ? `minutes ago` : `minute ago`);
        } else if (timeDiff < 24 * 60 && timeDiff > 60) {
          // less than 24 hours ago
          let t = Math.round(timeDiff / 60)
          prefix = `${t} ` + ((t > 1) ? `hours ago` : `hour ago`);
        } else if (timeDiff < 31 * 24 * 60 && timeDiff > 24 * 60) {
          // less than 7 days ago
          let t = Math.round(timeDiff / (60 * 24))
          prefix = `${t} ` + ((t > 1) ? `days ago` : `day ago`);
        } else {
          prefix = `${new Date(timestamp)}`;
        }
        return prefix;
      };
    
    
    const renderMessages = (msgs) => {

        return msgs.map((msg, i, arr) => (
            <li 
                key={msg.id} 
                style={{ marginBottom: arr.length - 1 === i ? "300px" : "15px" }}
                className={msg.author.name === user.name ? 'sent' : 'replies'}>
                <img src={window.location.origin + "/" + msg.author.avatar} />
                <p> {msg.content} <br/> 
                <small>{renderTimestamp(msg.timestamp)}</small>
                </p>
            </li>
        ));
    };

    // const scrollToBottom = () => {
    //     messagesEnd.scrollIntoView({ behavior: "smooth" });
    //   };

    
    return (
        <>
            <div className="messages" style={{marginBottom: "300px"}}>
                <ul id="chat-log">
                    { 
                        messages && 
                        renderMessages(messages) 
                    }
                    {/* <div>
                        style={{ float: "left", clear: "both" }}
                        ref = {el => {messagesEnd = el}}
                    </div> */}
                </ul>
            </div>
            <br/><br/><br/><br/>
            <SendMsg userID={user.id} chatID={chatID}/>
        </>
    );

}

