import DateSelector from "./DateSelector";
import RegionSelector from "./RegionSelector";
import "./Aside.css";

const Aside = () => {
    return (
        <div className="aside">
            <div className="logo-container">
                <div className="logo">
                    <img className="logo-img" alt="" src="/logo.jpg" />
                    <h1 style={{color : "white", fontFamily: 'BMHANNAPro'}}>무비빔밥</h1>
                </div>
            </div>
            <RegionSelector></RegionSelector>
            <DateSelector></DateSelector>
        </div>
    );
};
export default Aside;

