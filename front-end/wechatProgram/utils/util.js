const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : '0' + n
}

module.exports = {
  formatTime: formatTime
}

function json2Form(json) {
  var str = [];
  for (var p in json) {
    str.push(encodeURIComponent(p) + "=" + encodeURIComponent(json[p]));
  }
  return str.join("&");
}

function getsettings() {
  wx.getSetting({
    success: res => {
      if (res.authSetting['scope.userInfo']) {
        // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
        wx.getUserInfo({
          success: res => {
            // 可以将 res 发送给后台解码出 unionId
            
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
}
/*
function check_auth_status() {
  wx.getUserInfo({
    success(res) {
      console.log(res)
    },
    fail(err) {
      console.log(err, '获取用户信息失败')
      wx, wx.showModal({
        title: '警告',
        content: '尚未进行授权，请点击确定跳转到用户界面进行授权',
        success: function (res) {
          if (res.confirm) {
            console.log('用户点击确定')
            wx.switchTab({
              url: '../user/user',
            })
          }
        },
      })
    }
  })
}
*/

function login(){
  wx.login({
    success(res) {
      if (res.code) {
        console.log(res.code)
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
            console.log(res)
            app.globalData.openid = res.data.openid
          }
        })
      }
    }
  })
}
module.exports = {
  getsettings: getsettings,
  login: login,
}