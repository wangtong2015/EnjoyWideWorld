// pages/user/user.js

var app = getApp()
var the_url = 'http://wangtong15.com:20001/community'

Page({
  data: {
    list: null,
    list2: [],
  },


  onLoad: function (options) {
    var that = this;
    //加载数据
    wx.request({
      url: the_url + '/nearbyinfo',
      data: {
        user: app.globalData.openid,
        latitude: app.globalData.latitude,
        longitude: app.globalData.longitude
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      method: 'POST',
      success: function (res) {
        that.order(res);
      },
    });
  },
  order: function(e){
    var list2 = [];
    if (e.data.success == 0) { // 不存在这个用户
    }
    else {
      this.setData({ list: e.data });
      
      for (var i = 0; i < e.data.length; i++) {
        list2[i] = {
          avatarUrl: e.data["avatarUrl" + i],
          exp: e.data["exp" + i],
          isLiked: e.data["isLiked" + i] == 0? false:true,
          nickname: e.data["nickname" + i],
          wechatId: e.data["wechatId" + i],  // 就是openid
        }
      };
      this.setData({ list2: list2 })
    }
  },
  // returntape: function(e){
  //   this.setData({ my_modal_hidden: true })
  // },
  // tape: function(e){
  //   this.setData({hidden:true})
  // },
  // tape2: function (e) {
  //   this.setData({ hidden: false })
  // },
  zan: function (e) {
    var _index = e.currentTarget.dataset.index;
    var _list2 = [...this.data.list2]; // list2的引用
    _list2[_index].isLiked = !this.data.list2[_index].isLiked;
    
    this.setData({
      list2: _list2
    })
    wx.request({
      url: the_url + '/like',
      data: {
        user: app.globalData.openid, // 点赞/取消点赞的人的openid
        friend: this.data.list2[_index].wechatId,  // 被点赞/被取消点赞的人的openid
        type: this.data.list2[_index].isLiked? 1:0  // true: 点赞; false: 取消点赞
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      method: 'POST',
      success: function (res) {
      },
    });
  }
})