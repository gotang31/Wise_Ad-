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

function CoupangCodeToCategoryName(ccode) {
    const mapping = {
        445726 : "강아지 건식사료",
        445727 : "강아지 소프트사료",
        445728 : "강아지 습식사료",
        445729 : "강아지 건조/생식사료",
        445730 : "강아지 화식사료",
        445731 : "강아지 분유",
        118975 : "강아지 캔/파우치",
        385001 : "강아지 덴탈껌",
        385002 : "강아지\n건조간식/육포",
        385003 : "강아지 동결건조간식",
        118974 : "강아지 비스켓/시리얼/쿠키",
        225064 : "강아지 빵/케이크",
        118980 : "강아지 음료",
        486319 : "강아지 영양제",
        118920 : "강아지 하우스/울타리",
        118919 : "강아지 급식기/급수기",
        118926 : "강아지 의류/패션",
        118916 : "강아지 배변용품",
        118917 : "강아지 미용/목욕",
        118923 : "강아지 장난감/훈련",
        118922 : "강아지 이동장/외출",
        445860 : "고양이 건식사료",
        445861 : "고양이 소프트사료",
        445862 : "고양이 건조생식사료",
        445863 : "고양이 화식사료",
        446151 : "고양이 분유",
        119522 : "고양이 캔",
        120216 : "고양이 동결건조",
        119501 : "고양이 수제간식",
        119502 : "고양이 져키/스틱",
        119503 : "고양이 통살/소시지",
        119504 : "고양이 스낵",
        119505 : "고양이 캣닢/캣그라스",
        119506 : "고양이 음료",
        119567 : "고양이 캣타워/스크래쳐",
        119562 : "고양이 하우스/방석",
        157054 : "고양이 의류/패션",
        119558 : "고양이 배변용품",
        385076 : "고양이 미용/목욕",
        119568 : "고양이 장난감",
        119499 : "고양이 파우치",
        119559 : "고양이 건강관리",
        119561 : "고양이 급식기/급수기",
        119564 : "고양이 이동장/외출용품",
        120217 : "고양이 껌",
        225063 : "강아지 젤리",
        225106 : "강아지 도서",
        225107 : "고양이 도서",
        373649 : "강아지 건강관리",
        381523 : "강아지 배변봉투/삽",
        381526 : "강아지 물티슈/크리너",
        381527 : "강아지 기저귀/매너벨트",
        381528 : "강아지 입마개",
        381529 : "강아지 가슴줄/하네스",
        381532 : "강아지 목줄",
        381535 : "강아지 리드줄",
        381538 : "강아지 자동줄",
        381539 : "강아지 인식표/목걸이",
        381540 : "강아지 이동가방/캐리어",
        385004 : "강아지 져키/트릿",
        445733 : "강아지 테린/화식",
        445864 : "고양이 테린/화식",
        486328 : "강아지 건강보조제",
        486332 : "고양이 영양제",
        486342 : "고양이 건강보조제",
        486542 : "강아지 펫캠/가전용품",
        486545 : "고양이 펫캠/가전용품",
        509024 : "강아지 기능성사료",
        509026 : "고양이 기능성사료"        
    }

    return mapping[ccode];
}

export { 
    VideoIdExtractFromURL,
    TimestringToSec,
    SecToTimestring,
    SendMessageToChromeAPI,
    GetCurrentUrl,
    CoupangCodeToCategoryName
 }