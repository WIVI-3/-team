import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import User, Product, Favorite

@csrf_exempt
def add_to_favorites(request):
    """
    将商品添加到用户的收藏夹
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            openid = data.get('openid')
            product_id = data.get('product_id')

            # 查找用户和商品
            user = User.objects.get(openid=openid)
            product = Product.objects.get(product_id=product_id)

            # 检查用户是否已经收藏了这个商品
            if Favorite.objects.filter(user=user, product=product).exists():
                return JsonResponse({'success': False, 'message': '该商品已在收藏夹中'}, status=400)

            # 添加到收藏夹
            Favorite.objects.create(user=user, product=product)

            return JsonResponse({'success': True, 'message': '商品已添加到收藏夹'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': '商品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'发生错误: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': '仅支持 POST 请求'}, status=400)
