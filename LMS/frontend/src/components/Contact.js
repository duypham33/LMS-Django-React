
import React from "react";
import { NavLink } from "react-router-dom";

export default function Contact(props) {


    return (
        <NavLink to={`${props.chat.chatid}`} style={{ color: "#fff" }}>
            <li className="contact">
                <div className="wrap">
                    <span className="contact-status online"></span>
                    <img src={window.location.origin + '/' + props.chat.img_path} height="52px" alt="" 
                    style={{border: "3px solid", 
                    borderColor: "#2ecc71",
                    padding: "1px"}}/>
                    
                    <div className="meta">
                        <p className="name"> {props.chat.represent} </p>
                        <p className="preview"> {props.chat.lastest_msg} </p>
                    </div>
                </div>
            </li>
        </NavLink>
        // <li className="contact active">
        //     <div className="wrap">
        //         <span className="contact-status busy"></span>
        //         <img src="http://emilcarlsson.se/assets/harveyspecter.png" alt="" />
        //         <div className="meta">
        //             <p className="name">Harvey Specter</p>
        //             <p className="preview">Wrong. You take the gun, or you pull out a bigger one. Or, you call their bluff. Or, you do any one of a hundred and htmlForty six other things.</p>
        //         </div>
        //     </div>
        // </li>
    )
}