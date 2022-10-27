
import React, { useEffect, createContext, useState } from 'react';
import ReactDOM from 'react-dom';
import Messenger from './components/Messenger';
import Chat from './components/Chat';
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    Redirect,
    BrowserRouter,
  } from "react-router-dom";


// export const userContext = createContext()
// export const chatsContext = createContext()

export default function App(props) {
    // const [user, setUser] = useState({});
    // const [chats, setChats] = useState([]);

    // useEffect(()=>{
    //     WebSocketInstance.connect();
        
    //     let userID = JSON.parse(document.getElementById('userID').textContent);
    //     const requestContent = {
    //         method: "POST",
    //         withCredentials: true,
    //         headers: {
    //             'X-CSRFToken': Cookies.get('csrftoken'),
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({
    //             userid: userID
    //         })
    //     }
    //     console.log("fetch", userID)
    //     fetch('/chatapi/chats/', requestContent).then(res=>res.json()).then(data=>{
    //         console.log(data)
    
    //         setUser({
    //             id: userID,
    //             name: data.user_info.name,
    //             avatar: data.user_info.avatar,
    //         })

    //         setChats(data.chats)
    //     })

    // }, [])

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/chat" element={<Messenger/>}>
                    <Route path=":chatID" element={<Chat/>}/>
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

