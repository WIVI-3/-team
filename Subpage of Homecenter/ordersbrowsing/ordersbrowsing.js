const BASE_URL = "https://101972498yahu.vicp.fun"; // 后端服务器的基地址

Page({
  data: {
    currentUser: '', // 当前用户的用户名
    orders: [], // 买家和卖家的所有订单
    buyerOpenid: "",
    category1: "", // 当前选择的商品类别
    page: 1, // 页码
    hasMore: true, // 是否还有更多订单
    isLoading: false, // 是否正在加载
  },

  // 页面加载时初始化
  onLoad() {
    this.setOpenid();
    const openid = wx.getStorageSync('openid');
    
    this.fetchOrders();  // 加载买家和卖家的订单
  },

  onPullDownRefresh(){
    setTimeout(() => {
      wx.reLaunch({
        url: '/pages/homecenter/ordersbrowsing/ordersbrowsing',
      });
    }, 1000);
    wx.stopPullDownRefresh();
  },

  // 设置 Openid
  setOpenid() {
    const openid = wx.getStorageSync("openid");
    if (openid) {
      this.setData({ buyerOpenid: openid });
    } else {
      wx.showToast({ title: "请先登录", icon: "error" });
    }
  },

  // 切换商品类别
  selectCategory(e) {
    const category1 = e.currentTarget.dataset.category1;

    this.setData({
      category1: category1,
      orders: [], // 清空之前的订单数据
      page: 1, // 重置页码
      hasMore: true, // 重置加载标记
    }, () => {
      this.fetchOrders(); // 根据选择的类别重新加载订单
    });
  },

  // 请求买家和卖家订单（合并到一个订单数组）
  fetchOrders() {
    if (this.data.isLoading || !this.data.hasMore) return;

    this.setData({ isLoading: true }); // 设置加载中

    // 请求卖家订单
    wx.request({
      url: `${BASE_URL}/api/getsellerorder/`,
      method: "POST",
      data: {
        openid: this.data.buyerOpenid,
        category1: this.data.category1, // 当前选择的商品类别
        page: this.data.page, // 页码
      },
      success: (res) => {
        if (res.statusCode === 200 && res.data.orders) {
          const sellerOrders = res.data.orders.map((order) => {
            // 处理商品图片链接
            order.product_images = order.product_images.map((imageFileName) => {
              if (imageFileName.startsWith("/media/")) {
                imageFileName = imageFileName.replace("/media/", "");
              }
              return `${BASE_URL}/media/uploads/${imageFileName}`;
            });
            return order;
          });

          // 合并卖家订单到 orders 数组
          this.setData({
            orders: [...this.data.orders, ...sellerOrders], // 追加卖家订单
          });
        }
      },
      fail: () => {
        wx.showToast({ title: '网络请求失败', icon: 'none' });
      },
    });

    // 请求买家订单
    wx.request({
      url: `${BASE_URL}/api/getorder/`,
      method: "POST",
      data: {
        openid: this.data.buyerOpenid,
        category1: this.data.category1, // 当前选择的商品类别
        page: this.data.page, // 页码
      },
      success: (res) => {
        if (res.statusCode === 200 && res.data.orders) {
          const buyerOrders = res.data.orders.map((order) => {
            // 处理商品图片链接
            order.product_images = order.product_images.map((imageFileName) => {
              if (imageFileName.startsWith("/media/")) {
                imageFileName = imageFileName.replace("/media/", "");
              }
              return `${BASE_URL}/media/uploads/${imageFileName}`;
            });
            return order;
          });

          // 合并买家订单到 orders 数组
          this.setData({
            orders: [...this.data.orders, ...buyerOrders], // 追加买家订单
            page: this.data.page + 1, // 翻到下一页
            hasMore: buyerOrders.length > 0, // 判断是否还有更多订单
          });
        } else {
          wx.showToast({ title: '没有更多订单', icon: 'none' });
        }
      },
      fail: () => {
        wx.showToast({ title: '网络请求失败', icon: 'none' });
      },
      complete: () => {
        this.setData({ isLoading: false }); // 请求完成，停止加载状态
      }
    });
  },

  // 取消订单
  cancelOrder(e) {
    const orderId = e.currentTarget.dataset.id;
    wx.request({
      url: `${BASE_URL}/api/cancelorder/`,
      method: "POST",
      data: {
        order_id: orderId,
        buyer_openid: this.data.buyerOpenid
      },
      success: (res) => {
        if (res.data) {
          wx.showToast({ title: "订单已取消", icon: "success" });
          setTimeout(() => {
            wx.reLaunch({
              url: 'pages/homecenter/homecenter',
            });
          }, 1000);
        }
      }
    });
  },

  // 确认收货
  confirmReceipt(e) {
    const orderId = e.currentTarget.dataset.id;
    wx.request({
      url: `${BASE_URL}/api/getgoods/`,
      method: "POST",
      data: {
        order_id: orderId,
        buyer_openid: this.data.buyerOpenid
      },
      success: (res) => {
        if (res.statusCode === 200) {
          wx.showToast({
            title: res.data.message,  // 显示后端返回的信息
            icon: "success"
          });
          this.fetchOrders(); // 重新加载订单
        } else {
          wx.showToast({
            title: res.data.message,
            icon: 'none'
          });
        }
      },
      fail: () => {
        wx.showToast({
          title: '网络请求失败',
          icon: 'none'
        });
      }
    });
  },
  

  // 删除商品（卖家）
  deleteProduct(e) {
    const productId = e.currentTarget.dataset.id;
    wx.request({
      url: `${BASE_URL}/api/deleteproduct/`,
      method: "POST",
      data: {
        product_id: productId
      },
      success: (res) => {
        if (res.data) {
          wx.showToast({ title: "商品已下架", icon: "success" });
          this.fetchOrders(); // 重新加载订单
          setTimeout(() => {
            wx.reLaunch({
              url: '/pages/homecenter/homecenter',
            });
          }, 1000);
        }
      }
    });
  },

  // 完成交易（卖家）
  finishOrder(e) {
    const orderId = e.currentTarget.dataset.id;
    wx.request({
      url: `${BASE_URL}/api/finishorder/`,
      method: "POST",
      data: {
        order_id: orderId
      },
      success: (res) => {
        if (res.data) {
          wx.showToast({ title: "交易已完成", icon: "success" });
          wx.reLaunch({
            url: 'pages/homecenter/ordersbrowsing/ordersbrowsing',
          });
        }
      }
    });
  }
});

