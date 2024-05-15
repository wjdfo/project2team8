import {View,Text,StyleSheet, TouchableOpacity, Image} from 'react-native';
import { Color, Width, Height, FontFamily} from "../GlobalStyles";
import { fetchList,fetchURL } from './fetch-menus';
const MenuSelector =({setIsPlusOn,messages,setMessages,corpName}) =>{
    const handleList =() => {
        const result = fetchList(corpName);
        setMessages(items => [...items, {id:items[items.length - 1].id+1,user:0,content:{message:result}}])
        setIsPlusOn(false);
    };

    const handleURL = () => {
        const result = fetchURL(corpName);
        Object.keys(result).map((key)=>{
            setMessages(items => [...items, {id:items[items.length - 1].id+1,user:0,content:{message:key + '\n' +result[key]}}])
        })
        setIsPlusOn(false);
    }

    return (
    <View style = { stlyes.menuContainer}>
        <TouchableOpacity 
            style={[stlyes.menuTypeOne, {top:449*Height, left : 100*Width}]}
            onPress={handleList}>
            <Image
                  style={stlyes.icon}
                  resizeMode="contain"
                  source={require('../assets/ListIcon.png')}
              />
            <Text style = {stlyes.menuText}>
                기업 목록
            </Text>
        </TouchableOpacity>

        <TouchableOpacity 
            style={[stlyes.menuTypeTwo, {top:449*Height, left : 600*Width}]}
            onPress={handleURL}>
            <Image
                  style={stlyes.icon}
                  resizeMode="contain"
                  source={require('../assets/GetUrlIcon.png')}
              />
            <Text style = {stlyes.menuText}>
                원본 보고서 확인
            </Text>
        </TouchableOpacity>

        <TouchableOpacity 
            style={[stlyes.menuTypeTwo, {top:1000*Height, left : 100*Width}]}
            onPress={()=>setIsPlusOn(false)}>
            <Image
                  style={stlyes.icon}
                  resizeMode="contain"
                  source={require('../assets/SummarizeIcon.png')}
              />
            <Text style = {stlyes.menuText}>
                보고서 요약
            </Text>
        </TouchableOpacity>

        <TouchableOpacity 
            style={[stlyes.menuTypeOne, {top:1000*Height, left : 600*Width}]}
            onPress={()=>setIsPlusOn(false)}>
            <Image
                  style={stlyes.icon}
                  resizeMode="contain"
                  source={require('../assets/ComparisonIcon.png')}
              />
            <Text style = {stlyes.menuText}>
                보고서 비교
            </Text>
        </TouchableOpacity>




    </View>);

};

const stlyes = StyleSheet.create({
    menuContainer : {
        height : 1580 * Height,
        width : '100%',
        backgroundColor:Color.colorBG
    },
    menuTypeOne :{
        justifyContent:'center',
        alignItems: 'center',
        position : 'absolute',
        width : 350 * Width,
        height : 350 * Height,
        borderBottomRightRadius : 14,
        borderBottomLeftRadius : 14,
        borderTopLeftRadius : 14,
        borderTopRightRadius : 14,
        backgroundColor : Color.colorNewturn,
    },
    menuTypeTwo : {
        justifyContent:'center',
        alignItems: 'center',
        position : 'absolute',
        width : 350 * Width,
        height : 350 * Height,
        borderBottomRightRadius : 14,
        borderBottomLeftRadius : 14,
        borderTopLeftRadius : 14,
        borderTopRightRadius : 14,
        backgroundColor: '#377D64',
    },
    icon : {
        width : 220 * Width,
        height : 220 * Height,
    },
    menuText : {
        paddingTop:20*Height,
        fontFamily : FontFamily.kNUTRUTH,
        color : Color.colorWhite,
        fontSize : 48*Width,
    }

})


export default MenuSelector;