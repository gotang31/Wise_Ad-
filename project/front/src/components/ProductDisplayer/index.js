import React from "react";
import { useEffect } from "react";


//Test Import
import LOADING_IMAGE from "../../assets/Loading.png"
import { GetImage } from "../../api";

function ProductDisplayer(props){
    const productName = props.item[0];
    const productPrice = props.item[1];
    const productImage = props.item[2];
    const productLink = props.item[3];
    const curCategory = props.category;

    return(
        <div style={{width:"100%", height:"100%", backgroundColor:"#fff", borderRadius:10}} onClick={() => {if(productLink !== undefined) {window.open(productLink)} }}>
            <img style={{width:"100%", height:"80%"}} src={`http://localhost:5001/api/image?category=${curCategory}&imgID=${productImage}` || LOADING_IMAGE} className={productName} alt={productName} />
            <div style={{fontSize:9, marginLeft:5}}>{productName}</div>
            <div style={{textAlign:"right", marginRight:5, fontWeight:"700"}}>₩ {productPrice}</div>
        </div>
    )
}

export {ProductDisplayer}