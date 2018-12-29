// pages/user/user.js
const app = getApp()
/*var the_url = 'http://wangtong15.com:20000/map'*/
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
    userCharacter: {},
    userCharacterName:"Zhangsan",
    userCharacterLevel:"999",
    userLevelLeft:"20",
    audioSrc:'/audio/characterAudio.mp3',
    characterHP :"1000",
    characterAD:"150",
    characterDF :"80",
    characterSP:"70",
    characterMiss:"50%",
    characterRight:"100",
    characterBottom:"100",



    characterSrc:'/photos/Tom.jpg'
  },

  /*onLoad */
  onLoad: function (options) {
    var that = this;
    wx.showLoading({
      title: '加载中',
    }),
    this.getCharacter();
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

  getCharacter:function(){
    var that = this
    var markers = []
    wx.request({
      url: the_url + '/getname', // 仅为示例，并非真实的接口地址
      data: {
        latitude: this.data.latitude,
        longitude: this.data.longitude
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      method: "POST",
      success(res) {
        var length = res.data.length
        for (var i = 0; i < length; i++) {
          markers[i] = {
            iconPath: "/figs/location.png",
            name: res.data["name" + i],
            id: i,    //本地编号
            index: res.data["id" + i],    //服务器上的编号
            latitude: res.data["lat" + i],
            longitude: res.data["lon" + i],
            description: res.data["description" + i],
            item_linked: res.data["itemName" + i],
            picaddr: res.data["picaddr" + i],
            width: 25,
            height: 90
          }
        }
        that.setData({ markers: markers })
      }
    })

  }

})