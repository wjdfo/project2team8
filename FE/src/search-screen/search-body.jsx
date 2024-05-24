import { FlatList, StyleSheet, TouchableOpacity,Text,Alert } from "react-native";
import {useState,useEffect} from 'react';
import { Color, Width, Height, FontFamily,} from "../../GlobalStyles";
import { fetchSearch } from "../fetch-handling/fetch-search";
const SearchBody = ({navigation, route, text,keyboardHeight}) => {
    const [corpList, setCorpList] = useState([]);

    var data;
    useEffect( () => {
        async function search() {
            data =  await fetchSearch(text);
            setCorpList(data);
        }
        search();
    },[text]);

    const handlePressResult = (corp_name,isDart) => {
        if (route.params === undefined) {
            navigation.navigate('chatScreen',{searchedName:corp_name, sNisDart:isDart, keyboardHeight:keyboardHeight});
        }
        else{
            Alert.alert(
                corp_name,
                '확실한가요 ?',
                [
                    {text : '네', onPress:()=> navigation.navigate('chatScreen',{searchedName:route.params.searchedName,sNisDart:route.params.sNisDart,
                                                                            targetCorpName:corp_name,tNisDart:isDart, keyboardHeight:keyboardHeight}),style:'default'},
                    {text : '아니오',onPress:()=>{},style:'cancel'},
                ],
                {cancelable:true,
                onDismiss: () => {},
                },
            );
        }
    };

    const renderItem = ( {item} ) => (
        <TouchableOpacity style = {styles.resultItemContainer}
                        onPress={()=> handlePressResult(item.corp_name, item.isDart)}>
            <Text style = {styles.resultItem}>
                {item.corp_name}
            </Text>
        </TouchableOpacity>
    );
    

    return (
    <FlatList style={styles.resultBody}
    data = {corpList}
    renderItem={renderItem}
    keyExtractor={item => item.corp_name}/>
    );

};

const styles = StyleSheet.create({

    resultBody : {
        width : 1080 * Width,
        top : 222 * Height,
        height : 1442 * Height,
    },
    resultItemContainer : {
        width : 1080*Width,
        height : 206 * Height,
        justifyContent:'center',
    },
    resultItem : {
        fontFamily : FontFamily.kNUTRUTH,
        fontSize : 75 * Width,
        color : Color.colorWhite,
        left : 51 * Width,
    },

});


export default SearchBody;
