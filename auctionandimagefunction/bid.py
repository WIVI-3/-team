from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Order, Product
import json

@csrf_exempt
def bid(request):
    if request.method == 'POST':
        try:
            # 解析请求数据
            data = json.loads(request.body)
            print("请求数据:", data)  # 打印请求体，便于调试

            buyer_openid = data.get('buyer_openid')
            product_id = data.get('product_id')
            bid_price = data.get('bid_price')

            # 检查参数是否有效
            if not buyer_openid or not product_id or not bid_price:
                return JsonResponse({'success': False, 'message': '缺少必要的参数'}, status=400)

            # 查找商品
            product = Product.objects.filter(product_id=product_id).first()
            print(f"查询到的商品: {product}")  # 打印商品信息，便于调试
            if not product:
                return JsonResponse({'success': False, 'message': '商品不存在'}, status=404)

            # 查询与该商品关联的所有订单，并找出当前正在进行的订单
            order = Order.objects.filter(product_id=product_id, order_status='交易中').first()
            print(f"商品 {product.name} 关联的订单: {order}")  # 打印查询到的订单信息，便于调试

            if not order:
                return JsonResponse({'success': False, 'message': '商品尚未拍卖'}, status=400)

            # 检查是否为同一买家出价
            if order.buyer_openid == buyer_openid:
                return JsonResponse({'success': False, 'message': '您已经是当前的买家，不能再次出价'}, status=400)

            # 检查用户出价是否有效（出价必须高于当前最高价）
            if float(bid_price) <= float(order.transaction_price):
                return JsonResponse({'success': False, 'message': '出价必须高于当前最高价'}, status=400)

            # 更新订单的价格和买家
            order.transaction_price = float(bid_price)
            order.buyer_openid = buyer_openid
            order.save()

            return JsonResponse({'success': True, 'message': '出价成功', 'new_transaction_price': bid_price})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '请求体格式错误'}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'出价失败: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': '仅支持POST请求'}, status=405)

