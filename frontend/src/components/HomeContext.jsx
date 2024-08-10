import {createContext, useEffect, useState} from "react";

const HomeContext = createContext();
const Home = ({children}) => {

    const [movieInfo, setMovieInfo] = useState({
        movieName: null,
        region: null,
        date: null,
    });

    useEffect(() => {
        console.log("movieInfo : " + JSON.stringify(movieInfo));
    }, [movieInfo]);

    return (
        <HomeContext.Provider value={{ movieInfo, setMovieInfo }}>
            {children}
        </HomeContext.Provider>
    );
};

export { HomeContext, Home };