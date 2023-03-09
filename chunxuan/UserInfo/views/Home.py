from logging.config import valid_ident
from django.shortcuts import redirect, render
from UserInfo.utils.forms import UserLogin, Register
from UserInfo.models import UserInfo
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import pandas as pd
import torch

def card(color: str, title: str, date: str, summary: str, path: str):
    if color == "success":
        
        html = """<div class="row g-0 border rounded overflow-hidden flex-md-row mb-2 shadow-sm h-md-250 position-relative"><div class="col p-4 d-flex flex-column position-static">"""\
            + '<strong class="d-inline-block mb-2 text-{}">'.format(color)\
            +'World'\
            +'</strong>'\
            +' <h3 class="mb-0">'\
            +'{}'.format(title)\
            +'</h3>'\
            +'<div class="mb-1 text-muted">'\
            +'{}'.format(date)\
            +'</div><p class="card-text mb-auto">'\
            +'{}'.format(summary)\
            +'</p>'\
            +'<a href='\
            +'"/static/pdf/{}"'.format(path)\
            +'class="stretched-link text-success">Continue reading</a>'\
            +'</div><div class="col-auto d-none d-lg-block">'\
            +"""<svg class="bd-placeholder-img" width="200" height="250" xmlns="http://www.w3.org/2000/svg" role="img"aria-label="Placeholder: Thumbnail" preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title><rect width="100%" height="100%" fill="{}"></rect><text x="50%" y="50%" fill="#eceeef" dy=".3em">Science</text>
    </svg>
    </div>
    </div>""".format("#198754")
    else:
        html = """<div class="row g-0 border rounded overflow-hidden flex-md-row mb-2 shadow-sm h-md-250 position-relative"><div class="col p-4 d-flex flex-column position-static">"""\
            + '<strong class="d-inline-block mb-2 text-{}">'.format("primary")\
            +'World'\
            +'</strong>'\
            +' <h3 class="mb-0">'\
            +'{}'.format(title)\
            +'</h3>'\
            +'<div class="mb-1 text-muted">'\
            +'{}'.format(date)\
            +'</div><p class="card-text mb-auto">'\
            +'{}'.format(summary)\
            +'</p>'\
            +'<a href='\
            +'"/static/pdf/{}"'.format(path)\
            +'class="stretched-link text-primary">Continue reading</a>'\
            +'</div><div class="col-auto d-none d-lg-block">'\
            +"""<svg class="bd-placeholder-img" width="200" height="250" xmlns="http://www.w3.org/2000/svg" role="img"aria-label="Placeholder: Thumbnail" preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title><rect width="100%" height="100%" fill="{}"></rect><text x="50%" y="50%" fill="#eceeef" dy=".3em">Science</text>
    </svg>
    </div>
    </div>""".format("#0d63fd")
    return html

def get_html():
    card1 = card("primary", "阿尔兹海默症开山论文造假", "Jul 21 2022",
                 "学术界污点：阿尔茨海默症发病机制流行理论的奠基性论文，涉及到Aβ*56的图像被进行了后期加工，进行了多次复制粘贴操作，从而捏造了实验结果。",
                 "science.add9993.pdf")
    card2 = card("success", "中国阿尔茨海默病报告2021", "Jul 21 2022",
                 "目前,中国AD发病率、患病率及死亡率仍持续增高,AD死亡占城乡居民总死亡原因的第5位,给居民和社会带来的经济负担日渐加重。",
                 "中国阿尔茨海默病报告2021_任汝静.pdf")
    card3 = card("primary", "阿尔兹海默症简析", "Mar 26 2020",
                 "本研究通过查阅文献、了解、对比及总结其发病机理，并为该疾病的治疗做些许贡献。",
                 "阿尔兹海默症简析.pdf")
    card4 = card("success", "阿尔兹海默症开山论文造假", "Jul 21 2022",
                 "学术界污点：阿尔茨海默症发病机制流行理论的奠基性论文，涉及到Aβ*56的图像被进行了后期加工，进行了多次复制粘贴操作，从而捏造了实验结果。",
                 "science.add9993.pdf")
    
    cards = [card1, card2, card3, card4]
    cards = cards + cards
    cards = cards + cards
    return cards

def home(request) :
    if request.method == "GET" :
        return render(request, "Home.html")
    
def zixun(request) :
    zixun_html = {'results_html': get_html()}
    if request.method == 'GET' :
        return render(request, "zixun.html",zixun_html)

def test1(request) :
    questions = [
        '记得家人和熟人的职业、生日和住址',
        '记得最近发生的事情',
        '记得几天前谈话的内容',
        '记得自己的住址和电话号码',
        '记得今天是星期几、几月份',
        '记得东西经常是放在什么地方',
        '东西未放回原位，仍能找得到',
        '使用日常用具的能力（如电视机等）',
        '学习使用新的家用工具与电器的能力',
        '学习新事物的能力',
        '看懂电视或书本中讲的故事',
        '对日常生活事务自己会做决定',
        '会用钱买东西',
        '处理财务的能力（如取退休金、存款等）',
        '处理日常生活上的计算问题（如知道要买多少食物，知道朋友或家人上一次来访有多久了）',
        '了解正在发生什么事件，以及事件发生的原因'
    ]
    
    if request.method == "GET" :
        return render(request, "test1.html", {"questions": questions})
    data = request.POST.dict()
    point = 0
    for key, value in data.items():
        if key == "csrfmiddlewaretoken":
            continue
        value = int(value)
        if value != 9:
            point += value
    print(data)
    print("point：", point)
    return redirect("/home")

def test2(request):
    return render(request, "test2.html")