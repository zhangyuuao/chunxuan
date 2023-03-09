from django.db import models

# Create your models here.
class UserInfo (models.Model) :
    
    username = models.CharField(verbose_name="用户名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)

    email = models.EmailField(verbose_name="邮箱", max_length=32, blank=True)
    mobile = models.CharField(verbose_name="电话号码", max_length=11, blank=True)
    
    birthday = models.DateField(verbose_name="出生日期")
    age = models.IntegerField(verbose_name="年龄")
    
    gender_choices = (
        (1, "男"),
        (0, "女")
    )
    
    education_choices = (
        (1, "未上过学"),
        (2, "小学"),
        (3, "初中"),
        (4, "高中"),
        (5, "大学及以上"),
    )
    
    reside_choices = (
        (1, "独居"),
        (2, "双老居住"),
        (3, "子女同住"),
        (4, "农村幸福互助院"),
        (5, "其他养老机构"),
    )
    
    labour_choices = (
        (1, "仍工作/干农活"),
        (0, "不工作/不干农活")
    )
    
    health_choices = (
        (1, "自理"),
        (2, "半自理"),
        (3, "失能")
    )
    
    mainlife_choices = (
        (1, "养老金"),
        (2, "子女赡养"),
        (3, "社会救助"),
        (4, "劳动收入"),
        (5, "其他"),
    )
    
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    education = models.SmallIntegerField(verbose_name="文化程度", choices=education_choices)
    reside = models.SmallIntegerField(verbose_name="居住情况", choices=reside_choices)
    labour = models.SmallIntegerField(verbose_name="劳动情况", choices=labour_choices)
    health = models.SmallIntegerField(verbose_name="健康状况", choices=health_choices)
    life = models.SmallIntegerField(verbose_name="主要生活来源", choices=mainlife_choices)
    # connected_person = models.ForeignKey(to="UserInfo", to_field="user_name")

# class test1(models.Model):
#     date = models.DateTimeField()
#     score1 = models.DecimalField()
#     score2 = models.DecimalField()
#     score3 = models.DecimalField()
#     score4 = models.DecimalField()
    
#     risk_choices = (
#         (1, "健康"),
#         (2, "可能患病"),
#         (3, "轻度患病风险"),
#         (4, "中度患病风险"),
#         (5, "重度患病风险")
#     )
    
#     risk = models.SmallAutoField(verbose_name="患病风险", choices = risk_choices)

class aitest(models.Model):
    
    username = models.CharField(verbose_name="用户名", max_length=16)
    
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    
    test_time = models.DateTimeField(verbose_name="测试时间")

    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    height = models.IntegerField(verbose_name="身高")
    weight = models.DecimalField(verbose_name="体重", max_digits=10, decimal_places = 2)
    birthyear = models.IntegerField("出生年份")
    hosipital_year = models.DecimalField("去医院时间（填年份）", max_digits=10, decimal_places = 4)
    sleep = models.DecimalField("平均睡眠时间", max_digits=10, decimal_places=2)
    work = models.DecimalField("平均活动时间", max_digits=10, decimal_places=2)
    emotion = models.DecimalField("近日心情（0-100整数）", max_digits=10, decimal_places=2)
    emo_times = models.DecimalField("近一年内情绪失控次数", max_digits=10, decimal_places=2)
    
    education_choices = (
        (1, "未上过学"),
        (2, "小学"),
        (3, "初中"),
        (4, "高中"),
        (5, "大学及以上"),
    )
    
    reside_choices = (
        (1, "独居"),
        (2, "双老居住"),
        (3, "子女同住"),
        (4, "农村幸福互助院"),
        (5, "其他养老机构"),
    )
    
    mainlife_choices = (
        (1, "养老金"),
        (2, "子女赡养"),
        (3, "社会救助"),
        (4, "劳动收入"),
        (5, "其他"),
    )
    
    education = models.SmallIntegerField(verbose_name="文化程度", choices=education_choices)
    reside = models.SmallIntegerField(verbose_name="居住情况", choices=reside_choices)
    life = models.SmallIntegerField(verbose_name="主要生活来源", choices=mainlife_choices)
    
class testresult(models.Model):
    username = models.CharField("用户名", max_length=16, default="")
    test_time = models.DateTimeField(verbose_name="测试时间", default=None)
    score1 = models.DecimalField("记忆力", max_digits=10, decimal_places = 4, default=0)
    score2 = models.DecimalField("定向力", max_digits=10, decimal_places = 4, default=0)
    score3 = models.DecimalField("社会活动能力", max_digits=10, decimal_places = 4, default=0)
    score4 = models.DecimalField("问题解决能力", max_digits=10, decimal_places = 4, default=0)
    score5 = models.DecimalField("视空间能力", max_digits=10, decimal_places = 4, default=0)
        