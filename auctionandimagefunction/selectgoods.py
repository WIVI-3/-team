from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from myapp.models import Product, User

logger = logging.getLogger(__name__)
@csrf_exempt  # 禁用CSRF验证（开发时使用，生产环境应启用并处理）
def select_goods(request):
    if request.method == 'POST':
        # 获取前端传递的 product_id 参数
        try:
            body = json.loads(request.body)  # 解析请求体
            product_id = body.get('product_id')  # 获取 product_id

            if not product_id:
                return JsonResponse({'error': 'product_id is required'}, status=400)

            # 查询商品信息
            product = Product.objects.get(product_id=product_id)
            seller_name = product.user.username if product.user else 'Unknown Seller'
            seller_openid = product.user.openid if product.user else 'Unknown Seller'

            image_urls = []
            for image_path in product.images:
                    # 去掉 /media/ 前缀
                    image_url = image_path.replace('/media/', '')
                    image_urls.append(image_url)

            # 将商品数据打包成字典并返回
            product_data = {
                'product_id': product.product_id,
                'name': product.name,
                'price': str(product.price),  # 将价格转换为字符串
                'description': product.description,
                'phone': product.phone,
                'address': product.address,
                'images': image_urls,  # 商品图片
                'provide_service': product.provide_service,
                'rental_period': product.rental_period,
                'seller_name': seller_name,  # 卖家的用户名
                'seller_openid': seller_openid,
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