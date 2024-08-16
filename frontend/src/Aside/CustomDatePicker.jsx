import React, {useContext, useEffect, useState} from "react";
import DatePicker from "react-datepicker";
import moment from 'moment';
import "react-datepicker/dist/react-datepicker.css";
import {AppContext} from "../AppContext";
import "./CustomDatePicker.css";

const CustomDatePicker = () => {

    const { date, setDate } = useContext(AppContext); // AppContext에서 date와 setDate 가져오기
    const [startDate, setStartDate] = useState(new Date()); // 초기 날짜를 오늘로 설정

    const onChange = (date) => {
        setDate(date); 
        setDate(moment(date).format("YYYY-MM-DD")); 
    };

    return (
        <DatePicker
            selected={date}
            onChange={onChange}
            startDate={startDate}
            inline
        />
    );
};

export default CustomDatePicker;
