from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from myapp.models import Product, Order

logger = logging.getLogger(__name__)

@csrf_exempt  # 禁用CSRF验证（开发时使用，生产环境应启用并处理）
def select_auction(request):
    if request.method == 'POST':
        try:
            # 获取前端传递的 JSON 数据
            body = json.loads(request.body)
            product_id = body.get('product_id')  # 获取传递的 product_id

            if not product_id:
                return JsonResponse({'error': 'product_id is required'}, status=400)

            # 获取商品信息
            product = get_object_or_404(Product, product_id=product_id)

            # 获取当前订单信息（可能存在多个订单，取最新的一个）
            order = Order.objects.filter(product=product).order_by('-created_at').first()

            if not order:
                return JsonResponse({'error': 'No order found for this product'}, status=404)

            # 将商品数据打包成字典并返回
            product_data = {
                'product_id': product.product_id,
                'transaction_price': order.transaction_price,  # 当前订单价格
                'auction_end_time': product.auction_end_time,  # 拍卖结束时间
            }

            # 返回 JSON 响应
            return JsonResponse(product_data, safe=False)

        except Product.DoesNotExist:
            # 如果找不到商品，返回 404 错误
            logger.error(f'Product with id {product_id} does not exist')
            return JsonResponse({'error': 'Product not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
