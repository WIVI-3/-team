from django.shortcuts import get_object_or_404
from myapp.models import Product, Order, ProductStatus, OrderStatus
from django.http import JsonResponse, Http404
import json
from django.views.decorators.csrf import csrf_exempt
import logging
logger = logging.getLogger(__name__)


@csrf_exempt
def get_goods(request):
    if request.method == 'POST':
        try:
            # 记录原始请求体数据用于调试
            logger.info(f"Request body: {request.body.decode('utf-8')}")

            # 解析请求体中的JSON数据
            data = json.loads(request.body)
            logger.info(f"Received data: {data}")

            # 获取 order_id 和 buyer_openid
            order_id = data.get('order_id')
            buyer_openid = data.get('buyer_openid')

            # 检查参数是否缺失
            if not order_id or not buyer_openid:
                return JsonResponse({'message': '缺少参数: order_id 或 buyer_openid'}, status=400)

            # 尝试获取订单，捕获 404 错误
            try:
                order = get_object_or_404(Order, order_id=order_id)
            except Http404:
                logger.error(f"Order with id {order_id} not found.")
                return JsonResponse({'message': '订单未找到'}, status=404)

            logger.info(f"Found order: {order}")

            # 检查订单状态是否为 ONGOING
            if order.order_status != OrderStatus.ONGOING:
                return JsonResponse({'message': '该订单处于不可收货状态'}, status=400)

            # 更新订单状态
            order.order_status = OrderStatus.RECEIVE
            order.save()
            logger.info(f"Order status updated: {order}")

            return JsonResponse({
                'order_id': order.order_id,
                'message': '已收货'
            })

        except json.JSONDecodeError:
            logger.error("JSON decoding error")
            return JsonResponse({'message': '请求体格式错误'}, status=400)

        except Exception as e:
            logger.error(f"Error: {e}")
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': '仅支持 POST 请求'}, status=405)

