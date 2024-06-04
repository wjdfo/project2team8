import { View, StyleSheet,Image, 
    TextInput, TouchableOpacity,Keyboard} from "react-native";
import { useEffect } from "react";
import { Color, FontFamily, Width, Height,} from "../../GlobalStyles";
import fetchInput from "../fetch-handling/fetch-input";
import { useLayout } from '@react-native-community/hooks';

const ChatInput = ({inputText, setInputText, setMessages,messages, corpName, isDart, isKeyboardShown,keyboardHeight,
                    setIsPlusOn, setTextInputHeight}) => {
    
    const { onLayout, ...layout } = useLayout();

    useEffect(()=>{

        setTextInputHeight(layout.height);   
    },[layout.height])
                       
    const handleInputText = (text) => {
        setInputText(text);
    };
    
    const handleSubmit = async () => {
        setMessages(items => [...items, {id:items[items.length - 1].id+1,user:1,content:{message:inputText}}]);
        setInputText('');
        Keyboard.dismiss();
        setMessages(items => [...items, {id:items[items.length - 1].id+1,user:0,content:{message:'%LOADING%'}}]);
        const answerText = await fetchInput(inputText=inputText, corpName=corpName, isDart = isDart);
        setMessages(items => [...items.slice(0,-1), {id:items[items.length - 2].id+1,user:0,content:{message:answerText}}]);
        
    };
    return (
        <View style={[styles.chatWindow,
                    {bottom:isKeyboardShown?keyboardHeight+48 :48}
        ]}>
            <TouchableOpacity style={styles.plusButton} onPress={()=>setIsPlusOn(true)}>
            <Image
                style={styles.plusIcon}
                resizeMode="cover"
                source={require("../../assets/PlusCircle.png")}
            />
            </TouchableOpacity>

            <TextInput
                onLayout={onLayout} 
                multiline
                placeholder={`'`+corpName+`'에 대해 물어보세요.`}
                style={styles.inputTextBox}
                value={inputText}
                onChangeText={handleInputText}
            />

            {inputText?
            <TouchableOpacity style={styles.sendButton}
                     onPress={handleSubmit}>
                <Image
                    style={styles.sendIcon}
                    resizeMode="cover"
                    source={require("../../assets/SendButton.png")}
                />
            </TouchableOpacity>: null}

      </View>


    );

};

const styles = StyleSheet.create({
    chatWindow: {
        left: 53*Width,
        position: 'absolute',
        width: 974*Width,
        backgroundColor: '#D9D9D9',
        borderTopLeftRadius : 20,
        borderTopRightRadius : 20,
        borderBottomLeftRadius : 20,
        borderBottomRightRadius : 20,
        maxHeight: 250*Height,
        flexDirection:'column-reverse',
        alignSelf:'flex-start',
    },
    plusButton: {
        height: 90*Height,
        bottom: 15*Height,
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
      width : 650*Width,
      left: 120*Width,
      fontFamily: FontFamily.kNUTRUTH,
      fontSize : 40*Width,
      color: Color.colorLightGray,
      textAlignVertical : "top",
      marginVertical:10*Height,
      paddingBottom:0,
    },
    sendButton:{
        height: 90*Height,
        bottom: 15*Height,
        left: 800*Width,
        width: 150*Width,
        position:'absolute',
        backgroundColor:Color.colorWhite,
        borderTopLeftRadius : 50,
        borderTopRightRadius : 50,
        borderBottomLeftRadius : 50,
        borderBottomRightRadius : 50,
        backgroundColor: Color.colorNewturn,
        
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