import React from "react";
import ChatHeader from "./ChatHeader";
import "./Chat.css";
import ChatInput from "./ChatInput";
import ChatReaction from "./ChatReaction";
//헤더 & chatting & 푸터(인풋)

function Chat() {
    return (
        <div className="chat-container">
            <div className="chat-header"><ChatHeader /></div>
            <div className="chat-reaction"><ChatReaction /></div>
            <div className="chat-input"><ChatInput /></div>
        </div>
    );
}

export default Chat;
