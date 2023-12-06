import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import React from "react";

import { TestScreen } from "../screens/TestScreen";
import { MainScreen } from "../screens/MainScreen";

const ExtensionRouter = () => {
    return (
        <BrowserRouter>
        <Link to={"/"}>Hello</Link>
            <Routes>
                <Route path="/" element={<MainScreen />} />
                <Route path="/test" element={<TestScreen />} />
            </Routes>
        </BrowserRouter>
    )
}

export { ExtensionRouter }