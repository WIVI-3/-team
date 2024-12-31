from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from myapp.models import User, History, Product

# 设置日志记录
logger = logging.getLogger(__name__)

@csrf_exempt  # 禁用CSRF验证（开发时使用，生产环境应启用并处理）
def get_history(request):
    if request.method == 'POST':
        try:
            logger.debug('Received request body: %s', request.body)  # Log raw request body

            # 解析请求体
            body = json.loads(request.body)
            openid = body.get('openid')  # 获取用户的 openid
            logger.debug('Extracted openid: %s', openid)  # Log the extracted openid

            # 检查是否提供了 openid
            if not openid:
                logger.warning('Missing openid in request body')  # Log warning if openid is missing
                return JsonResponse({'error': 'openid is required'}, status=400)

            try:
                # 查找用户是否存在
                user = User.objects.get(openid=openid)
                logger.debug('Found user: %s', user)  # Log the user object
            except User.DoesNotExist:
                # 如果用户不存在，返回 404 错误
                logger.error(f'User with openid {openid} does not exist')  # Log error when user is not found
                return JsonResponse({'error': 'User not found'}, status=404)

            # 获取用户浏览的历史商品
            history_items = History.objects.filter(user=user).order_by('-viewed_at')
            logger.debug('Found %d history items for user %s', history_items.count(), openid)  # Log number of history items

            # 如果没有浏览历史，返回空列表
            if not history_items:
                logger.info('No history found for user %s', openid)  # Log info if no history is found
                return JsonResponse({'message': 'No history found'}, status=200)

            # 构造商品数据
            history_products = []
            for history in history_items:
                try:
                    product = history.product  # 获取浏览的商品
                    logger.debug('Processing product: %s', product)  # Log each product being processed

                    # 构造每个商品的数据，按照需求只返回名称、价格、图片和租赁周期
                    product_data = {
                        'name': product.name,
                        'price': str(product.price),  # 将价格转换为字符串
                        'images': product.images,  # 商品图片
                        'rental_period': product.rental_period  # 租赁周期
                    }
                    history_products.append(product_data)
                except Product.DoesNotExist:
                    # 如果对应商品不存在，跳过该记录并继续处理下一个
                    logger.warning(f"Product for history item {history.id} does not exist. Skipping.")  # Log missing product
                    continue  # 跳过当前历史记录

            # 返回浏览历史商品的 JSON 响应
            logger.debug('Returning %d history products', len(history_products))  # Log number of products being returned
            return JsonResponse({'history': history_products}, safe=False, status=200)

        except json.JSONDecodeError as e:
            # 如果请求体不是有效的 JSON 数据
            logger.error('Invalid JSON data: %s', e)  # Log the JSON decode error
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            # 捕获其他异常并记录
            logger.error(f'Unexpected error occurred: {str(e)}')  # Log unexpected errors
            return JsonResponse({'error': 'An error occurred'}, status=500)

    else:
        # 如果不是 POST 请求
        logger.warning('Invalid HTTP method used: %s', request.method)  # Log invalid HTTP method
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
