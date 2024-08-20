import { useState, useEffect, useContext } from "react";
import { AppContext } from "../AppContext";

function ManualChat() {
    const { setManual } = useContext(AppContext);
    const [isFirstVisit, setIsFirstVisit] = useState(false);

    useEffect(() => {
        const firstVisit = sessionStorage.getItem("firstVisit");

        if (!firstVisit) {
            setIsFirstVisit(true);
            sessionStorage.setItem("firstVisit", "false");
        }
    }, []);

    useEffect(() => {
        if (isFirstVisit) {
            setManual(
                `안녕하세요! 저는 여러 영화관의 정보를 통합하여 제공하는 지능형 고객 지원 챗봇입니다.\n` +
                `원하는 날짜, 시간, 지역에 따른 맞춤형 영화 상영 스케줄 정보를 제공합니다.\n` +
                `날짜, 지역을 선택하고 보고싶은 영화 제목을 입력해주세요!`
            );
            setIsFirstVisit(false);
        }
    }, [isFirstVisit, setManual]);

    return null;
}

export default ManualChat;
