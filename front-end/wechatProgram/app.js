//app.js
var the_url = 'http://wangtong15.com:20001'
App({
  onLaunch: function () {
    // 展示本地存储能力
    var that = this
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              that.globalData.userInfo = res.userInfo
              wx.request({
                url: the_url + '/user/add',
                data: {
                  wechatId: that.globalData.openid,
                  nickname: that.globalData.userInfo.nickName,
                  avatarurl: that.globalData.userInfo.avatarUrl,
                  province: that.globalData.userInfo.province,
                  city: that.globalData.userInfo.city
                },
                header: {
                  'content-type': 'application/x-www-form-urlencoded'
                },
                success: function (res) {
                  //从数据库获取用户信息
                  // that.queryUsreInfo();
                  console.log("更新小程序登录用户信息成功！");
                  
                }
              });
              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
        else {
          wx.reLaunch({
            url: '/pages/authorize/authorize',
          })
        }
      }
    })
    // 获取用户信息
    wx.login({
      success(res) {
        if (res.code) {
          // 发起网络请求
          wx.request({
            url: the_url + '/user/openid',
            data: {
              code: res.code
            },
            header: {
              'content-type': 'application/x-www-form-urlencoded'
            },
            method: "POST",
            success(res) {
              that.globalData.openid = res.data.openid
            }
          })
        }
      }
    })
  },



  globalData: {
    userInfo: null,
    latitude: null,
    longitude: null,
    openid: 0,
    totalLikes: 0,
  }
})