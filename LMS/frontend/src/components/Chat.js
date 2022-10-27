
import React, { useContext, useEffect, useState } from 'react';
import WebSocketInstance from '../websocket';
import { useParams } from "react-router-dom";
import { chatsContext, userContext } from './Messenger';
import SendMsg from './SendMsg';

export default function Chat(props) {
    const {chatID} = useParams();
    const [messages, setMessages] = useState(null);
    const user = useContext(userContext);
    const [chats, setChats, chatsOrderChg, setOrderChg] = useContext(chatsContext);
    
    const newNessages = (parsedData) => {
        if (parsedData.chatID === chatID){
            if (!parsedData.action)
                updateChats(parsedData);
            
            setMessages(parsedData.messages.reverse());
        }

        else
            updateChats(parsedData);
    }

    const updateChats = (parsedData)=>{
        let cs = chats;
        let index = chats.indexOf(chats.filter((c)=>c.chatid == parsedData.chatID)[0]);
        let c = {};
        let lm = parsedData.messages[0];
        console.log(parsedData)
        try{
            c = cs[index];
            cs.splice(index, 1);
            c.lastest_msg = lm.content
        }
        catch{
            c = {
                chatid: parsedData.chatID,
                represent: lm.author.name,  //Since this case is sent by the other
                img_path: lm.author.avatar,
                lastest_msg: lm.content
            }
        }
        
        cs.unshift(c);

        setChats(cs);
        setOrderChg(true);
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

                WebSocketInstance.connect(chatID);
                waitForSocketConnection(callback);
            }
        }, 100)
    }


    useEffect(() => {
        if(chatID.includes('0_') === false){
            waitForSocketConnection(()=>{
                WebSocketInstance.addCallbacks(newNessages);
                WebSocketInstance.fetchMessages(chatID);
            });
    
            WebSocketInstance.connect(chatID);
        }

        else
            setMessages([]);
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

        return msgs.map((msg, i) => (
            <li 
                key={msg.id} 
                className={msg.author.name === user.name ? 'sent' : 'replies'}>
                <img src={window.location.origin + "/" + msg.author.avatar} />
                <p> {msg.content} <br/> 
                <small>{renderTimestamp(msg.timestamp)}</small>
                </p>
            </li>
        ));
    };

    
    return (
        <>
            <div className="messages">
                <ul id="chat-log">
                { 
                    messages && 
                    renderMessages(messages) 
                }
                </ul>
            </div>

            <SendMsg userID={user.id} chatID={chatID}/>
        </>
    );

}

