// pages/secondhand/confirmorder/confirmorder.js
Page({
  data: {
    goods: {}, // 商品信息
    buyer: {}, // 买家信息
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

  getBuyerInfo: function (openid) {
    wx.request({
      url: 'https://101972498yahu.vicp.fun/api/getuserinfo/',  // 后端接口 URL
      method: 'POST',
      data: JSON.stringify({ openid: openid }),  // 发送 openid 到后端
      header: {
        'Content-Type': 'application/json',
      },
      success: (res) => {
        if (res.statusCode === 200) {
          // 返回成功，设置买家信息到 data 中
          const userInfo = res.data.user_info;
          this.setData({
            buyer: userInfo  // 保存买家信息到页面 data 中
          });

          // 打印买家信息到控制台，供调试使用
          console.log("买家信息:", userInfo);
        } else {
          wx.showToast({
            title: res.data.error || '获取买家信息失败',
            icon: 'none',
          });
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '网络错误，请稍后再试',
          icon: 'none',
        });
        console.error('请求失败', err);
      }
    });
  },


  onLoad(options) {
 // 获取传递过来的商品价格
 const productId = options.query;
 this.setData({
   productId: productId,  // 解码商品价格
 });
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
const openid = wx.getStorageSync('openid');  // 假设 openid 存储在全局数据中 
if (openid) {
  // 调用获取买家信息的方法
  this.getBuyerInfo(openid);
} else {
  wx.showToast({
    title: '未检测到登录信息，请登录',
    icon: 'none'
  });
}
},

 // 提交订单
submitOrder: function () {
  const { productId, buyer, seller_openid, productPrice } = this.data;

  // 检查买家信息是否获取成功
  if (!buyer || !buyer.openid) {
    wx.showToast({
      title: '买家信息获取失败',
      icon: 'none',
    });
    return;
  }

  // 检查买家的地址和电话是否为空
  if (buyer.address === 'Not set' || buyer.phone=== 'Not set') {
    wx.showToast({
      title: '地址和电话不能为空',
      icon: 'none',
    });
    return;
  }
  console.log(productId,buyer.openid);
  // 提交订单请求
  wx.request({
    url: 'https://101972498yahu.vicp.fun/api/changeorder/',  // 后端创建订单接口
    method: 'POST',
    data: JSON.stringify({
      product_id: productId,
      openid: buyer.openid,  // 买家的 openid
    }),
    header: {
      'Content-Type': 'application/json',
    },
    success: (res) => {
      if (res.statusCode === 200) {
        // 订单创建成功
        const order = res.data;
        wx.showToast({
          title: '订单创建成功',
          icon: 'success',
        });

        // 延迟 1 秒后执行跳转回到主页
        setTimeout(() => {
          wx.reLaunch({
            url: '/pages/secondhand/secondhand',
          });
        }, 1000);
      } else {
        wx.showToast({
          title: res.data.error || '订单创建失败',
          icon: 'none',
        });
      }
    },
    fail: (err) => {
      wx.showToast({
        title: '网络错误，请稍后再试',
        icon: 'none',
      });
      console.error('请求失败', err);
    }
  });
}


})