
import React, { useContext, createContext, useState, useEffect } from "react";
import { Outlet, useNavigate } from 'react-router-dom'
import Sidepanel from './Sidepanel'
import WebSocketInstance from '../websocket';
import Cookies from "js-cookie";

export const userContext = createContext()
export const chatsContext = createContext()

export default function Messenger(props) {
    const [user, setUser] = useState({});
    const [chats, setChats] = useState([]);
    const [chatsOrderChg, setOrderChg] = useState(false); //Help re-render when object chats updated
    const nav = useNavigate();
    const [info, setInfo] = useState({});

    console.log('I rerendered!', chats);
    useEffect(()=>{

        WebSocketInstance.addCallbacks("notice", updateChats);
        console.log('I called!')

        let chatid = window.location.pathname.split("/")[2];
        
        if (chatid !== ''){
            console.log('I get info!');
            let param = chatid.split("_")
    
            const requestContent = {
                method: "POST",
                withCredentials: true,
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    command: "info",
                    info_id: param.slice(-1)[0],
                    isChatID: param.length === 1
                })
            }
            
            fetch('/chatapi/friends_search/', requestContent).then(res=>{
                if (res.ok)
                    return res.json();
                nav("/chat/");
                
            }).then(data=>{
                setInfo({represent: data.represent, img_path: data.img_path});
            })
        }
        else
            setInfo({represent: user.name, img_path: user.avatar});

        if(chats.length === 0 || chats.length === 1) {
            console.log('I fetched!');
            fetch('/chatapi/chats/').then(res=>res.json()).then(data=>{
                setUser({
                    id: data.user_info.id,
                    name: data.user_info.name,
                    avatar: data.user_info.avatar,
                })

                if (chatid === '')
                    setInfo({represent: data.user_info.name, img_path: data.user_info.avatar});
    
                setChats(data.chats);
                setOrderChg(true);
            })
        }
    }, [location.pathname, chats.length]);



    const updateChats = (parsedData) => {
        console.log(chats);
        let chatID = parsedData.chat.chatid;
        let author = parsedData.author;
        let ch = parsedData.chat;
        let cs = chats;
        let index = cs.indexOf(cs.filter(c => c.chatid == chatID)[0]);
        console.log(index);
        let c = {};

        try {
            c = cs[index];
            cs.splice(index, 1);
            c.lastest_msg = ch.lastest_msg;
        }
        catch {
            c = ch;

            if (author.id == user.id){
                let others = parsedData.others;
                if (others.is_group_chat === false){
                    c.represent = others.friend_name;
                    c.img_path = others.friend_avatar;
                }
            }
        }
        
        cs.unshift(c);

        setChats(cs);
        setOrderChg(true);
        console.log(chats);
    }




    return (
        <userContext.Provider value={user}>
            <chatsContext.Provider value={[chats, setChats, chatsOrderChg, setOrderChg]}>
                <div id="frame">
                    <Sidepanel />
                    <div className="content">
                        <div className="contact-profile">
                            <img src={window.location.origin + "/" + info.img_path} alt="" 
                            height="60px"/>
                            <p>{info.represent}</p>
                            <div className="social-media">
                                <i className="fa fa-facebook" aria-hidden="true"></i>
                                <i className="fa fa-twitter" aria-hidden="true"></i>
                                <i className="fa fa-instagram" aria-hidden="true"></i>
                            </div>
                        </div>
                        
                        <Outlet />
                    </div>
                </div>
            </chatsContext.Provider>
        </userContext.Provider>
    )
}