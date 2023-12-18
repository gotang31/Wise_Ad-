//External Imports
import React from "react"

//Static Imports
import "./index.css"

function BlinkText(props){
    return(
        <div className="blink" style={props.style}>
            {props.children}
        </div>
    )
}

export { BlinkText }