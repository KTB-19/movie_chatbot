import React, {createContext, useEffect, useState} from "react";

const AppContext = createContext();

const AppProvider = ({ children }) => {
    const [movieName, setMovieName] = useState('');
    const [region, setRegion] = useState('');
    const [date, setDate] = useState('');

    useEffect(() => {
        console.log("movieName : " + movieName)
        console.log("region : " + region)
        console.log("date : " + date)
    }, [movieName, region, date]);

    return (
        <AppContext.Provider value={{ movieName, setMovieName, region, setRegion, date, setDate }}>
            {children}
        </AppContext.Provider>
    );
};

export { AppContext, AppProvider };