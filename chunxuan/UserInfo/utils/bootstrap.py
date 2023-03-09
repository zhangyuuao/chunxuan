from django import forms
class BootStrapModelForm(forms.ModelForm) :
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items() :
            
            # 设置表单项里的标签
            # 字段中有属性则添加，不能直接覆盖
            if field.widget.attrs :
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else : 
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                    }
            