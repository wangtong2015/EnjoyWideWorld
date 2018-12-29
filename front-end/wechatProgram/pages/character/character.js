// pages/user/user.js
const app = getApp()
var the_url = 'http://wangtong15.com:20001/pet'
/*var the_url ='http://127.0.0.1:8000/map'*/
Page({

  /**
   * 页面的初始数据
   */
  onReady: function (e) {
    // 使用 wx.createAudioContext 获取 audio 上下文 context
   // this.audioCtx = wx.createAudioContext('myAudio')

  },

  data: {
    character:{
    characterId: "",
    characterName:"Zhangsan",
    characterHP :"1000",
    characterAD:"150",
    characterDF :"80",
    characterSP:"70",
    characterMiss:"50%",
    characterAppearance:"1",
    characterExp:"100",
    },


    characterLevel: "0",
    levelLeft:"0",
    levelSet: ["20", "40", "80", "160", "320", "480", "640", "1000", "4000"],//等级相关
    characterRight: "100",
    characterBottom: "100",//运动相关
    audioSrc: '/audio/characterAudio.mp3',
    characterSrc:'/photos/Tom.jpg'//调用显示声音相关
  },

  /*onLoad */
  onLoad: function (options) {
    var that = this;
    wx.showLoading({
      title: '加载中',
    }),
    this.getCharacter();
    var i=1;
    while(character.characterExp>levelSet[i-1]){
      i++;
    }
    var left=100*(levelSet[i]-characterExp)/levelSet[i];
    this.setData({
      characterLevel:i.toString,
      levelLeft:left.toString,
    }),

    wx.hideLoading();
  },

  /*onReady */
  onReady: function (e) {
    //wx.getFileSystemManager()
  },

  /*角色触摸反响 */
  to_act() {
    console.log('角色触摸反响')
    this.audioCtx.play()


  },

  getCharacter:function(){
    var that = this
    var characterA
    wx.request({
      url: the_url + '/petinfo', // 仅为示例，并非真实的接口地址
      data: {
        wechatId: app.globalData.openid
      },
      
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      method: "POST",
      success(res) {

        characterA:{
            characterId: res.data["id" ]; 
            characterName: res.data["name" ];
            characterAppearance:res.data["appearance"];
            characterExp: res.data["exp"];
            characterHP: res.data["health"];
            characterAD: res.data["attack"];
            characterDF: res.data["defend"];
            characterSP: res.data["speed"];
            characterMiss: res.data["dodegRate"];
        }
          
        
        that.setData({ character: characterA })
      }
    })

  }

})