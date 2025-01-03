// pages/auction/search/searchresult/searchresult.js
Page({
  data: {
    results: [],  // 搜索结果
    query: '',    // 搜索关键字
    imagesUrl: [], // 存储图片路径
  },

  onLoad(options) {
    // 获取传递的搜索关键字
    const query = decodeURIComponent(options.query); // 解码传递的 URL 参数
    this.setData({
      query,  // 将搜索关键字保存在页面的 data 中
    });

    // 根据关键字执行搜索操作
    this.searchProducts(query);
  },

  // 执行搜索操作，获取搜索结果
  searchProducts(query) {
    if (!query) {
      wx.showToast({
        title: '请输入搜索关键词',
        icon: 'none',
      });
      return;
    }

    // 请求后端接口获取搜索结果
    wx.request({
      url: 'https://101972498yahu.vicp.fun/api/auctionsearch/',  // 后端接口URL
      method: 'POST',
      data: { keyword: query },  // 传递查询的关键字
      success: (res) => {
        if (res.statusCode === 200) {
          // 获取返回的商品列表
          const products = res.data.products || [];

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
            results: products,  // 存储搜索结果
          });

          // 打印搜索结果
          console.log("搜索结果:", products);
        } else {
          wx.showToast({
            title: '没有找到相关商品',
            icon: 'none',
          });
          this.setData({
            results: [],
          });
        }
      },
      fail: (err) => {
        console.error('搜索失败:', err);
        wx.showToast({
          title: '请求失败，请稍后重试',
          icon: 'none',
        });
        this.setData({
          results: [],
        });
      },
    });
  },

  // 点击商品时跳转到商品详情页
  goodListClickHandle(e) {
    const productId = e.currentTarget.dataset.productId; // 获取点击商品的 product_id
  
    wx.navigateTo({
      url: `/pages/auction/goods/goods?query=${encodeURIComponent(productId)}`,
    });
  },
});
