// pages/homecenter/homecenter.js
Page({
  data: {
    nickName: '',  
    avatarUrl: '',
    showLoginButton: false,
    showLogoutButton: false,
  },

  // 页面加载时的逻辑
  onLoad() {
    const avatarUrl = wx.getStorageSync('avatarUrl');
    const nickName = wx.getStorageSync('nickName');

    // 初始化头像和昵称
    this.setData({
      avatarUrl: avatarUrl,
      nickName: nickName,
    });

    // 根据头像和昵称是否存在，显示不同的按钮
    if (nickName && avatarUrl) {
      // 如果头像和昵称都存在，则显示头像和退出登录按钮
      this.setData({
        showLogoutButton: true,
        showLoginButton: false
      });
    } else {
      // 如果头像和昵称不存在，显示授权登录按钮
      this.setData({
        showLogoutButton: false,
        showLoginButton: false
      });
    }
    //判断拍卖状态
    wx.request({
      url: 'https://101972498yahu.vicp.fun/api/checkauctionstatus/',  // 后端接口地址
      method: 'POST',
      data: {
        now: new Date().toISOString().slice(0, 19).replace('T', ' '),
      },
      success(res) {
        if (res.statusCode === 200) {
          console.log('拍卖商品状态已更新:', res.data);
        } else {
          console.error('操作失败:', res.data.error);
        }
      },
      fail(err) {
        console.error('请求失败:', err);
      }
    });
  },

  // 获取用户头像
  getAvatar(e) {
    this.setData({
      avatarUrl: e.detail.avatarUrl
    });
    this.checkLoginButtonStatus();
  },

  // 获取用户昵称并登录
  getName(e) {
    this.setData({
      nickName: e.detail.value
    });
    this.checkLoginButtonStatus();  
  },

  // 检查是否显示登录按钮
  checkLoginButtonStatus() {
    // 只有当昵称和头像都已获取时，才显示确认登录按钮
    if (this.data.nickName && this.data.avatarUrl) {
      this.setData({
        showLoginButton: true,
      });
    } else {
      this.setData({
        showLoginButton: false,
      });
    }
  },

  // 确认登录
  confirmLogin() {
    wx.login({
      success: (res) => {
        if (res.code) {
          // 发起网络请求，将登录code发送给后端
          wx.request({
            url: 'https://101972498yahu.vicp.fun/api/login/',  // 后端接口地址
            method: 'POST',
            data: {
              code: res.code,  // 发送登录code
              nickName: this.data.nickName,  // 发送用户昵称
              avatarUrl: this.data.avatarUrl,  // 发送用户头像
            },
            success: (response) => {
              if (response.data.success) {
                const { openid, session_key } = response.data;
                wx.setStorageSync('openid', openid);
                wx.setStorageSync('sessionKey', session_key);
                wx.setStorageSync('nickName', this.data.nickName);
                wx.setStorageSync('avatarUrl', this.data.avatarUrl);
                wx.setStorageSync('userInfo', {
                  nickName: this.data.nickName,
                  avatarUrl: this.data.avatarUrl,
                  openid: openid,
                  session_key: session_key,
                });

                wx.showToast({
                  title: '登录成功',
                  icon: 'success',
                });

                this.setData({
                  showLoginButton: false,  // 登录成功后隐藏按钮
                  showLogoutButton: true,  // 显示退出登录按钮
                });
              } else {
                wx.showToast({
                  title: response.data.message || '登录失败，请重试',
                  icon: 'none',
                });
              }
            },
            fail: (err) => {
              wx.showToast({
                title: '网络请求失败，请稍后再试',
                icon: 'none',
              });
              console.error(err);
            }
          });
        } else {
          console.log('登录失败！' + res.errMsg);
        }
      }
    });
  },

  // 退出登录
  logout() {
    wx.removeStorageSync('userInfo'); // 删除本地存储的用户信息
    wx.removeStorageSync('sessionKey');
    wx.removeStorageSync('nickName');
    wx.removeStorageSync('openid');
    wx.removeStorageSync('avatarUrl');
    this.setData({
      nickName: '',
      avatarUrl: '',
      showLoginButton: false,  // 登录按钮可见
      showLogoutButton: false,  // 退出登录按钮不可见
    });
    wx.showToast({
      title: '已退出登录',
      icon: 'success',
    });
  },

  // 其他页面跳转逻辑...
  onGoToinformation() {
    wx.navigateTo({
      url: '/pages/homecenter/personalinformation/personalinformation',
    });
  },

  onGoTobrowse() {
    wx.navigateTo({
      url: '/pages/homecenter/browsinghistory/browsinghistory',
    });
  },

  onGoTofavorites() {
    wx.navigateTo({
      url: '/pages/homecenter/favorites/favorites',
    });
  },

  onGoToorders() {
    wx.navigateTo({
      url: '/pages/homecenter/ordersbrowsing/ordersbrowsing',
    });
  }
});




