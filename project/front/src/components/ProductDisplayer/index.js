import React from "react";

import TESTIMAGE from "../../assets/ExampleProductPhoto.png"

function ProductDisplayer(props){
    const productName = props.item[0];
    const productPrice = props.item[1];
    const productImage = props.item[2];

    return(
        <div style={{width:"100%", height:"100%", backgroundColor:"#fff"}}>
            <img style={{width:"100%", height:"80%"}} src={TESTIMAGE} className={productName} alt={productName} />
            <div style={{fontSize:9 }}>{productName}</div>
            <div style={{textAlign:"right", fontWeight:"700"}}>₩ {productPrice}</div>
        </div>
    )
}

export {ProductDisplayer}