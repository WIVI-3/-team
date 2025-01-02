from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
import logging
from myapp.models import Product, Order, ProductStatus, OrderStatus, User

# 设置日志记录
logger = logging.getLogger(__name__)

@csrf_exempt
def change_order(request):
    if request.method == 'POST':
        # 解析 JSON 数据
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的 JSON 数据'}, status=400)

        openid = data.get('openid')
        product_id = data.get('product_id')

        logger.info(f"openid: {openid}, product_id: {product_id}")

        # 参数验证
        if not openid or not product_id:
            return JsonResponse({'error': 'openid 和 product_id 是必填的'}, status=400)

        try:
            # 获取用户信息
            user = get_object_or_404(User, openid=openid)

            # 获取商品信息
            product = get_object_or_404(Product, product_id=product_id)
            logger.info(f"Found product: {product}")

            # 查找与该商品相关的订单
            order = get_object_or_404(Order, product=product)
            logger.info(f"Found order: {order}")

            # 修改商品状态为锁定
            product.product_status = ProductStatus.LOCK
            product.save()

            # 修改订单状态为交易中
            order.buyer_openid = openid
            order.order_status = OrderStatus.ONGOING
            order.save()

            # 返回成功响应
            return JsonResponse({'message': '订单状态和商品状态已成功更新'}, status=200)

        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': '请求方法不支持'}, status=405)
