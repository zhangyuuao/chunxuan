from django.shortcuts import redirect, render
from UserInfo.utils.forms import testInfo
from UserInfo.utils import mmoe
from UserInfo.models import UserInfo, testresult
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy import io
import numpy as np
import torch

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


## 共享底层参数的多任务学习模型 ## 

def rank(score):
    if score < 1:
        return "健康"
    if score >= 1 and score < 1.5:
        return "轻度风险"
    if score >= 1.5 and score < 2.5:
        return "中度风险"
    if score >= 2.5:
        return "重度风险"

def aitest(request):
    if request.method == "GET":
        form = testInfo(username=request.session["info"]["name"])
        row_data = testresult.objects.filter(username = request.session["info"]["name"]).order_by('-test_time')
        number = len(row_data)
        context = {
            "form": form,
            "row_data": row_data[:5],
            "number": number,
            "queryset_all": row_data
        }
        
        return render(request, "aitest.html", context)

    data = request.POST

    form = testInfo(username=request.session["info"]["name"], data = data)
    result = testresult()
    if form.is_valid():
        form.instance.test_time = datetime.now()
        form.save()
        input = pd.DataFrame(dict(data)).iloc[0, 2:].to_numpy().reshape(1, -1)
        print(input.shape)
        stdclr = StandardScaler()
        train_data = io.loadmat("/Users/zhangyuyao/Desktop/大创/chunxuan/UserInfo/static/data1.mat")
        X = train_data["X"][:, :12]
        stdclr.fit(X)
        input = stdclr.transform(input)
        input = torch.tensor(input, dtype=torch.float32)
        model = mmoe.MMoE(12, 16, 16, 5, 5)
        model = torch.load("mmoe.pkl")
        with torch.no_grad():
            score1, score2, score3, score4, score5 = model(input)
            score1 = score1.item() / 9
            score2 = score2.item() / 7
            score3 = score3.item() / 11
            score4 = score4.item() / 6
            score5 = score5.item() / 5
            
            testresult.objects.create(username=form.instance.username, test_time=form.instance.test_time, score1=score1, score2=score2, score3=score3, score4=score4, score5=score5)    
            context = {
                "score1": round(score1, 2),
                "score2": round(score2, 2),
                "score3": round(score3, 2),
                "score4": round(score4, 2),
                "score5": round(score5, 2),
                "rank1": rank(score1),
                "rank2": rank(score2),
                "rank3": rank(score3),
                "rank4": rank(score4),
                "rank5": rank(score5)
            } 
        return render(request, "result.html", context)
    
    return redirect("/aitest")