import React, { useEffect, useRef, useState } from "react";
import { FaArrowUp } from "react-icons/fa6";
import './ChatInput.css';

function ChatInput({ inputValues, sendInputValue, getOutputValue, sendOutputValue, disabled }) {
    const [currentInput, setCurrentInput] = useState(''); 
    const textareaRef = useRef();

    // 사용자가 input submit 이후
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (currentInput !== "") {
            sendInputValue(currentInput);
            setCurrentInput(''); 
            await getOutputValue(currentInput);
        }
    };

    // input 창 스크롤
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    }, [currentInput]);

    // 엔터 키를 누르면 제출
    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();  // 줄바꿈 방지
            handleSubmit(e);  // 폼 제출
        }
    };

    return (
        <div className="chat-input-container">
            <form onSubmit={handleSubmit}>
                <textarea 
                    ref={textareaRef}
                    value={currentInput}
                    onChange={(e) => setCurrentInput(e.target.value)} 
                    onKeyDown={handleKeyDown}  // 엔터 키 이벤트 처리
                    placeholder="메시지를 입력하세요...(한글, 영어, 숫자, 특수문자만 입력 가능)"
                    disabled={disabled} // disabled 속성 추가
                />
                <button 
                    type="submit" 
                    className={currentInput === '' || disabled ? 'disabled' : 'enabled'} 
                    disabled={currentInput === '' || disabled} // 버튼도 disabled
                >
                    <FaArrowUp />
                </button>
            </form>
        </div>
    );
}

export default ChatInput;
