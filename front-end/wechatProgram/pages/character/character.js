// pages/character/character.js
var app = getApp();
var the_url = 'http://wangtong15.com:20001/pet';
var countTimeout = null;
var imageSrc = '../../photos/';
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
      characterName: "Tom",
      characterHP: 0,
      characterAD: 0,
      characterDF: 0,
      characterSP: 0,
      characterMiss: 0, // 小数形式
      characterAppearance: 0,
      characterExp: 0,
    },
    level: 0, // 宠物的等级
    levelLeft: 0, // 在这级宠物已有的经验占这级总经验的百分比
    levelAbs: 0, // 在这级宠物已有的绝对经验
    levelSet: [0, 20, 60, 140, 300, 620, 1260, 2260], //不同等级对应的总经验值（不是该级的经验）
    levels: 7, // 目前levelSet中最大经验值对应的级数
    characterRight: "100",
    characterBottom: "100", //运动相关
    // audioSrc: '../../audio/characterAudio.mp3',
    characterSrc: ''
  },

  /*onLoad */
  onLoad: function(options) {
    var that = this
    var i = 1
    wx.showLoading({
        title: '加载中',
      }),
      that.getCharacter(),
      // var left = 100 * (levelSet[i] - characterExp) / levelSet[i];
      // that.setData({
      //   level: i.toString,
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
      url: the_url + '/petinfo',
      data: {
        wechatId: app.globalData.openid
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      method: "POST",
      success(res) {
        if (res.data.success == 1) {
          that.changeCharacter(res)
        } else { // 没有宠物
          wx.showToast({
            title: '创立初始角色……',
            icon: 'loading',
            duration: 3000
          })
          that.resetTimeout(function() {
            var appearance = Math.floor(Math.random() * 10)
            that.setPetInfo(appearance)
            }, 3000)
        }
      }
    })
  },
  changeCharacter: function(res) {
    var that = this
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
    that.setData({
      character: characterA
    })
    that.setData({
      characterSrc: imageSrc + res.data["name"] + '.png'
    })
    that.level(characterA['characterExp'])
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
            levelAbs: res - this.data.levelSet[i]
          })
          this.setData({
            levelLeft: 100 * (res - this.data.levelSet[i]) / (this.data.levelSet[i + 1] - this.data.levelSet[i])
          })
          break
        }
      }
    } else { // 超出levels的情况下，以后每级的经验值不变
      left = res - this.data.levelSet[this.data.levels]
      leftLevels = parseInt(left / (this.data.levelSet[this.data.levels] - this.data.levelSet[this.data.levels - 1]))
      left = res - leftLevels * (this.data.levelSet[this.data.levels] - this.data.levelSet[this.data.levels - 1])
      this.setData({
        level: this.data.levels + leftLevels
      })
      this.setData({
        levelAbs: left
      })
      this.setData({
        levelLeft: 100 * left / (this.data.levelSet[this.data.levels] - this.data.levelSet[this.data.levels - 1])
      })
    }
  },
  tapPet: function() {
    var str = JSON.stringify(this.data);
    wx.navigateTo({
      url: '/pages/petinfo/petinfo?jsonStr=' + str,
      success: function(res) {
        // success
      },
      fail: function(res) {
        // fail
      },
      complete: function(res) {
        // complete
      }
    });
  },
  resetTimeout: function(timeFunc, time) {
    if (countTimeout != null) {
      clearTimeout(countTimeout);
    }
    countTimeout = setTimeout(timeFunc, time);
  },
  // 通过appearance到图像
  setPetInfo: function(res) {
    var that = this
    var name = null
    var image = null
    var characterHP = null
    var characterAD = null
    var characterDF = null
    var characterSP = null
    var characterMiss = null; // 小数形式
    var characterAppearance = null;
    that.setData({
      'character.characterAppearance': res
    })
    switch (res) {
      case 0:
        image = 'cat.png';
        name = 'cat';
        characterHP = 12;
        characterAD = 16;
        characterDF = 7;
        characterSP = 19;
        characterMiss = 0.08; // 小数形式
        characterAppearance = 0;
        break;
      case 1:
        image = 'cattle.png';
        name = 'cattle';
        characterHP = 20;
        characterAD = 13;
        characterDF = 18;
        characterSP = 9;
        characterMiss = 0.02; // 小数形式
        characterAppearance = 1;
        break;
      case 2:
        image = 'dog.png';
        name = 'dog';
        characterHP = 14;
        characterAD = 15;
        characterDF = 11;
        characterSP = 15;
        characterMiss = 0.05; // 小数形式
        characterAppearance = 2;
        break;
      case 3:
        image = 'elephant.png';
        name = 'elephant';
        characterHP = 20;
        characterAD = 10;
        characterDF = 20;
        characterSP = 4;
        characterMiss = 0.01; // 小数形式
        characterAppearance = 3;
      case 4:
        image = 'fox.png';
        name = 'fox';
        characterHP = 10;
        characterAD = 18;
        characterDF = 5;
        characterSP = 19;
        characterMiss = 0.1; // 小数形式
        characterAppearance = 4;
        break;
      case 5:
        image = 'giraffe.png';
        name = 'giraffe';
        characterHP = 14;
        characterAD = 13;
        characterDF = 9;
        characterSP = 12;
        characterMiss = 0.06; // 小数形式
        characterAppearance = 5;
        break;
      case 6:
        image = 'lion.png';
        name = 'lion';
        characterHP = 15;
        characterAD = 19;
        characterDF = 12;
        characterSP = 18;
        characterMiss = 0.09; // 小数形式
        characterAppearance = 6;
        break;
      case 7:
        image = 'pig.png';
        name = 'pig';
        characterHP = 19;
        characterAD = 9;
        characterDF = 16;
        characterSP = 10;
        characterMiss = 0.06; // 小数形式
        characterAppearance = 7;
        break;
      case 8:
        image = 'rabbit.png';
        name = 'rabbit';
        characterHP = 7;
        characterAD = 11;
        characterDF = 5;
        characterSP = 20;
        characterMiss = 0.12; // 小数形式
        characterAppearance = 8;
        break;
      case 9:
        image = 'sheep.png';
        name = 'sheep';
        characterHP = 17;
        characterAD = 15;
        characterDF = 11;
        characterSP = 7;
        characterMiss = 0.03; // 小数形式
        characterAppearance = 9;
        break;
    }
    that.setData({
      characterSrc: imageSrc + image,
      'character.characterName': name,
      'character.characterHP': characterHP,
      'character.characterAD': characterAD,
      'character.characterDF': characterDF,
      'character.characterSP': characterSP,
      'character.characterMiss': characterMiss,
      'character.characterAppearance': characterAppearance,
      'character.characterExp': 0,
    })
    wx.request({
      url: the_url + '/add',
      data: {
        wechatId: app.globalData.openid,
        character: {
          characterName: name,
          characterHP: characterHP,
          characterAD: characterAD,
          characterDF: characterDF,
          characterSP: characterSP,
          characterMiss: characterMiss, // 小数形式
          characterAppearance: characterAppearance,
          characterExp: 0,
        }
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      method: "POST",
      success(res) {
        console.log(res)
      }
    })
  }
})