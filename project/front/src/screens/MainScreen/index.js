import { Link } from "react-router-dom"
import React from "react"
import { useState, useEffect } from "react"

function MainScreen(){
    const [curUrl, setCurUrl] = useState("")
    const [curTime, setCurTime] = useState("00:00")

    useEffect(() =>{
        chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
            let url = tabs[0].url;
            setCurUrl(url);
        })
    },
    [])

    setInterval(() => {
        chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
            let id = tabs[0]?.id;
            if(id !== undefined){
                chrome.scripting.executeScript({
                    target: {tabId: id},
                    func: getYoutubeCurTime
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
    return(
        <div style={{display:"flex", flexDirection:"column"}}>
            <div>
            {curUrl}
            </div>
            <div>
            {curTime}
            </div>

            <Link to={"test"}>To TestScreen</Link>
            <button onClick={() => {
                chrome.runtime.sendMessage({action: "LOAD"}, (response)=>{console.log(response)})
                }}>Send Message Chrome API</button>
            
            <button onClick={() => {
                chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
                    let url = tabs[0].url;
                    setCurUrl(url);
                });
            }}>GetCurrentUrl</button>
            
            <button onClick={()=>{
                console.log("P")
                    
            }}>GetCurrentVideoTime</button>
        </div>
    )
}

function getYoutubeCurTime() {
    return document.getElementsByClassName("ytp-time-current")[0].innerHTML
}

export { MainScreen }