import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import User, Product, Favorite

@csrf_exempt
def remove_from_favorites(request):
    """
    从收藏夹中移除商品
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            openid = data.get('openid')
            product_id = data.get('product_id')

            # 查找用户和商品
            user = User.objects.get(openid=openid)
            product = Product.objects.get(product_id=product_id)

            # 查找用户是否已经收藏了这个商品
            favorite = Favorite.objects.filter(user=user, product=product).first()

            if not favorite:
                return JsonResponse({'success': False, 'message': '该商品不在收藏夹中'}, status=400)

            # 删除收藏
            favorite.delete()

            return JsonResponse({'success': True, 'message': '商品已从收藏夹移除'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': '商品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'发生错误: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': '仅支持 POST 请求'}, status=400)
