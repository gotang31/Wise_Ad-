import { HashRouter, Routes, Route, useNavigate } from "react-router-dom";
import React, { useEffect } from "react";
//STATIC IMPORTS

import { TestScreen } from "../screens/TestScreen";
import { StartScreen } from "../screens/StartScreen";
import { MainScreen } from "../screens/MainScreen";

const ExtensionRouter = () => {
    useEffect(()=>{console.log("online")}, [])
    
    return (
        <HashRouter>
            <Routes>
                <Route path="/" element={<StartScreen />} />
                <Route path="/main" element={<MainScreen />} />
                <Route path="/test" element={<TestScreen />} />
            </Routes>
        </HashRouter>
    )
}

export { ExtensionRouter }