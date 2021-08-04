import axios from 'axios';

export const BASE_URL = process.env.REACT_APP_API_V1

export default async function loginAccessToken(username, password, isRemember, path) {
  var bodyFormData = new FormData();
  bodyFormData.append('username', username);
  bodyFormData.append('password', password);
  let isLogin = false;

  await axios({
    method: "post",
    url: BASE_URL + "account/login/access-token",
    data: bodyFormData,
    headers: { "Content-Type": "multipart/form-data" },
  })
    .then(function (response) {
      if (response.status === 200){
        const data = response.data
        if (isRemember === true) {
          console.log("save token")
          localStorage.setItem('isRemember', isRemember)
          localStorage.setItem('tokenType', data.token_type)
          localStorage.setItem('accessToken', data.access_token)        
          localStorage.setItem('freshToken', data.refresh_token)   
          localStorage.setItem('expireAccessToken', data.expire_token)   
          localStorage.setItem('expireFreshToken', data.expire_refresh_token)
          window.location.href = path   
        }
        isLogin = true     
      }else if (response.status === 400 || response.status === 404) {
        console.log("wrong email or password")
      }
    })
    .catch(function (response) {
      console.log(response);
    });
  return isLogin
  
}
