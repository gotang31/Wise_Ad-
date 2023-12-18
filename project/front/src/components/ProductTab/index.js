//External Imports
import React, { useState } from "react"

//Local Imports
import { ProductDisplayer } from "../ProductDisplayer"

//Static Imports
import "./index.css"

//Test Import
import TESTIMAGE from "../../assets/ExampleProductPhoto.png"

function ProductTab(props) {
    const [currentCategory, SetCategory] = useState("")

    return(
        <div style={{display:"flex", flexDirection:"column", width:"100%", height:"100%", alignItems:"center", justifyContent:"center"}}>
            <div style={{display:"flex", flexDirection:"row", width:"100%", marginRight:10, marginLeft:10}}>
                    <Tab curCategory={currentCategory} setCategoryFunction={SetCategory}>{props.tabFirst}</Tab>
                    <Tab curCategory={currentCategory} setCategoryFunction={SetCategory}>{props.tabSecond}</Tab>
                    <Tab curCategory={currentCategory} setCategoryFunction={SetCategory}>{props.tabThird}</Tab>
                    <Tab curCategory={currentCategory} setCategoryFunction={SetCategory}>{props.tabFourth}</Tab>
            </div>
            <DisplayProducts curCategory={currentCategory} />
        </div>
    )
}

function Tab(props){
    let currentColor = ""
    if(props.curCategory == props.children){
        currentColor = "#c01718"
    }
    else {
        currentColor = "rgba(255,255,255,0.2)"
    }

    return(
        <div style={{color:"#fff",
            width:"25%",
            height: 30,
            display:"flex", 
            alignItems:"center", 
            justifyContent:"center", 
            backgroundColor: currentColor, 
            borderTopRightRadius:10,
            borderTopLeftRadius:10,
            fontSize:10
        }} 
        onClick={()=>{props.setCategoryFunction(props.children)}}>{props.children}</div>
    )
}

function DisplayProducts(props){
    const TESTDATA = [["강아지사료건식사료", "39,800", TESTIMAGE],["고양이사료건식사료", "39,800", TESTIMAGE],["펭귄사료건식사료", "39,800", TESTIMAGE],["기린사료건식사료", "39,800", TESTIMAGE]]

    return(
        <div style={{display:"flex", flexDirection:"row", flexWrap:"wrap", width:"100%", height:"90%", backgroundColor:"#fff", borderBottomLeftRadius:10, borderBottomRightRadius:10}}>
            {TESTDATA.map((item, index)=>{
                return(
                    <div key={index} style={{display:"flex", width:"50%", height:"50%", alignItems:"center", justifyContent:"center" ,backgroundColor:"#c01718", borderRadius:10}}>
                        <ProductDisplayer item={item} />
                    </div>
                )
            })}
        </div>
    )
}

export { ProductTab, DisplayProducts }