import './App.css';
import Aside from "./Aside/Aside";
import Chat from "./Chat/Chat";
import ManualChat from './Chat/ManualChat';
import { AppProvider } from "./AppContext";
import { useEffect, useState } from 'react';
import { PiSidebarSimple } from "react-icons/pi";

function App() {
    // 사이드바 조절
    const [isSidebarVisible, setSidebarVisible] = useState('');

    useEffect(() => {
        const handleResize = () => {
            setSidebarVisible(window.innerWidth > window.screen.width / 2);
        };
        
        // 브라우저 창의 크기가 변경될 때마다 handleResize 함수를 실행하도록 이벤트 리스너를 추가
        window.addEventListener('resize', handleResize);
        handleResize(); // 초기 로드 시 실행
        
        // 컴포넌트가 언마운트될 때만 실행
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    const toggleSidebar = () => {
        setSidebarVisible(!isSidebarVisible);
    };


    return (
        <AppProvider>
            <div className="ratioContainer">
                <ManualChat />
                <button className="toggle-button" onClick={toggleSidebar}>
                    <div className='sidebar-button'>
                        < PiSidebarSimple />
                    </div>
                </button>
                {isSidebarVisible && <div className="sidebar"><Aside /></div>}
                <Chat />
            </div>
        </AppProvider>
    );
}

export default App;