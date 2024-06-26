import API from '../cookie-handling/axiosAPI';

const fetchInput =  async (inputText,corpName,isDart) => {

    var result;
    const request = await API.post('/api/prompt',{
        question : inputText,
        corpName : corpName,
        isDart : isDart
    })
    .then((response)=>{result = response.data;})
    .catch((error)=>{
      console.error('Error:', error);
      return 'server went wrong';
    });

    return result['response'];

  };



export default fetchInput;