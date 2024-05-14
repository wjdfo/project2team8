import Axios from "axios";

const API = Axios.create({
  baseURL: process.env.REACT_APP_BASE_URL,
  headers : {
    'Content-Type' : 'application/json',
  },
  withCredentials : true,
});


export default API;
