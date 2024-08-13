import './App.css';
import Aside from "./Aside/Aside";
import {AppProvider} from "./AppContext";

function App() {
  return (
      <AppProvider>
        <Aside />
      </AppProvider>
  );
}

export default App;
