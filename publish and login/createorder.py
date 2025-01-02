from django.shortcuts import get_object_or_404
from myapp.models import Product, Order, ProductStatus, Category1, OrderStatus
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            # 解析请求体中的JSON数据
            data = json.loads(request.body)

            # 获取传递的 product_id 和 buyer_openid
            product_id = data.get('product_id')
            buyer_openid = data.get('buyer_openid')

            # 检查参数是否传递完整
            if not product_id or not buyer_openid:
                return JsonResponse({'message': '缺少参数: product_id 或 buyer_openid'}, status=400)

            # 获取对应的商品对象，如果商品不存在则返回 404 错误
            product = get_object_or_404(Product, product_id=product_id)
            if product.category1 == '拍卖':
                # 创建订单
                order = Order.objects.create(
                    buyer_openid=buyer_openid,
                    product=product,  # 关联商品
                    transaction_price=product.price,  # 订单成交价格
                )
            else: order = Order.objects.create(
                    product=product,  # 关联商品
                    transaction_price=product.price,  # 订单成交价格
                )



            # 设置商品状态和订单状态
            if product.category1 == Category1.AUCTION:
                # 对于拍卖类商品，订单状态为 交易中 (ONGOING)
                product.product_status = ProductStatus.LIST  # 拍卖商品上架
                order.order_status = OrderStatus.ONGOING  # 订单状态为进行中
            else:
                # 对于二手商品，订单状态为 已发布 (PUBLISH)
                product.product_status = ProductStatus.LIST  # 商品上架
                order.order_status = OrderStatus.PUBLISH  # 订单状态为已发布

            # 保存商品和订单的状态
            product.save()
            order.save()

            # 返回订单创建成功的响应
            return JsonResponse({
                'order_id': order.order_id,
                'product_name': order.product.name,
                'buyer_openid': order.buyer_openid,
                'seller_openid': order.product.user.openid,
                'rental_period': order.rental_period,  # 返回租期信息
                'message': '订单创建成功'
            })

        except json.JSONDecodeError:
            # 如果请求体无法解析为 JSON，返回格式错误的响应
            return JsonResponse({'message': '请求体格式错误'}, status=400)

        except Exception as e:
            # 捕获其他异常并返回错误信息
            return JsonResponse({'message': str(e)}, status=500)
