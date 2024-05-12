import * as React from "react";
import { View, StyleSheet, Text, useWindowDimensions  } from "react-native";
import {width, height, Color} from '../GlobalStyles'; //width,height 받아오기

function Frame(){
  return (
    <View style={styles.introViewParent}>
      <View style={styles.introViewPosition}>
        <Text style={styles.knuturn}>knuturn</Text>
      </View>
    </View>
  );s
};



const styles = StyleSheet.create({
  introViewPosition: {
    width: 1080 * Width,
    left: 0,
    top: 0,
    position: "absolute",
    height: 2220*Height,
    backgroundColor: Color.colorBG,
    justfyContent:"center",
    alignItems :"center"
  },
  knuturn: {
    top: 682*Height,
    fontSize: 128*Width,
    fontWeight: "500",
    fontFamily: FontFamily.gmarketSans,
    color: Color.colorNewturn,
    textAlign: "center",
    position: "absolute",
  },
  introViewParent: {
    backgroundColor: Color.colorWhite,
    flex: 1,
    width: 1080 * Width,
    overflow: "hidden",
    height: 2220*Height,
  },
});

export default Frame;
