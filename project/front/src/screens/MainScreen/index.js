//External Imports
import { Link } from "react-router-dom"
import React from "react"
import { useState, useEffect } from "react"
import Lottie from "lottie-react"

//Local Imports
import { ProductTab } from "../../components/ProductTab/index.js"

//Static Imports
import OwlFindingLottie from "../../assets/OwlFindingLottie.json"
import { BlinkText } from "../../components/textContainer/index.js"


function MainScreen(){
    const [curUrl, setCurUrl] = useState("");
    const [curTime, setCurTime] = useState("00:00");
    const [curTabs, setCurTabs] = useState(["강아지", "고양이", "낙타", "펭귄"])

    useEffect(() =>{GetCurrentUrl(setCurUrl);}, []);

    //Get Current Tabs Youtube Video Time per second. activated properly when timeline visible
    if(chrome.tabs !== undefined){
        setInterval(() => {
            chrome.tabs?.query({active: true, lastFocusedWindow: true}, tabs => {
                let id = tabs[0]?.id;
                if(id !== undefined){
                    chrome.scripting.executeScript({
                        target: {tabId: id},
                        func: GetYoutubeCurTime
                    }).then((result) => {
                        if(curTime !== result[0].result){
                            setCurTime(result[0].result);
                        }
                        else
                            true
                    })
                }
                else {
                    setCurTime("Please Check Video Timeline")
                }
            })
        }, 1000)
    }

    return(
        <div style={{display:"flex", width:"100%", height:"100%", flexDirection:"column", backgroundColor: "#123"}}>
            <div className="Header" style={{height:"5%", display:"flex", alignItems:"center", justifyContent:"center", color:"#fff", marginLeft:10}}>YOURECO ({curTime})</div>
            <div className="ProductDisplay" style={{height:"70%", marginLeft:10, marginRight:10}}>
                <ProductTab tabFirst={curTabs[0]} tabSecond={curTabs[1]} tabThird={curTabs[2]} tabFourth={curTabs[3]}/>
            </div>
            <div className="UserInterface" style={{height:"25%", display:"flex"}}>
                <div style={{display:"flex", height:"100%", flexDirection:"column", justifyContent:"center", alignItems:"center"}}><Lottie style={{height:"80%"}} animationData={OwlFindingLottie}></Lottie><BlinkText style={{fontSize: 11, color:"#fff", fontWeight:"500"}}>영상 인식중..</BlinkText></div>
                <button style={{width:"70px", height:"30px"}} onClick={() => {GetCurrentUrl(setCurUrl); alert(curUrl)}}>Show CurrentUrl</button>
                <button style={{width:"70px", height:"70px",borderRadius:400}} onClick={() => {SendMessageToChromeAPI("LOAD")}}>Send Message Chrome API</button>
            </div>
        </div>
    )
}

function GetYoutubeCurTime() {
    return document.getElementsByClassName("ytp-time-current")[0].innerHTML
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

function SendMessageToChromeAPI(action){
    if(chrome.tabs !== undefined){
        chrome.runtime.sendMessage({action: action}, (response)=>{console.log(response)})
    }
    else if(chrome.tabs === undefined){
        console.log("!SendMessageToChromeAPI : System Not Running on Chrome Extension")
    }
}

export { MainScreen }