import { View, StyleSheet, Text, TouchableOpacity, Image} from "react-native";
import {Width,Color, Height,FontFamily} from '../GlobalStyles'; //width,height 받아오기
import { setItem, getItem } from './cookie-handling/cookie';


const Initial = ({navigation}) => {
  const setCookie = async (user) => {
    try {
      await setItem('@user-id', user);
      console.log('cookie complete');
    } catch (e) {
      console.log(e);
    }
  };
  
  // const getCookie = async () => {
  //   const result = await getItem('key');
  //   return result;
  // };

  const handleInitialEntry = () => {
    setCookie('user--1');
    navigation.navigate('initial-searchScreen');
  }

  return (
    <View style={styles.introViewParent}>
      <View style={styles.introViewPosition}>
        <TouchableOpacity title = 'go to next page' onPress={handleInitialEntry}
                style={ styles.introCorpSearch}>

          <Text style={styles.introCorpSearchText}>원하는 기업을 찾아보세요...</Text>
          <Image
                    style={styles.searchIcon}
                    resizeMode="contain"
                    source={require("../assets/Search.png")}
                    />
        </TouchableOpacity>

        <Text style={styles.knuturn}>knuturn</Text>
        <View style={ {width : 500*Width,height : 500 * Height, backgroundColor:Color.colorNewturn, position:'absolute',top:0}}/>

      </View>
    </View>
  );
};



const styles = StyleSheet.create({
  introViewPosition: {
    width: 1080 * Width,
    left: 0,
    top: 0,
    position: "absolute",
    height: 2220*Height,
    backgroundColor: Color.colorBG,
    justfyContent:"center",
    alignItems :"center"
  },
  knuturn: {
    top: 600*Height,
    fontSize: 200*Width,
    fontWeight: "500",
    fontFamily: FontFamily.gmarketSans,
    color: Color.colorNewturn,
    textAlign: "center",
    position: "absolute",
  },
  introViewParent: {
    backgroundColor: Color.colorWhite,
    flex: 1,
    width: 1080 * Width,
    overflow: "hidden",
    height: 2220*Height,
  },
  introCorpSearch:{
    backgroundColor:'#4B4B4B',
    width : 839*Width,
    height : 178 * Height,
    top : 850*Height,
    borderTopRightRadius : 40,
    borderTopLeftRadius : 40,
    borderBottomLeftRadius : 40,
    borderBottomRightRadius : 40,
    justifyContent:'center',
  },
  introCorpSearchText:{
    color:'#BDBDBD', 
    fontSize:48*Width,
    left : 70 * Width,
    fontFamily: FontFamily.kNUTRUTH
  },
  searchIcon : {
    width : 69 * Width,
    height : 60 * Height,
    position : "absolute",
    right : 65 * Width,
  }
});

export default Initial;
