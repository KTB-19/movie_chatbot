import React, { useEffect, useRef, useState } from "react";
import './ChatInput.css';

function ChatInput({ inputValues, sendInputValue, getOutputValue, sendOutputValue }) {
    const [currentInput, setCurrentInput] = useState('');  // 초기 상태를 빈 문자열로 설정
    const textareaRef = useRef();

    // 사용자가 input submit 이후
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (currentInput !== "") {
            const outputValue = await getOutputValue(currentInput);  // 비동기 처리
            sendOutputValue(outputValue);
            sendInputValue(currentInput);
            setCurrentInput('');  // 입력 후 필드를 초기화
        }
    };

    // input 창 스크롤
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    }, [currentInput]);

    return (
        <div className="chat-input-container">
            <form onSubmit={handleSubmit}>
                <textarea 
                    ref={textareaRef}
                    value={currentInput}
                    onChange={(e) => setCurrentInput(e.target.value)} 
                    placeholder="메시지를 입력하세요..."
                />
                <button type="submit">보내기</button>
            </form>
        </div>
    );
}

export default ChatInput;
