import API from './cookie-handling/axiosAPI';

const handleInput = async ({inputText,corpName}) => {
    const result = await API.post('/melong',{
        question : {inputText}
    })
    .then((response)=>response.json())
    .catch((error)=>{
      console.error('Error:', error);
    });

    return result['answer'];

    // const data = {'isDart' : isDart, 'query' : inputText};
    // const url = '';
    // const rr = fetch(url, {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify(data),
    // })
    //   .then(response => response.json())
    //   .catch(error => {
    //     console.error('Error:', error);
    // });
    // if ( rr === undefined){
    //   return '서버가 응답이 없어요.';
    // }
    // else{
    //   return rr['answer'];
    // }
  };



export default handleInput;