import Axios from "axios";
import {REACT_APP_BASE_URL} from '@env';


const API = Axios.create({
  baseURL: REACT_APP_BASE_URL,
  withCredentials : true,
});


export default API;
