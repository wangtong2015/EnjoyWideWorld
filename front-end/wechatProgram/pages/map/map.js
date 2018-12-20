// pages/map/map.js
var the_url= 'http://wangtong15.com:20000/map'
/*var the_url ='http://127.0.0.1:8000/map'*/



Page({
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
      index:null,               //服务器上的编号
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
      index: null,
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
      index: null,
      latitude: 39.949526696601716,
      longitude: 116.30325651855469,
      width: 25,
      height: 90,
      description: "id=2",
      item_linked: "item2",
      picaddr: "/photos/f756c2ec0f62d341fe128038bccde5e0.jpg",
    }],
    explore_photo_path: "/photos/1ed73edb52d890c4b589d56c5149c28f.jpg",
    title:"清华大学",
    item_linked:"水晶",
    exp:10,
    description:"清华大学（英语：Tsinghua University，缩写作 THU），简称清华，旧称清华学堂、清华学校、国立清华大学，是一所位于中华人民共和国北京市海淀区清华园的公立大学。始建于1911年，因北京西北郊清华园而得名。"
  },

  /*从服务器获取地点数据*/
  getpositons:function () {
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
        console.log(res)
        var length=res.data.length
        for(var i=0; i<length;  i++)
        {
          markers[i] = {
            iconPath: "/figs/location.png",
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
        that.setData({markers:markers})
      }
    })

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
          longitude: res.longitude,
          latitude: res.latitude
        })
        wx.hideLoading();
      }
    })
    /*从服务器加载positions */
    //this.getpositons();
    
  },


  
  
  /*onReady */
  onReady: function (e) {
    this.mapCtx=wx.createMapContext("my_map")
    wx.getFileSystemManager()
    //this.get_marker_data()  
  },

  /*地图中心移到marker点 */
  move_to_marker: function (marker_id){
    this.setData({
      longitude: this.data.markers[marker_id].longitude,
      latitude: this.data.markers[marker_id].latitude,
    })
  },

  /*打开信息页 */
  show_markerinfo_page:function(marker_id){
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

  /*点击marker点显示该点信息 */
  markertap(e) {
    var that=this
    var marker_index=e.markerId
    //console.log(e)
    //console.log(marker_index)
    this.move_to_marker(marker_index)
    //console.log(this.data.markers[marker_index])
    
    this.setData({ 
      description: this.data.markers[marker_index]['description'],
      item_linked: this.data.markers[marker_index]['item_linked']
     })
    setTimeout(function () {
      that.show_markerinfo_page(marker_index)
    }, 500)
  },

  /*重置页面以当前位置为中心 */
  to_reset() {
    console.log('重置定位')
    this.setData({scale: 16})
    this.mapCtx.moveToLocation()
  },

  /*打卡 */
  to_check() {
    var that =this
    console.log("打卡")
    //找到最近marker点，判断距离小于10米则
    /*this.mapCtx.getCenterLocation({
      type: 'gcj02',
      success: (res) => {
        let longitude = res.longitude;
        let latitude = res.latitude;
      }
    })*/
    //this.getpositons();
    
    
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

  /*从探索页返回(目前操作为点击图片，待改进) */
  return_tap(){
    this.setData({ my_modal_hidden: true})
  },

  /*点击地图tab，功能重置当前位置为页面中心 */
  onTabItemTap(item){
    this.setData({ scale: 16 })
    this.mapCtx.moveToLocation()
  },

  /*自动规划步行路线（需要改用高德地图API） */
  to_go(){
    console.log("改用高德API规划路线")
  }
})