import API from './cookie-handling/axiosAPI';

export const fetchSearch = async (queryCorp) => {
    var result;
    const request = await API.post('/api/search_recommendation',{
        search:queryCorp
    })
    .then((response)=>{result = response.data;})
    .catch((error)=>{
      console.error('Error:', error);
      return 'server went wrong';
    });

    console.log(result['list']);
    return queryCorp;
    return result['list'];

}