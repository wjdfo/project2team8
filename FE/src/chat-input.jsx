import { View, StyleSheet,Image, 
    TextInput, TouchableOpacity} from "react-native";
import { Color, FontFamily, Width, Height,} from "../GlobalStyles";
import handleInput from "./fetch-input";

const ChatInput = ({inputText, setInputText, messages, setMessages,corpName}) => {
    const handleInputText = (text) => {
        setInputText(text);
    };
    
    const handleSubmit = () => {
        setMessages(items => [...items, {id:items[items.length - 1].id+1,user:1, time:"01:00",content:inputText}])
        setInputText('');
        const answerText = handleInput(inputText={inputText}, corpName={corpName});
        setMessages(items => [...items, {id:items[items.length - 1].id+1,user:0, time:"01:00",content:answerText}])
        
    };

    return (
        <View style={styles.chatWindow}>
            <TouchableOpacity style={styles.plusButton}>
            <Image
                style={styles.plusIcon}
                resizeMode="cover"
                source={require("../assets/PlusCircle.png")}
            />
            </TouchableOpacity>

            <TextInput
                multiline
                style={styles.inputTextBox}
                placeholder={`Write your message .  . .`}
                value={inputText}
                onChangeText={handleInputText}
            />

            {inputText?
            <TouchableOpacity style={styles.sendButton}
                     onPress={handleSubmit}>
                <Image
                    style={styles.sendIcon}
                    resizeMode="cover"
                    source={require("../assets/SendButton.png")}
                />
            </TouchableOpacity>: null}
      </View>



    );

};

const styles = StyleSheet.create({
    chatWindow: {
        top: 1950*Height,
        left: 53*Width,
        position: 'absolute',
        width: 974*Width,
        height: 119*Height,
        backgroundColor: '#D9D9D9',
        borderTopLeftRadius : 50,
        borderTopRightRadius : 50,
        borderBottomLeftRadius : 50,
        borderBottomRightRadius : 50,
    },
    plusButton: {
        height: 90*Height,
        top: 15*Width,
        left: 20*Width,
        width: 90*Width,
        position: 'absolute',
    },
    plusIcon: {
        height: 70*Height,
        top: 10*Width,
        left: 10*Width,
        width: 70*Width,
        right: 0,
        tintColor : Color.colorNewturn,
        position:'absolute',
    },
    inputTextBox: {
      top: 0*Height,
      width : 650*Width,
      left: 120*Width,
      position: "absolute",
      fontFamily: FontFamily.kNUTRUTH,
      color: "#797c7b",

    },
    sendButton:{
        height: 90*Height,
        top: 15*Height,
        left: 800*Width,
        width: 150*Width,
        position:'absolute',
        backgroundColor:Color.colorWhite,
        borderTopLeftRadius : 50,
        borderTopRightRadius : 50,
        borderBottomLeftRadius : 50,
        borderBottomRightRadius : 50,
        backgroundColor: Color.colorNewturn
    },
    sendIcon: {
        width: 80*Width,
        height: 80*Height,
        left: 45 *Width,
        top : 5*Height,
        tintColor : Color.colorWhite,
        position:'absolute',
    },
})

export default ChatInput;