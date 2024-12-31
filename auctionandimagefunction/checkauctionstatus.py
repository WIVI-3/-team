from django.conf import settings
from django.utils import timezone
from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from myapp.models import Product, ProductStatus

logger = logging.getLogger(__name__)


@csrf_exempt  # 禁用CSRF验证（开发时使用，生产环境应启用并处理）
def check_auction_status(request):
    if request.method == 'POST':
        try:
            # 解析请求体中的JSON数据
            data = json.loads(request.body)

            # 获取前端传递的商品 ID
            product_id = data.get('product_id')  # 获取前端传递的商品 ID

            if not product_id:
                return JsonResponse({"success": False, "message": "缺少商品ID参数"})

            # 获取传递的商品 ID
            try:
                product = Product.objects.get(product_id=product_id, category1='拍卖',
                                              product_status=ProductStatus.LIST)
            except Product.DoesNotExist:
                return JsonResponse({"success": False, "message": "商品未找到或不符合条件"})

            # 打印商品的拍卖结束时间，便于调试
            logger.info(f"Checking product: {product.name}, Auction end time: {product.auction_end_time}")

            # 如果拍卖时间已过，将商品状态更新为锁定
            product.product_status = ProductStatus.LOCK
            product.save()

            logger.info(f"Product {product.name} (ID: {product.product_id}) has been locked due to auction end time.")
            return JsonResponse({"success": True, "message": f"商品 {product.name} 已被锁定"})

        except Exception as e:
            logger.error(f"Error in check_auction_status: {e}")
            return JsonResponse({"success": False, "message": f"操作失败: {str(e)}"})

    return JsonResponse({'success': False, 'message': '仅支持POST请求'})
