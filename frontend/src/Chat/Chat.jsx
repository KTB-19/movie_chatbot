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
    const [isSubmitting, setIsSubmitting] = useState(false); // 요청 중인지 상태
    const [renderCheckBoxes, setRenderCheckBoxes] = useState(false);
    const [selectedOptions, setSelectedOptions] = useState([]);
    const [responseMessage, setResponseMessage] = useState('');  // 응답 메시지 상태
    const [runningTimesQueryExecuted, setRunningTimesQueryExecuted] = useState(false); // 3번 쿼리 실행 여부

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

    // 상태가 업데이트된 후 checker 실행 및 입력 활성화
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
            setIsSubmitting(false);  // 요청이 끝나면 버튼을 다시 활성화

            // 응답 처리 후 입력을 활성화하도록 로직 추가
            if (!renderCheckBoxes) {
                setIsInputDisabled(false);
            }
        }
    }, [responseMessage, renderCheckBoxes]);

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
        setIsInputDisabled(true); // Yes/No 응답을 기다리는 동안 입력을 비활성화

        // Yes/No 값을 사용자 입력으로 취급하여 저장
        sendInputValue(response);

        if (response === 'Yes') {
            console.log('Yes selected');
            getOutputValue('Yes').then(() => {
                setIsInputDisabled(false); // 응답 후 입력 활성화
            });
        } else if (response === 'No') {
            console.log('No selected');
            setRenderCheckBoxes(true);
            renderOutput('무엇을 변경하시겠습니까?', false, true);
            setIsInputDisabled(false); // 응답 후 입력 활성화
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
        setIsInputDisabled(true); // 변경 처리 중 입력 비활성화
    
        let changedValues = '';
    
        if (shouldChange) {
            if (selectedOptions.length === 0) {
                // 아무것도 선택하지 않은 경우
                sendInputValue('변경하지 않았습니다.');
            } else {
                if (selectedOptions.includes('date')) {
                    await setDate(prevDate => ''); // 날짜 시간 변경
                    dateRef.current = '';
                    changedValues += 'date ';
                }
                if (selectedOptions.includes('region')) {
                    await setRegion(prevRegion => ''); // 지역 변경
                    regionRef.current = '';
                    changedValues += 'region ';
                }
                if (selectedOptions.includes('movieName')) {
                    await setMovieName(prevMovieName => ''); // 영화명 변경
                    movieNameRef.current = '';
                    changedValues += 'moviename ';
                }
    
                let inputText = changedValues + "정보를 변경했습니다.";
                sendInputValue(inputText);
            }
    
            setRenderCheckBoxes(false);
            setSelectedOptions([]);
            await getOutputValue("info changed");  // 상태 변경 후 새 요청
        } else {
            let inputText = "변경하지 않았습니다.";
            sendInputValue(inputText);
            await getOutputValue('Yes');
        }
    
        setIsInputDisabled(false); // 체크박스 동작 후 입력 활성화
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
        renderOutput(message, shouldShowYesNoButtons && !runningTimesQueryExecuted, false); // runningTimesQueryExecuted 상태 추가
        if (shouldShowYesNoButtons) {
            setIsInputDisabled(true); // Yes/No 버튼이 표시되면 입력을 비활성화
        }
    };

    const sendInputValue = (value) => {
        const newInputValues = [...inputValues, value];
        setInputValues(newInputValues);
        sessionStorage.setItem("inputValues", JSON.stringify(newInputValues));
    };

    const sendOutputValue = (message, withYesNoButtons = false, withCheckBoxes = false) => {
        renderOutput(message, withYesNoButtons && !runningTimesQueryExecuted, withCheckBoxes); // runningTimesQueryExecuted 상태 추가
    };

    // 매뉴얼 메시지 보내기
    useEffect(() => {
        if (manualMessage) {
            sendOutputValue(manualMessage);
            setManual('');
        }
    }, [manualMessage]);

    const getOutputValue = async (currentInput) => {
        setIsSubmitting(true);  // 요청 시작 시 버튼 비활성화
        setIsInputDisabled(true);  // 요청 시작 시 입력 비활성화

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
            let isRunningTimesQuery = false;

            if (movieNameRef.current && regionRef.current && dateRef.current) {
                endpoint = `/api/v1/movie/running-times`;
                isRunningTimesQuery = true; // 3번 쿼리 상태 설정
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

            if (isRunningTimesQuery) {
                setRunningTimesQueryExecuted(true); // 3번 쿼리 실행 후 상태 설정
            }

            if (data.movieName) setMovieName(() => data.movieName);
            if (data.region) setRegion(() => data.region);
            if (data.date) setDate(() => data.date);
            if (data.time) setTime(() => data.time);

            console.log("응답값: ", data);

            setResponseMessage(data.message);  // 응답 메시지를 상태에 저장
            setIsInputDisabled(false);  // 요청이 성공적으로 완료되면 입력을 활성화

        } catch (error) {
            console.error("Error fetching movie data:", error);
            setIsSubmitting(false);  // 오류 발생 시 버튼을 다시 활성화
            setIsInputDisabled(false);  // 오류 발생 시 입력을 다시 활성화
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
                    disabled={isInputDisabled || isSubmitting} // 입력 필드와 버튼 비활성화 설정
                />
            </div>
        </div>
    );
}

export default Chat;
