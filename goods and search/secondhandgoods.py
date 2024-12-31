from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from myapp.models import Product, Category1, ProductStatus

@csrf_exempt
def secondhand_goods(request):
    if request.method == 'GET':
        try:
            # 查询所有 category1 为 'SECOND_HAND' 且商品状态为 'LIST' 的商品
            secondhand_products = Product.objects.filter(
                category1=Category1.SECOND_HAND,
                product_status=ProductStatus.LIST  # 确保返回的商品是上架中状态
            )

            # 将查询结果转换为字典列表，并去掉 images 中的 /media/ 前缀
            product_list = []
            for product in secondhand_products:
                # 获取商品的图片路径列表
                image_urls = []
                for image_path in product.images:
                    # 去掉 /media/ 前缀
                    image_url = image_path.replace('/media/', '')
                    image_urls.append(image_url)

                # 创建一个商品字典，并加入修改后的图片路径
                product_data = {
                    'product_id': product.product_id,
                    'name': product.name,
                    'price': str(product.price),  # 将价格转换为字符串，避免浮动精度问题
                    'description': product.description,
                    'address': product.address,
                    'phone': product.phone,
                    'images': image_urls  # 存储去掉 /media/ 前缀后的图片路径
                }
                product_list.append(product_data)

            return JsonResponse({'products': product_list}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # 如果不是 GET 请求，返回方法不允许
    return JsonResponse({'error': 'Method not allowed'}, status=405)
