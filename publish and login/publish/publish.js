// publish.js
Page({
  data: {
    categories1: ['二手交易', '拍卖', '租赁'],  // 商品类别
    selectedCategory1: '二手交易',  // 默认选择类别
    categories2: ['电子产品', '服装', '书籍', '运动', '其他'], 
    selectedCategory2: '电子产品', 
    name: '',  // 商品名称
    price: '',  // 商品价格
    description: '',  // 商品介绍
    phone: '',  // 联系电话
    address: '',  // 卖家地址
    images: [],    // 存储已选择的图片
    uploadImageSrc: '/images/uploadimages.png',
    provideService: true,
    rentalPeriod: ['/天', '/月'], 
    selectedrentalperiod: '/天', // 默认值
    nickName: '',  // 用户昵称
    avatarUrl: '',  // 用户头像
    openid: '',  // 存储 openid
    auctionEndTime: '',  // 拍卖结束时间
    product_id:'',
  },

  onLoad(options) {
    const openid = wx.getStorageSync('openid');
      // 将用户信息存储到 data 中
      this.setData({
        openid : openid,  // 存储 openid
      });
  },

  // 选择商品类别
  onCategoryChange1(e) {
    const selectedIndex1 = e.detail.value;
    this.setData({
      selectedCategory1: this.data.categories1[selectedIndex1]
    });
    // 如果选择的是拍卖类别，显示时间选择框
    if (this.data.categories1[selectedIndex1] === '拍卖') {
      this.setData({
        auctionStartTime: '',  // 清空拍卖开始时间
        auctionEndTime: '',    // 清空拍卖结束时间
      });
    }
  },

  // 选择拍卖结束日期
onDateChange: function (e) {
  const date = e.detail.value;
  this.setData({
    auctionEndDate: date,  // 更新拍卖结束日期
  });
},

// 选择拍卖结束时间
onTimeChange: function (e) {
  const time = e.detail.value;
  this.setData({
    auctionEndTime: time,  // 更新拍卖结束时间
  });
},


  onCategoryChange2(e) {
    const selectedIndex2 = e.detail.value;
    this.setData({
      selectedCategory2: this.data.categories2[selectedIndex2]
    });
  },

  // 商品名称输入处理
onNameChange(e) {
  let name = e.detail.value;
  if (name.length > 10) {
    name = name.substring(0, 10);  // 截取前 10 个字符
    wx.showToast({
      title: '商品名称不能超过10个字',
      icon: 'none',
    });
  }
  this.setData({
    name: name  // 更新商品名称，自动删除超出的部分
  });
},


  // 商品价格输入处理
  onPriceChange(e) {
    this.setData({
      price: e.detail.value
    });
  },

  // 商品介绍输入处理
  onDescriptionChange(e) {
    this.setData({
      description: e.detail.value
    });
  },

  // 联系电话
  onPhoneChange(e) {
    const phone = e.detail.value;
    // 仅保留数字
    const phoneNumber = phone.replace(/\D/g, '');
    this.setData({
      phone: phoneNumber
    });

    // 检查是否为 11 位
    if (phoneNumber.length > 11) {
      wx.showToast({
        title: '联系电话不能超过 11 位',
        icon: 'none',
      });
      this.setData({
        phone: phoneNumber.slice(0, 11)  // 限制为 11 位
      });
    }
  },

  // 选择是否提供上门服务
  onServiceChange(e) {
    const provideService = e.detail.value.includes('provideService');
    this.setData({
      provideService: provideService
    });
  },

  // 卖家地址输入处理
  onAddressChange(e) {
    this.setData({
      address: e.detail.value
    });
  },

  // 选择租赁单位
  onRentalPeriodChange(e) {
    const selectedrentalPeriod = e.detail.value;
    this.setData({
      selectedrentalperiod: this.data.rentalPeriod[selectedrentalPeriod]
    });
  },
  
  // 上传图片
  chooseImage() {
    const currentImages = this.data.images;
    if (currentImages.length >= 3) {
      wx.showToast({
        title: '最多只能上传 3 张图片',
        icon: 'none',
      });
      return; // 如果已上传 3 张图片，停止选择
    }

    wx.chooseMedia({
      count: 3 - currentImages.length,  // 根据已上传的图片数量限制选择数量
      mediaType: ['image'],  // 只选择图片
      sourceType: ['album', 'camera'],  // 可从相册或相机选择
      success: (res) => {
        const newImages = res.tempFiles.map(file => file.tempFilePath);
        this.setData({
          images: [...this.data.images, ...newImages],  // 将新选中的图片添加到 images 数组中
          uploadImageSrc: newImages[0],  // 更新上传按钮为选中的图片
        });
      },
      fail: (err) => {
        console.error('选择图片失败', err);
      }
    });
  },


  // 删除图片
  deleteImage(e) {
    const index = e.currentTarget.dataset.index; // 获取图片索引
    const images = this.data.images;
    images.splice(index, 1);  // 从数组中删除该图片
    this.setData({
      images: images,  // 更新图片数组
      uploadImageSrc: images.length === 0 ? '/images/upload-image.png' : this.data.uploadImageSrc,  // 如果没有图片，则恢复默认按钮图片
    });
  },

  // 提交商品
onSubmit() {
  const { selectedCategory1, selectedCategory2, name, price, description, phone, address, images, provideService, selectedrentalperiod, auctionEndDate, auctionEndTime } = this.data;

  const openid = wx.getStorageSync('openid');
  // 检查是否登录
  if (!openid) {
    wx.showToast({
      title: '未获取到用户信息，请登录后再试',
      icon: 'none',
    });
    return;
  }

  // 将价格转换为浮动类型
  const parsedPrice = parseFloat(price);

  // 检查必填项是否已填写
  if (!name || !parsedPrice || !description || !phone) {
    wx.showToast({
      title: '请填写所有信息',
      icon: 'none'
    });
    return;
  }

  if (isNaN(parsedPrice)) {
    wx.showToast({
      title: '请输入有效的价格',
      icon: 'none',
    });
    return;
  }

  // 如果用户没有勾选送货上门，才检查地址是否填写
  if (!provideService && !address) {
    wx.showToast({
      title: '请填写卖家地址',
      icon: 'none'
    });
    return;
  }

  // 检查是否至少上传一张图片
  if (this.data.images.length === 0) {
    wx.showToast({
      title: '请上传至少一张图片',
      icon: 'none',
    });
    return;  // 如果没有上传图片，阻止提交
  }

  // 通过检查 provideService 来设置 finalAddress
  const finalAddress = provideService ? '0' : address;

  // 判断是否填写拍卖结束日期和时间
  if (selectedCategory1 === '拍卖' && (!auctionEndDate || !auctionEndTime)) {
    wx.showToast({
      title: '请填写拍卖结束日期和时间',
      icon: 'none',
    });
    return;
  }

  // 判断拍卖结束时间是否至少比当前时间晚 2 小时
  const auctionEndDateTime = new Date(`${auctionEndDate} ${auctionEndTime}`);
  const currentTime = new Date();

  const twoHoursLater = new Date(currentTime.getTime() + 2 * 60 * 60 * 1000); // 当前时间加 2 小时

  if (auctionEndDateTime <= twoHoursLater) {
    wx.showToast({
      title: '拍卖结束时间必须至少比当前时间晚 2 小时',
      icon: 'none',
    });
    return;
  }

  // 显示提交提示
  wx.showToast({
    title: '商品发布中...',
    icon: 'loading',
    duration: 20000
  });

  // 检查是否获取到 openid
  if (openid) {
    // 上传图片
    const imageUploads = this.data.images.map(image => {
      return new Promise((resolve, reject) => {
        wx.uploadFile({
          url: 'https://101972498yahu.vicp.fun/api/uploadimages/', // 图片上传接口
          filePath: image,
          name: 'file',  // 后端接收文件字段名
          success: (uploadRes) => {
            const responseData = JSON.parse(uploadRes.data);
            resolve(responseData.file_url); // 返回上传后的图片 URL
          },
          fail: (err) => {
            reject('图片上传失败');
          }
        });
      });
    });

    // 等待所有图片上传完成
    Promise.all(imageUploads)
      .then((imageUrls) => {
        // 将图片 URL 添加到商品信息中
        const that = this;  // 保留对页面实例的引用
        wx.request({
          url: 'https://101972498yahu.vicp.fun/api/products/', // 后端接口地址
          method: 'POST',
          header: {
            'Content-Type': 'application/json', // 请求的内容类型
          },
          data: {
            category1: selectedCategory1,  // 选择的类别1
            category2: selectedCategory2,  // 选择的类别2
            name: name,  // 商品名称
            price: parsedPrice,  // 商品价格
            description: description,  // 商品介绍
            phone: phone,  // 联系电话
            address: finalAddress,  // 卖家地址，如果提供上门服务则返回 "0"
            images: imageUrls,  // 上传的图片 URL 数组
            provideService: provideService,  // 是否提供上门服务
            rentalPeriod: selectedrentalperiod, 
            auctionEndDate: auctionEndDate,  // 拍卖结束日期
            auctionEndTime: auctionEndTime,  // 拍卖结束时间
            openid: openid,  // 添加 openid
          },

          success(res) {
            wx.hideToast(); // 隐藏加载提示
            if (res.statusCode === 200 && res.data.success) {
              const product_id = res.data.product_id;
              that.setData({ product_id: product_id });
              wx.showToast({
                title: '商品发布成功',
                icon: 'success',
              });

              // 创建订单，无论商品是否为拍卖
              const productid = res.data.product_id;
              console.log("productid：", productid);

              wx.request({
                url: 'https://101972498yahu.vicp.fun/api/createorder/', // 创建订单接口
                method: 'POST',
                header: {
                  'Content-Type': 'application/json',
                },
                data: {
                  product_id: productid,
                  buyer_openid: wx.getStorageSync('openid'),  // openid
                },
                success(orderRes) {
                  if (orderRes.statusCode === 200 && orderRes.data) {         
                    wx.showToast({
                      title: '订单创建成功',
                      icon: 'success',
                    }); 
                     // 延迟 1 秒后执行跳转回到主页
        setTimeout(() => {
          wx.reLaunch({
            url: '/pages/publish/publish',
          });
        }, 1000);
                    
                  } else {
                    wx.showToast({
                      title: orderRes.data.message || '订单创建失败',
                      icon: 'none',
                    });
                  }
                },
                fail(err) {
                  wx.showToast({
                    title: '网络错误，请稍后重试',
                    icon: 'none',
                  });
                  console.error('订单创建失败', err);
                }
              });
            } else {
              wx.showToast({
                title: res.data.message || '发布失败，请重试',
                icon: 'none',
              });
            }
          },
          fail(err) {
            wx.hideToast();
            wx.showToast({
              title: '网络错误，请稍后重试',
              icon: 'none',
            });
            console.error('请求失败', err);
          }
        });
      })
      .catch((err) => {
        wx.showToast({
          title: err,
          icon: 'none',
        });
      });
  } else {
    wx.showToast({
      title: '未获取到 openid，请登录',
      icon: 'none',
    });
  }
}

  
});

