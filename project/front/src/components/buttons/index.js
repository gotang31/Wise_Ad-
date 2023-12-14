import React, { useState } from "react";
import { Link } from "react-router-dom";

//Static Imports
import "./index.css"

function RoundedButton(props) {
    const [isHovering, setIsHovering] = useState(false);
  
    const handleMouseOver = () => {
      setIsHovering(true);
    };
  
    const handleMouseOut = () => {
      setIsHovering(false);
    };

    return (
        <Link style={{
            width:'50%',
            heigh:"40px",
            paddingTop:'5px',
            paddingBottom:'5px',
            display:'flex',
            justifyContent:'center',
            alignItems:'center',
            margin: '5px',
            textDecoration:'none',
            backgroundColor: "#fff",
            color:'#123',
            borderRadius:'20px',
            fontWeight:'700'
        }}
        className={isHovering ? "grow" : ""} 
        to={'/' + props.link} 
        onMouseOver={handleMouseOver}
        onMouseOut={handleMouseOut}>
            {props.text}
        </Link>
    )
}

export {RoundedButton}