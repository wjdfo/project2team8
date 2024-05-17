module.exports = {
  presets: ['module:@react-native/babel-preset'],
  plugins : [
    ['module:react-native-dotenv',{
      'modulename': '@env',
      'path': '.env',
      'safe' : true,
      'allowUndefined' : false
    }]
  ]
};
