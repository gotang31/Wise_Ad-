//External Imports
import React, { useState, useEffect } from "react"

//Local Imports
import { ProductDisplayer } from "../ProductDisplayer"
import { CoupangCodeToCategoryName } from "../../utils";

//Static Imports
import "./index.css"

function ProductTab(props) {
    const [curTabIdx, setCurTabIdx] = useState(0);
    const [itemList, setItemList] = useState([]);
    const category = [props.tabFirst, props.tabSecond, props.tabThird, props.tabFourth]
    const [curCategoryCode, setCurCategoryCode] = useState("");

    useEffect(() => {
        setItemList(props.itemlist[curTabIdx])
        setCurCategoryCode(category[curTabIdx])
    }, [])

    useEffect(() => {
        setItemList(props.itemlist[curTabIdx])
        setCurCategoryCode(category[curTabIdx])
    }, [curTabIdx,props])

    const firstTab = CoupangCodeToCategoryName(props.tabFirst)
    const secondTab = CoupangCodeToCategoryName(props.tabSecond)
    const thirdTab = CoupangCodeToCategoryName(props.tabThird)
    const fourthTab = CoupangCodeToCategoryName(props.tabFourth)
    
    return(
        <div style={{display:"flex", flexDirection:"column", width:"100%", height:"100%", alignItems:"center", justifyContent:"center"}}>
            <div style={{display:"flex", flexDirection:"row", width:"100%", marginRight:10, marginLeft:10}}>
                    <Tab idx={0} setIdxFunction={setCurTabIdx} curIdx={curTabIdx}>{firstTab}</Tab>
                    <Tab idx={1} setIdxFunction={setCurTabIdx} curIdx={curTabIdx}>{secondTab}</Tab>
                    <Tab idx={2} setIdxFunction={setCurTabIdx} curIdx={curTabIdx}>{thirdTab}</Tab>
                    <Tab idx={3} setIdxFunction={setCurTabIdx} curIdx={curTabIdx}>{fourthTab}</Tab>
            </div>
            <DisplayProducts curItemList={itemList} category={curCategoryCode} />
        </div>
    )
}

function Tab(props){
    let currentColor = ""
    if(props.idx == props.curIdx){
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
            textAlign:'center',
            backgroundColor: currentColor, 
            borderTopRightRadius:10,
            borderTopLeftRadius:10,
            fontSize:10,
            wordWrap:'normal'
        }} 
        onClick={()=>{props.setIdxFunction(props.idx);}}>{props.children}</div>
    )
}

function DisplayProducts(props){
    const itemData = props.curItemList || [["Loading", "Loading", undefined, undefined],["Loading", "Loading", undefined, undefined],["Loading", "Loading", undefined, undefined],["Loading", "Loading", undefined, undefined]]
    console.log(props.curItemList)
    return(
        <div style={{display:"flex", flexDirection:"row", flexWrap:"wrap", width:"100%", height:"90%", backgroundColor:"#fff", borderBottomLeftRadius:10, borderBottomRightRadius:10}}>
            {itemData.map((item, index)=>{
                return(
                    <div key={index} style={{display:"flex", width:"50%", height:"50%", alignItems:"center", justifyContent:"center" ,backgroundColor:"#c01718", borderRadius:10}}>
                        <ProductDisplayer item={item} category={props.category} />
                    </div>
                )
            })}
        </div>
    )
}

export { ProductTab, DisplayProducts }