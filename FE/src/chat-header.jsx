import {View, TouchableOpacity, Image, Text, StyleSheet} from 'react-native';
import { Height, Width,Color, FontFamily } from '../GlobalStyles';
const ChatHeader = ({navigation,searchedName}) => {
    return (
        <View style={styles.headerPosition}>
            <View style={[styles.headerChild, styles.headerPosition]} />
            
            <TouchableOpacity style={styles.corpSearchBox}
                              onPress={()=>navigation.navigate('searchScreen')}>
                <Text style={styles.corpName}>{searchedName}</Text>
                <Image
                style={styles.searchIcon}
                resizeMode="contain"
                source={require("../assets/Search.png")}
                />

            </TouchableOpacity>            

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
    corpSearchBox:{
        backgroundColor:'#4B4B4B',
        maxWidth: "80%",
        top : 73 * Height,
        left : 53* Width,
        alignSelf: "flex-start",
        flexDirection: "row",
        borderTopRightRadius : 90,
        borderTopLeftRadius : 90,
        borderBottomLeftRadius : 90,
        borderBottomRightRadius : 90,
        
    },
    corpName: {
      fontSize: 96*Width,
      fontFamily: FontFamily.kNUTRUTH,
      color: Color.colorWhite,
      paddingLeft: 30*Width,
      marginLeft: 30*Width,
      paddingTop: 25*Height,
      paddingBottom : 25*Height,
    },
  
    searchIcon: {
        width : 55 * Width,
        height : 55 * Height,
        top : 55 * Height,
        paddingRight: 40*Width,
        marginRight : 40*Width,
        marginLeft : 15*Width,
    },
            
})

export default ChatHeader;