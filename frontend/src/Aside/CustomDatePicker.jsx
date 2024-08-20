import React, { useContext, useEffect } from "react";
import DatePicker from "react-datepicker";
import moment from "moment";
import "react-datepicker/dist/react-datepicker.css";
import { AppContext } from "../AppContext";
import "./CustomDatePicker.css";
import { ko } from "date-fns/locale";

const CustomDatePicker = () => {
    const { date, setDate } = useContext(AppContext);

    // 세션 스토리지에서 날짜 불러오기
    useEffect(() => {
        const savedDate = sessionStorage.getItem("date");
        if (savedDate) {
            setDate(savedDate);
        }
    }, [setDate]);

    const onChange = (date) => {
        const formattedDate = moment(date).format("YYYY-MM-DD");
        setDate(formattedDate); 
        sessionStorage.setItem("date", formattedDate); 
    };

    return (
        <DatePicker
            locale={ko}
            selected={date ? moment(date, "YYYY-MM-DD").toDate() : null} // 문자열을 Date 객체로 변환하여 DatePicker에 전달
            onChange={onChange}
            inline
        />
    );
};

export default CustomDatePicker;
