// pages/petinfo/petinfo.js
var app = getApp()
var the_url = 'http://wangtong15.com:20001/pet'

Page({
  data: {
    petInfo: null,
    ce: null, // 战斗力
    location: null,
    mood: null,
    level: null,
    levelLeft: null,
    levelAbs: null, // 宠物已获得的该级的经验
    totalExp: null, // 该级的总经验
  },
  onLoad: function(options) {
    var that = this
    var object = JSON.parse(options.jsonStr);
    that.setData({
      petInfo: object.character // 之后要加上性别和心情
    })
    that.setData({
      ce: ((object.character.characterHP + object.character.characterAD + object.character.characterDF + object.character.characterSP + 100 * object.character.characterMiss) / 5).toFixed()
    })
    that.setData({
      location: app.globalData.userInfo.province
    })
    // that.setData({
    //   mood: object.characterMood < 50 ? '伤心' : object.characterMood > 80? '开心': '一般'
    // })
    that.setData({
      level: object.level,
      levelLeft: object.levelLeft,
      levelAbs: object.levelAbs,
      totalExp: object.level < 7 ? object.levelSet[object.level + 1] - object.levelSet[object.level] : object.levelSet[object.levels] - object.levelSet[object.levels - 1]
    })
  }
})