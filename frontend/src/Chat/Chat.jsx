import React, { useState, useEffect } from "react";
import ChatHeader from "./ChatHeader";
import "./Chat.css";
import ChatInput from "./ChatInput";
import ChatReaction from "./ChatReaction";
//헤더 & chatting & 인풋

function Chat() {
    const [inputValue, setInputValue] = useState('');
    const [reactionValue, setReactionValue] = useState('');

    useEffect(() => {
        // 페이지가 로드될 때 세션 스토리지에서 값을 불러옴
        const savedValue = sessionStorage.getItem("user");
        if (savedValue) {
            setReactionValue(savedValue);
        }
    }, []);


    const sendInputValue = (value) => {
        setReactionValue(value);

        // 세션 스토리지에 값 저장
        // 여러개 저장되도록 하기..
        sessionStorage.setItem("user", value); 
    };

    return (
        <div className="chat-container">
            <div className="chat-header"><ChatHeader /></div>
            <div className="chat-reaction">
                <ChatReaction inputValue={reactionValue} />
            </div>
            <div className="chat-input">
                <ChatInput inputValue={inputValue} setInputValue={setInputValue} sendInputValue={sendInputValue} />
            </div>
        </div>
    );
}

export default Chat;

