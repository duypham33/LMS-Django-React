
import React, {useEffect, useContext, createContext} from 'react';
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
import WebSocketInstance from './websocket';

export const socketContext = createContext();

export default function App(props) {
    let userID = JSON.parse(document.getElementById('userID').textContent);

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

    useEffect(()=>{

        WebSocketInstance.connect("notice", userID);
        waitForSocketConnection(()=>{
            return;
        });

    }, [userID]);

    return (
        <socketContext.Provider value={waitForSocketConnection}>
            <BrowserRouter>
                <Routes>
                    <Route path="/chat" element={<Messenger/>}>
                        <Route path=":chatID" element={<Chat/>}/>
                    </Route>
                </Routes>
            </BrowserRouter>
        </socketContext.Provider>
    )
}

