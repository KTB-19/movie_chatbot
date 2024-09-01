import React, { useState, useEffect, useRef, useContext } from "react";
import ChatHeader from "./ChatHeader";
import "./Chat.css";
import ChatInput from "./ChatInput";
import ChatReaction from "./ChatReaction";
import { AppContext } from "../AppContext";

function Chat() {
    const [inputValues, setInputValues] = useState([]);
    const [outputValues, setOutputValues] = useState([]);
    const [yesNoValue, setYesNoValue] = useState('');
    const [isInputDisabled, setIsInputDisabled] = useState(false);
    const [renderCheckBoxes, setRenderCheckBoxes] = useState(false);
    const [selectedOptions, setSelectedOptions] = useState([]);
    const [responseMessage, setResponseMessage] = useState('');  // 응답 메시지 상태

    const scrollRef = useRef();
    const { movieName, region, date, time, setTime, setMovieName, setRegion, setDate, manualMessage, setManual } = useContext(AppContext);

    const movieNameRef = useRef(movieName);
    const regionRef = useRef(region);
    const dateRef = useRef(date);

    // 상태가 변경될 때마다 ref에 최신 상태를 저장
    useEffect(() => {
        movieNameRef.current = movieName;
        regionRef.current = region;
        dateRef.current = date;
    }, [movieName, region, date]);

    // input과 output 세션 스토리지에서 불러오기
    useEffect(() => {
        const savedInputValues = JSON.parse(sessionStorage.getItem("inputValues") || "[]");
        const savedOutputValues = JSON.parse(sessionStorage.getItem("outputValues") || "[]");
        setInputValues(savedInputValues);
        setOutputValues(savedOutputValues);
    }, []);

    // 상태가 업데이트된 후 checker 실행
    useEffect(() => {
        if (responseMessage) {
            console.log("Running checker with the response message...");
            checker({
                message: responseMessage,  // 응답 메시지 사용
                movieName: movieNameRef.current,
                region: regionRef.current,
                date: dateRef.current,
            });
            setResponseMessage('');  // 메시지 초기화
        }
    }, [responseMessage]);

    // 새로운 input or output 추가되면 scroll to bottom
    useEffect(() => {
        scrollToBottom();
    }, [inputValues, outputValues]);

    const scrollToBottom = () => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    };

    const handleYesNoResponse = (response) => {
        console.log('YesNo button clicked:', response);
        setYesNoValue(response);
        setIsInputDisabled(true);

        if (response === 'Yes') {
            console.log('Yes selected');
            getOutputValue('Yes');
            setIsInputDisabled(false);
        } else if (response === 'No') {
            console.log('No selected');
            setRenderCheckBoxes(true);
            setIsInputDisabled(false);
            renderOutput('무엇을 변경하시겠습니까?', false, true);
        }
    };
    
    const handleCheckBoxChange = (option) => {
        setSelectedOptions(prevState =>
            prevState.includes(option)
                ? prevState.filter(opt => opt !== option)
                : [...prevState, option]
        );
    };

    const handleChangeOrNot = async (shouldChange) => {
        if (shouldChange) {
            if (selectedOptions.includes('date')) {
                await setDate(prevDate => ''); // 날짜 시간 변경
            }
            if (selectedOptions.includes('region')) {
                await setRegion(prevRegion => ''); // 지역 변경
            }
            if (selectedOptions.includes('movieName')) {
                await setMovieName(prevMovieName => ''); // 영화명 변경
            }

            console.log("Context values changed:", {
                movieName: movieNameRef.current,
                region: regionRef.current,
                date: dateRef.current,
            });

            setRenderCheckBoxes(false);
            setSelectedOptions([]);
            getOutputValue("info changed");  // 상태 변경 후 새 요청

        } else {
            getOutputValue('Yes');
        }
    };

    const renderOutput = (message, withYesNoButtons, withCheckBoxes) => {
        const outputEntry = [message, withYesNoButtons, withCheckBoxes];
        const newOutputValues = [...outputValues, outputEntry];
        setOutputValues(newOutputValues);
    
        console.log("outputValues:", newOutputValues);
    
        sessionStorage.setItem("outputValues", JSON.stringify(newOutputValues));
    };

    const checker = (value) => {
        const { message } = value;
        console.log("in checker", message);
    
        const shouldShowYesNoButtons = (movieNameRef.current && regionRef.current && dateRef.current) ? true : false;

        console.log("in checker", shouldShowYesNoButtons, movieNameRef.current, regionRef.current, dateRef.current);
        renderOutput(message, shouldShowYesNoButtons, false);
    };

    const sendInputValue = (value) => {
        const newInputValues = [...inputValues, value];
        setInputValues(newInputValues);
        sessionStorage.setItem("inputValues", JSON.stringify(newInputValues));
    };

    const sendOutputValue = (message, withYesNoButtons = false, withCheckBoxes = false) => {
        renderOutput(message, withYesNoButtons, withCheckBoxes);
    };

    // 매뉴얼 메시지 보내기
    useEffect(() => {
        if (manualMessage) {
            sendOutputValue(manualMessage);
            setManual('');
        }
    }, [manualMessage]);

    const getOutputValue = async (currentInput) => {
        let endpoint;
        let body;

        const formatDate = (date) => {
            const d = new Date(date);
            const month = '' + (d.getMonth() + 1);
            const day = '' + d.getDate();
            const year = d.getFullYear();
            return [year, month.padStart(2, '0'), day.padStart(2, '0')].join('-');
        };

        const formatTime = (time) => {
            if (!time) return null;
        
            const t = new Date(time);
            if (isNaN(t.getTime())) {
                console.error("Invalid time value:", time);
                return null; 
            }
            
            return t.toISOString().slice(11, 16);
        };

        try {
            if (movieNameRef.current && regionRef.current && dateRef.current) {
                endpoint = `/api/v1/movie/running-times`;
                body = {
                    movieName: movieNameRef.current || "",
                    region: regionRef.current || "",
                    date: dateRef.current ? formatDate(dateRef.current) : null,
                    time: time ? formatTime(time) : null
                };
            } else if (movieNameRef.current || regionRef.current || dateRef.current) {
                endpoint = `/api/v1/movie/query/additional`;
                body = {
                    parsedQuery: {
                        ...(movieNameRef.current && { movieName: movieNameRef.current }),
                        ...(regionRef.current && { region: regionRef.current }),
                        ...(dateRef.current && { date: formatDate(dateRef.current) }),
                        ...(time && { time: formatTime(time) })
                    },
                    message: currentInput || ""
                };
            } else {
                endpoint = `/api/v1/movie/query?message=${encodeURIComponent(currentInput)}`;
                body = null;
            }

            console.log("보낸값 혹은 설정값", movieNameRef.current, regionRef.current, dateRef.current, time);
            console.log("endpoint", endpoint, body);

            const response = await fetch(endpoint, {
                method: body ? "POST" : "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                body: body ? JSON.stringify(body) : null,
            });

            const data = await response.json();

            if (data.movieName) setMovieName(() => data.movieName);
            if (data.region) setRegion(() => data.region);
            if (data.date) setDate(() => data.date);
            if (data.time) setTime(() => data.time);

            console.log("응답값: ", data);

            setResponseMessage(data.message);  // 응답 메시지를 상태에 저장

        } catch (error) {
            console.error("Error fetching movie data:", error);
            return { error: "Error fetching movie data." };
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-header"><ChatHeader /></div>
            <div className="chat-reaction" ref={scrollRef}>
                <ChatReaction
                    inputValues={inputValues}
                    outputValues={outputValues}
                    onYes={() => handleYesNoResponse('Yes')}
                    onNo={() => handleYesNoResponse('No')}
                    renderCheckBoxes={renderCheckBoxes}
                    handleCheckBoxChange={handleCheckBoxChange}
                    handleChangeOrNot={handleChangeOrNot}
                />
            </div>
            <div className="chat-input">
                <ChatInput
                    inputValues={inputValues}
                    sendInputValue={sendInputValue}
                    getOutputValue={getOutputValue}
                    disabled={isInputDisabled} // 입력 필드 비활성화 설정
                />
            </div>
        </div>
    );
}

export default Chat;
