
import React, { useContext, useEffect, useState } from 'react';
import { chatsContext, userContext } from './Messenger';
import Contact from './Contact';
import Cookies from 'js-cookie';

export default function Sidepanel(props) {
    const user = useContext(userContext)
    const [chats, setChats, chatsOrderChg, setOrderChg] = useContext(chatsContext)
    const [kw, setKW] = useState('');
    const [contacts, setContacts] = useState([]);

    let chatid = window.location.pathname.split("/")[2];
    
    useEffect(()=>{
        console.log('This me!')
        if (kw === '') {
            console.log('Contacts to chats?')
            setContacts(chats);
            setOrderChg(false);
        }
            
        else {
            console.log('Did I fetch?')
            const requestContent = {
                method: "POST",
                withCredentials: true,
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    command: "kw",
                    kw: kw
                })
            }
            
            fetch('/chatapi/friends_search/', requestContent).then(res=>res.json()).then(data=>{
                setContacts(data.contacts);
            })

            setOrderChg(false);
        }
    }, [chats, chatsOrderChg, kw, chatid])

    const searchHandler = (event) => {
        setKW(event.target.value);
    }

    const isActive = contact => {
        try{
            return contact.chatid == chatid ? "active" : "";
        }
        catch{
            return '';
        }
    }

    return (
        <div id="sidepanel">
            <div id="profile">
                <div className="wrap">
                    <img id="profile-img" src={window.location.origin + "/" + user.avatar} 
                    className="online" alt="" height="60px"/>
                    <p>{user.name}</p>
                    <i className="fa fa-chevron-down expand-button" aria-hidden="true"></i>
                    <div id="status-options">
                        <ul>
                            <li id="status-online" className="active"><span className="status-circle"></span> <p>Online</p></li>
                            <li id="status-away"><span className="status-circle"></span> <p>Away</p></li>
                            <li id="status-busy"><span className="status-circle"></span> <p>Busy</p></li>
                            <li id="status-offline"><span className="status-circle"></span> <p>Offline</p></li>
                        </ul>
                    </div>
                    <div id="expanded">
                        <label htmlFor="twitter"><i className="fa fa-facebook fa-fw" aria-hidden="true"></i></label>
                        <input name="twitter" type="text" value="mikeross" />
                        <label htmlFor="twitter"><i className="fa fa-twitter fa-fw" aria-hidden="true"></i></label>
                        <input name="twitter" type="text" value="ross81" />
                        <label htmlFor="twitter"><i className="fa fa-instagram fa-fw" aria-hidden="true"></i></label>
                        <input name="twitter" type="text" value="mike.ross" />
                    </div>
                </div>
            </div>
            <div id="search">
                <label htmlFor=""><i className="fa fa-search" aria-hidden="true"></i></label>
                <input type="text" placeholder="Search contacts..." value={kw} onChange={searchHandler}/>
            </div>
            <div id="contacts">
                <ul>
                    {contacts.map(u => <Contact chat = {u} active = {isActive(u)} />)}
                </ul>
            </div>
            <div id="bottom-bar">
                <button id="addcontact"><i className="fa fa-user-plus fa-fw" aria-hidden="true"></i> <span>Add contact</span></button>
                <button id="settings"><i className="fa fa-cog fa-fw" aria-hidden="true"></i> <span>Settings</span></button>
            </div>
        </div>
    )
}
