import {View, TouchableOpacity, Image, Text, StyleSheet} from 'react-native';
import { Height, Width,Color, FontFamily } from '../GlobalStyles';
const ChatHeader = ({isDart,setIsDart}) => {
    const handleHeaderButtonPress  = () =>{
        setIsDart(!isDart);
    }
    return (
        <View style={styles.headerPosition}>
            <View style={[styles.headerChild, styles.headerPosition]} />
            
            {isDart?
            <TouchableOpacity style={[styles.headerText,{width: 375*Width}]}
                              onPress = {handleHeaderButtonPress}>
                <Text style={styles.dartText}>DART</Text>
                <Image
                style={[styles.dropDownIcon,{left: 310*Width}]}
                resizeMode="cover"
                source={require("../assets/DownArrow.png")}
                />
            </TouchableOpacity>            
            :
            <TouchableOpacity style={[styles.headerText,{width: 450*Width}]}
                              onPress = {handleHeaderButtonPress}>
                <Text style={styles.edgarText}>EDGAR</Text>
                <Image
                style={[styles.dropDownIcon,{left: "90%"}]}
                resizeMode="cover"
                source={require("../assets/DownArrow.png")}
                />
            </TouchableOpacity>
            }

        </View>
    );

};

const styles = StyleSheet.create({
    headerPosition: {
      height: 323*Height,
      width: 1080*Width,
      left: 0,
      top: 0,
      position: "absolute",
      elevation : 10,
    },
    headerChild: {
      shadowColor: "rgba(24, 200, 31, 1)",
      shadowOffset: {
        width: 0,
        height: 5*Height,
      },
      shadowRadius: 20*Height,
      elevation: 10,
      shadowOpacity: 1,
      backgroundColor: Color.colorBG,
    },
    headerText: {
        top: 95*Height,
        left: 93*Width,
    },
    dartText: {
      fontSize: 128*Width,
      width: 324*Width,
      fontFamily: FontFamily.kNUTRUTH,
      textAlign: "left",
      color: Color.colorWhite,
      left: 0,
      top: 0,
    },
    edgarText: {
        fontSize: 128*Width,
        width: 500*Width,
        fontFamily: FontFamily.kNUTRUTH,
        textAlign: "left",
        color: Color.colorWhite,
        left: 0,
        top: 0,
    },
  
    dropDownIcon: {
        height: 35*Height,
        width: 100*Width,
        top: 75*Height,
        position: 'absolute',
        tintColor : '#D9D9D9'
    },
            
})

export default ChatHeader;