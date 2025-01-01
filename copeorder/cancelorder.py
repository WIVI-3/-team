from django.shortcuts import get_object_or_404
from myapp.models import Product, Order, ProductStatus, OrderStatus
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def cancel_order(request):
    if request.method == 'POST':
        try:
            # 解析请求体中的JSON数据
            data = json.loads(request.body)

            # 获取传递的 order_id和buyer_openid
            order_id = data.get('order_id')
            buyer_openid = data.get('buyer_openid')

            # 检查参数是否传递完整
            if not order_id or not buyer_openid:
                return JsonResponse({'message': '缺少参数: order_id 或 buyer_openid'}, status=400)

            # 获取对应的商品对象，如果商品不存在则返回 404 错误
            order = get_object_or_404(Order, order_id=order_id)

            # 检查交易是否处于交易中
            if order.order_status != OrderStatus.ONGOING:
                return JsonResponse({'message': ' 订单处于不可取消状态'}, status=400)

            #订单取消
            order.order_status = OrderStatus.FAIL
            order.save()

            # 商品重新上架
            product = order.product
            product.product_status = ProductStatus.LIST
            product.save()

            # 返回订单创建成功的响应
            return JsonResponse({
                'order_id': order.order_id,
                'message': '订单已取消'
            })

        except json.JSONDecodeError:
            # 如果请求体无法解析为 JSON，返回格式错误的响应
            return JsonResponse({'message': '请求体格式错误'}, status=400)

        except Exception as e:
            # 捕获其他异常并返回错误信息
            return JsonResponse({'message': str(e)}, status=500)
