
import React from "react";
import { NavLink } from "react-router-dom";

export default function Contact(props) {
    
    // let loct = {
    //     pathname: `${props.chat.chatid}`,
    //     state: {
    //         name: props.chat.represent,
    //         img_path: props.chat.img_path
    //     }
    // }
    
    return (
        <NavLink to={`${props.chat.chatid}`}
        style={{ color: "#fff" }}>
            <li className={`contact ${props.active}`}>
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
    )
}