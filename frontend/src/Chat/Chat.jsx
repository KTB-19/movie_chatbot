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
    const [regionOptions, setRegionOptions] = useState([]); // 지역 선택 옵션
    const [showRestartButton, setShowRestartButton] = useState(false); // 재시작 버튼 표시 여부

    const scrollRef = useRef();
    const { movieName, region, date, time, setTime, setMovieName, setRegion, setDate, manualMessage, setManual } = useContext(AppContext);

    const movieNameRef = useRef(movieName);
    const regionRef = useRef(region);
    const dateRef = useRef(date);

    useEffect(() => {
        // 상태가 변경될 때마다 ref에 최신 상태를 저장
        movieNameRef.current = movieName;
        regionRef.current = region;
        dateRef.current = date;
    }, [movieName, region, date]);

    useEffect(() => {
        // input과 output 세션 스토리지에서 불러오기
        const savedInputValues = JSON.parse(sessionStorage.getItem("inputValues") || "[]");
        const savedOutputValues = JSON.parse(sessionStorage.getItem("outputValues") || "[]");
        setInputValues(savedInputValues);
        setOutputValues(savedOutputValues);
    }, []);

    useEffect(() => {
        // 상태가 업데이트된 후 checker 실행 및 입력 활성화
        if (responseMessage) {
            console.log("Running checker...");
            checker({
                message: responseMessage,
                movieName: movieNameRef.current,
                region: regionRef.current,
                date: dateRef.current,
            });
            setResponseMessage('');  // 메시지 초기화
            setIsSubmitting(false);  // 요청이 끝나면 입력 다시 활성화

            // 응답 처리 후 입력을 활성화
            if (!renderCheckBoxes) {
                setIsInputDisabled(false);
            }
        }
    }, [responseMessage, renderCheckBoxes]);

    useEffect(() => {
        // 새로운 input or output 추가되면 scroll to bottom
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
            sendOutputValue('무엇을 변경하시겠습니까?', false, true);
            setIsInputDisabled(false); // 응답 후 입력 활성화
        }
    };
    
    // 확인필요
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
                    await setDate('');
                    dateRef.current = '';
                    changedValues += 'date ';
                }
                if (selectedOptions.includes('region')) {
                    await setRegion('');
                    regionRef.current = '';
                    sessionStorage.setItem("wideArea", '');
                    sessionStorage.setItem("basicArea", '');
                    changedValues += 'region ';
                }
                if (selectedOptions.includes('movieName')) {
                    await setMovieName('');
                    movieNameRef.current = '';
                    changedValues += 'moviename ';
                }
    
                let inputText = changedValues + "정보를 변경할래.";
                sendInputValue(inputText);
                sendOutputValue("변경할 "+ changedValues + "정보를 입력하세요");
            }
    
            setRenderCheckBoxes(false);
            setSelectedOptions([]);
            // await getOutputValue(changedValues+" 정보들을 변경할래");  // 상태 변경 후 새 3 요청
        } else {
            let inputText = "변경하지 않았습니다.";
            sendInputValue(inputText);
            await getOutputValue('Yes');
        }
    
        setIsInputDisabled(false); // 체크박스 동작 후 입력 활성화
    };

    const handleRegionSelection = (selectedRegion) => {
        console.log("in regionselector", selectedRegion);
        setRegion(selectedRegion);
        regionRef.current = selectedRegion; 

        // 지역이 선택되면 지역 선택 옵션을 초기화하고, getOutputValue를 호출하여 다음 단계로 진행
        setRegionOptions([]);
        setIsInputDisabled(false);
        getOutputValue(selectedRegion);
    };

    // 확인필요
    const renderRegionSelectionButtons = (regions) => {
        if (regions.length === 2) {
            sendOutputValue("지역을 선택하세요", false, false, true);
            setIsInputDisabled(true);
        }
    };

    const sendOutputValue = (message, withYesNoButtons, withCheckBoxes, withRegionButtons = false, onClickHandler = null) => {
        const outputEntry = [message, withYesNoButtons, withCheckBoxes, withRegionButtons, onClickHandler];
        if (outputValues.length > 0 && outputValues[outputValues.length - 1][0] === "응답 대기 중...(새로고침하지 마세요)") {
            outputValues[outputValues.length - 1] = outputEntry;
            setOutputValues(outputValues);
            console.log("outputValues:", outputValues);
            if (message !== "응답 대기 중...(새로고침하지 마세요)") sessionStorage.setItem("outputValues", JSON.stringify(outputValues));
        } else {
            const newOutputValues = [...outputValues, outputEntry];
            setOutputValues(newOutputValues);
            console.log("outputValues:", newOutputValues);
            if (message !== "응답 대기 중...(새로고침하지 마세요)") sessionStorage.setItem("outputValues", JSON.stringify(newOutputValues));
        }
    };

    const checker = (value) => {
        const { message } = value;
        console.log("in checker", message);
    
        // 세 값이 모두 null이 아니면 yesno button 띄우기 (& 3번 요청이 아니었음)
        const shouldShowYesNoButtons = (movieNameRef.current && regionRef.current && dateRef.current) ? true : false;

        console.log("in checker", shouldShowYesNoButtons, movieNameRef.current, regionRef.current, dateRef.current);
        sendOutputValue(message, shouldShowYesNoButtons && !runningTimesQueryExecuted, false); // runningTimesQueryExecuted 상태 추가
        if (shouldShowYesNoButtons) {
            setIsInputDisabled(true); // Yes/No 버튼이 표시되면 입력을 비활성화
        }
    };

    const sendInputValue = (value) => {
        const newInputValues = [...inputValues, value];
        setInputValues(newInputValues);
        sessionStorage.setItem("inputValues", JSON.stringify(newInputValues));
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
        sendOutputValue("응답 대기 중...(새로고침하지 마세요)", false, false, null);

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
                endpoint = `${process.env.REACT_APP_ENDPOINT}/api/v1/movie/running-times`;
                isRunningTimesQuery = true;
                body = {
                    movieName: movieNameRef.current || "",
                    region: regionRef.current || [""],
                    date: dateRef.current ? formatDate(dateRef.current) : null,
                    time: time ? formatTime(time) : null
                };
            } 
            // else (movieNameRef.current || regionRef.current || dateRef.current) {
            else {
                endpoint = `${process.env.REACT_APP_ENDPOINT}/api/v1/movie/query/additional`;
                body = {
                    parsedQuery: {
                        ...(movieNameRef.current && { movieName: movieNameRef.current }),
                        ...(regionRef.current && { region: regionRef.current }),
                        ...(dateRef.current && { date: formatDate(dateRef.current) }),
                        ...(time && { time: formatTime(time) })
                    },
                    message: currentInput || ""
                };
            } 
            // else {
            //     endpoint = `/api/v1/movie/query?message=${encodeURIComponent(currentInput)}`;
            //     body = null;
            // }

            console.log("보낸값", movieNameRef.current, regionRef.current, dateRef.current, time);
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
                setShowRestartButton(true); // 3번 쿼리 실행 후 재시작 버튼 표시
            }

            let isTwoRegion = false;

            if (data.movieName) {
                setMovieName(data.movieName);
                movieNameRef.current = data.movieName;
            }

            if (data.region) {
                if (Array.isArray(data.region) && data.region.length === 2) {
                    setRegionOptions(data.region);
                    renderRegionSelectionButtons(data.region);
                    isTwoRegion = true;
                } else if (Array.isArray(data.region)) {
                    setRegion(data.region[0]);
                    regionRef.current = data.region[0];
                    setRegionOptions([]); // 초기화
                }
            } 
            // else {
            //     setRegionOptions([]); // 초기화
            // }

            if (data.date) {
                setDate(data.date);
                dateRef.current = data.date;
            }

            if (data.time) {
                setTime(data.time);
            }

            console.log("응답값: ", data);

            if (!isTwoRegion) {
                setResponseMessage(data.message);
                setIsInputDisabled(false);
            }

        } catch (error) {
            console.error("Error fetching movie data:", error);
            setIsSubmitting(false);
            setIsInputDisabled(false);
        }
    };

    const handleRestartChat = () => {
        // 채팅 상태 및 세션 스토리지 초기화
        setInputValues([]);
        setOutputValues([]);
        sessionStorage.clear();
        setManual(
            `안녕하세요! 저는 여러 영화관의 정보를 통합하여 제공하는 지능형 고객 지원 챗봇입니다.\n` +
            `원하는 날짜, 시간, 지역에 따른 맞춤형 영화 상영 스케줄 정보를 제공합니다.\n` +
            `왼쪽 사이드바에서 날짜, 지역을 선택하고 보고싶은 영화 제목을 입력해주세요!`
        );

        setMovieName('');
        setRegion('');
        setDate('');
        setTime('');
        movieNameRef.current = '';
        regionRef.current = '';
        dateRef.current = '';
        setShowRestartButton(false);
        setRunningTimesQueryExecuted(false); // 리셋 후 3번 쿼리 상태 초기화

        // 매뉴얼 메시지 다시 출력, output 배열의 첫 번째 항목으로 추가
        if (manualMessage) {
            setOutputValues([manualMessage]);
            sessionStorage.setItem("outputValues", JSON.stringify([manualMessage]));
            sendOutputValue(manualMessage);  // 매뉴얼 메시지를 출력하도록 getOutputValue 호출
            setManual('');
        }

        console.log("restart", outputValues);
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
                regionOptions={regionOptions} 
                handleRegionSelection={handleRegionSelection} 
            />
                {showRestartButton && (
                <div className="chat-restart">
                    <button onClick={handleRestartChat}>채팅 재시작</button>
                </div>
            )}
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
