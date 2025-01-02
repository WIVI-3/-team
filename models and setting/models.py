from django.db import models

# 商品类别枚举类（可根据需要扩展）
class Category1(models.TextChoices):
    SECOND_HAND = '二手交易', '二手交易'
    AUCTION = '拍卖', '拍卖'
    RENTAL = '租赁', '租赁'

class Category2(models.TextChoices):
    ELECTRONICS = '电子产品', '电子产品'
    CLOTHING = '服装', '服装'
    BOOKS = '书籍', '书籍'
    SPORTS = '运动', '运动'
    OTHERS = '其他', '其他'

# 租赁周期枚举类
class RentalPeriod(models.TextChoices):
    DAY = '每天', '每天'
    MONTH = '每月', '每月'

 # 商品交易状态
class OrderStatus(models.TextChoices):
    PUBLISH = '已发布', '已发布'
    ONGOING = '交易中', '交易中'
    FINISH = '交易成功', '交易成功'
    FAIL = '交易取消', '交易取消'
    RECEIVE = '已收货', '已收货'


 # 商品状态
class ProductStatus(models.TextChoices):
    LIST = '上架中', '上架中'
    LOCK = '锁定', '锁定'

# 用户模型
class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # 用户ID，自动生成
    openid = models.CharField(max_length=255, unique=True,null=True)  # 微信用户的 openid，唯一
    wechat_id = models.CharField(max_length=100, unique=True, null=True, blank=True)  # 微信号，唯一且可选
    username = models.CharField(max_length=255)  # 用户名
    email = models.EmailField(unique=True, null=True, blank=True)  # 邮箱，可选
    phone = models.CharField(max_length=15, null=True, blank=True)  # 联系电话，可选
    address = models.CharField(max_length=255, null=True, blank=True)  # 地址，可选
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # 头像，可选

    def __str__(self):
        return self.username

# 商品信息模型
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)  # 商品编号，自动生成
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # 外键：微信用户，允许为空
    category1 = models.CharField(max_length=20, choices=Category1.choices)  # 商品类别1
    category2 = models.CharField(max_length=20, choices=Category2.choices)  # 商品类别2
    name = models.CharField(max_length=255)  # 商品名称
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 商品价格
    description = models.TextField()  # 商品描述
    phone = models.CharField(max_length=15)  # 联系电话
    address = models.CharField(max_length=255)  # 卖家地址
    images = models.JSONField(default=list)  # 商品图片（存储图片路径的列表）
    provide_service = models.BooleanField(default=False)  # 是否提供上门服务
    rental_period = models.CharField(max_length=10, choices=RentalPeriod.choices, default=RentalPeriod.DAY)  # 租赁周期（天/月）
    created_at = models.DateTimeField(auto_now_add=True)  # 商品创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 商品更新时间
    product_status = models.CharField(max_length=10, choices=ProductStatus.choices, default=ProductStatus.LIST)
    auction_end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

# 订单信息模型
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)  # 订单编号，自动生成
    buyer_openid = models.CharField(max_length=100,null=True)  # 买家 openid
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 关联商品
    created_at = models.DateTimeField(auto_now_add=True)  # 订单创建时间
    transaction_price = models.DecimalField(max_digits=10, decimal_places=2)   #订单成交价
    order_status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.ONGOING) #交易状态
    rental_period = models.IntegerField(null=True, blank=True)  # 租期，为数字

    def __str__(self):
        return f"订单 {self.order_id} - {self.product.name} ({self.buyer_openid})"

#用户收藏的商品
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 外键：用户
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 外键：商品
    created_at = models.DateTimeField(auto_now_add=True)  # 收藏时间

    class Meta:
        unique_together = ('user', 'product')  # 确保同一用户不能重复收藏同一商品

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.product.name}"

#用户浏览历史页面
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='histories')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='histories')
    viewed_at = models.DateTimeField(auto_now_add=True)  # 记录浏览时间

    def __str__(self):
        return f"{self.user.username} viewed {self.product.name} at {self.viewed_at}"

