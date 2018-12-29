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