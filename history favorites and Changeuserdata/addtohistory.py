from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from myapp.models import User, Product, History

@csrf_exempt  # 禁用CSRF验证（开发时使用，生产环境应启用并处理）
def add_to_history(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)  # 解析请求体
            openid = body.get('openid')  # 获取用户的 openid
            product_id = body.get('product_id')  # 获取商品的 product_id

            if not openid or not product_id:
                return JsonResponse({'error': 'openid and product_id are required'}, status=400)

            # 查找用户和商品
            user = User.objects.get(openid=openid)
            product = Product.objects.get(product_id=product_id)

            # 查询是否已经有该商品的历史记录
            existing_history = History.objects.filter(user=user, product=product).first()

            if existing_history:
                # 如果存在历史记录，更新（或者删除再创建）
                existing_history.delete()  # 删除旧记录
                # 重新创建新的历史记录
                History.objects.create(user=user, product=product)

                return JsonResponse({'success': True, 'message': '历史浏览记录已更新'}, status=200)
            else:
                # 如果没有历史记录，直接创建新的记录
                History.objects.create(user=user, product=product)
                return JsonResponse({'success': True, 'message': '历史浏览记录添加成功'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
