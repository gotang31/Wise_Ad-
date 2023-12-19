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

function IconButton(props) {
  const image = props.image
  const userFunction = props.onClick
  const buttonText = props.text

  return (
    <div style={{display:"flex",flexDirection:"column", alignItems:"center", justifyContent:"center"}} onClick={userFunction}>
      <img src={image} style={{width:"50px", height:"50px"}} />
      <div style={{width:"80px", height:"20px", marginTop:10,  color:"#fff", fontWeight:"700", fontSize:12, borderRadius:20, borderStyle:"none", backgroundColor:"rgba(0,0,0,0)", textAlign:"center"}}>{buttonText}</div>
    </div>
  )
}

export {RoundedButton, IconButton}