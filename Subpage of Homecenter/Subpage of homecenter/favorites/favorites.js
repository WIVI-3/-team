Page({
  data: {
    favorites: [], // 收藏夹列表
    page: 1, // 当前页数
    loading: false, // 是否加载中
    noMoreData: false, // 是否没有更多数据
  },

  onLoad() {
    this.fetchFavorites(); // 页面加载时获取收藏夹
  },

  // 获取收藏夹内容
  fetchFavorites() {
    if (this.data.noMoreData || this.data.loading) return;
    wx.getStorage({
      key: 'openid',
      success: (res) => {
        const openid = res.data;
        const BASE_URL = "https://101972498yahu.vicp.fun"; // 基础 URL
        this.setData({ loading: true });
        wx.request({
          url: `${BASE_URL}/api/getfavorites/`,
          method: 'POST',
          data: { openid },
          success: (res) => {
            if (res.data) {
              const newFavorites = res.data.favorites.map((item) => {
                const fixedImages = item.images.map((imageFileName) => {
                  if (imageFileName.startsWith('/media/')) {
                    imageFileName = imageFileName.replace('/media/', '');
                  }
                  return `${BASE_URL}/media/uploads/${imageFileName}`;
                });
                return {
                  ...item,
                  images: fixedImages,
                  imageUrl: fixedImages[0],
                };
              });
              const noMoreData = newFavorites.length === 0;
              this.setData({
                favorites: [...this.data.favorites, ...newFavorites],
                page: this.data.page + 1,
                noMoreData,
              });
            } else {
              wx.showToast({ title: '获取收藏夹失败', icon: 'none' });
            }
          },
          fail: () => wx.showToast({ title: '网络错误', icon: 'none' }),
          complete: () => this.setData({ loading: false }),
        });
      },
      fail: () => wx.showToast({ title: '获取 openid 失败', icon: 'none' }),
    });
    
  },

  // 移除单个订单
  removeFavorite(e) {
    const { id } = e.currentTarget.dataset;
    wx.getStorage({
      key: 'openid',
      success: (res) => {
        const openid = res.data;
        wx.request({
          url: 'https://101972498yahu.vicp.fun/api/removefromfavorites/',
          method: 'POST',
          data: { openid, product_id: id },
          success: (res) => {
            if (res.data) {
              this.setData({
                favorites: this.data.favorites.filter((fav) => fav.product_id !== id),
              });
              wx.showToast({ title: '移除成功', icon: 'success' });
            } else {
              wx.showToast({ title: '移除失败', icon: 'none' });
            }
          },
        });
      },
      fail: () => wx.showToast({ title: '获取 openid 失败', icon: 'none' }),
    });
  },

  navigateToProductDetail(e) {
    const { id: productId, category1 } = e.currentTarget.dataset; // 获取数据集中的 id 和 category1
  console.log(`Product ID: ${productId}, Category: ${category1}`);

  if (!productId || !category1) {
    wx.showToast({
      title: '商品信息缺失',
      icon: 'none',
    });
    return;
  }
    
    let targetPage = '';
    switch (category1) {
      case '二手交易':
        targetPage = '/pages/secondhand/goods/testpage';
        break;
      case '拍卖':
        targetPage = '/pages/auction/goods/goods';
        break;
      case '租赁':
        targetPage = '/pages/rental/goods/rentalgoods';
        break;
      default:
        wx.showToast({
          title: '未知分类',
          icon: 'none',
        });
        return; // 如果分类未知，退出方法
    }
  
    // 跳转到目标页面，并传递商品 ID
    wx.navigateTo({
      url: `${targetPage}?query=${encodeURIComponent(productId)}`,
    });
  },
  
  


  // 清空收藏夹
  clearAllFavorites() {
    wx.getStorage({
      key: 'openid',
      success: (res) => {
        const openid = res.data;
        wx.showModal({
          title: '提示',
          content: '确定清空收藏夹吗？',
          success: (modalRes) => {
            if (modalRes.confirm) {
              wx.request({
                url: 'https://101972498yahu.vicp.fun/api/clearfavorites/',
                method: 'POST',
                data: { openid },
                success: (res) => {
                  if (res.data) {
                    this.setData({ favorites: [] });
                    wx.showToast({ title: '清空成功', icon: 'success' });
                  } else {
                    wx.showToast({ title: '清空失败', icon: 'none' });
                  }
                },
              });
            }
          },
        });
      },
      fail: () => wx.showToast({ title: '获取 openid 失败', icon: 'none' }),
    });
  },
});
