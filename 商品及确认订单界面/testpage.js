Page({
  data: {
    productId: '',
    productName: '', // 存储商品名称
    productPrice: '', // 存储商品价格
    productImage: '', // 存储商品图片主图
    goods_img: [],     // 存储商品图片数组
    goods_info: {},    // 存储商品的所有详细信息
    goods_description: '',
    provide_service: true,
    rental_period: '',
    seller_name: '',
    seller_openid: ''
  },

  // 页面加载时获取商品信息
  onLoad: function (options) {
    const productId = options.query;

    // 更新页面数据
    this.setData({
      productId: productId,
    });

    // 调用后端接口获取商品详情
    wx.request({
      url: 'https://101972498yahu.vicp.fun/api/selectgoods/', // 替换为实际的后端接口 URL
      method: 'POST',
      data: {
        product_id: productId,  // 传递商品 ID
      },
      success: (res) => {
        if (res.statusCode === 200) {
          // 假设返回的数据结构与期望一致
          const productData = res.data;
          const fullImageUrls = productData.images.map(image => `https://101972498yahu.vicp.fun/media/uploads/${image}`);

          // 处理商品数据
          this.setData({
            goods_info: productData,   // 商品详细信息
            productName: productData.name,
            productPrice: productData.price,
            goods_img: fullImageUrls,  // 商品图片数组
            productImage: fullImageUrls[0] || '', // 主图
            goods_description: productData.description,
            provide_service: productData.provide_service,
            seller_name: productData.seller_name,
            seller_openid: productData.seller_openid,
          });

          // 如果 rental_period 不为 0，则存入 data 中
          if (productData.rental_period !== 0) {
            this.setData({
              rental_period: productData.rental_period, // 存储租赁期限
            });
          }
        } else {
          wx.showToast({
            title: '商品信息加载失败',
            icon: 'none',
          });
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '请求失败，请稍后再试',
          icon: 'none',
        });
      }
    });
    //添加到历史浏览记录
    wx.request({
      url: 'https://101972498yahu.vicp.fun/api/addtohistory/',  // 后端接口地址
      method: 'POST',
      data: {
        openid: wx.getStorageSync('openid'),  // 从本地存储获取用户的 openid
        product_id: productId,  // 商品的 product_id，假设你已经定义了该变量
      },
      success: (res) => {
        // 请求成功的回调函数
        if (res.statusCode === 200 && res.data.success) {
          // 处理成功的情况
         console.log("productid:",productId,"已添加到历史记录");
        } else {
          console.log("添加失败");
        }
      },
      fail: (err) => {
        // 请求失败的回调函数
        wx.showToast({
          title: '请求失败，请稍后重试',
          icon: 'none',
          duration: 2000
        });
      }
    });
    
  },

  // 预览商品图片
  previewImage: function (e) {
    var current = e.target.dataset.src;  // 当前点击的图片URL
    var goodsImg = this.data.goods_img || []; // 确保图片字段存在
    var imgList = goodsImg.map(img => img);  // 假设每张图片是完整的URL

    wx.previewImage({
      current: current,  // 当前显示图片的http链接  
      urls: imgList,      // 需要预览的图片http链接列表
    });
  },

  // 点击购买
  buy: function () {
    const openid = wx.getStorageSync('openid');
    const productPrice = this.data.productPrice;
    const sellerOpenid = this.data.seller_openid;

    // 检查是否登录
    if (!openid) {
      wx.showToast({
        title: '未获取到用户信息，请登录后再试',
        icon: 'none',
      });
      return;
    }

    // 判断是否为自己的商品
    if (openid === sellerOpenid) {
      wx.showToast({
        title: '不能购买自己发布的商品',
        icon: 'none',
      });
      return;
    }
    
    const productId=this.data.productId;
    // 跳转到确认订单页面
    wx.navigateTo({
      url: `/pages/secondhand/confirmorder/confirmorder?query=${encodeURIComponent(productId)}` // 跳转到确认订单页面
    });
  },

  collect() {
    const openid = wx.getStorageSync('openid');
    const product_id = this.data.productId;

    // 发送请求到后端添加收藏
    wx.request({
      url: 'https://101972498yahu.vicp.fun/api/addtofavorites/',  // 后端接口URL
      method: 'POST',
      data: {
        openid: openid,
        product_id: product_id
      },
      header: {
        'Content-Type': 'application/json'
      },
      success: (res) => {
        if (res.data.success) {
          this.setData({
            isFavorited: true  // 设置商品为已收藏
          });
          wx.showToast({
            title: '收藏成功',
            icon: 'success'
          });
        } else {
          wx.showToast({
            title: res.data.message || '操作失败',
            icon: 'none'
          });
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '请求失败，请重试',
          icon: 'none'
        });
      }
    });
  },

  // 页面其他生命周期函数
  onReady() {},
  onShow() {},
  onHide() {},
  onUnload() {},
  onPullDownRefresh() {},
  onReachBottom() {}
});
