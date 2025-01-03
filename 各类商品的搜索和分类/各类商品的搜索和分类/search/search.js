// pages/secondhand/search/search.js
Page({
  data: {
    searchQuery: '',
    history: [],  // 存储历史记录
  },

  onInputChange(e) {
    this.setData({
      searchQuery: e.detail.value,
    });
  },

   Search() {
    const { searchQuery, history } = this.data;

    if (searchQuery && !history.includes(searchQuery)) {
      // 添加新搜索词到历史记录
      const newHistory = [searchQuery, ...history].slice(0, 10); // 保留最近10条历史
      this.setData({
        history: newHistory,
      });
      wx.setStorageSync('searchHistory', newHistory);  // 将历史记录存储到本地
    }
    // 跳转到搜索结果页面并传递搜索关键字
    wx.navigateTo({
      url: `/pages/secondhand/search/searchresults/searchresults?query=${encodeURIComponent(searchQuery)}`,
    });
  },

  onSelectHistory(e) {
    const selectedQuery = e.currentTarget.dataset.query;
    this.setData({
      searchQuery: selectedQuery,
    });
     // 跳转到搜索结果页面并传递历史记录的搜索关键字
     wx.navigateTo({
      url: `/pages/secondhand/search/searchresults/searchresults?query=${encodeURIComponent(selectedQuery)}`,
    });
  },

  clearHistory() {
    this.setData({
      history: [],
    });
    wx.removeStorageSync('searchHistory');  // 清除本地存储的历史记录
  },

  onLoad() {
    const storedHistory = wx.getStorageSync('searchHistory') || [];
    this.setData({
      history: storedHistory,
    });
  },
});
