Page({
  data: {
    wechatid: '',
    username: '',
    phone: '',
    email: '',
    address: '',
    hasAddress: false, // 根据实际情况初始化
  },

  // 返回上一页
  goBack() {
    wx.navigateBack({
      delta: 1, // 返回上一页
    });
  },

  // 输入框绑定的值改变
  handleInputChange(e) {
    const { field } = e.currentTarget.dataset;
    this.setData({
      [field]: e.detail.value,
    });
  },

  // 保存修改
  saveChanges() {
    const { wechatid, username, phone, email, address } = this.data;
  
    // 分别存储变量
    wx.setStorage({
      key: 'wechatid',
      data: wechatid,
      success: () => console.log('Wechat ID 保存成功'),
      fail: (err) => console.error('Wechat ID 保存失败:', err),
    });
  
    wx.setStorage({
      key: 'username',
      data: username,
      success: () => console.log('Username 保存成功'),
      fail: (err) => console.error('Username 保存失败:', err),
    });
  
    wx.setStorage({
      key: 'phone',
      data: phone,
      success: () => console.log('Phone 保存成功'),
      fail: (err) => console.error('Phone 保存失败:', err),
    });
  
    wx.setStorage({
      key: 'email',
      data: email,
      success: () => console.log('Email 保存成功'),
      fail: (err) => console.error('Email 保存失败:', err),
    });
  
    wx.setStorage({
      key: 'address',
      data: address,
      success: () => {
        // 更新 hasAddress 状态
        this.setData({
          hasAddress: !!address, // 如果 address 存在，hasAddress 为 true，否则为 false
        });
  
        wx.showToast({
          title: '保存成功',
          icon: 'success',
        });
      },
      fail: (err) => {
        wx.showToast({
          title: '保存失败，请重试',
          icon: 'none',
        });
        console.error('Address 保存失败:', err);
      },
    });
  
    // 发送 POST 请求保存到服务器
    wx.getStorage({
      key: 'openid',
      success: (res) => {
        const openid = res.data;
        wx.request({
          url: 'https://101972498yahu.vicp.fun/api/changeuserdata/',
          method: 'POST',
          data: {
            openid: openid,
            username: username,
            email: email,
            phone: phone,
            address: address,
            wechat_id: wechatid,
          },
          success: (res) => {
            if (res.data.success) {
              wx.showToast({
                title: '服务器保存成功',
                icon: 'success',
              });
            } else {
              wx.showToast({
                title: '服务器保存失败，请重试',
                icon: 'none',
              });
            }
          },
          fail: (err) => {
            wx.showToast({
              title: '网络请求失败',
              icon: 'none',
            });
            console.error('服务器请求错误:', err);
          },
        });
      },
      fail: () => {
        wx.showToast({
          title: '获取 openid 失败',
          icon: 'none',
        });
      },
    });
  },  

  onLoad(options) {
    // 分别从本地存储加载用户信息
    wx.getStorage({
      key: 'wechatid',
      success: (res) => {
        this.setData({ wechatid: res.data });
      },
      fail: () => console.log('未找到存储的 Wechat ID'),
    });

    wx.getStorage({
      key: 'username',
      success: (res) => {
        this.setData({ username: res.data });
      },
      fail: () => console.log('未找到存储的 Username'),
    });

    wx.getStorage({
      key: 'phone',
      success: (res) => {
        this.setData({ phone: res.data });
      },
      fail: () => console.log('未找到存储的 Phone'),
    });

    wx.getStorage({
      key: 'email',
      success: (res) => {
        this.setData({ email: res.data });
      },
      fail: () => console.log('未找到存储的 Email'),
    });

    wx.getStorage({
      key: 'address',
      success: (res) => {
        this.setData({
          address: res.data,
          hasAddress: !!res.data, // 判断是否有地址
        });
      },
      fail: () => console.log('未找到存储的 Address'),
    });
  },
});
