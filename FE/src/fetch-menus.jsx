import API from './cookie-handling/axiosAPI';

export const fetchList = (corpName) => {
    // var result = await API.post('/melong',{
    //     corpName : {corpName}
    // })
    // .then((response)=>response.json())
    // .catch((error)=>{
    //   console.error('Error:', error);
    //   result = 'server error';
    // });

    return corpName;

};

export const fetchURL = (corpName) => {

    return { "삼성전자" : "www.naver.com", "애플" : "www.google.com"};
}
