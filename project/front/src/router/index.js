import { HashRouter, Routes, Route } from "react-router-dom";
import React, { useEffect, useState } from "react";

//Local IMPORTS
import { GetCurrentUrl } from "../utils";
import { TestScreen } from "../screens/TestScreen";
import { StartScreen } from "../screens/StartScreen";
import { MainScreen } from "../screens/MainScreen";
import { NotAvailableScreen } from "../screens/NotAvailableScreen";
import { WishlistScreen } from "../screens/WishlistScreen";

const ExtensionRouter = () => {
    const [curUrl, setCurUrl] = useState("");
    useEffect(() =>{GetCurrentUrl(setCurUrl);}, []);
    
    setInterval(() => {GetCurrentUrl(setCurUrl);},1000)

    let initialPage = <StartScreen />;
    let curUrlIsYoutube = curUrl?.search("youtube.com/watch");
    if(curUrlIsYoutube == -1){
        initialPage = <StartScreen /> //NotAvailableScreen, Temp Start Screen
    }
    else if(curUrlIsYoutube != -1){
        initialPage = <StartScreen />
    }
    
    return (
        <HashRouter>
            <Routes>
                <Route path="/" element={initialPage} />
                <Route path="/main" element={<MainScreen />} />
                <Route path="/start" element={<StartScreen />} />
                <Route path="/wish" element={<WishlistScreen />} />
                <Route path="/invalid" element={<NotAvailableScreen />} />
            </Routes>
        </HashRouter>
    )
}

export { ExtensionRouter }