import React from 'react';

function YesNoButtons({ onYes, onNo }) {
    return (
        <div>
            <button onClick={onYes}>Yes</button>
            <button onClick={onNo}>No</button>
        </div>
    );
}

export default YesNoButtons;