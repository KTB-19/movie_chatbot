import './App.css';
import Aside from "./Aside/Aside";
import Chat from "./Chat/Chat";
import {AppProvider} from "./AppContext";

function App() {
    return (
        <AppProvider>
            <div className="ratioContainer">
                <div className="sidebar"><Aside /></div>
                <Chat />
            </div>
        </AppProvider>
    );
}

export default App;