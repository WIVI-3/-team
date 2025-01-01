from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from myapp.models import Product, User, Category1, ProductStatus, Order

logger = logging.getLogger(__name__)


@csrf_exempt  # 禁用CSRF验证（开发时使用，生产环境应启用并处理）
def delete_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 解析请求体中的JSON数据
            product_id = data['product_id']
            # 日志：查看接收到的数据
            logger.info(f"Received data: {data}")

            # 获取商品对象
            product = Product.objects.get(product_id=product_id)

            # 检查商品是否已发布，且可以删除
            if product.product_status == ProductStatus.LIST:
                # 删除与该商品关联的订单
                orders = Order.objects.filter(product=product)
                if orders.exists():
                    # 如果有相关订单，先删除订单
                    orders.delete()
                    logger.info(f"Deleted orders for product {product_id}")

                # 删除商品本身
                product.delete()
                logger.info(f"Deleted product {product_id}")
                return JsonResponse({'message': '成功删除商品及相关订单'}, status=200)
            else:
                return JsonResponse({'message': '当前状态不能删除'}, status=400)

        except Product.DoesNotExist:
            logger.error(f"Product with ID {product_id} does not exist.")
            return JsonResponse({'success': False, 'message': '商品不存在'}, status=404)

        except Exception as e:
            logger.error(f"Error in product deletion: {str(e)}")
            return JsonResponse({'success': False, 'message': f"删除失败: {str(e)}"})

    return JsonResponse({'success': False, 'message': '仅支持POST请求'})
