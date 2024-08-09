import React, { useEffect, useRef } from "react";
import './ChatInput.css';

function ChatInput({ inputValue, setInputValue, sendInputValue }) {
    const textareaRef = useRef(null);

    const handleSubmit = (e) => {
        e.preventDefault();
        // 백엔드로 보내기

        // 중간 버블창에 띄우기
        sendInputValue(inputValue);
        
        setInputValue('');
    };

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    }, [inputValue]);

    return (
        <div className="chat-input-container">
            <form onSubmit={handleSubmit}>
                <textarea 
                    ref={textareaRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)} 
                    placeholder="메시지를 입력하세요..."
                />
                <button type="submit">보내기아이콘</button>
            </form>
        </div>
    );
}

export default ChatInput;
