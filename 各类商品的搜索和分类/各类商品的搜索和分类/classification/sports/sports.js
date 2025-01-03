// pages/secondhand/classification/sports/sports.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    category1:'二手交易',
    category2:'运动',
    secondhandGoods: [],  // 用来存储商品列表
    productIds: [],       // 存储所有商品的 product_id
    imagesUrl:[],
  },

  onLoad() {
    // 获取分类信息
    const category1 = this.data.category1;
    const category2 = this.data.category2;

    wx.request({
      url: 'https://101972498yahu.vicp.fun/api/selectcategory/', // 后端接口URL
      method: 'POST',  // 修改为POST方法
      data: JSON.stringify({
        category1: category1,
        category2: category2
      }),  // 传递 category1 和 category2
      header: {
        'Content-Type': 'application/json'
      },
      success: (res) => {
        if (res.statusCode === 200) {
          // 获取商品列表
          const products = res.data.products;

          // 遍历商品列表，为每个商品的 images 数组中的图片文件名拼接完整的 URL
          products.forEach(product => {
            // 获取图片文件名
            const imageFileName = product.images[0];  // 获取第一个图片的文件名
            
            // 拼接成完整的 URL
            product.imageUrl = `https://101972498yahu.vicp.fun/media/uploads/${imageFileName}`;

            // 如果你需要所有图片路径，遍历 product.images 数组
            product.images = product.images.map(imageFileName => {
              return `https://101972498yahu.vicp.fun/media/uploads/${imageFileName}`;
            });
          });

          // 更新商品列表
          this.setData({
            secondhandGoods: products,
          });

          // 打印商品详情
          console.log("商品列表:", products);
        } else {
          wx.showToast({
            title: '加载商品失败',
            icon: 'none'
          });
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '请求失败，请稍后重试',
          icon: 'none'
        });
      }
    });
  },
 // 点击商品时跳转到商品详情页
 goodListClickHandle(e) {
  const productId = e.currentTarget.dataset.productId; // 获取点击商品的 product_id

  wx.navigateTo({
     url: `/pages/secondhand/goods/testpage?query=${encodeURIComponent(productId)}`,
  });
},
})