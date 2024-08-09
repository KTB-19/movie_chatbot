import React from "react";
import './ChatReaction.css';

function ChatReaction({ inputValue }) {
    return (
        <div className="chat-reaction-container">
            <div className="chat-reaction-box">
                {inputValue}
            </div>
        </div>
    );
}

export default ChatReaction;
