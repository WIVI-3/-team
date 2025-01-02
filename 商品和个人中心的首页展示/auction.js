// pages/auction/auction.js
Page({ 
  data: {
    auctiondGoods:[],
  productIds: [],      // 存储所有商品的 product_id
  imagesUrl:[],
},

onLoad() {
  wx.request({
    url: 'https://101972498yahu.vicp.fun/api/auctiongoods/', // 后端接口URL
    method: 'GET',
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
  
        // 提取每个商品的 product_id，并保存在 data.productIds 数组中
        const productIds = products.map(product => product.product_id);
  
        // 更新商品列表和 productIds
        this.setData({
          auctiondGoods: products,    // 存储商品列表
          productIds: productIds,       // 存储所有商品的 product_id
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

onPullDownRefresh() {
  wx.request({
    url: 'https://101972498yahu.vicp.fun/api/auctiongoods/', // 后端接口URL
    method: 'GET',
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
  
        // 提取每个商品的 product_id，并保存在 data.productIds 数组中
        const productIds = products.map(product => product.product_id);
  
        // 更新商品列表和 productIds
        this.setData({
          auctiondGoods: products,    // 存储商品列表
          productIds: productIds,       // 存储所有商品的 product_id
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



goodListClickHandle(e) {
  const productId = e.currentTarget.dataset.productId; // 获取点击商品的 product_id
  console.log('Product ID:', productId);  // 打印 productId，确保它的值正确
  wx.navigateTo({
     url: `/pages/auction/goods/goods?query=${encodeURIComponent(productId)}`,
  });
},
  onGoToSearchPage() {
    wx.navigateTo({
      url: '/pages/auction/search/search' 
    });
  },

  onGoToelectronics() {
    wx.navigateTo({
      url: '/pages/auction/classification/electronics/auctionelectronics' 
    });
  },

  onGoToclothing() {
    wx.navigateTo({
      url: '/pages/auction/classification/clothing/auctionclothing' 
    });
  },

  onGoTobooks() {
    wx.navigateTo({
      url: '/pages/auction/classification/books/auctionbooks' 
    });
  },

  onGoTosports() {
    wx.navigateTo({
      url: '/pages/auction/classification/sports/auctionsports' 
    });
  },

  onGoToothers() {
    wx.navigateTo({
      url: '/pages/auction/classification/others/auctionothers' 
    });
  },
  

});