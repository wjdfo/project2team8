import {Dimensions} from 'react-native';

export const basicDimensions = { // 디자이너가 작업하고 있는 XD파일 스크린의 세로,가로
    height: 2220,
    width: 1080,
  };
  

export const Height = ( // 높이 변환 작업
  Dimensions.get('screen').height * ( 1/ basicDimensions.height)
);

export const Width = ( // 가로 변환 작업
  Dimensions.get('screen').width * ( 1/ basicDimensions.width)
);

/* fonts */
export const FontFamily = {
  gmarketSans: "Gmarket Sans",
  kNUTRUTH: "KNU TRUTH",
};
/* Colors */
export const Color = {
  colorWhite: "#fff",
  colorNewturn: "#18c81f",
  colorBG: "#292f3f",
};
/* border radiuses */
export const Border = {
  br_21xl: 40,
};
