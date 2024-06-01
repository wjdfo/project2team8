import { View, Text, StyleSheet,ActivityIndicator} from "react-native";
import { Color, Border, FontFamily, Width, Height} from "../../GlobalStyles";
import Hyperlink from 'react-native-hyperlink';
import { Linking } from 'react-native';


export default function IndiviMessage({content, isUser}){
	
    const isUserM = (type) => {
		if (isUser && type === "messageContainer") {
			return {
				alignSelf: "flex-end",
				backgroundColor: "#494949",
				borderTopRightRadius: 0,
			};
		} else if (isUser && type === "message") {
			return {
				color: "#000",
			};
		} else if (isUser && type === "time") {
			return {
				color: "darkgray",
			};
		} else {
			return {
				borderTopLeftRadius: 0,
			};
		}
	};
    

    return (
      <View style={[styles.messageContainer, isUserM("messageContainer")]}>
		{content.message == '%LOADING%'?
		<ActivityIndicator size='large' color='#000ff' />
		:
		<Hyperlink
			linkStyle={{fintSize: 8, color: '#505050'}}
			onPress={(url) => Linking.openURL(url)}
		>
        	<Text style ={styles.message}>{content.message}</Text>
		</Hyperlink>
		}
      </View>
    );
};
  
const styles = StyleSheet.create({
	messageContainer: {
		backgroundColor: Color.colorNewturn,
		maxWidth: "80%",
		alignSelf: "flex-start",
		flexDirection: "row",
		borderRadius: 15,
		paddingHorizontal: 30*Width,
		marginHorizontal: 30*Width,
		paddingTop: 25*Height,
		paddingBottom: 25*Height,
        marginBottom : 30*Height,
	},
	message: {
		color: 'white',
		alignSelf: "flex-start",
		fontSize: 60*Width,
        fontFamily: FontFamily.kNUTRUTH,
	},

})

