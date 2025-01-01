from django import forms
from myapp.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'wechat_id', 'email', 'phone', 'address', 'profile_picture']  # 排除 user_openid 和 user_id
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    # 重写 clean 方法以防止修改 user_openid 和 user_id
    def clean(self):
        cleaned_data = super().clean()
        user_openid = cleaned_data.get('user_openid')
        user_id = cleaned_data.get('user_id')

        if user_openid or user_id:
            raise forms.ValidationError("您不能修改微信的唯一标识号或用户ID")

        return cleaned_data
