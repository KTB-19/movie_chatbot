import DateSelector from "./DateSelector";
import RegionSelector from "./RegionSelector";
import "../styles/home.css";
const Aside = () => {
    return (
        <div className="aside">
            <div className="logo-container">
                <div className="logo">
                    <h1 style={{color : "white"}}>Logo</h1>
                </div>
            </div>
            <RegionSelector></RegionSelector>
            <DateSelector></DateSelector>
        </div>
    );
};
export default Aside;