//External Imports
import { useNavigate } from "react-router-dom"
import React from "react"
import { useState, useEffect } from "react"
import Lottie from "lottie-react"

//Local Imports
import { ProductTab } from "../../components/ProductTab/index.js"
import { GetByYoutubeLink, GetByYoutubeLinkAndSec } from "../../api/index.js"
import { VideoIdExtractFromURL, SecToTimestring, TimestringToSec, GetCurrentUrl } from "../../utils/index.js"

//Static Imports
import OwlFindingLottie from "../../assets/OwlFindingLottie.json"
import { BlinkText } from "../../components/textContainer/index.js"
import { IconButton } from "../../components/buttons/index.js"
import SearchImage from "../../assets/Icon_Glass.png"
import WishlistImage from "../../assets/Icon_wishlist.png"
import RefreshImage from "../../assets/Icon_Refresh.png"


function MainScreen(){
    const [curUrl, setCurUrl] = useState("");
    const [curTime, setCurTime] = useState("00:00");
    const [duration, setDuration] = useState("00:00");
    const [curTabs, setCurTabs] = useState(["낙타", "펭귄", "나무늘보", "키위"])
    const [curFocusKey, setCurFocusKey] = useState("강아지")
    const navigate = useNavigate()
    
    useEffect(() =>{GetCurrentUrl(setCurUrl);}, []);
    useEffect(() =>{
        const videoID = VideoIdExtractFromURL(curUrl);
        if(curUrl !== ""){
            GetByYoutubeLink(videoID).then((res)=>{
                if(res == "None"){
                    navigate("/start")
                }
                else {
                    navigate("/main")
                    alert(res)
                    console.log(res)
                }
            })
        }
    },[curUrl])
    
    
    //Get Current Tabs Youtube Video Time per second. activated properly when timeline visible
    if(chrome.tabs !== undefined){
        setTimeout(() => {
            chrome.tabs?.query({active: true, lastFocusedWindow: true}, tabs => {
                let id = tabs[0]?.id;
                if(id !== undefined){
                    chrome.scripting.executeScript({
                        target: {tabId: id},
                        func: GetYoutubeTime,
                    }).then((result) => {
                        const curSec = result[0].result[0];
                        const duration = result[0].result[1];
                        console.log(curSec, "/", duration);
                        setCurTime(SecToTimestring(curSec));
                        setDuration(SecToTimestring(duration));
                        GetCurrentUrl(setCurUrl);
                    })
                }
            })
        }, 1000)
    }

    return(
        <div style={{display:"flex", width:"100%", height:"100%", flexDirection:"column", backgroundColor: "#123", borderRadius:10}}>
            <div className="Header" style={{height:"7%", display:"flex", alignItems:"center", justifyContent:"center", color:"#fff", fontSize:17, fontWeight:"700"}}>YOURECO ({curTime} / {duration})</div>
            <div className="URL" style={{height:"3%", display:"flex", alignItems:"center", justifyContent:"center", color:"#fff"}}>{curUrl}</div>
            <div className="ProductDisplay" style={{height:"70%", marginLeft:10, marginRight:10}}>
                <ProductTab tabFirst={curTabs[0]} tabSecond={curTabs[1]} tabThird={curTabs[2]} tabFourth={curTabs[3]}/>
            </div>
            <div className="UserInterface" style={{height:"20%", display:"flex"}}>
                <div style={{display:"flex", width:"30%", height:"100%", flexDirection:"column", justifyContent:"start", alignItems:"center"}}><Lottie style={{height:"80%"}} animationData={OwlFindingLottie}></Lottie><BlinkText style={{fontSize: 11, color:"#fff", fontWeight:"500", marginTop:-20}}>영상 인식중..</BlinkText></div>
                <div style={{display:"flex", width:"70%", flexDirection:"column"}}>
                    <div style={{display:"flex", color:"#fff", alignItems:"center", justifyContent:"center", marginTop:20, marginBottom:20}}>
                        현재 추천 카테고리 : {curFocusKey || "없음"}
                    </div>
                    <div style={{display:"flex", width:"100%", justifyContent:"space-evenly", alignItems:"center"}}>
                        <IconButton image={SearchImage} text={"Search"} onClick={() => {GetByYoutubeLinkAndSec(VideoIdExtractFromURL(curUrl),TimestringToSec(curTime))}} />
                        <IconButton image={WishlistImage} text={"Wishlist"} onClick={() => {navigate("/wish")}}/>
                        <IconButton image={RefreshImage} text={"Refresh"} onClick={() => {ResetTimeout(curTime, setCurTime)}} />
                    </div>
                </div>
            </div>
        </div>
    )
}

function GetYoutubeTime() {
    let curTime = parseInt(document.querySelector("video").currentTime);
    let duration = parseInt(document.querySelector("video").duration);
    
    return [curTime, duration]
}

function ResetTimeout(curTime, resetFunction) {
    if(curTime == "0"){
        resetFunction("-1")
    }
    else {
        resetFunction("0");
    }
}

export { MainScreen }