import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import {View} from 'react-native';
import chat from './chat-screen/chat';
import initial from './initial';
import searchWindow from './search-screen/search-window';
const Stack = createNativeStackNavigator();

const App = () => {
    return(
        <NavigationContainer>
            <Stack.Navigator initialRouteName = 'initialScreen' screenOptions={{ headerShown: false }}>
                <Stack.Screen name = 'initialScreen' component={initial}/>
                <Stack.Screen name = 'chatScreen' component={chat}/>
                <Stack.Screen name = 'initial-searchScreen' component={searchWindow}/>
                <Stack.Screen name = 'searchScreen' component={searchWindow}/>
            </Stack.Navigator>
        </NavigationContainer>
    );

}

export default App;