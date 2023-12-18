import React, { useState, useEffect } from "react";
import Lottie from "lottie-react"

//Internal Imports
import { RoundedButton } from "../../components/buttons";
import { BlinkText } from "../../components/textContainer";
import { GetByYoutubeLink } from "../../api";
import { VideoIdExtractFromURL, GetCurrentUrl } from "../../utils";

//STATIC IMPORTS
import OwlNoddingLottie from "../../assets/OwlNoddingLottie.json"
import { useNavigate } from "react-router";

function StartScreen(){
    const [curUrl, setCurUrl] = useState("");
    const navigate = useNavigate();

    useEffect(() =>{GetCurrentUrl(setCurUrl);}, []);
    useEffect(() =>{
        const videoID = VideoIdExtractFromURL(curUrl);
        if(curUrl !== ""){
            GetByYoutubeLink(videoID).then((res)=>{
                if(res == "None"){
                    let curUrlIsYoutube = curUrl?.search("youtube.com/watch");
                    if(curUrlIsYoutube == -1){
                        navigate("/invalid")
                    }
                    else {
                        navigate("/start")
                    }
                }
                else {
                    navigate("/main")
                }
            })
        }
    },[curUrl])

    setInterval(() => {GetCurrentUrl(setCurUrl);},1000)
    
    return (
        <div style={{width: '100%', height: '100%', backgroundColor:'#e1c02c', display: "flex", justifyContent:'center', alignItems: 'center', flexDirection:'column', borderRadius:10}}>
            <div style={{color:"#fff"}}>영상인식 기반 상품 추천 시스템</div>
            <div style={{color:"#fff", fontSize:40, fontWeight:"700"}}>YOURECO</div>
            <div style={{display:"flex", height:"30%", flexDirection:"column", justifyContent:"center", alignItems:"center"}}>
                <Lottie style={{height:"100%"}} animationData={OwlNoddingLottie} />
            </div>
            <div style={{color:"#c01718", fontSize:15, fontWeight:"500"}}>현재 영상에 대한 데이터가 없습니다.</div>
            <RoundedButton link={"Sned"} text={"요청보내기"}></RoundedButton>
            <BlinkText style={{fontSize:10, color:"#fff", marginTop:10}}>*YOURECO로 영상 기반 실시간 추천을 받아보세요</BlinkText>
        </div>
    )
}

export { StartScreen }