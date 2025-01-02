const BASE_URL = "https://101972498yahu.vicp.fun"; // 后端服务器的基地址
Page({
  data: {
    history: [], // 浏览记录列表
    page: 1, // 当前页数
    loading: false, // 是否加载中
    noMoreData: false, // 是否没有更多数据
  },

  onLoad() {
    this.fetchHistory(); // 页面加载时获取历史浏览记录
  },

  // 获取openid
  getOpenId() {
    return wx.getStorageSync('openid') || '';
  },

  // 获取历史浏览记录
  fetchHistory() {
    if (this.data.noMoreData || this.data.loading) return; // 如果没有更多数据或正在加载中，直接返回
  
    const openid = this.getOpenId();
    if (!openid) {
      wx.showToast({
        title: '请先登录',
        icon: 'none',
      });
      return;
    }
  
    this.setData({ loading: true });
    wx.request({
      url: `${BASE_URL}/api/gethistory/`,
      method: 'POST',
      data: {
        openid: openid,
        page: this.data.page,
      },
      success: (res) => {
        console.log(res.data);
        if (res.data && res.data.history) {
          const newHistory = res.data.history.map((record) => {
            // 拼接图片 URL 如果需要
            record.images = record.images.map((imageFileName) => {
              if (imageFileName.startsWith('/media/')) {
                imageFileName = imageFileName.replace('/media/', '');
              }
              return `${BASE_URL}/media/uploads/${imageFileName}`;
            });
            return record;
          });
  
          this.setData({
            history: [...this.data.history, ...newHistory], // 追加历史记录
            page: this.data.page + 1,
            noMoreData: newHistory.length === 0, // 判断是否还有更多数据
          });
        } else {
          wx.showToast({
            title: '获取历史记录失败',
            icon: 'none',
          });
        }
      },
      fail: (err) => {
        console.error(err);
        wx.showToast({
          title: '网络错误，请稍后再试',
          icon: 'none',
        });
      },
      complete: () => {
        this.setData({ loading: false });
      },
    });
  },
  



  // 清空历史浏览记录
  clearHistory() {
    const openid = this.getOpenId();
    if (!openid) {
      wx.showToast({
        title: '请先登录',
        icon: 'none',
      });
      return;
    }

    wx.request({
      url: 'https://101972498yahu.vicp.fun/api/clearhistory/',
      method: 'POST',
      data: {
        openid: openid,
      },
      success: (res) => {
        if (res.data.success) {
          wx.showToast({
            title: '历史记录已清空',
            icon: 'success',
          });
          this.setData({ history: [], page: 1, noMoreData: false });
        } else {
          wx.showToast({
            title: '清空失败',
            icon: 'none',
          });
        }
      },
      fail: (err) => {
        console.error(err);
        wx.showToast({
          title: '网络错误，请稍后再试',
          icon: 'none',
        });
      },
    });
  },
});
