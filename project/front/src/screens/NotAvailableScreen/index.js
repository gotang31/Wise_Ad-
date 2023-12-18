import React, {useEffect, useState} from "react";
import Lottie from "lottie-react"
import { useNavigate } from "react-router-dom"

//Local Imports
import { BlinkText } from "../../components/textContainer";
import { VideoIdExtractFromURL, GetCurrentUrl } from "../../utils";
import { GetByYoutubeLink } from "../../api";

//STATIC IMPORTS
import OwlNoddingLottie from "../../assets/OwlNoddingLottie.json"

function NotAvailableScreen(){
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
            <BlinkText style={{fontSize:12, color:"#c01718", marginTop:10}}>YOURECO는 Youtube 영상 시청중에 사용 가능합니다.</BlinkText>
        </div>
    )
}

export { NotAvailableScreen }