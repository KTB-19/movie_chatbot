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
    const { movieName, region, date, time, setMovieName, setRegion, setDate, setTime } = useContext(AppContext); // AppContext에서 상태와 업데이트 함수들을 가져옴

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
    }, [inputValues, outputValues]);

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

    // 요청 경우 나누기
    // app context의 네 값 확인 후 네 값이 다 null 이 아니면 3,
    // 1개 혹은 2개 부족하면 2,
    // 네 값이 다 null 혹은 by default 1

    const getOutputValue = async (currentInput) => {
        // setRegion("Seoul Gangnam-gu");
        let endpoint;
        let body;
        let initialRequestWas3 = false;
    
        // 날짜 형식 변환
        const formatDate = (date) => {
            const d = new Date(date);
            const month = '' + (d.getMonth() + 1);
            const day = '' + d.getDate();
            const year = d.getFullYear();
    
            return [year, month.padStart(2, '0'), day.padStart(2, '0')].join('-');
        };
    
        // 초기 요청 경우 나누기
        if (movieName && region && date) {
            // 3. /movie/running-times (POST)
            initialRequestWas3 = true;
            endpoint = `/api/v1/movie/running-times`;
            body = {
                movieName,
                region,
                date: formatDate(date),
                time
            };
        } else if (movieName || region || date) {
            // 2. /movie/query/additional (POST)
            endpoint = `/api/v1/movie/query/additional`;
            body = { message: currentInput };
        } else {
            // 1. /movie/query (GET)
            endpoint = `/api/v1/movie/query?message=${encodeURIComponent(currentInput)}`;
            body = null; 
        }
        console.log(endpoint);
    
        try {
            const response = await fetch(endpoint, {
                method: body ? "POST" : "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                body: body ? JSON.stringify(body) : null,
            });
    
            const data = await response.json();
    
            // 응답으로 받은 데이터로 상태를 업데이트
            if (data.movieName) setMovieName(data.movieName);
            if (data.region) setRegion(data.region);
            if (data.date) setDate(data.date);
            if (data.time) setTime(data.time);
    
            console.log(movieName, region, date, time);
    
            // 초기 요청이 3번이 아니었고, 모든 엔티티가 존재하는지 다시 확인
            if (!initialRequestWas3 && data.movieName && data.region && data.date) {
                // 모든 엔티티가 존재하면, 다시 3 실행
                endpoint = `/api/v1/movie/running-times`;
                body = {
                    movieName: movieName,
                    region: region,
                    date: formatDate(date),
                    time: time
                };
                console.log('Re-fetching with all entities:', endpoint);
    
                const finalResponse = await fetch(endpoint, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(body),
                });
    
                const finalData = await finalResponse.json();

                sendOutputValue(finalData.message);
                return finalData.message;
            }
    
            sendOutputValue(data.message);
            return data.message;
    
        } catch (error) {
            console.error("Error fetching movie data:", error);
            return { error: "Error fetching movie data." };
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
