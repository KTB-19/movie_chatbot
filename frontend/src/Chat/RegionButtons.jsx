import React from 'react';
import "./RegionButtons.css";

function RegionButtons({ regions, onRegionSelect }) {
    return (
        <div className="region-buttons">
            {regions.map((region, idx) => (
                <button 
                    key={idx} 
                    className="region-button"
                    onClick={() => onRegionSelect(region)}
                >
                    {region}
                </button>
            ))}
        </div>
    );
}

export default RegionButtons;
