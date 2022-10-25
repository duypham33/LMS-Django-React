import React, { useEffect } from 'react';
import ReactDOM from 'react-dom';
import Messenger from './components/Messenger';
import Chat from './components/Chat';
import WebSocketInstance from './websocket';
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    Redirect,
    BrowserRouter,
  } from "react-router-dom";


export default function App(props) {

    useEffect(()=>{
        WebSocketInstance.connect();
    }, [])

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/chat" element={<Messenger/>}>
                    <Route path="test" element={<Chat/>}/>
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

