import React, { useState, useEffect, useRef } from "react";
import ChatHeader from "./ChatHeader";
import "./Chat.css";
import ChatInput from "./ChatInput";
import ChatReaction from "./ChatReaction";

function Chat() {
    // questions(output) & answers(input)
    const [inputValues, setInputValues] = useState([]);
    const [outputValues, setOutputValues] = useState([]);
    
    const scrollRef = useRef();

    // input과 output 세션 스토리지에서 불러오기
    useEffect(() => {
        const savedInputValues = JSON.parse(sessionStorage.getItem("inputValues")) || [];
        const savedOutputValues = JSON.parse(sessionStorage.getItem("outputValues")) || [];
        setInputValues(savedInputValues);
        setOutputValues(savedOutputValues);
    }, []);

    // 새로운 input 추가되면 scroll to bottom
    useEffect(() => {
        scrollToBottom();
    }, [inputValues]);
 
    const scrollToBottom = () => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    };

    const sendInputValue = (value) => {
        const newInputValues = [...inputValues, value];
        setInputValues(newInputValues);
        sessionStorage.setItem("inputValues", JSON.stringify(newInputValues));
    };

    const sendOutputValue = (value) => {
        const newOutputValues = [...outputValues, value];
        setOutputValues(newOutputValues);
        sessionStorage.setItem("outputValues", JSON.stringify(newOutputValues));
    };

    const getOutputValue = () => {
        // 일단 아무거나 출력
        return "아웃풋입니다";
    };

    // ChatInput에서 inputValue를 받고
    // inputValue를 ChatReaction에 전달 & inputValue로 outputValue를 받아와서 ChatReaction에 전달

    return (
        <div className="chat-container">
            <div className="chat-header"><ChatHeader /></div>
            <div className="chat-reaction" ref={scrollRef}>
                <ChatReaction inputValues={inputValues} outputValues={outputValues} />
            </div>
            <div className="chat-input">
                <ChatInput 
                    inputValues={inputValues} 
                    setInputValue={sendInputValue} 
                    getOutputValue={getOutputValue} 
                    sendOutputValue={sendOutputValue} 
                />
            </div>
        </div>
    );
}

export default Chat;
