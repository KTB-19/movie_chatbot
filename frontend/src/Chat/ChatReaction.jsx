import React from "react";
import './ChatReaction.css';
import { LiaRobotSolid } from "react-icons/lia";
import { LuUser } from "react-icons/lu";

function ChatReaction({ inputValues, outputValues }) {
    return (
        <div className="chat-reaction-container">
            {outputValues.map((output, index) => (
                <div key={index} className="chat-message-pair">
                    {/* inputValues와 outputValues의 인덱스가 맞지 않는 경우 처리 */}
                    {index > 0 && inputValues[index - 1] && (
                        <div className="chat-question">
                            <div className="chat-question-box">{inputValues[index - 1]}</div>
                            <LuUser className="chat-icon-q" />
                        </div>
                    )}
                    <div className="chat-answer">
                        <LiaRobotSolid className="chat-icon-a" />
                        <div className="chat-answer-box">
                            {typeof output === 'object' && output !== null
                                ? <pre>{JSON.stringify(output, null, 2)}</pre>
                                : output || ''}
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default ChatReaction;
