import React, { useState,  useRef,  } from "react";
import { StyleSheet,FlatList,TouchableWithoutFeedback} from "react-native";
import { Color, Width, Height,} from "../../GlobalStyles";
import Message from "./message";

const ChatBody =({isKeyboardShown, keyboardHeight, messages,textInputHeight, isScrollable,setIsScrollable}) =>{
    const selectFlatList = useRef();

    const renderItem = ({item})=> (
        <Message content={item.content} isUser={item.user}/>
    );
    
    return (
      <TouchableWithoutFeedback>

        <FlatList 
        style={[styles.chatBody,
          {height:isKeyboardShown? (1590*Height)-keyboardHeight-textInputHeight : 1500*Height },
        ]} 
        data={isScrollable?[...messages].reverse():[...messages]} 
        renderItem={renderItem}
        keyExtractor={item => item.id} 
        ref = {selectFlatList}
        onContentSizeChange={(w,h)=> {
                        if ( h > 1560 * Height) setIsScrollable(true);
                        isScrollable? selectFlatList.current.scrollToIndex({index:0}) 
                                              : selectFlatList.current.scrollToEnd();}} 
        // onScrollBeginDrag={() => setIsScrollable(true)}
        inverted = {isScrollable?true:false}
        nestedScrollEnabled

        />
        </TouchableWithoutFeedback>

    );
};


const styles = StyleSheet.create({
    chatBody: {
      width: '100%',
      position: "absoulte",
      flexGrow: 0,
      top:350*Height,

    },
  });
export default ChatBody;