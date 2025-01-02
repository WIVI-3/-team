from django.conf import settings
from django.utils import timezone
from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from myapp.models import Product, User, ProductStatus, Category1, Order

logger = logging.getLogger(__name__)

@csrf_exempt  # 禁用CSRF验证（开发时使用，生产环境应启用并处理）
def publish_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 解析请求体中的JSON数据
            openid = data.get('openid')  # 获取 openid

            # 获取前端传递的商品信息
            category1 = data.get('category1')
            category2 = data.get('category2')
            name = data.get('name')
            price = data.get('price')
            description = data.get('description')
            phone = data.get('phone')
            images = data.get('images')
            address = data.get('address')
            provide_service = data.get('provideService', False)  # 默认值 False
            rental_period = data.get('rentalPeriod', '0')
            auction_end_date = data.get('auctionEndDate')  # 获取拍卖结束日期
            auction_end_time = data.get('auctionEndTime')  # 获取拍卖结束时间

            if auction_end_date and auction_end_time:
                auction_end_datetime_str = f"{auction_end_date} {auction_end_time}"  # 格式： "YYYY-MM-DD HH:MM"
                try:
                    auction_end_datetime_naive = datetime.strptime(auction_end_datetime_str, "%Y-%m-%d %H:%M")

                    # 转换为带时区的时间，使用当前时区（例如，Django的默认时区）
                    auction_end_datetime = timezone.make_aware(auction_end_datetime_naive,
                                                               timezone.get_current_timezone())

                    # 将时区感知的时间转换为本地时间
                    auction_end_datetime_local = timezone.localtime(auction_end_datetime)

                    # 如果 USE_TZ = False，将带时区的时间转换为朴素的时间
                    if not settings.USE_TZ:
                        auction_end_datetime_local = auction_end_datetime_local.replace(tzinfo=None)

                except ValueError:
                    return JsonResponse({"success": False, "message": "无效的日期或时间格式"}, status=400)
            else:
                auction_end_datetime_local = None  # 如果没有提供拍卖结束日期和时间

            # 日志：查看接收到的数据
            logger.info(f"Received data: {data}")

            # 检查必填项是否完整
            if not name or not price or not description or not phone or not address or not images:
                return JsonResponse({'success': False, 'message': '请提供完整的商品信息'})

            # 类型转换和验证
            try:
                price = float(price)  # 确保价格是浮动类型
            except ValueError:
                return JsonResponse({'success': False, 'message': '价格必须是数字'})

            # 检查图片数组
            if not isinstance(images, list) or not all(isinstance(image, str) for image in images):
                return JsonResponse({'success': False, 'message': '图片必须是一个包含图片路径的字符串列表'})

            # 验证租赁周期（rentalPeriod）字段
            if category1 == '租赁':
                if rental_period not in ['/天', '/月']:
                    return JsonResponse({'success': False, 'message': '无效的租赁周期，必须为 "天" 或 "月"'})
            else:
                rental_period = '0'  # 非租赁商品，设置租赁周期为 0

            # 获取对应的用户
            user = User.objects.filter(openid=openid).first()

            if not user:
                return JsonResponse({'success': False, 'message': '用户未登录或无效的 openid'})

            # 日志：打印即将传入 create 的数据
            logger.info(
                f"Creating product with values: category1={category1}, category2={category2}, name={name}, price={price}, description={description}, phone={phone}, address={address}, images={images}, provide_service={provide_service}")

            # 创建商品记录
            product = Product.objects.create(
                user=user,  # 关联用户
                category1=category1,
                category2=category2,
                name=name,
                price=price,
                description=description,
                phone=phone,
                address=address,
                images=images,
                provide_service=provide_service,  # 使用 provideService 字段
                rental_period=rental_period,
                auction_end_time=auction_end_datetime_local,  # 存入本地时区的时间
                product_status=ProductStatus.LIST,  # 假设商品状态是 LIST
            )

            # 添加日志输出
            logger.info(f"Product created: {product}")

            return JsonResponse({'success': True, 'message': '商品发布成功', 'product_id': product.product_id})

        except Exception as e:
            logger.error(f"Error in product publishing: {str(e)}")
            return JsonResponse({'success': False, 'message': f"发布失败: {str(e)}"})

    return JsonResponse({'success': False, 'message': '仅支持POST请求'})
