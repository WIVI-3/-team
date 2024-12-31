from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from myapp.models import User

@csrf_exempt  # 禁用 CSRF 验证
def change_user_data(request):
    """
    修改用户个人信息，使用 openid 查找用户并更新，但不能修改 openid。
    """
    if request.method == 'POST':
        try:
            # 获取前端传来的数据
            data = json.loads(request.body)

            # 获取 openid 和要更新的用户信息
            openid = data.get('openid')  # 获取用户的 openid
            if not openid:
                return JsonResponse({'success': False, 'message': 'openid 不能为空'})

            # 查找用户，确保用户存在
            user = User.objects.filter(openid=openid).first()
            if not user:
                return JsonResponse({'success': False, 'message': '用户不存在'})


            # 获取要更新的字段
            username = data.get('username', user.username)
            email = data.get('email', user.email)
            phone = data.get('phone', user.phone)
            address = data.get('address', user.address)
            wechat_id = data.get('wechat_id', user.wechat_id)  # 更新微信号
            profile_picture = data.get('profile_picture', user.profile_picture)

            if email and User.objects.filter(email=email).exclude(openid=openid).exists():
                return JsonResponse({'success': False, 'message': '该邮箱已经被其他用户使用'})

            # 更新用户数据
            user.username = username
            user.email = email
            user.phone = phone
            user.address = address
            user.wechat_id = wechat_id  # 更新微信号
            if profile_picture:  # 如果有新的头像图片，则更新
                user.profile_picture = profile_picture

            # 保存更新后的用户信息
            user.save()

            # 返回成功响应
            return JsonResponse({
                "success": True,
                "message": "用户数据更新成功",
                "user_id": user.user_id,
                "nick_name": user.username,
                "avatar_url": user.profile_picture.url if user.profile_picture else None,  # 返回头像 URL
                "wechat_id": user.wechat_id  # 返回更新后的微信号
            }, status=200)

        except Exception as e:
            print(f"Error: {str(e)}")  # 打印错误日志
            # 捕获异常并返回错误信息
            return JsonResponse({
                "success": False,
                "message": f"发生错误: {str(e)}"
            }, status=500)

    else:
        # 如果不是 POST 请求，返回错误
        return JsonResponse({
            "success": False,
            "message": "只支持 POST 请求"
        }, status=400)

