# 실행 방법

`민국 : 우선 Android 기준으로 개발했어요. IOS는 코드 대부분을 그대로 두고 특수 처리만 해주면 될듯한데 머리아파서 일단 놔뒀음`

## # 1: 설치할 것들

- react native

```bash
npm install -g react-native-cli
```

- Android Studio

[안드로이드 스튜디오 설치](https://developer.android.com/studio?hl=ko#get-android-studio) <br>
저는 android-studio-2023.3.1.18-windows.exe 했습니다.

- JDK 17

환경변수 설정도 하세용 [JDK 17 설치](https://jdk.java.net/java-se-ri/17
) <br><br>
## # 2: 프로젝트 만들기

- react native
```bash
# MyNative 라는 이름의 Project 생성
npx react-native init MyNative
```
생성되는 폴더 내에 지금 폴더(FE) 내용물 복붙하면 됨
<br>
- Android Studio

[참고...](https://yun5o.tistory.com/entry/React-Native-%EB%A6%AC%EC%95%A1%ED%8A%B8-%EB%84%A4%EC%9D%B4%ED%8B%B0%EB%B8%8C-%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD-%EC%84%A4%EC%A0%955-%EC%95%88%EB%93%9C%EB%A1%9C%EC%9D%B4%EB%93%9C-%EC%8A%A4%ED%8A%9C%EB%94%94%EC%98%A4-%EC%84%A4%EC%B9%98)



## # 3: 실행
- Android Studio

우선 Emulator 알아서 실행 ( Virtual Device )

Android Studio에서 직접 실행해도 되고(-> 다 켜질 때까지 기다려야 함) react native 실행할 때 자동으로 켜지게 할 수도
```
개발환경 : Pixel 3a API 34
```

- react native
```bash
npm run adroid
```

