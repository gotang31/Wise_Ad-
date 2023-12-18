import React from "react";

function VideoIdExtractFromURL(curUrl){
    const url = curUrl;
    const regex = /[?&]v=([^&]+)/;

    const match = url.match(regex);
    const videoID = match ? match[1] : null;

    return videoID;
}


function TimestringToSec(str) {
    let sec = str[0] * 600 + str[1] * 60 + str[3] * 10 + str[4] * 1

    return sec
}

function SecToTimestring(sec) {
    let timeString = ""
    timeString += parseInt(sec / 600);
    sec = sec % 600
    timeString += parseInt(sec / 60);
    sec = sec % 60
    timeString += ":"
    timeString += parseInt(sec / 10);
    sec = sec % 10
    timeString += parseInt(sec / 1);

    return timeString
}

function SendMessageToChromeAPI(action){
    if(chrome.tabs !== undefined){
        chrome.runtime.sendMessage({action: action}, (response)=>{console.log(response)})
    }
    else if(chrome.tabs === undefined){
        console.log("!SendMessageToChromeAPI : System Not Running on Chrome Extension")
    }
}

function GetCurrentUrl(SetURLFunction) {
    if(chrome.tabs !== undefined){
        chrome.tabs?.query({active: true, lastFocusedWindow: true}, tabs => {
            let url = tabs[0]?.url;
            SetURLFunction(url);
        })
    }
    else if(chrome.tabs === undefined){
        console.log("!GetCurrentUrl : System Not Running on Chrome Extension")
    }
}

export { 
    VideoIdExtractFromURL,
    TimestringToSec,
    SecToTimestring,
    SendMessageToChromeAPI,
    GetCurrentUrl
 }