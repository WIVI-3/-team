from django.shortcuts import get_object_or_404
from myapp.models import Product, Order, ProductStatus, OrderStatus
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_rental_order(request):
    if request.method == 'POST':
        try:
            # 解析请求体中的JSON数据
            data = json.loads(request.body)

            # 获取传递的 product_id、buyer_openid 和 rental_period
            product_id = data.get('product_id')
            buyer_openid = data.get('buyer_openid')
            rental_period = data.get('rental_period')  # 获取租期参数

            # 检查参数是否传递完整
            if not product_id or not buyer_openid or rental_period is None:
                return JsonResponse({'message': '缺少参数: product_id, buyer_openid 或 rental_period'}, status=400)

            # 将租期转换为整数类型
            try:
                rental_period = int(rental_period)
            except ValueError:
                return JsonResponse({'message': '租期必须是有效的数字'}, status=400)

            # 检查租期是否是有效数字
            if rental_period <= 0:
                return JsonResponse({'message': '租期必须是正整数'}, status=400)

            # 获取对应的商品对象，如果商品不存在则返回 404 错误
            product = get_object_or_404(Product, product_id=product_id)

            # 查找与该商品关联的正在进行中的订单
            existing_order = Order.objects.filter(product=product, order_status=OrderStatus.PUBLISH).first()

            if not existing_order:
                # 如果商品没有进行中的订单，返回错误
                return JsonResponse({'message': '没有找到进行中的订单'}, status=404)

            # 计算成交价（商品价格 * 租期）
            transaction_price = product.price * rental_period

            # 修改现有订单
            existing_order.buyer_openid = buyer_openid  # 更新买家openid
            existing_order.rental_period = rental_period  # 更新租期
            existing_order.order_status = OrderStatus.ONGOING  # 设置订单状态为交易中
            existing_order.transaction_price = transaction_price  # 更新成交价
            existing_order.save()

            # 修改商品状态为锁定
            product.product_status = ProductStatus.LOCK
            product.save()

            # 返回订单修改成功的响应
            return JsonResponse({
                'order_id': existing_order.order_id,
                'product_name': existing_order.product.name,
                'buyer_openid': existing_order.buyer_openid,
                'seller_openid': existing_order.product.user.openid,
                'rental_period': existing_order.rental_period,  # 返回租期信息
                'transaction_price': existing_order.transaction_price,  # 返回计算后的成交价
                'message': '订单修改成功'
            })

        except json.JSONDecodeError:
            # 如果请求体无法解析为 JSON，返回格式错误的响应
            return JsonResponse({'message': '请求体格式错误'}, status=400)

        except Exception as e:
            # 捕获其他异常并返回错误信息
            return JsonResponse({'message': str(e)}, status=500)
