from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from myapp.models import User, Favorite, Product

logger = logging.getLogger(__name__)

@csrf_exempt  # 禁用CSRF验证（开发时使用，生产环境应启用并处理）
def get_favorites(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)  # 解析请求体
            openid = body.get('openid')  # 获取用户的 openid
            logger.debug(f'OpenID: {openid}')
            if not openid:
                return JsonResponse({'error': 'openid is required'}, status=400)



            # 查找用户是否存在
            user = User.objects.get(openid=openid)

            # 获取用户收藏的商品
            favorites = Favorite.objects.filter(user=user)

            # 如果没有收藏商品，返回空列表
            if not favorites:
                return JsonResponse({'message': 'No favorites found'}, status=200)

            # 构造商品数据
            favorite_products = []
            for favorite in favorites:
                product = favorite.product  # 获取收藏的商品
                product_data = {
                    'product_id': product.product_id,
                    'name': product.name,
                    'price': str(product.price),  # 将价格转换为字符串
                    'description': product.description,
                    'phone': product.phone,
                    'address': product.address,
                    'images': product.images,  # 商品图片
                    'provide_service': product.provide_service,
                    'rental_period': product.rental_period,
                }
                favorite_products.append(product_data)

            # 返回收藏夹商品的 JSON 响应
            return JsonResponse({'favorites': favorite_products}, safe=False, status=200)

        except User.DoesNotExist:
            # 如果找不到用户，返回 404 错误
            logger.error(f'User with openid {openid} does not exist')
            return JsonResponse({'error': 'User not found'}, status=404)
        except json.JSONDecodeError:
            # 如果请求体不是有效的 JSON 数据
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            # 捕获其他异常并记录
            logger.error(f'Error: {str(e)}')
            return JsonResponse({'error': 'An error occurred'}, status=500)

    else:
        # 如果不是 POST 请求
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
