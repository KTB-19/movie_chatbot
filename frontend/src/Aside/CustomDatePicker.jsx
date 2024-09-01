import React, { useContext, useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import moment from "moment";
import "react-datepicker/dist/react-datepicker.css";
import { AppContext } from "../AppContext";
import "./CustomDatePicker.css";
import { ko } from "date-fns/locale";

const CustomDatePicker = () => {
    const { date, setDate } = useContext(AppContext);
    const [selectedDate, setSelectedDate] = useState(null);

    // 세션 스토리지에서 날짜 불러오기
    useEffect(() => {
        const savedDate = sessionStorage.getItem("date");
        if (savedDate) {
            setDate(savedDate);
        }
    }, [setDate]);

    // context의 date 값이 변경될 때 로컬 상태도 업데이트
    useEffect(() => {
        if (date) {
            setSelectedDate(moment(date, "YYYY-MM-DD").toDate());
            sessionStorage.setItem("date", date); // 세션 스토리지에 저장
        } else {
            setSelectedDate(null);
            sessionStorage.removeItem("date"); // 값이 없을 때는 세션 스토리지에서 제거
        }
    }, [date]);

    const onChange = (date) => {
        const formattedDate = moment(date).format("YYYY-MM-DD");
        setDate(formattedDate);
        sessionStorage.setItem("date", formattedDate);
    };

    return (
        <DatePicker
            locale={ko}
            selected={selectedDate} // 로컬 상태를 DatePicker에 전달
            onChange={onChange}
            inline
        />
    );
};

export default CustomDatePicker;
