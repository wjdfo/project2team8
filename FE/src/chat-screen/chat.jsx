import React, { useState,  useEffect } from "react";
import { View, StyleSheet, Keyboard,  
  TouchableWithoutFeedback, Text, Image, TouchableOpacity} from "react-native";
import { Color, Width, Height,FontFamily} from "../../GlobalStyles";
import ChatHeader from "./chat-header";
import ChatInput from "./chat-input";
import ChatBody from "./chat-body";
import MenuSelector from "./menu-selector";
import { fetchCompare } from "../fetch-handling/fetch-menus";

const FrameScreen = ({navigation,route}) => {
  const [messages,setMessages] = useState([
    {
      id : 0,
      user : 0,
      content : {
        message : '안녕하세요? 선택하신 기업에 대해서 무엇이든 물어보세요.',
      },
    },
    {
      id : 1,
      user : 0,
      content : {
        message : '아래에 + 버튼을 터치해 다른 기능도 살펴보세요 !',
      }
    }

  ]);

  const [inputText, setInputText] = useState('');
  const [isKeyboardShown, setIsKeyboardShown] = useState(false);
  const [keyboardHeight, setKeyboardHeight] = useState(route.params.keyboardHeight);
  const [isPlusOn, setIsPlusOn] = useState(false);
  const [textInputHeight, setTextInputHeight] = useState(0);
  const [isScrollable, setIsScrollable] = useState(false);

  useEffect(
    () =>
      navigation.addListener('beforeRemove', (e) => {
        e.preventDefault();
      }),
      
    []
  );

  useEffect(() => {
    if(route.params.targetCorpName != undefined){
      handleComparePrint(corpName=route.params.searchedName,isDart=route.params.sNisDart, targetCorpName=route.params.targetCorpName,targetIsDart=route.params.tNisDart);
    }
  },[route.params.targetCorpName]);
  
  const handleComparePrint = async (corpName,isDart,targetCorpName,targetIsDart) => {
    const result = await fetchCompare(corpName=corpName, isDart=isDart, targetCorpName=targetCorpName,targetIsDart=targetIsDart);
    setMessages(items => [...items, {id:items[items.length - 1].id+1,user:0,content:{message:result}}]);
  }
  const dissmissKeyboard = () => {
    Keyboard.dismiss();
  };


  const handleShowedKeyboard = Keyboard.addListener('keyboardDidShow', (e) =>{
    setKeyboardHeight(e.endCoordinates.height);
    setIsKeyboardShown(true);  
  });
  const handleHideKeyboard = Keyboard.addListener('keyboardDidHide', () =>{
    setIsKeyboardShown(false);  
  });

  return (
      //
      <TouchableWithoutFeedback
      style={{ height: "100%" }}
      onPress={() => dissmissKeyboard()}
      > 
        <View style={styles.chatViewContainer}>
          

          {/*Body : MenuSelector or ChatBody*/}
          {isPlusOn?
          <MenuSelector 
                        navigation = {navigation}
                        setIsPlusOn={setIsPlusOn}
                        messages={messages}
                        setMessages={setMessages}
                        corpName={route.params.searchedName}
                        isDart={route.params.sNisDart}
          />
          
          : <ChatBody
                    isScrollable={isScrollable}
                    setIsScrollable={setIsScrollable}
                    isKeyboardShown={isKeyboardShown} 
                    keyboardHeight={keyboardHeight}
                    textInputHeight ={textInputHeight}
                    messages ={messages}
          />}

          {/*Bottom : Text View or ChatInput*/}

          {isPlusOn?
            <View style={styles.bottomWindow}>
              <TouchableOpacity style={styles.minusButton} onPress={()=>setIsPlusOn(false)}>
              <Image
                  style={styles.minusIcon}
                  resizeMode="cover"
                  source={require("../../assets/MinusCircle.png")}
              />
              </TouchableOpacity>

              <Text style={styles.bottomWindowText}>원하시는 서비스를 선택해보세요.</Text>
            </View>

            :
            // Text Input
            <ChatInput 
                    inputText={inputText} setInputText={setInputText} 
                    setMessages={setMessages}
                    corpName={route.params.searchedName}
                    isDart={route.params.sNisDart}
                    isKeyboardShown={isKeyboardShown}
                    keyboardHeight={keyboardHeight}
                    setIsPlusOn={setIsPlusOn}
                    isPlusOn={isPlusOn}
                    setTextInputHeight={setTextInputHeight}

            />
          }
          {/*Header*/}
          <ChatHeader navigation={navigation} searchedName={route.params.searchedName}/>
        </View>
      </TouchableWithoutFeedback>
  );  
};

const styles = StyleSheet.create({
  chatViewContainer: {
    width: 1080*Width,
    left: 0,
    top: 0,
    position: "absolute",
    height: 2100*Height,
    backgroundColor : Color.colorBG
  },
  chatViewParent: {
    backgroundColor: Color.colorWhite,
    overflow: "hidden",
    height: 2220*Height,
    width: "100%",
  },

  bottomWindow: {
    left: 53*Width,
    bottom:50*Height,
    height : 120*Height,
    position: 'absolute',
    width: 974*Width,
    backgroundColor: Color.colorLightGray,
    borderTopLeftRadius : 20,
    borderTopRightRadius : 20,
    borderBottomLeftRadius : 20,
    borderBottomRightRadius : 20,
    justifyContent:'center',
},
  bottomWindowText : {
    width : 650*Width,
    left: 125*Width,
    fontFamily: FontFamily.kNUTRUTH,
    color: '#D9D9D9',
    fontSize : 48*Width,

  },
  minusButton: {
    height: 90*Height,
    bottom: 15*Height,
    left: 20*Width,
    width: 90*Width,
    position: 'absolute',
  },
  minusIcon: {
    height: 70*Height,
    top: 10*Width,
    left: 10*Width,
    width: 70*Width,
    right: 0,
    tintColor : Color.colorNewturn,
    position:'absolute',
  },  

});

export default FrameScreen;
