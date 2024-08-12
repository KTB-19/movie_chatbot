import React from "react";
import './ChatReaction.css';
import { LiaRobotSolid } from "react-icons/lia";
import { LuUser } from "react-icons/lu";


// input과 output을 세트로 나열
function ChatReaction({ inputValues, outputValues }) {
    return (
        <div className="chat-reaction-container">
            {inputValues.map((input, index) => (
                <div key={index} className="chat-message-pair">
                    <div className="chat-question">
                        <div className="chat-question-box">{input}</div>
                        <LuUser className="chat-icon-q" />
                    </div>
                    <div className="chat-answer">
                        <LiaRobotSolid className="chat-icon-a" />
                        <div className="chat-answer-box">{outputValues[index] || ''}</div>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default ChatReaction;
