from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from myapp.models import Product, Category1, ProductStatus

@csrf_exempt  # 禁用CSRF验证（开发时使用，生产环境应启用并处理）
def rental_search(request):
    if request.method == 'POST':
        try:
            # 获取前端传来的关键词
            body = json.loads(request.body)  # 解析请求体
            keyword = body.get('keyword', '').strip()  # 获取关键词并去除空格

            if not keyword:
                return JsonResponse({'error': 'Keyword is required'}, status=400)

            # 筛选出 category1 为 '租赁' 且商品状态为 'LIST' 的商品
            products = Product.objects.filter(
                category1=Category1.RENTAL,
                product_status=ProductStatus.LIST  # 只查询上架中状态的商品
            )

            # 再进行商品名称的模糊匹配
            products = products.filter(name__icontains=keyword)  # `icontains` 用于不区分大小写的模糊匹配

            # 将查询结果转换为字典列表
            product_list = []
            for product in products:
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
                    'category1': product.category1,
                    'category2': product.category2,
                    'rental_period': product.rental_period,  # 添加租赁周期字段
                    'images': image_urls  # 存储去掉 /media/ 前缀后的图片路径
                }
                product_list.append(product_data)

            # 返回匹配的商品列表
            return JsonResponse({'products': product_list}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
