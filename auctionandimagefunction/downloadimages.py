import json

from django.http import JsonResponse, HttpResponse
from django.conf import settings
import os
from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Product  # 替换为你的应用名称

@csrf_exempt  # 禁用 CSRF 验证
def download_image(request,image_name):
    # 图片存储的路径
    image_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image_name)

    # 检查图片是否存在
    if not os.path.exists(image_path):
        return JsonResponse({'error': 'File not found'}, status=404)

    # 构建图片的 URL
    image_url = f"{settings.MEDIA_URL}uploads/{image_name}"

    # 返回图片 URL
    return JsonResponse({'image_url': image_url})