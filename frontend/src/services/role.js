import axios from "axios";

export const BASE_URL = process.env.REACT_APP_API_V1

export default async function roleNameCheck(role) {
  const token = localStorage.getItem("accessToken")
  let check = false
    await axios({
      method: "get",
      url: BASE_URL + "account/role/role-name",
      headers: { "Content-Type": "application/json" , "Authorization": "Bearer " + token,},
    })
      .then(function (response) {
        if (response.status === 200){
          const data = response.data
          
          data.every(item =>{
            if (role.indexOf(item) > -1){
              check = true
              return false
            }else return true
          })
        }else if (response.status === 400 || response.status === 404) {
          console.log("wrong email or password")
        }
        return check
      })
      .catch(function (response) {
        console.log(response);
        return check
      });
}