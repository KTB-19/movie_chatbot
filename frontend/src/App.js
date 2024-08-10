import './App.css';
import Aside from "./components/Aside";
import {Home} from "./components/HomeContext";

function App() {
  return (
      <Home>
        <Aside />
      </Home>
  );
}

export default App;
