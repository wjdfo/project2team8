import API from '../cookie-handling/axiosAPI';

export const fetchList = async (corpName, isDart) => {
    const request = await API.post('/api/corporations',{
        corpName : corpName,
        isDart : isDart
    })
    .then((response)=>{result = response.data;})
    .catch((error)=>{
      console.error('Error:', error);
      return 'server went wrong';
    });
    return result['list'];
};

export const fetchURL = async (corpName,fromDate,toDate,isDart) => {
    const request = await API.post('/api/report_url',{
        corpName : corpName,
        fromDate : fromDate,
        toDate : toDate,
        isDart : isDart
    })
    .then((response)=>{result = response.data;})
    .catch((error)=>{
      console.error('Error:', error);
      return 'server went wrong';
    });
    return result['link'];
};

export const fetchSummary = async (corpName,reportYear, isDart) => {

    const request = await API.post('/api/summary',{
        corpName : corpName,
        reportNum : reportYear,
        isDart : isDart
    })
    .then((response)=>{result = response.data;})
    .catch((error)=>{
      console.error('Error:', error);
      return 'server went wrong';
    });

    return result['summary'];

};

export const fetchCompare = async (corpName,isDart, targetCorpName,targetIsDart ) => {
    const request = await API.post('/api/compare',{
        corpName : corpName,
        corpIsDart : isDart,
        targetCorpName : targetCorpName,
        targetIsDart : targetIsDart
    })
    .then((response)=>{result = response.data;})
    .catch((error)=>{
      console.error('Error:', error);
      return 'server went wrong';
    });

    return result['report'];

};