import React, { useState, useEffect, useRef, useContext } from "react";
import ChatHeader from "./ChatHeader";
import "./Chat.css";
import ChatInput from "./ChatInput";
import ChatReaction from "./ChatReaction";
import { AppContext } from "../AppContext";

function Chat() {
    // questions(output) & answers(input)
    const [inputValues, setInputValues] = useState([]);
    const [outputValues, setOutputValues] = useState([]);
    
    const scrollRef = useRef();
    const { movieName, region, date, setMovieName, setRegion, setDate } = useContext(AppContext); // AppContext에서 상태와 업데이트 함수들을 가져옴

    // input과 output 세션 스토리지에서 불러오기
    useEffect(() => {
        const savedInputValues = JSON.parse(sessionStorage.getItem("inputValues")) || [];
        const savedOutputValues = JSON.parse(sessionStorage.getItem("outputValues")) || [];
        setInputValues(savedInputValues);
        setOutputValues(savedOutputValues);
    }, []);

    // 새로운 input or output 추가되면 scroll to bottom
    useEffect(() => {
        scrollToBottom();
    }, [inputValues || outputValues]);
 
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

    const getOutputValue = async (currentInput) => {
        let endpoint;
        let body = { userInput: currentInput }; // 사용자의 입력을 서버로 보냄

        // 요청 경우 나누기
        // app context의 세 값 확인 후 세 값이 다 null 이 아니면  3, 
        // 1개 혹은 2개 부족하면 2, 
        // 세 값이 다 null 혹은 by default 1, 실행
        
        // 1. /movie/query
        // 2. /movie/query/additional
        // 3. /movie/running-times

        
        if (movieName && region && date) {
            // 3. /movie/running-times
            endpoint = "/movie/running-times";
            body = { ...body, movieName, region, date }; // 필요한 데이터를 함께 전송
        } else if (movieName || date || region) {
            // 2. /movie/query/additional
            endpoint = "/movie/query/additional";
            body = { ...body, movieName, region, date }; // 필요한 데이터를 함께 전송
        } else {
            // 1. /movie/query
            endpoint = "/movie/query";
        }
        console.log(movieName, date, region);
        console.log("endpoint", endpoint);
        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(body),
            });

            const data = await response.json();
            
            // 받아온 데이터를 AppContext에 저장
            if (data.movieName) setMovieName(data.movieName);
            if (data.region) setRegion(data.region);
            if (data.date) setDate(data.date);
            
            return `Movie: ${data.movieName || movieName}, Date: ${data.date || date}, Region: ${data.region || region}`;
        } catch (error) {
            console.error("Error fetching movie data:", error);
            return "Error fetching movie data.";
        }
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
                    sendInputValue={sendInputValue} 
                    getOutputValue={getOutputValue} 
                    sendOutputValue={sendOutputValue} 
                />
            </div>
        </div>
    );
}

export default Chat;