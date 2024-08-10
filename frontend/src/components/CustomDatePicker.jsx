import React, {useContext, useEffect, useState} from "react";
import DatePicker from "react-datepicker";
import moment from 'moment';
import "react-datepicker/dist/react-datepicker.css";
import {HomeContext} from "./HomeContext";
const CustomDatePicker = () => {

    const { movieInfo, setMovieInfo } = useContext(HomeContext);
    const [startDate, setStartDate] = useState(moment().format("YYYY-MM-DD"));
    const onChange = (start) => {
        setStartDate(moment(start).format("YYYY-MM-DD"));
    };

    useEffect(() => {
        setMovieInfo({ ...movieInfo, date: startDate });
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