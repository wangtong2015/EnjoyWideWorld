// pages/fight/fight.js

var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    list: [],
    text: null,
    length: null
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var that = this
    var attacker = null
    var attacked = null
    var i = 0
    var winner = 1
    attacker = JSON.parse(options.str1)
    attacked = JSON.parse(options.str2)
    console.log(attacker)
    console.log(attacked)
    that.dialog(attacker, attacked).then((res) => {
      that.setData({
        list: res
      })
      that.show(that.list[0]).then((res) => {
        console.log(res)
      })
    })

  },

  dialog: function(attacker, attacked) {
    var that = this
    var list = []
    var i = 0
    var winner = 0
    return new Promise(function(resolve, reject) {
      for (; winner == 0 && i < 100; i++) {
        switch (i % 4) {
          case 0:
            if (attacker.health < 1) {
              list[i] = attacker.name + "生命值归零，游戏结束"
              winner = 2
            } else {
              list[i] = attacker.name + "发起进攻";
            }
            break;
          case 1:
            if (Math.random() < attacked.dodgeRate / 100) {
              list[i] = attacked.name + "闪避成功，" + attacker.name + "的攻击没有命中"
            } else {
              attacked.health -= (attacker.attack - attacked.defend) > 0 ? attacker.attack : 1
              list[i] = attacker.name + "的攻击命中，" + attacked.name + "的生命值下降"
            }
            break;
          case 2:
            if (attacked.health < 1) {
              list[i] = attacked.name + "生命值归零，游戏结束"
              winner = 1
            } else {
              list[i] = attacked.name + "发起进攻";
            }
            break;
          case 3:
            if (Math.random() < attacker.dodgeRate / 100) {
              list[i] = attacker.name + "闪避成功，" + attacked.name + "的攻击没有命中"
            } else {
              attacker.health -= (attacked.attack - attacker.defend) > 0 ? attacked.attack : 1
              list[i] = attacked.name + "的攻击命中，" + attacker.name + "的生命值下降"
            }
            break;
        }
      }
      if (winner != 0) {
        that.setData({
          length: i
        })
        resolve(list)
      } else {}
    })
  },

  show: function(story) {
    var that = this
    return new Promise(function(resolve, reject) {
      var time = setInterval(function() {
        var text = story.substring(0, i);
        i++;
        that.setData({
          text: text
        });
        if (text.length == story.length) {
          //   console.log("定时器结束！");
          clearInterval(time);
          resolve(list)
        } else {}
      }, 200)
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  }
})