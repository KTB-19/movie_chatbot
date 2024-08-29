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
    const [yesNoValue, setYesNoValue] = useState('');
    const [recommendMessage, setRecommendMessage] = useState(''); // recommendMessage 상태 추가
    const [isInputDisabled, setIsInputDisabled] = useState(false); // 사용자가 버튼 입력할 때(yesno, checkbox) input 비활성화 상태 추가

    const scrollRef = useRef();
    const { movieName, region, date, time, setMovieName, setRegion, setDate, setTime, manualMessage, setManual } = useContext(AppContext);

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

    function YesNoButtons({ onYes, onNo }) {
        return (
            <div>
                <button onClick={onYes}>Yes</button>
                <button onClick={onNo}>No</button>
            </div>
        );
    }

    useEffect(() => {
        if (yesNoValue === 'Yes') {
            // yes면 checker에서 value.recommendMessage를 outputMessage로 두고 sendOutputValue(recommendMessage), return recommendMessage
            console.log('Yes 선택함');
            sendOutputValue(recommendMessage); // 추천 메시지 전송
            setIsInputDisabled(false); // 입력을 다시 활성화
        } else if (yesNoValue === 'No') {
            // no면 체크박스 세개 만들어서(날짜 바꾸기, 지역 바꾸기, 영화 바꾸기) 중복선택가능하게. 
            const handleOptionChange = (option) => {
                switch (option) {
                    case 'date':
                        setDate('');
                        break;
                    case 'region':
                        setRegion('');
                        break;
                    case 'movieName':
                        setMovieName('');
                        break;
                    default:
                        break;
                }
            };

            const options = (
                <div>
                    <label>
                        <input type="checkbox" onChange={() => handleOptionChange('date')} />
                        날짜 바꾸기
                    </label>
                    <label>
                        <input type="checkbox" onChange={() => handleOptionChange('region')} />
                        지역 바꾸기
                    </label>
                    <label>
                        <input type="checkbox" onChange={() => handleOptionChange('movieName')} />
                        영화 바꾸기
                    </label>
                </div>
            );

            sendOutputValue(options);

            //no인 경우 getoutputvalue의 additional query 실행.
            getOutputValue("");
            setIsInputDisabled(false); // 입력을 다시 활성화
        }
    }, [yesNoValue, recommendMessage]);

    const handleYesNoResponse = (response) => {
        setYesNoValue(response);
        setIsInputDisabled(true); // YesNoButtons이 활성화되면 입력 비활성화
    };

    const checker = (value) => {
        // let outputMessage = "";
        // const theaters = value.theaterRunningTimes || [];
        // const count = theaters.length;
    
        // if (count > 0) {
        //     outputMessage += `${region} 지역 ${date}의 ${movieName} 상영시간표입니다:\n\n`;
        
        //     theaters.forEach(theater => {
        //         const times = theater.times.join(", ");
        //         outputMessage += `극장: ${theater.theaterName}\n`;
        //         outputMessage += `상영 시간: ${times}\n\n`;
        //     });
        // } else {
        //     outputMessage = "상영 스케줄이 없습니다.";
        // }

        // const checkMessage = value.checkMessage;
        const checkMessage = "checkMessage입니다.";

        const messageWithButtons = (
            <div>
                <p>{checkMessage}</p>
                <YesNoButtons
                    onYes={() => handleYesNoResponse('Yes')}
                    onNo={() => handleYesNoResponse('No')}
                />
            </div>
        );

        sendOutputValue(messageWithButtons);
        setRecommendMessage(value.recommendMessage);
        return messageWithButtons;
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

    // 매뉴얼 메시지 보내기
    useEffect(() => {
        if (manualMessage) {
            const newOutputValues = [...outputValues, manualMessage];
            setOutputValues(newOutputValues);
            setManual('');
        }
    }, [manualMessage, outputValues, setManual]);

    const getOutputValue = async (currentInput) => {
        let endpoint;
        let body;
        let initialRequestWas3 = false;
    
        const formatDate = (date) => {
            const d = new Date(date);
            const month = '' + (d.getMonth() + 1);
            const day = '' + d.getDate();
            const year = d.getFullYear();
            return [year, month.padStart(2, '0'), day.padStart(2, '0')].join('-');
        };
    
        const formatTime = (time) => {
            if (!time) return null;
        
            // time이 이미 "HH:mm" 형식의 문자열인 경우 그대로 반환
            if (typeof time === 'string' && time.match(/^\d{2}:\d{2}$/)) {
                return time;
            }
        
            const t = new Date(time);
            if (isNaN(t.getTime())) {
                console.error("Invalid time value:", time);
                return null; // 유효하지 않은 시간 값 처리
            }
        
            return t.toISOString().slice(11, 16); // "HH:mm" 형식
        };
        
    
        if (movieName && region && date) {
            initialRequestWas3 = true;
            endpoint = `/api/v1/movie/running-times`;
            body = {
                movieName: movieName || "",
                region: region || "",
                date: date ? formatDate(date) : null,
                time: time ? formatTime(time) : null
            };
        } else if (movieName || region || date) {
            endpoint = `/api/v1/movie/query/additional`;
            body = {
                parsedQuery: {
                    ...(movieName && { movieName }),
                    ...(region && { region }),
                    ...(date && { date: formatDate(date) }),
                    ...(time && { time: formatTime(time) })
                },
                message: currentInput || ""
            };
        } else {
            endpoint = `/api/v1/movie/query?message=${encodeURIComponent(currentInput)}`;
            body = null; 
        }
    
        console.log("보낸값 혹은 설정값", movieName, region, date, time);
        console.log("endpoint", endpoint, body);
    
        try {
            const response = await fetch(endpoint, {
                method: body ? "POST" : "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                body: body ? JSON.stringify(body) : null,
            });
    
            const data = await response.json();
    
            if (initialRequestWas3) {
                return checker(data);
            }
    
            if (data.movieName) setMovieName(data.movieName);
            if (data.region) setRegion(data.region);
            if (data.date) setDate(data.date);
            if (data.time) setTime(data.time);
    
            console.log("응답값", movieName, region, date, time, data.message);
    
            if (!initialRequestWas3 && data.movieName && data.region && data.date) {
                endpoint = `/api/v1/movie/running-times`;
                body = {
                    movieName: movieName,
                    region: region,
                    date: date ? formatDate(date) : null,
                    time: time ? formatTime(time) : null
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
                return checker(finalData);
            }
    
            sendOutputValue(data.message);
            return data.message;
    
        } catch (error) {
            console.error("Error fetching movie data:", error);
            return { error: "Error fetching movie data." };
        }
    };
    
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
                    // sendOutputValue={sendOutputValue} 
                    disabled={isInputDisabled} // 입력 비활성화 속성 추가
                />
            </div>
        </div>
    );
}

export default Chat;
