import {View,Text,StyleSheet, TouchableOpacity, Image, Modal, TouchableWithoutFeedback,Alert} from 'react-native';
import { Color, Width, Height, FontFamily} from "../../GlobalStyles";
import { fetchList,fetchURL, fetchSummary } from '../fetch-handling/fetch-menus';
import { useState } from 'react';
import { Dropdown } from 'react-native-element-dropdown';

const MenuSelector =({navigation,setIsPlusOn,messages,setMessages,corpName,isDart}) =>{
    const [isCompareVisible,setIsCompareVisible] = useState(false);
    const [isSummaryVisible,setIsSummaryVisible] = useState(false);
    const [isURLVisible,setIsURLVisible] = useState(false);

    const [URLfrom, setURLfrom] = useState(null);
    const [URLto, setURLto] = useState(null);

    const [summaryValue, setSummaryValue] = useState(null);

    const handleList = async () => {
        const result = await fetchList(corpName,isDart);
        var resultArry =[];
        result.map((i)=>{
            resultArry = [...resultArry,'- '+i+'\n'];
        })
        setMessages(items => [...items, {id:items[items.length - 1].id+1,user:0,content:{message:resultArry}}]);
        setIsPlusOn(false);
    };

    
    const handleURL = async (fromDate, toDate) => {
        if ( fromDate > toDate ) {
            Alert.alert(
                '날짜 오류',
                '날짜를 지켜주세요 !',
                [
                    { text : '닫기',
                    onPress: () => {},
                    style:'cancel'}
                ],
                {cancelable:true,
                onDismiss: () => {}}
            )
        }
        else{
            const result = await fetchURL(corpName=corpName,fromDate=fromDate,toDate=toDate, isDart=isDart);

            Object.keys(result).map((key)=>{
                setMessages(items => [...items, {id:items[items.length - 1].id+1,user:0,content:{message:key + '\n' +result[key]}}]);
            })
            setIsPlusOn(false);
    
        }
    };

    const handleSummary = async (reportYear) => {
        const result = await fetchSummary(corpName=corpName, reportYear = reportYear, isDart = isDart);
        setMessages(items => [...items, {id:items[items.length - 1].id+1,user:0,content:{message:result}}])
        setIsPlusOn(false);
    };

    const handleURLModal = () => {
        setURLfrom(null);
        setURLto(null);
        setIsURLVisible(true);
    };

    const handleSummaryModal = () => {
        setSummaryValue(null);
        setIsSummaryVisible(true);
    };

    const handleCompareModal = () => {
        setIsCompareVisible(true);
    };

    const year_data = [
        { label : '2024', value : '2024'},
        { label : '2023', value : '2023'},
        { label : '2022', value : '2022'},
        { label : '2021', value : '2021'},
        { label : '2020', value : '2020'},
        { label : '2019', value : '2019'},

    ];

    return (
    <View style = { styles.menuContainer}>
        <TouchableOpacity 
            style={[styles.menuTypeOne, {top:449*Height, left : 100*Width}]}
            onPress={handleList}>
            <Image
                  style={styles.icon}
                  resizeMode="contain"
                  source={require('../../assets/ListIcon.png')}
              />
            <Text style = {styles.menuText}>
                기업 목록
            </Text>
        </TouchableOpacity>

        <TouchableOpacity 
            style={[styles.menuTypeTwo, {top:449*Height, left : 600*Width}]}
            onPress={handleURLModal}>
            <Image
                  style={styles.icon}
                  resizeMode="contain"
                  source={require('../../assets/GetUrlIcon.png')}
              />
            <Text style = {styles.menuText}>
                원본 보고서 확인
            </Text>
        </TouchableOpacity>

        <TouchableOpacity 
            style={[styles.menuTypeTwo, {top:1000*Height, left : 100*Width}]}
            onPress={handleSummaryModal}>
            <Image
                  style={styles.icon}
                  resizeMode="contain"
                  source={require('../../assets/SummarizeIcon.png')}
              />
            <Text style = {styles.menuText}>
                보고서 요약
            </Text>
        </TouchableOpacity>

        <TouchableOpacity 
            style={[styles.menuTypeOne, {top:1000*Height, left : 600*Width}]}
            onPress={handleCompareModal}>
            <Image
                  style={styles.icon}
                  resizeMode="contain"
                  source={require('../../assets/ComparisonIcon.png')}
              />
            <Text style = {styles.menuText}>
                보고서 비교
            </Text>
        </TouchableOpacity>
        
        <Modal
            visible={isURLVisible}
            transparent={true}
        >
            <TouchableOpacity
                style={styles.modalView}
                onPressIn ={()=>setIsURLVisible(false)}>
                <TouchableWithoutFeedback  onPress={()=>{}}>
                    <View style = {[styles.modalMain, {backgroundColor: Color.colorNewturnSec,}]}>
                        <Text style={{color:'#FFFFFF', fontSize:55*Width, top:50*Height,fontFamily:FontFamily.kNUTRUTH}}>
                        출력 범위를 정해주세요.
                        </Text>
                        
                        <View style = {{top:150*Height,flexDirection:'row',alignItems:'center',justifyContent:'center'}}>


                            <Dropdown
                                style = {[styles.dropDownBox,{width:200*Width,top:0}]}
                                data={year_data}
                                placeholder={'년도'}
                                placeholderStyle= {{color : Color.colorWhite, left:30*Width, fontFamily:FontFamily.kNUTRUTH}}
                                containerStyle = {styles.dropDownContainer}
                                itemTextStyle = {{color:Color.colorWhite}}
                                selectedTextStyle = {{color : Color.colorWhite, left:30*Width, fontFamily:FontFamily.kNUTRUTH}}
                                labelField='label'
                                valueField='value'
                                activeColor='#686b6a'
                                maxHeight={600*Height}
                                value={URLfrom}
                                onChange={item => {
                                    setURLfrom(item.value);
                                }}
                            />

                            <Text style={{color:Color.colorWhite, paddingHorizontal:50*Width,fontSize:50*Width,fontWeight:'bold'}}>
                                ~
                            </Text>

                            <Dropdown
                                style = {[styles.dropDownBox,{width:200*Width,top:0}]}
                                data={year_data}
                                placeholder={'년도'}
                                placeholderStyle= {{color : Color.colorWhite, left:30*Width, fontFamily:FontFamily.kNUTRUTH}}
                                containerStyle = {styles.dropDownContainer}
                                itemTextStyle = {{color:Color.colorWhite}}
                                selectedTextStyle = {{color : Color.colorWhite, left:30*Width, fontFamily:FontFamily.kNUTRUTH}}
                                labelField='label'
                                valueField='value'
                                activeColor='#686b6a'
                                maxHeight={600*Height}
                                value={URLto}
                                onChange={item => {
                                    setURLto(item.value);
                                }}
                            />

                        </View>
                        {URLto&&URLfrom?
                        <TouchableOpacity 
                            style={[styles.summarySubmit,{width:300*Width}]}
                            onPress={()=>{handleURL(URLfrom,URLto)}}
                        >
                            <Text style={{color:Color.colorWhite, fontFamily:FontFamily.kNUTRUTH}}>
                                원본보고서 받기
                            </Text>
                        </TouchableOpacity>
                        :<View/>}
        
                    </View>
                </TouchableWithoutFeedback>
            </TouchableOpacity>

        </Modal>


        <Modal
            visible={isSummaryVisible}
            transparent={true}>
            <TouchableOpacity
                style={styles.modalView}
                onPressIn ={()=>setIsSummaryVisible(false)}>
                <TouchableWithoutFeedback onPress={()=>{}}>
                    <View style = {[styles.modalMain, {backgroundColor: Color.colorNewturnSec}]}>
                        <Text style={{color:'#FFFFFF', fontSize:55*Width, top:50*Height,fontFamily:FontFamily.kNUTRUTH}}>
                        몇 년도 보고서를 요악할까요 ?
                        </Text>
                        <Dropdown
                            style = {styles.dropDownBox}
                            data={year_data}
                            placeholder={'년도 선택'}
                            placeholderStyle= {{color : Color.colorWhite, left:30*Width, fontFamily:FontFamily.kNUTRUTH}}
                            containerStyle = {styles.dropDownContainer}
                            itemTextStyle = {{color:Color.colorWhite}}
                            selectedTextStyle = {{color : Color.colorWhite, left:30*Width, fontFamily:FontFamily.kNUTRUTH}}
                            labelField='label'
                            valueField='value'
                            activeColor='#686b6a'
                            maxHeight={600*Height}
                            value={summaryValue}
                            onChange={item => {
                                setSummaryValue(item.value);
                            }}
                            />
                        {summaryValue?
                        <TouchableOpacity 
                            style={styles.summarySubmit}
                            onPress={()=>{handleSummary(summaryValue)}}
                        >
                            <Text style={{color:Color.colorWhite, fontFamily:FontFamily.kNUTRUTH}}>
                                요약해주기
                            </Text>
                        </TouchableOpacity>
                        :<View/>}
                            
                    </View>
                
                </TouchableWithoutFeedback>           
            </TouchableOpacity>

        </Modal>


        <Modal
            visible={isCompareVisible}
            transparent ={true}>

            <TouchableOpacity 
                style={styles.modalView}
                onPressIn ={()=>setIsCompareVisible(false)}>
                <TouchableWithoutFeedback onPress={()=>{}}>
                <View style = {[styles.modalMain,{backgroundColor:Color.colorNewturn,}]}>
                    <Text style={{color:'#FFFFFF', fontSize:55*Width, top:50*Height,fontFamily:FontFamily.kNUTRUTH}}>
                     어떤 기업과 비교하시겠어요 ?
                    </Text>

                    <TouchableOpacity style={styles.corpSearchBox}
                        onPress = {()=>{
                            setIsPlusOn(false);
                            setIsCompareVisible(false);
                            navigation.navigate('searchScreen',{searchedName:corpName, sNisDart : isDart});
                        }}

                    >
                        <Text style={{color:Color.colorWhite, fontFamily:FontFamily.kNUTRUTH}}>
                            검색하기
                        </Text>
                        <Image
                        style={styles.searchIcon}
                        resizeMode="contain"
                        source={require("../../assets/Search.png")}
                        />

                    </TouchableOpacity>
                </View>
                </TouchableWithoutFeedback>
            </TouchableOpacity>
        </Modal>



    </View>);

};

