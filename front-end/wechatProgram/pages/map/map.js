// pages/map/map.js

var app = getApp()
var the_url= 'http://wangtong15.com:20000/map'
/*var the_url ='http://127.0.0.1:8000/map'*/


Page({
  /*data */
  data: {
    latitude: 39.958119466670300,
    longitude: 116.298038013743000,
    scale: 16,
    show_location: true,
    my_modal_hidden: true,
    //markers:[],
    markers: [{
      iconPath: "/figs/location.png",
      id: 0,                    //本地编号
      index:10,               //服务器上的编号
      latitude: 39.95248757392302,
      longitude: 116.28737784118653,
      width: 25,
      height: 90,
      description: "id=0",
      item_linked: "item0",
      picaddr: "/photos/1ed73edb52d890c4b589d56c5149c28f.jpg",
    },
    {
      iconPath: "/figs/location.png",
      id: 1,
      index: 11,
      latitude: 39.959724734463265,
      longitude: 116.30231238098145,
      width: 25,
      height: 90,
      description: "id=1",
      item_linked: "item1",
      picaddr: "/photos/b137801beac4b407567927509bce4130.jpg",
    },
    {
      iconPath: "/figs/location.png",
      id: 2,
      index: 12,
      latitude: 39.95933,
      longitude: 116.29845,
      width: 25,
      height: 90,
      description: "id=2",
      item_linked: "item2",
      picaddr: "/photos/f756c2ec0f62d341fe128038bccde5e0.jpg",
    }],
    explore_photo_path: "/photos/1ed73edb52d890c4b589d56c5149c28f.jpg",
    title:"清华大学",
    item_linked:"",
    exp:10,
    description:"",
    userInfo: null
  },



  /*onLoad */
  onLoad: function (options) {
    var that = this;
    wx.showLoading({
      title: '加载中',
    })
    wx.getLocation({
      type: 'gcj02',
      success: (res) => {
        this.setData({
          latitude: res.latitude,
          longitude: res.longitude,
        })
        app.globalData.latitude = res.latitude
        app.globalData.longitude = res.longitude
        wx.hideLoading();
      }
    })
    this.getpositons();    //从服务器加载positions
    // 我觉得下面这种方式更好一点
    // wx.getUserInfo({
    //   success(res){
    //     console.log(res)
    //   },
    //   fail(err){
    //     console.log(err, '获取用户信息失败')
    //     wx,wx.showModal({
    //       title: '警告',
    //       content: '尚未进行授权，请点击确定跳转到用户界面进行授权',
    //       success: function(res) {
    //         if(res.confirm){
    //           console.log('用户点击确定')
    //           wx.switchTab({
    //             url: '../user/user',
    //           })
    //         }
    //       },
    //     })
    //   }
    // })
  },
  
  /*onReady */
  onReady: function (e) {
    this.mapCtx=wx.createMapContext("my_map")
    wx.getFileSystemManager()
    this.check_auth_status()
  },



  /*点击marker点显示该点信息 */
  markertap(e) {
    var that=this
    var marker_index=e.markerId
    this.move_to_marker(marker_index)
    this.setData({ 
      description: this.data.markers[marker_index]['description'],
      item_linked: this.data.markers[marker_index]['item_linked']
     })
    setTimeout(function () {
      that.show_markerinfo_page(marker_index)
    }, 500)
  },

  /*重定位 */
  to_reset() {
    console.log('重置定位')
    this.setData({scale: 16})
    this.mapCtx.moveToLocation()
  },

  /*打卡 */
  to_check() {
    var that = this
    console.log("打卡")
    var length = this.data.markers.length
    var lat, lng
    var checkinpoint = null
    if (app.globalData.userInfo != null) {
      //找到最近marker点，判断距离小于10米则打卡
      for (var i = 0; i < length; i++) {
        lat = this.data.markers[i]['latitude']
        lng = this.data.markers[i]['longitude']
        if (this.getdistance(app.globalData.latitude, app.globalData.longitude, lat, lng) < 0.01) checkinpoint = i
      }
      if (checkinpoint != null) {
        wx.request({
          url: the_url + '/checkin', // 仅为示例，并非真实的接口地址
          data: {
            wechatId: null,
            positionId: this.data.markers[checkinpoint]['index']
          },
          header: {
            'content-type': 'application/x-www-form-urlencoded' // 默认值
          },
          method: "POST",
          success(res) { }
        })
      }
      else{
        wx.showModal({
          title: '',
          content: '10米内没有打卡点',
          showCancel: false,
          confirmColor: '#e67d22ce'
        })
      }
    }
    else{
      this.check_auth_status()
    }
  },

  /*探索 */
  to_explore() {
    console.log('探索')
    var that =this
    var marker_index=Math.floor(Math.random() * this.data.markers.length)
    this.move_to_marker(marker_index)
    this.setData({ 
      description: this.data.markers[marker_index]['description'],
      item_linked: this.data.markers[marker_index]['item_linked']
      })
    setTimeout(function () {
      that.show_markerinfo_page(marker_index)
    }, 500)
  },

  /*检查授权状态 */
  check_auth_status: function(){
    var that = this
    wx.getSetting({
      success(res) {
        if (!res.authSetting['scope.userInfo']) {
          wx.showToast({
            title: '请授权',
            icon: 'loading',
            duration: 1000,
            mask: false,
            success: (res) => {
              setTimeout(function () {
                wx.switchTab({
                  url: '/pages/user/user',
                })
              }, 500)
            }
          })
        }
        else {
          wx.getUserInfo({
            success: function (res) {
              that.setData({
                userInfo: res.userInfo
              })
              app.globalData.userInfo= res.userInfo
            }
          })
        }
      }
    })
  },

  /*从服务器获取地点数据*/
  getpositons: function () {
    var that = this
    var markers = []
    wx.request({
      url: the_url + '/getpositions', // 仅为示例，并非真实的接口地址
      data: {
        latitude: this.data.latitude,
        longitude: this.data.longitude
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded' // 默认值
      },
      method: "POST",
      success(res) {
        var length = res.data.length
        for (var i = 0; i < length; i++) {
          markers[i] = {
            iconPath: "/figs/location.png",
            name: res.data["name" + i],
            id: i,    //本地编号
            index: res.data["id" + i],    //服务器上的编号
            latitude: res.data["lat" + i],
            longitude: res.data["lon" + i],
            description: res.data["description" + i],
            item_linked: res.data["itemName" + i],
            picaddr: res.data["picaddr" + i],
            width: 25,
            height: 90
          }
        }
        that.setData({ markers: markers })
      }
    })

  },

  /*经纬度求距离 */
  getdistance: function (lat1, lng1, lat2, lng2) {
    var radLat1 = lat1 * Math.PI / 180.0;
    var radLat2 = lat2 * Math.PI / 180.0;
    var a = radLat1 - radLat2;
    var b = lng1 * Math.PI / 180.0 - lng2 * Math.PI / 180.0;
    var s = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(a / 2), 2) + Math.cos(radLat1) * Math.cos(radLat2) * Math.pow(Math.sin(b / 2), 2)));
    s = s * 6378.137;// EARTH_RADIUS;
    s = Math.round(s * 10000) / 10000;
    return s;
  },

  /*地图中心移到marker点 */
  move_to_marker: function (marker_id) {
    this.setData({
      longitude: this.data.markers[marker_id].longitude,
      latitude: this.data.markers[marker_id].latitude,
    })
  },

  /*打开信息页 */
  show_markerinfo_page: function (marker_id) {
    let file
    wx.getFileSystemManager().readdir({
      dirPath: "/photos",
      success: (res) => {
        file = res.files[marker_id]
        this.setData({
          explore_photo_path: '/photos/' + file,
          my_modal_hidden: false
        })
      }
    })
  },

  /*退出信息页 */
  return_tap(){
    this.setData({ my_modal_hidden: true})
  },

  /*点击地图tab */
  onTabItemTap(item){
    console.log(app.globalData.userInfo)
  },

  /*自动规划步行路线（需要改用高德地图API） */
  route_planning(){
    console.log("改用高德API规划路线")
  }
})