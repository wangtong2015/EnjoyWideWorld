// pages/user/user.js

var app = getApp()
var base_url = 'http://wangtong15.com:20001'
var the_url = 'http://wangtong15.com:20001/community'

Page({
  data: {
    list: null,
    list2: [], // 展示的列表

  },


  onLoad: function(options) {
    var that = this;
    //加载数据
    wx.showLoading({
        title: '加载中',
      }),
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
        success: function(res) {
          that.order(res);
        },
      }),
      wx.hideLoading();
  },
  order: function(e) {
    var list2 = [];
    if (e.data.success == 0) { // 不存在这个用户
    } else {
      this.setData({
        list: e.data
      });

      for (var i = 0; i < e.data.length; i++) {
        list2[i] = {
          avatarUrl: e.data["avatarUrl" + i],
          exp: e.data["exp" + i],
          isLiked: e.data["isLiked" + i] == 0 ? false : true,
          isFighted: e.data["isFighted" + i] == 0 ? false : true, //
          nickname: e.data["nickname" + i],
          wechatId: e.data["wechatId" + i], // 就是openid
        }
      };
      this.setData({
        list2: list2
      })
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
  zan: function(e) {
    var that = this
    var _index = e.currentTarget.dataset.index;
    var _list2 = [...that.data.list2]; // list2的引用
    _list2[_index].isLiked = !that.data.list2[_index].isLiked;

    that.setData({
      list2: _list2
    })
    wx.request({
      url: the_url + '/like',
      data: {
        user: app.globalData.openid, // 点赞/取消点赞的人的openid
        friend: that.data.list2[_index].wechatId, // 被点赞/被取消点赞的人的openid
        type: that.data.list2[_index].isLiked ? 1 : 0 // true: 点赞; false: 取消点赞
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      method: 'POST',
      success: function(res) {},
    });
  },
  fight: function(e) {
    var that = this
    var _index = e.currentTarget.dataset.index;
    var _list2 = [...this.data.list2]; // list2的引用
    var attacker = null;
    var attacked = null;
    if (!_list2[_index].isFighted && (app.globalData.openid != that.data.list2[_index].wechatId)) {
      _list2[_index].isFighted = true; // 此时已经不能再战了
      that.setData({
        list2: _list2
      })
      that.getPetInfo(app.globalData.openid).then((res1) => {
        attacker = res1
        that.getPetInfo(that.data.list2[_index].wechatId).then((res2) => {
          attacked = res2
          if (Math.random() < 0.5) {
            wx.showToast({
              title: '挑战成功',
              duration: 2000,
              icon: 'none',
              success: function(){
                console.log()
                wx.request({
                  url: the_url + '/afterbattle',
                  data: {
                    attacker: res1.userId,
                    defender: res2.userId,
                    petId: res1.id,
                    addExp: res1.exp > res2.exp ? 50 : 100
                  },
                  success: (res) => { },
                  fail: () => { },
                  complete: () => {
                  }
                })
              }
            })
            
          }else{
            wx.showToast({
              title: '挑战失败',
              duration: 2000,
              icon: 'none',
              success: function () {
                wx.request({
                  url: the_url + '/afterbattle',
                  data: {
                    attacker: res1.userId,
                    defender: res2.userId,
                    petId: res1.id,
                    addExp: 25
                  },
                  success: (res) => { },
                  fail: () => { },
                  complete: () => {
                  }
                })
              }
            })
          };
          // var str1 = JSON.stringify(attacker)
          // var str2 = JSON.stringify(attacked)
          // wx.navigateTo({
          //   url: '/pages/fight/fight?str1=' + str1 + '&str2=' + str2,
          //   success: function (res) {
          //     // success
          //   },
          //   fail: function (res) {
          //     // fail
          //   },
          //   complete: function (res) {
          //     // complete
          //   }
          // });
        }).catch((res2) => {
          console.log(res2)
        })
      }).catch((res1) => {
        console.log(res1)
      })
    }
    if (app.globalData.openid == that.data.list2[_index].wechatId){
      wx.showToast({
        title: '不能挑战自己',
        duration: 2000,
        icon: 'none'
      })
    }
    if (_list2[_index].isFighted){
      wx.showToast({
        title: '已挑战过此人',
        duration: 2000,
        icon: 'none'
      })
    }
  },
  getPetInfo: function(e) {
    var that = this
    var userAndPet = null
    return new Promise(function(resolve, reject) {
      wx.request({
        url: base_url + '/pet/petinfo',
        data: {
          wechatId: e
        },
        header: {
          'content-type': 'application/x-www-form-urlencoded' // 默认值
        },
        method: "POST",
        success(res) {
          if (res.data.success == 1) {
            userAndPet = res.data
            userAndPet['userId'] = e
            resolve(userAndPet)
          } else { // 没有宠物
            wx.showToast({
              title: '请创立初始角色',
            })
            wx.switchTab({
              url: '/pages/character/character',
            })
          }
        },
      })
    })

  },
})