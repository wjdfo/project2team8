import { View, StyleSheet, Text, TouchableOpacity, Image} from "react-native";
import { Width,Color, Height,FontFamily } from '../GlobalStyles';
import { setItem, getItem } from './cookie-handling/cookie';
import uuid from 'react-native-uuid';

const Initial = ({navigation}) => {
  const setCookie = async (user) => {
    try {
      await setItem('@uid', user);
      console.log('cookie complete');
    } catch (e) {
      console.log(e);
    }
  };
  
  const getCookie = async (key) => {
    const result = await getItem(key);
    return result;
  };

  const handleInitialEntry = async () => {
    try {
      var cookie = await getCookie('@uid');

      if(!cookie){
        cookie = uuid.v4();
        await setCookie(cookie);

      }
      console.log('cookie : ' , cookie);
      navigation.navigate('initial-searchScreen');

    } catch(e) {
      console.error('cookie error : ', e);
    }
  };

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
      <Text style= {styles.warningText}>
          ※ 투자의 책임은 투자자 본인에게 있습니다. ※
      </Text>
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
    alignItems :"center"

  },
  introCorpSearch:{
    backgroundColor:Color.colorDarkenGray,
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
  },
  warningText : {
    fontFamily : FontFamily.gmarketSans,
    fontSize : 50 * Width,
    position : 'absolute',
    bottom : 100*Height,
    color : '#FA4C4C',
    fontWeight : 'bold',
  }
});

export default Initial;