const styles = StyleSheet.create({
    menuContainer : {
        height : 1580 * Height,
        width : '100%',
        backgroundColor:Color.colorBG
    },
    menuTypeOne :{
        justifyContent:'center',
        alignItems: 'center',
        position : 'absolute',
        width : 350 * Width,
        height : 350 * Height,
        borderBottomRightRadius : 14,
        borderBottomLeftRadius : 14,
        borderTopLeftRadius : 14,
        borderTopRightRadius : 14,
        backgroundColor : Color.colorNewturn,
    },
    menuTypeTwo : {
        justifyContent:'center',
        alignItems: 'center',
        position : 'absolute',
        width : 350 * Width,
        height : 350 * Height,
        borderBottomRightRadius : 14,
        borderBottomLeftRadius : 14,
        borderTopLeftRadius : 14,
        borderTopRightRadius : 14,
        backgroundColor: Color.colorNewturnSec,
    },
    icon : {
        width : 220 * Width,
        height : 220 * Height,
    },
    menuText : {
        paddingTop:20*Height,
        fontFamily : FontFamily.kNUTRUTH,
        color : Color.colorWhite,
        fontSize : 48*Width,
    },
    // 
    modalView : {
        width : '100%',
        height : '100%',
        backgroundColor:'rgba(0,0,0,0.8)',
        
    },
    modalMain : {
        left : 190 * Width,
        top : 400 * Height,
        width : 700*Width,
        height : 500 *Height,
        borderBottomLeftRadius : 20,
        borderBottomRightRadius : 20,
        borderTopLeftRadius : 20,
        borderTopRightRadius : 20,
        alignItems : 'center',
    },
    //
    corpSearchBox:{
        backgroundColor:Color.colorDarkenGray,
        width : 600 * Width,
        height : 100*Height,
        top : 150 * Height,
        borderTopRightRadius : 20,
        borderTopLeftRadius : 20,
        borderBottomLeftRadius : 20,
        borderBottomRightRadius : 20,
        alignItems:'center',
        justifyContent:'center',
        flexDirection:'row',
    },

    searchIcon: {
        width : 55 * Width,
        height : 55 * Height,
        marginLeft : 15*Width,
    },
    // 
    dropDownBox :{
        top : 100 * Height,
        width : 300*Width, 
        borderColor : Color.colorWhite,  
        backgroundColor : Color.colorDarkenGray,
        borderTopRightRadius : 10,
        borderTopLeftRadius : 10,
        borderBottomLeftRadius : 10,
        borderBottomRightRadius : 10,
    },
    dropDownContainer :{ 
        borderTopRightRadius : 10,
        borderTopLeftRadius : 10,
        borderBottomLeftRadius : 10,
        borderBottomRightRadius : 10,
        backgroundColor : Color.colorLightGray,
        borderColor:Color.colorLightGray
    },
    summarySubmit : {width : 200*Width, height:100*Height,
        bottom:20*Height,
        position:'absolute',
        backgroundColor:Color.colorLightGray,
        justifyContent:'center',
        alignItems:'center',
        borderBottomRightRadius : 14,
        borderBottomLeftRadius : 14,
        borderTopLeftRadius : 14,
        borderTopRightRadius : 14,
    },
})


export default MenuSelector;