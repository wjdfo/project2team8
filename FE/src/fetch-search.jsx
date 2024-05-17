import API from './cookie-handling/axiosAPI';

export const fetchSearch = async (queryCorp) => {
    var arry = [];
    var result;
    const request = await API.post('/api/search_recommendation',{
        search:queryCorp
    })
    .then((response)=>{result = response.data;})
    .catch((error)=>{
      console.error('Error:', error);
      return 'server went wrong';
    });

    const rr = JSON.parse(result['list']);
    var each_json;
    
    Object.keys(rr).map((key)=>{
      each_json = { corp_name : rr[key]['fields']['corp_name']};
      arry = [...arry,each_json];
    })
    return arry;

}