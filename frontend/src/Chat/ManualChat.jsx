import React, { useState, useEffect, useContext } from "react";
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
            setManual("안녕하세요! 이 사이트에 오신 것을 환영합니다. 사용 방법은 다음과 같습니다: ...");
            setIsFirstVisit(false);
        }
    }, [isFirstVisit, setManual]);

    return null;
}

export default ManualChat;
