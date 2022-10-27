
import React from 'react';
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



export default function App(props) {
    //let userID = JSON.parse(document.getElementById('userID').textContent);

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

