import React, {createContext, useState} from "react";

const AppContext = createContext();

const AppProvider = ({ children }) => {
    const [movieName, setMovieName] = useState('');
    const [region, setRegion] = useState('');
    const [date, setDate] = useState('');
    const [time, setTime] = useState('');

    const [manualMessage, setManual] = useState('');

    return (
        <AppContext.Provider value={{ movieName, setMovieName, region, setRegion, date, setDate, time, setTime, manualMessage, setManual }}>
            {children}
        </AppContext.Provider>
    );
};

export { AppContext, AppProvider };