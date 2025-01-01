from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from myapp.models import Order, User, Product

logger = logging.getLogger(__name__)

@csrf_exempt  # 禁用CSRF验证（开发时使用，生产环境应启用并处理）
def get_user_orders(request):
    if request.method == 'POST':
        try:
            # 获取前端传递的 JSON 数据
            body = json.loads(request.body)
            openid = body.get('openid')  # 获取传递的 openid
            category1 = body.get('category1')  # 获取传递的 category1

            if not openid:
                return JsonResponse({'error': 'openid is required'}, status=400)

            # 查询该用户作为买家的所有订单
            buyer_orders = Order.objects.filter(buyer_openid=openid).select_related('product__user')

            # 如果传递了 category1 参数，进行筛选
            if category1:
                buyer_orders = buyer_orders.filter(product__category1=category1)

            # 如果该用户没有订单，返回空的订单列表
            if not buyer_orders.exists():
                return JsonResponse({'message': '没有找到该用户的订单'}, status=200)

            order_list = []

            # 处理买家订单
            for order in buyer_orders:
                product = order.product
                seller = product.user  # 获取商品的卖家信息
                buyer = User.objects.filter(openid=order.buyer_openid).first()  # 获取买家信息
                if not seller:
                    logger.error(f"Seller for product {product.product_id} not found.")
                    continue  # 如果找不到卖家信息，跳过该订单
                order_data = {
                    'type': 'buyer',  # 标记为买家订单
                    'buyer': {
                        'username': buyer.username,  # 买家用户名
                        'phone': buyer.phone,  # 买家联系电话
                        'address': buyer.address,  # 买家地址
                        'profile_picture': buyer.profile_picture.url if buyer.profile_picture else None  # 买家头像
                    },
                    'order_id': order.order_id,
                    'product_id': product.product_id,
                    'category1': product.category1,
                    'product_name': product.name,
                    'product_images': product.images,
                    'transaction_price': str(order.transaction_price),  # 交易价格
                    'order_status': order.get_order_status_display(),  # 获取订单状态的可读值
                    'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化时间
                    'rental_period': str(order.rental_period) if order.rental_period else None,  # 租期（如果有）
                    'seller': {
                        'username': seller.username,  # 卖家用户名
                        'phone': seller.phone,  # 卖家联系电话
                        'address': seller.address,  # 卖家地址
                        'profile_picture': seller.profile_picture.url if seller.profile_picture else None  # 卖家头像
                    }
                }
                order_list.append(order_data)

            # 返回所有买家订单
            return JsonResponse({'orders': order_list}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
