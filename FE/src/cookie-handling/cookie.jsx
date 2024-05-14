import AsyncStorage from "@react-native-async-storage/async-storage";

export const setItem = async (key, value) => {
    try {
      await AsyncStorage.setItem(key, value);
      
      console.log(`setItem... ${key} : ${value}`);
    } catch (e) {
      throw e;
    }
  };
  
  export const getItem = async (key) => {
    try {
      const res = await AsyncStorage.getItem(key);
      return res || '';
    } catch (e) {
      throw e;
    }
  };
  