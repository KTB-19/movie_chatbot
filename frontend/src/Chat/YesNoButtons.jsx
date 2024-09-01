import React from 'react';
import "./YesNoButtons.css";

function YesNoButtons({ onYes, onNo }) {
    return (
        <div className="yesno-buttons">
            <button className="yes-button" onClick={onYes}>Yes</button>
            <button className="no-button" onClick={onNo}>No</button>
        </div>
    );
}

export default YesNoButtons;
