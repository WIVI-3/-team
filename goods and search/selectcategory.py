from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Product, ProductStatus
import json

@csrf_exempt
def select_category(request):
    if request.method == 'POST':
        try:
            # 解析前端传入的json数据
            body = json.loads(request.body)
            category1 = body.get('category1')
            category2 = body.get('category2')

            if not category1 or not category2:
                return JsonResponse({"message": "category1 and category2 are required."}, status=400)

            # 根据传入的category1和category2筛选商品
            products = Product.objects.filter(category1=category1, category2=category2, product_status=ProductStatus.LIST)

            product_list = []
            for product in products:
                image_urls = []
                for image_path in product.images:
                     # 去掉 /media/ 前缀
                    image_url = image_path.replace('/media/', '')
                    image_urls.append(image_url)

                product_info = {
                    'product_id': product.product_id,
                    'name': product.name,
                    'price': str(product.price),  # 转换为字符串以避免精度丢失
                    'description': product.description,
                    'phone': product.phone,
                    'address': product.address,
                    'images': image_urls,
                    'provide_service': product.provide_service,
                    'rental_period': product.rental_period,
                    'created_at': product.created_at.isoformat(),
                    'updated_at': product.updated_at.isoformat(),
                    'product_status': product.product_status,
                }
                product_list.append(product_info)

            # 返回筛选后的商品信息
            return JsonResponse({"products": product_list}, status=200)

        except Exception as e:
            # 发生异常时返回错误信息
            return JsonResponse({"error": str(e)}, status=500)
