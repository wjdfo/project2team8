import { View, StyleSheet,  
     TextInput,TouchableOpacity, Image, Keyboard, Alert} from "react-native";
import React, { useState } from "react";
import { Color, Width, Height, FontFamily,} from "../../GlobalStyles";
import SearchBody from "./search-body";

const SearchWindow = ({navigation,route}) =>{
    const [searchText,setSearchText] = useState('');
    const [keyboardHeight, setKeyboardHeight] = useState(0);



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
                    source={require("../../assets/GoBack.png")}
                    />
                </TouchableOpacity>

                <TextInput placeholder={'어떤 기업을 찾을까요 ?'}
                           placeholderTextColor={Color.colorLightGray}
                           style = {styles.searchTextBox}
                           value={searchText}
                           onChangeText={(text)=>setSearchText(text)}
                           />

                <TouchableOpacity style={styles.cancelButton} onPress={()=>setSearchText('')}>
                    <Image
                    style={styles.cancelIcon}
                    resizeMode="contain"
                    source={require("../../assets/Cancel.png")}
                    />
                </TouchableOpacity>

            </View>
            <SearchBody navigation={navigation}
                        route={route}
                        text={searchText}
                        keyboardHeight={keyboardHeight}
                        />

        </View>

    );
};

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
        backgroundColor : Color.colorDarkenGray,
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


export default SearchWindow;