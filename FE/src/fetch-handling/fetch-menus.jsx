import API from '../cookie-handling/axiosAPI';

export const fetchList = async (corpName) => {
    return corpName;

    const request = await API.post('/api/corporations',{
        corpName : corpName
    })
    .then((response)=>{result = response.data;})
    .catch((error)=>{
      console.error('Error:', error);
      return 'server went wrong';
    });
    console.log(result['list']);
    return result['list'];
};

export const fetchURL = async (corpName,fromDate,toDate) => {


    return { "삼성전자" : "www.naver.com", "애플" : "www.google.com"};

    const request = await API.post('/api/report_url',{
        corpName : corpName,
        fromDate : fromDate,
        toDate : toDate,
    })
    .then((response)=>{result = response.data;})
    .catch((error)=>{
      console.error('Error:', error);
      return 'server went wrong';
    });

    return result['link'];
};

export const fetchSummary = async (corpName,reportYear) => {
    return corpName+reportYear;

    const request = await API.post('/api/summary',{
        corpName : corpName,
        reportNum : reportYear
    })
    .then((response)=>{result = response.data;})
    .catch((error)=>{
      console.error('Error:', error);
      return 'server went wrong';
    });

    return result['summary'];

};

export const fetchCompare = async (corpName, targetCorpName ) => {
    return corpName + targetCorpName;

    const request = await API.post('/api/compare',{
        corpName : corpName,
        targetCorpName : targetCorpName
    })
    .then((response)=>{result = response.data;})
    .catch((error)=>{
      console.error('Error:', error);
      return 'server went wrong';
    });

    return result['report'];

};