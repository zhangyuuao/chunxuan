# Generated by Django 4.0.6 on 2022-09-02 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='main_life',
            field=models.SmallIntegerField(choices=[(1, '养老金'), (2, '子女赡养'), (3, '社会救助'), (4, '劳动收入'), (5, '其他')], verbose_name='主要生活来源'),
        ),
    ]
