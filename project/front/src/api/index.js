import axios from "axios"

function GetResponse(){
    axios.get('/test')
        .then((response) => {
            alert(response.data);
        })
        .catch((error) => {
            alert(error);
        })

}

function GetByYoutubeLink(videoID){
    return new Promise(function(resolve,reject) {
        axios.get(`/videoinfo?vID=${videoID}`)
            .then((response) => {
                const res = response.data
                // console.log(`request for ${videoID} has been successfully delivered`);
                // console.log(`response ${res}`)

                resolve(res)
            })
            .catch((error) => {
                alert(error)
            })
    })
}

function GetByYoutubeLinkAndSec(videoID, sec) {
    axios.get(`/videosecinfo?vID=${videoID}&second=${sec}`)
        .then((response) => {
            // console.log(`request for ${videoID}:${sec} has been successfully delivered`)
            // console.log(`response ${response.data}`)
        })
}

function GetImage(category, imgID) {
    return new Promise(function(resolve,reject) {
        axios.get(`/image?category=${category}&imgID=${imgID}`)
            .then((response) => {
                const res = response.data
                resolve(res)
            })
            .catch((error) => {
                alert(error)
            })
    })
}

export { GetResponse, GetByYoutubeLink, GetByYoutubeLinkAndSec, GetImage }