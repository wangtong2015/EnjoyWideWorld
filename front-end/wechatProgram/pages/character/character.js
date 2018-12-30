// pages/user/user.js
var app = getApp()
var the_url = 'http://wangtong15.com:20001/pet'
/*var the_url ='http://127.0.0.1:8000/map'*/
Page({

  /**
   * 页面的初始数据
   */
  onReady: function(e) {
    // 使用 wx.createAudioContext 获取 audio 上下文 context
    // this.audioCtx = wx.createAudioContext('myAudio')

  },

  data: {
    character: {
      characterId: "",
      characterName: "Zhangsan",
      characterHP: "1000",
      characterAD: "150",
      characterDF: "80",
      characterSP: "70",
      characterMiss: "50%",
      characterAppearance: "1",
      characterExp: 0,
    },
    characterLevel: "0",
    level: 0, // 宠物的经验
    levelLeft: 0, // 在这级宠物已有的经验占这级总经验的百分比
    levelSet: [0, 20, 60, 140, 300, 620, 1260, 2260], //等级相关
    levels: 7, // 目前levelSet中最大经验值对应的级数
    characterRight: "100",
    characterBottom: "100", //运动相关
    audioSrc: '../../audio/characterAudio.mp3',
    characterSrc: '../../photos/Tom.jpg' //调用显示声音相关
  },

  /*onLoad */
  onLoad: function(options) {
    var that = this
    var i = 1
    wx.showLoading({
        title: '加载中',
      }),
      that.getCharacter()
    that.level(that.data.character['characterExp'])
    console.log(that.data.level)
    console.log(that.data.levelLeft)
    // var left = 100 * (levelSet[i] - characterExp) / levelSet[i];
    // that.setData({
    //   characterLevel: i.toString,
    //   levelLeft: left.toString,
    // }),
    wx.hideLoading();
  },

  /*onReady */
  onReady: function(e) {
    //wx.getFileSystemManager()
  },

  /*角色触摸反响 */
  to_act() {
    console.log('角色触摸反响')
    this.audioCtx.play()
  },

  getCharacter: function() {
    var that = this
    // var characterA = {}
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
        that.changeCharacter(res)
      }
    })
  },
  changeCharacter: function(res) {
    var characterA = {}
    characterA = {
      characterId: res.data["id"],
      characterName: res.data["name"],
      characterHP: parseInt(res.data["health"]),
      characterAD: parseInt(res.data["attack"]),
      characterDF: parseInt(res.data["defend"]),
      characterSP: parseInt(res.data["speed"]),
      characterMiss: parseInt(res.data["dodgeRate"]) / 100.0,
      characterAppearance: parseInt(res.data["appearance"]),
      characterExp: parseInt(res.data["exp"]),
    }
    this.setData({
      character: characterA
    });
  },
  level: function(res) {
    var left = 0
    var leftLevels = 0
    if (res < this.data.levelSet[this.data.levels]) {
      for (var i = 0; i < this.data.levels; i++) {
        if (this.data.levelSet[i] <= res && res < this.data.levelSet[i + 1]) {
          this.setData({
            level: i
          })
          this.setData({
            levelLeft: 100*(res - this.data.levelSet[i]) / (this.data.levelSet[i + 1] - this.data.levelSet[i])
          })
          break
        }
      }
    }
    else{
      left = res - this.data.levelSet[this.data.levels]
      leftLevels = parseInt(left / (this.data.levelSet[this.data.levels] - this.data.levelSet[this.data.levels - 1]))
      left = res - leftLevels * (this.data.levelSet[this.data.levels] - this.data.levelSet[this.data.levels - 1])
      this.setData({
        level: this.data.levels + leftLevels
      })
      this.setData({
        levelLeft: 100*left / (this.data.levelSet[levels] - this.data.levelSet[levels-1])
      })
    }
  }

})