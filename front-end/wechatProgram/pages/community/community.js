// pages/community/community.js
var the_url = 'http://127.0.0.1:8000/'
Page({

  /**
   * 页面的初始数据
   */
  data: {
    latitude: 39.958119466670300,
    longitude: 116.298038013743000,
    scale: 16,
    show_location: true,
    my_modal_hidden: true,
    markers: [{
      iconPath: "/figs/Location (24x24).png",
      id: 0,
      latitude: 39.95248757392302,
      longitude: 116.28737784118653,
      width: 25,
      height: 35
    },
    {
      iconPath: "/figs/Location (24x24).png",
      id: 1,
      latitude: 39.959724734463265,
      longitude: 116.30231238098145,
      width: 25,
      height: 35
    },
    {
      iconPath: "/figs/Location (24x24).png",
      id: 2,
      latitude: 39.949526696601716,
      longitude: 116.30325651855469,
      width: 25,
      height: 35
    }],
    explore_photo_path: "/photos/1ed73edb52d890c4b589d56c5149c28f.jpg",
    title: "清华大学",
    harvest: "水晶",
    exp: 10,
    description: "清华大学（英语：Tsinghua University，缩写作 THU），简称清华，旧称清华学堂、清华学校、国立清华大学，是一所位于中华人民共和国北京市海淀区清华园的公立大学。始建于1911年，因北京西北郊清华园而得名。"

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    wx.showLoading({
      title: '加载中',
    })
    wx.getLocation({
      type: 'gcj02',
      success: (res) => {
        this.setData({
          longitude: res.longitude,
          latitude: res.latitude
        })
        wx.hideLoading();
      }
    })

    wx.request({
      url: the_url + 'community', // 仅为示例，并非真实的接口地址
      data: {
        latitude: this.data.latitude,
        longitude: this.data.longitude
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      method: "POST",
      success(res) {
        console.log(res.data)
      }
    })  
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})