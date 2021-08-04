import axios from 'axios';


export const BASE_URL = process.env.REACT_APP_API_V1


export default function isUserLogin(){
    const freshToken = localStorage.getItem('freshToken');
    const accessToken = localStorage.getItem('accessToken');
    const isRemember = localStorage.getItem('isRemember');
    var expireAccessToken = localStorage.getItem('expireAccessToken');
    var expireFreshToken = localStorage.getItem('expireFreshToken');
    expireAccessToken = new Date(expireAccessToken)
    expireFreshToken = new Date(expireFreshToken)
    var d1 = new Date();
    var now = new Date( d1.getUTCFullYear(), d1.getUTCMonth(), d1.getUTCDate(), d1.getUTCHours(), d1.getUTCMinutes(), d1.getUTCSeconds() );
    const bodyFreshToken = new FormData();
    bodyFreshToken.append("refresh_token", freshToken);
    let check = false


    if (accessToken === null) return check
    else if (expireAccessToken > now) {
        check = true
        console.log("good token")
        return check
    }
    else if (expireFreshToken < now) {
        console.log("bad token")
        return check
    }
    else if (expireAccessToken < now && expireFreshToken && isRemember === true){
        console.log("refresh token")
        axios({
            method: "post",
            url: BASE_URL + "account/login/refresh-token",
            data: bodyFreshToken,
            headers: { "Content-Type": "multipart/form-data" },
        }).then(function (response) {
            if (response.status === 200){
                check = true
                const data = response.data
                localStorage.setItem('tokenType', data.token_type)
                localStorage.setItem('accessToken', data.access_token)        
                localStorage.setItem('freshToken', data.refresh_token)   
                localStorage.setItem('expireAccessToken', data.expire_token)   
                localStorage.setItem('expireFreshToken', data.expire_refresh_token) 
                console.log("save new token")
                return check
            }
            else {
                localStorage.clear()
                console.log("fresh error token")
                return check
            }
        }).catch(function (response) {
            localStorage.clear();
            console.log("api error token")
            return check
        });
    }
    else {
        console.log("khac")
        return check
    }
}