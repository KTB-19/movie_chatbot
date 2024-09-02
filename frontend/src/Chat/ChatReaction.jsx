import React from "react";
import './ChatReaction.css';
import { LiaRobotSolid } from "react-icons/lia";
import { LuUser } from "react-icons/lu";
import YesNoButtons from "./YesNoButtons";

function ChatReaction({ 
    inputValues, 
    outputValues, 
    onYes, 
    onNo, 
    renderCheckBoxes, 
    handleCheckBoxChange, 
    handleChangeOrNot, 
    regionOptions, 
    handleRegionSelection // 추가된 부분
}) {
    return (
        <div className="chat-reaction-container">
            {outputValues.map((output, index) => (
                <div key={index} className="chat-message-pair">
                    {index > 0 && inputValues[index - 1] && (
                        <div className="chat-question">
                            <div className="chat-question-box">{inputValues[index - 1]}</div>
                            <LuUser className="chat-icon-q" />
                        </div>
                    )}
                    <div className="chat-answer">
                        <LiaRobotSolid className="chat-icon-a" />
                        <div className="chat-answer-box">
                            {output[0] && (
                                <div>{output[0]}</div>
                            )}
                            {output[1] && !renderCheckBoxes && (
                                <YesNoButtons
                                    onYes={onYes}
                                    onNo={onNo}
                                />
                            )}
                            {renderCheckBoxes && output[2] && (
                                <div className="checkbox-container">
                                    <label>
                                        <input type="checkbox" onChange={() => handleCheckBoxChange('date')} />
                                        날짜 바꾸기
                                    </label>
                                    <label>
                                        <input type="checkbox" onChange={() => handleCheckBoxChange('region')} />
                                        지역 바꾸기
                                    </label>
                                    <label>
                                        <input type="checkbox" onChange={() => handleCheckBoxChange('movieName')} />
                                        영화 바꾸기
                                    </label>
                                    <div className="checkbox-buttons">
                                        <button onClick={() => handleChangeOrNot(true)}>변경하기</button>
                                        <button className="cancel-button" onClick={() => handleChangeOrNot(false)}>유지하기</button>
                                    </div>
                                </div>
                            )}
                            {regionOptions.length > 0 && (
                                <div className="region-selection-buttons">
                                    {regionOptions.map((region, idx) => (
                                        <button 
                                            key={idx} 
                                            onClick={() => handleRegionSelection(region)}
                                        >
                                            {region}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default ChatReaction;
