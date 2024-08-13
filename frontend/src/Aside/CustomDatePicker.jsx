import React, {useContext, useEffect, useState} from "react";
import DatePicker from "react-datepicker";
import moment from 'moment';
import "react-datepicker/dist/react-datepicker.css";
import {AppContext} from "../AppContext";

const CustomDatePicker = () => {

    const { date, setDate } = useContext(AppContext)
    const [startDate, setStartDate] = useState(moment().format("YYYY-MM-DD"));
    const onChange = (start) => {
        setStartDate(moment(start).format("YYYY-MM-DD"));
    };

    useEffect(() => {
        setDate(startDate);
    }, [startDate]);

    return (
        <DatePicker
            selected = {startDate}
            onChange = {onChange}
            startDate = {startDate}
            inline
            />
        );
}

export default CustomDatePicker;