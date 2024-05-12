import { View, Text, StyleSheet} from "react-native";
import { Color, Border, FontFamily, Width, Height,} from "../GlobalStyles";


export default function IndiviMessage({message, isUser, time}){
	
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
        <Text style ={styles.message}>{message}</Text>
      </View>
    );
}
  
const styles = StyleSheet.create({
	messageContainer: {
		backgroundColor: Color.colorNewturn,
		maxWidth: "80%",
		alignSelf: "flex-start",
		flexDirection: "row",
		borderRadius: 15,
		paddingHorizontal: 10,
		marginHorizontal: 10,
		paddingTop: 5,
		paddingBottom: 10,
        marginBottom : 10*Width
	},
	message: {
		color: 'white',
		alignSelf: "flex-start",
		fontSize: 60*Width,
        fontFamily: FontFamily.kNUTRUTH,
	},

})

