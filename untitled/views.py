from django.shortcuts import render, redirect, reverse
from . import db
from django.http.response import JsonResponse
import hashlib
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.transaction import atomic
from django.views.decorators.csrf import csrf_exempt
import random
import string
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from user.models import *
from resource.models import *
from django.core.paginator import Paginator
from django_redis import get_redis_connection
from django.views.decorators.cache import cache_page


def path(request, path):
    return render(request, f"{path}.html")


def register(request):
    param = request.POST.dict()
    username = request.POST.get("name1")
    pwd = request.POST.get("pwd")
    newpwd = request.POST.get("newpwd")
    user = db.query("select * from usernew where name1 = %s", params=(username,))

    if user is None:
        sql = "insert into usernew(name1,pwd,tel) values(%(name1)s,%(pwd)s,%(tel)s)"
        if 6 <= len(pwd) <= 20 and pwd == newpwd:
            db.update(sql, param)
            return redirect(to="/login")
        param.setdefault("msg", "密码格式不对或两次输入的密码不同")
        return render(request, "register.html", param)
    return HttpResponse("用户已存在，注册失败")


def login(request):
    param = request.POST.dict()
    username = request.POST.get("name1")
    userpwd = request.POST.get("pwd")
    user = db.query("select * from usernew where name1 = %s and pwd =%s", params=(username, userpwd))
    if user is None:
        param.setdefault("msg", "用户名或密码不对")
        return render(request, "login.html", param)
    return redirect(to="/")


def index(request):
    users = db.query_list("select * from usernew")
    return render(request, "index.html", {"users": users})


@require_http_methods(["POST"])
def register_ai(request):
    account = request.POST.get("account")
    password = request.POST.get("password")
    pwd = hashlib.md5(password.encode()).hexdigest()
    user = User.objects.filter(account=account).first()
    # sql = "select * from t_user where account = %s"
    # user = db.query(sql, params=(account,))
    if user:
        return render(request, "register_ai.html", {"msg": "账号已被注册", "account": account})

    user = User.objects.create(account=account, pwd=pwd)
    # sql = "insert into t_user (account,pwd,reg_time,status)" \
    #       "value(%s,%s,now(),1)"
    # pk = db.update(sql, params=(account, pwd))
    return render(request, "re_next.html", {"pk": user.pk})


@require_http_methods(["POST"])
def re_next(request):
    params = request.POST.dict()
    photo = request.FILES.get("photo")
    photo = photo.read()
    params.setdefault("photo", photo)

    user_id = params.pop("user_id")

    user = User.objects.get(pk=user_id)
    params.setdefault("user", user)
    params.pop("csrfmiddlewaretoken")
    UserInfo.objects.create(**params)
    # sql = "insert into t_user_info(email,birth,nickname,realname,sex,photo,user_id)" \
    #       "value( %(email)s, %(birth)s, %(nickname)s, %(realname)s, %(sex)s, %(photo)s, %(user_id)s )"
    # db.update(sql, params=params)
    user.status = 2
    user.save()
    # sql = "update t_user set status =2 where id =%s"
    # db.update(sql, params=(params.get("user_id"),))
    params.pop("photo")
    return render(request, "re_end.html", params)


@csrf_exempt
@require_http_methods(["POST"])
def check_user(request):
    account = request.POST.get("account")
    sql = "select * from t_user where account = %s"
    user = db.query(sql, params=(account,))
    if user:
        return JsonResponse(data={"status": False, "message": "账号已被注册"})
    return JsonResponse(data={"status": True})


@cache_page(timeout=60)
@require_http_methods(["GET"])
def index1(request, page):
    queryset = Resource.objects.all().order_by("-upload_time")

    paginator = Paginator(queryset, 2)
    page = int(page) if page != "" else 1
    page = paginator.get_page(page)
    # sql = "select t.*, u.nickname from t_resource t left join t_user_info u on u.user_id = t.user_id order by upload_time desc"
    # data = db.query_list(sql)
    nums = {}
    for p in page:
        # pk = p.pk
        # redis = get_redis_connection()
        # num = redis.get(f"resource:visit:{pk}")
        # nums.setdefault(pk, num)
        nums.setdefault(p.pk, b"0")
    return render(request, "index1.html", {"page": page, "nums": nums})


def login1(request):
    params = request.POST.dict()
    sql = "select * from t_user where account =%(account)s and pwd=md5(%(pwd)s)"
    user = db.query(sql, params=params)
    if user is None:
        return render(request, "index1.html", {"msg": "账号或密码不正确", "account": params.get("account")})
    if 1 == user.get("STATUS"):
        return render(request, "re_next.html", {"pk": user.get("id")})
    elif 3 == user.get("STATUS"):
        return render(request, "index1.html", {"msg": "您的账号已被冻结"})
    else:
        user.pop("pwd")
        user.pop("reg_time")
        request.session.setdefault("LOGIN_LOCAL_FLAG", user)
        if "url" in params.keys():
            return redirect(to=params.get("url"))

        return redirect(to="/")


def logout(request):
    request.session.clear_expired()
    request.session.flush()
    return redirect(to="/")


def celery(request):
    from .celerys import debug_task

    debug_task.delay()
    return HttpResponse("Celery测试异步代码")


@csrf_exempt
def find_pass(request):
    if request.method == "GET":
        return render(request, "findpass.html")

    # 开始处理 找回密码的逻辑

    # 1、获取账号 和 邮箱
    account = request.POST.get("account")
    email = request.POST.get("email")

    # 2、根据账号和邮箱查询 用户是否存在，如果存在，则才能修改密码

    sql = "select t.* from t_user t left join t_user_info f " \
          "on t.id = f.user_id where t.account = %s and f.email = %s"

    # 3、执行SQL
    user = db.query(sql, params=(account, email))

    if user is None:
        return render(request, "findpass.html", {"msg": "账号或者邮箱不正确"})

    # 4、生成一个新的密码
    strpass = string.ascii_letters + string.digits

    # 6. 随机产生一个 6位长度的密码
    password = random.choices(strpass, k=6)

    password = "".join(password)

    # 7. 对密码进行MD5加密，并存储到表中

    sql = "update t_user set pwd = md5(%s) where account = %s"

    db.update(sql, params=(password, account))

    # 8、将新密码以邮件的形式发送给用户
    from datetime import datetime
    times = datetime.now()
    subject = "爱下载-密码找回"
    to = [email]
    body = f"尊敬的<span style='color:red;'>{account}</span>,您于<span>{times}</span>找回密码，" \
        f"您的新的密码是<span style='color:red;'>{password}</span>,请登录后尽快修改~"

    message = EmailMessage(subject=subject, body=body, to=to)

    message.content_subtype = "html"
    # 发送邮件
    message.send()

    # from user.tasks import send_mail
    #
    # send_mail.delay(subject, body, to)

    return JsonResponse(data={"msg": "邮件已发送，请查阅您的邮件"})
