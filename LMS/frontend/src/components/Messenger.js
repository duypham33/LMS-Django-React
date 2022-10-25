
import React from "react";
import { Outlet } from 'react-router-dom'
import Sidepanel from './Sidepanel'

export default function Messenger(props) {
    
    return (
        <div id="frame">
            <Sidepanel />
            <div className="content">
                <div className="contact-profile">
                    <img src="http://emilcarlsson.se/assets/harveyspecter.png" alt="" />
                    <p>username</p>
                    <div className="social-media">
                        <i className="fa fa-facebook" aria-hidden="true"></i>
                        <i className="fa fa-twitter" aria-hidden="true"></i>
                        <i className="fa fa-instagram" aria-hidden="true"></i>
                    </div>
                </div>
                
                <Outlet/>
            </div>
        </div>
    )
}