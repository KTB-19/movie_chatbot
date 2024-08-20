import './App.css';
import Aside from "./Aside/Aside";
import Chat from "./Chat/Chat";
import ManualChat from './Chat/ManualChat';
import { AppProvider } from "./AppContext";

function App() {
    return (
        <AppProvider>
            <div className="ratioContainer">
                <ManualChat />
                <div className="sidebar"><Aside /></div>
                <Chat />
            </div>
        </AppProvider>
    );
}

export default App;