import React, { useState, useEffect } from "react";
import Lottie from "lottie-react"

//Internal Imports
import { RoundedButton } from "../../components/buttons";
import { BlinkText } from "../../components/textContainer";

//STATIC IMPORTS
import OwlNoddingLottie from "../../assets/OwlNoddingLottie.json"
import OwlSayNoLottie from "../../assets/OwlSayNoLottie.json"

function StartScreen(){
    const [curUrl, setCurUrl] = useState("");
    useEffect(() =>{GetCurrentUrl(setCurUrl);}, []);
    
    return (
        <div style={{width: '100%', height: '100%', backgroundColor:'#e1c02c', display: "flex", justifyContent:'center', alignItems: 'center', flexDirection:'column'}}>
            <div style={{color:"#fff"}}>영상인식 기반 상품 추천 시스템</div>
            <div style={{color:"#fff", fontSize:40, fontWeight:"700"}}>YOURECO</div>
            <div style={{color:"#fff", marginTop: 40}}>{curUrl || "현재 URL이 없습니다."}</div>
            <div style={{display:"flex", height:"30%", flexDirection:"column", justifyContent:"center", alignItems:"center"}}>
                <Lottie style={{height:"100%"}} animationData={OwlNoddingLottie} />
            </div>
            <RoundedButton link={"Sned"} text={"요청보내기"}></RoundedButton>
            <RoundedButton link={"Main"} text={"상품찾기"}></RoundedButton>
            <BlinkText style={{fontSize:10, color:"#fff", marginTop:10}}>*시간 인식이 잘 되지 않는 경우 유튜브 영상에 마우스를 올려주세요</BlinkText>
        </div>
    )
}

function GetCurrentUrl(SetURLFunction) {
    if(chrome.tabs !== undefined){
        chrome.tabs?.query({active: true, lastFocusedWindow: true}, tabs => {
            let url = tabs[0].url;
            SetURLFunction(url);
        })
    }
    else if(chrome.tabs === undefined){
        console.log("!GetCurrentUrl : System Not Running on Chrome Extension")
    }
}

export { StartScreen }