// pages/user/user.js
const app = getApp()
/*var the_url = 'http://wangtong15.com:20000/map'*/
/*var the_url ='http://127.0.0.1:8000/map'*/
Page({

  /**
   * 页面的初始数据
   */
  data: {
    userCharacter: {},
    userCharacterName:"Zhangsan",
    userCharacterLevel:"999",
    audioSrc:"audio/characterAudio.mp3",
  },

  /*onLoad */
  onLoad: function (options) {
    var that = this;
    wx.showLoading({
      title: '加载中',
    }),
    this.setData({
      userCharacterName:"Lisi",
      userCharacterLevel:"88",
      audioSrc: "audio/characterAudio.mp3",
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



})