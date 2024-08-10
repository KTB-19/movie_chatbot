import React, {useState} from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
const CustomDatePicker = () => {
    const [startDate, setStartDate] = useState(new Date());
    const onChange = (start) => {
        setStartDate(start);
    };

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