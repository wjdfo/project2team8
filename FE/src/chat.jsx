import React, { useState,  useRef, useEffect } from "react";
import { View, StyleSheet, Keyboard,  
  FlatList,KeyboardAvoidingView,
  TouchableWithoutFeedback,Platform} from "react-native";
import { Color, Width, Height,} from "../GlobalStyles";
import Message from "./message";
import ChatHeader from "./chat-header";
import ChatInput from "./chat-input";



const FrameScreen = ({navigation,route}) => {
  const [messages,setMessages] = useState([
    {
      id : 0,
      user : 0,
      time : '11:00',
      content : '안녕하세요?',
    },
  ]);

  const [inputText, setInputText] = useState('');
  const [isKeyboardShown, setIsKeyboardShown] = useState(false);
  const [keyboardHeight, setKeyboardHeight] = useState(0);
  const [isScrollable, setIsScrollable] = useState(false);
  const selectFlatList = useRef();

  useEffect(
    () =>
      navigation.addListener('beforeRemove', (e) => {
        e.preventDefault();
      }),
    []
  );



  const dissmissKeyboard = () => {
    Keyboard.dismiss();
  };

  const renderItem = ({item})=> (
    <Message message={item.content} isUser={item.user} time={item.time}/>
  );

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
          

          <KeyboardAvoidingView style={{flex:1}}
                                keyboardVerticalOffset={44*Height}
                                behavior = {Platform.os === 'ios' ? 'padding' : 'position'}
                                >

            {/*Message List*/}
            <FlatList 
                      style={[styles.chatBody,
                        {height:isKeyboardShown? (1550*Height)-(keyboardHeight)+(65*Height): 1550*Height},
                        {top:isKeyboardShown? (395*Height)+(keyboardHeight)-(65*Height) : 395*Height},
                      ]
                      } 
                      data={isScrollable?[...messages].reverse():[...messages]} 
                      renderItem={renderItem}
                      keyExtractor={item => item.id} 
                      ref = {selectFlatList}
                      onContentSizeChange={()=> isScrollable? selectFlatList.current.scrollToIndex({index:0}) 
                                                            : selectFlatList.current.scrollToEnd()} 
                      onScrollBeginDrag={() => setIsScrollable(true)}
                      
                      inverted = {isScrollable?true:false}

                      /> 
            

          {/*Text Input*/}
            <ChatInput inputText={inputText} setInputText={setInputText} 
                      messages={messages} setMessages={setMessages}
                      corpName={route.params.searchedName}
                      />
          </KeyboardAvoidingView>
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
  chatBody: {
    width: '100%',
    position: "absoulte",
  },
  chatViewParent: {
    backgroundColor: Color.colorWhite,
    overflow: "hidden",
    height: 2220*Height,
    width: "100%",
  },
});

export default FrameScreen;
