import React from "react";
import './ChatReaction.css';
import { LiaRobotSolid } from "react-icons/lia";
import { LuUser } from "react-icons/lu";
import YesNoButtons from "./YesNoButtons";
import RegionButtons from "./RegionButtons"; // 새로 만든 컴포넌트 임포트

function ChatReaction({ 
    inputValues, 
    outputValues, 
    onYes, 
    onNo, 
    renderCheckBoxes, 
    handleCheckBoxChange, 
    handleChangeOrNot, 
    regionOptions, 
    handleRegionSelection 
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
                            {output[3] && regionOptions.length > 0 && (
                                <RegionButtons 
                                    regions={regionOptions} 
                                    onRegionSelect={handleRegionSelection}
                                />
                            )}
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default ChatReaction;
