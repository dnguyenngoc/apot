import React from 'react';
import DigiLogo from "../../assets/img/brand-logo/digi-texx.png"

const Logo = () => {
  return (
    <div className="pds-bottom-20">
      <a href = "https://digi-texx.vn">
        <img src={DigiLogo} className='bgs-white pds-top-5 pds-bottom-5' alt=""></img>
      </a>
    </div>
  );
};

export default Logo;