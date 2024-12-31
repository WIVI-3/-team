from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.views.decorators.csrf import csrf_exempt
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings


@csrf_exempt  # 禁用 CSRF 验证
def upload_images(request):
    if request.method == 'POST' and request.FILES.get('file'):
        # 获取上传的文件
        uploaded_file = request.FILES['file']

        # 选择文件存储路径
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))

        # 保存文件，使用原始文件名
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)  # 获取文件的 URL 地址

        return JsonResponse({'file_url': file_url}, status=200)

    return JsonResponse({'error': 'No file uploaded'}, status=400)