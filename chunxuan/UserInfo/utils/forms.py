from dataclasses import fields
from UserInfo.models import UserInfo, aitest
from django.core.exceptions import ValidationError
from UserInfo.utils.encrypt import md5
from UserInfo.utils.bootstrap import BootStrapModelForm
from django import forms

class UserLogin(BootStrapModelForm) :
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items() :
            
            # 设置表单项里的标签
            # 字段中有属性则添加，不能直接覆盖
            if field.widget.attrs :
                field.widget.attrs["class"] = "form-control rounded-4"
                field.widget.attrs["placeholder"] = field.label
            else : 
                field.widget.attrs = {
                    "class": "",
                    "placeholder": field.label
                    }
    class Meta :
        model = UserInfo
        fields = ["username", "password"]
        widgets = {
            "name": forms.TextInput(),
            "password": forms.PasswordInput,
        }
        
    
    def clean_password (self) :
        pwd = self.cleaned_data.get("password")
        return md5(pwd)
        
    
class Register(BootStrapModelForm) :
    
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput
    )
    
    class Meta :
        model = UserInfo
        exclude = ['age']
        
        widgets = {
            "password": forms.PasswordInput(render_value = True)
        }
        
    def clean_password (self) :
        pwd = self.cleaned_data.get("password")
        return md5(pwd)
    
    def clean_confirm_password (self) :
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm :
            raise ValidationError("两次密码不一致！")
        
        # 返回的是最终保存的密码
        return confirm
    
class myInfo(BootStrapModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items() :
            
    #         # 设置表单项里的标签
    #         # 字段中有属性则添加，不能直接覆盖
    #         if name == "birthday" or name == "age" or name =="username" :
    #             field.widget.attrs["disabled"]="disabled"
    
    birthday = forms.DateField(disabled=False, label="出生日期")
    age = forms.IntegerField(disabled=True, label="年龄")
    
    class Meta:
        model = UserInfo
        exclude = ["password"]
        
class testInfo(BootStrapModelForm):
    def __init__(self, username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items() :
            if name == "username":
                field.widget.attrs["value"] = username
                
    class Meta:
        model = aitest
        exclude = ["test_time"]
    