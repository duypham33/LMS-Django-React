
import React, { useContext, createContext, useState, useEffect } from "react";
import { Outlet } from 'react-router-dom'
//import { userContext } from "../App";
import Sidepanel from './Sidepanel'
import WebSocketInstance from '../websocket';
import Cookies from 'js-cookie';

export const userContext = createContext()
export const chatsContext = createContext()

export default function Messenger(props) {
    const [user, setUser] = useState({});
    const [chats, setChats] = useState([]);
    
    //console.log(window.location.pathname == '/chat/')
    //console.log(window.location)

    useEffect(()=>{
        // const userID = JSON.parse(document.getElementById('userID').textContent);
        // const requestContent = {
        //     method: "POST",
        //     withCredentials: true,
        //     headers: {
        //         'X-CSRFToken': Cookies.get('csrftoken'),
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify({
        //         userid: JSON.parse(document.getElementById('userID').textContent)
        //     })
        // }
        //console.log("fetch", userID)
        fetch('/chatapi/chats/').then(res=>res.json()).then(data=>{
            setUser({
                id: userID,
                name: data.user_info.name,
                avatar: data.user_info.avatar,
            })

            setChats(data.chats)
        })

    }, [])

    return (
        <userContext.Provider value={user}>
            <chatsContext.Provider value={chats}>
                <div id="frame">
                    <Sidepanel />
                    <div className="content">
                        <div className="contact-profile">
                            <img src={window.location.origin + "/" + user.avatar} alt="" />
                            <p>{user.name}</p>
                            <div className="social-media">
                                <i className="fa fa-facebook" aria-hidden="true"></i>
                                <i className="fa fa-twitter" aria-hidden="true"></i>
                                <i className="fa fa-instagram" aria-hidden="true"></i>
                            </div>
                        </div>
                        
                        <Outlet/>
                    </div>
                </div>
            </chatsContext.Provider>
        </userContext.Provider>
    )
}