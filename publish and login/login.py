from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from myapp.models import User

# 微信小程序的 appid 和 secret
APPID = 'wx10f46e398d58b5b5'  # 替换为你的 appid
SECRET = 'bd837f7cb3f9215e7853edcea3a8472b'  # 替换为你的 secret
@csrf_exempt  # 禁用 CSRF 验证
def wechat_login(request):
    if request.method == 'POST':
        try:
            # 获取前端传来的 code，nickname 和 avatarUrl
            data = json.loads(request.body)
            code = data.get('code')  # 小程序登录 code
            nick_name = data.get('nickName')  # 用户昵称
            avatar_url = data.get('avatarUrl')  # 用户头像

            # 如果没有收到 code，则返回错误
            if not code:
                return JsonResponse({'success': False, 'message': 'code 不能为空'})

            # 请求微信服务器进行用户身份认证
            url = f'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={code}&grant_type=authorization_code'
            response = requests.get(url)
            result = response.json()

            # 如果返回结果包含 openid 和 session_key，说明认证成功
            if 'openid' in result:
                openid = result['openid']
                session_key = result['session_key']

                # 打印获取到的 openid 和 session_key
                print(f"Received openid: {openid}")
                print(f"Received session_key: {session_key}")

                # 查找是否已有该用户
                user = User.objects.filter(openid=openid).first()
                if user:
                # 如果不需要创建用户，可以在此阶段结束，返回成功响应
                    return JsonResponse({
                    'success': True,
                    'message': '登录成功',
                    'openid': openid,  # 返回 openid 作为示例
                    'session_key': session_key, # 返回 session_key 作为示例
                    'user_id': user.user_id,  # 返回用户 ID
                    'nick_name': user.username,  # 返回用户名
                    'avatar_url': user.profile_picture.url if user.profile_picture else None, # 返回头像URL
                    'wechat_id':user.wechat_id,
                    'email': user.email,
                    'phone': user.phone,
                    'address': user.address,
                })
                else:
                    # 如果用户不存在，则创建新用户
                    user = User.objects.create(
                        openid=openid,
                        username=nick_name,
                        profile_picture=avatar_url  # 存储头像 URL
                    )
                    # 返回新创建用户的登录信息
                    return JsonResponse({
                        'success': True,
                        'message': '注册并登录成功',
                        'openid': openid,
                        'session_key': session_key,
                        'user_id': user.user_id,  # 返回新用户 ID
                        'nick_name': user.username,  # 返回用户名
                        'avatar_url': user.profile_picture.url if user.profile_picture else None,  # 返回头像URL
                        'wechat_id': user.wechat_id,
                        'email': user.email,
                        'phone': user.phone,
                        'address': user.address,
                    })


            else:
                # 如果没有获取到 openid，则返回错误信息
                return JsonResponse({'success': False, 'message': '微信登录失败，code 无效'})

        except Exception as e:
            # 捕获异常并返回错误信息
            return JsonResponse({'success': False, 'message': f'登录失败，错误信息: {str(e)}'})

    # 如果不是 POST 请求，返回错误
    return JsonResponse({'success': False, 'message': '仅支持 POST 请求'})