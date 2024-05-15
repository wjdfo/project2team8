import { View, Text, StyleSheet,  
    FlatList, TextInput,TouchableOpacity, Image, Keyboard} from "react-native";
import React, { useState,  useRef, useEffect } from "react";
import { Color, Width, Height, FontFamily,} from "../GlobalStyles";

const SearchWindow = ({navigation}) =>{
    const [searchText,setSearchText] = useState('');
    const [corpList, setCorpList] = useState([]);
    const [keyboardHeight, setKeyboardHeight] = useState(0);

    const data = [
        {
            corp_name : '삼성전자',
        },
        {
            corp_name : '현대자동차',
        },
        {
            corp_name : '경북대학교',
        }
    ];


    const renderItem = ( {item} ) => (
        <TouchableOpacity style = {styles.resultItemContainer}
                        onPress={()=> handlePressResult(item.corp_name)}>
            <Text style = {styles.resultItem}>
                {item.corp_name}
            </Text>
        </TouchableOpacity>
    );
    

    const handlePressResult = (corp_name) => {
        navigation.navigate('chatScreen',{searchedName:corp_name, keyboardHeight:keyboardHeight});
    };

    const handleSearchText =(text) =>{
        // CorpList 업데이트
        setCorpList(data);
        setSearchText(text);
    };

    const handleShowedKeyboard = Keyboard.addListener('keyboardDidShow', (e) =>{
        setKeyboardHeight(e.endCoordinates.height);
      });
    

    return (
        <View style={styles.searchWindowContainer}>
            <View style={styles.searchBox}>
                <TouchableOpacity style={styles.goBackButton} onPress={()=>navigation.goBack()}>
                    <Image
                    style={styles.goBackIcon}
                    resizeMode="contain"
                    source={require("../assets/GoBack.png")}
                    />
                </TouchableOpacity>

                <TextInput placeholder={'어떤 기업을 찾을까요 ?'}
                           placeholderTextColor="#797c7b"
                           style = {styles.searchTextBox}
                           value={searchText}
                           onChangeText={handleSearchText}
                           />

                <TouchableOpacity style={styles.cancelButton} onPress={()=>setSearchText('')}>
                    <Image
                    style={styles.cancelIcon}
                    resizeMode="contain"
                    source={require("../assets/Cancel.png")}
                    />
                </TouchableOpacity>

            </View>

            <FlatList style={styles.resultBody}
                      data = {corpList}
                      renderItem={renderItem}
                      keyExtractor={item => item.corp_name}/>
            

        </View>

    );
}
;

const styles = StyleSheet.create({
    searchWindowContainer : {
        width: 1080*Width,
        left: 0,
        top: 0,
        position: "absolute",
        height: 2100*Height,
        backgroundColor : Color.colorBG
  
    },
    searchBox : {
        width : 1080*Width,
        height : 222 * Height,
        backgroundColor : '#4B4B4B',
        position : 'absolute',
        top : 0,
        left : 0,
    },
    searchTextBox : {
        width : 800 * Width,
        top : 40 * Height,
        left : 150 * Width,
        fontSize : 70 * Width,
        fontFamily : FontFamily.kNUTRUTH,
        color : Color.colorWhite,
    },
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
    goBackButton : {
        width : 60 * Width,
        height : 100 * Height,
        position: 'absolute',
        left : 45 * Width,
        top : 71 * Height,
    },
    goBackIcon : {
        width: 60 * Width,
        height : 100 * Height,
    },
    cancelButton : {
        width : 100 * Width,
        height : 100 * Height,
        position: 'absolute',
        left : 954 * Width,
        top : 71 * Height,
    },
    cancelIcon :{
        width: 90 * Width,
        height : 90 * Height,

    },
});


export default SearchWindow