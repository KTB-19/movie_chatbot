import React from "react";
import './ChatReaction.css';  // 스타일이 정의된 파일을 가져옵니다.
import { LiaRobotSolid } from "react-icons/lia";
import { LuUser } from "react-icons/lu";
import YesNoButtons from "./YesNoButtons";  // Yes/No 버튼 컴포넌트를 가져옵니다.

function ChatReaction({ inputValues, outputValues, onYes, onNo, renderCheckBoxes, handleCheckBoxChange, handleChangeOrNot }) {
    return (
        <div className="chat-reaction-container">
            {outputValues.map((output, index) => (
                <div key={index} className="chat-message-pair">
                    {/* input 출력 */}
                    {index > 0 && inputValues[index - 1] && (
                        <div className="chat-question">
                            <div className="chat-question-box">{inputValues[index - 1]}</div>
                            <LuUser className="chat-icon-q" />
                        </div>
                    )}
                    {/* output 출력 */}
                    <div className="chat-answer">
                        <LiaRobotSolid className="chat-icon-a" />
                        <div className="chat-answer-box">
                            {/* 메시지 출력 */}
                            {output[0] && (
                                <div>{output[0]}</div>
                            )}
                            {/* Yes/No 버튼 출력 */}
                            {output[1] && !renderCheckBoxes && (
                                <YesNoButtons
                                    onYes={onYes}
                                    onNo={onNo}
                                />
                            )}
                            {/* 체크박스 출력 및 변경/유지 버튼 */}
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
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default ChatReaction;
