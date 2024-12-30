from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from myapp.models import User

logger = logging.getLogger(__name__)

@csrf_exempt  # 禁用CSRF验证（开发时使用，生产环境应启用并处理）
def get_user_info(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)  # 解析请求体
            openid = body.get('openid')  # 获取用户的 openid

            if not openid:
                return JsonResponse({'error': 'openid is required'}, status=400)

            # 查找用户是否存在
            user = User.objects.get(openid=openid)

            # 构造用户数据
            user_data = {
                'user_id': user.user_id,
                'openid': user.openid,
                'wechat_id': user.wechat_id if user.wechat_id else 'Not set',
                'username': user.username,
                'email': user.email if user.email else 'Not set',
                'phone': user.phone if user.phone else 'Not set',
                'address': user.address if user.address else 'Not set',
                'profile_picture': user.profile_picture.url if user.profile_picture else 'No profile picture',
            }

            # 返回用户数据的 JSON 响应
            return JsonResponse({'user_info': user_data}, status=200)

        except User.DoesNotExist:
            # 如果找不到用户，返回 404 错误
            logger.error(f'User with openid {openid} does not exist')
            return JsonResponse({'error': 'User not found'}, status=404)
        except json.JSONDecodeError:
            # 如果请求体不是有效的 JSON 数据
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            # 捕获其他异常并记录
            logger.error(f'Error: {str(e)}')
            return JsonResponse({'error': 'An error occurred'}, status=500)

    else:
        # 如果不是 POST 请求
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
