import React from "react";
import Chat from "./Chat/Chat";
import "./App.css";
import { AppProvider } from "./AppContext";

function App() {
    return (
        <AppProvider>
            <div className="ratioContainer">
                <div className="sidebar">Sidebar</div>
                <Chat />
            </div>
        </AppProvider>
    );
}

export default App;
