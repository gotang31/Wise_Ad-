import React from "react"
import { Link } from "react-router-dom"

//Local Imports
import { ProductDisplayer } from "../../components/ProductDisplayer"
import { DisplayProducts } from "../../components/ProductTab"

function WishlistScreen() {

    return(
        <div style={{display:"flex", width:"100%", height:"100%", flexDirection:"column", backgroundColor: "#123", borderRadius:10}}>
            <Link to={"/main"}>BACK</Link>
            <div className="Header" style={{height:"7%", display:"flex", alignItems:"center", justifyContent:"center", color:"#fff", fontSize:17, fontWeight:"700"}}>YOURECO</div>
            <div className="wishlist" style={{width:"95%",borderRadius:10, paddingTop:10, backgroundColor:"#fff"}}>
                <DisplayProducts />
            </div>
        </div>
    )
}

export { WishlistScreen }