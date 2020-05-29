import os

from django.shortcuts import render, redirect
from untitled import db
from django.http import HttpResponse, JsonResponse
from django.utils.http import urlquote
from untitled.decorators import auto_session
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from resource.models import *
from .forms import ResourceModelForm
from untitled.decorators import auto_session
from django_redis import get_redis_connection


# Create your views here.
@auto_session
def upload(request):
    form = ResourceModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        resource = form.instance
        file = request.FILES.get("resource")
        name = file.name
        index = name.rfind(".")
        ext = name[index + 1:]
        resource.ext = ext
        size = file.size
        resource.resourceSize = size
        resource.content_type = file.content_type
        user = request.session.get("LOGIN_LOCAL_FLAG")
        userid = user.get("id")
        resource.user = User.objects.get(pk=userid)
        resource.save()

    # params = request.POST.dict()
    # resource = request.FILES.get("resource")
    #
    # user = request.session.get("LOGIN_LOCAL_FLAG")
    # userid = user.get("id")
    # params["user_id"] = userid
    #
    # name = resource.name
    # index = name.rfind(".")
    # ext = name[index + 1:]
    # params["ext"] = ext
    # resourceSize = resource.size
    # params["resourceSize"] = resourceSize
    # content_type = resource.content_type
    # params["content_type"] = content_type
    #
    # import uuid
    #
    # filename = uuid.uuid4().hex
    #
    # with open(f"upload/{filename}", "wb") as f:
    #     for cn in resource.chunks():
    #         f.write(cn)
    #
    # params["resource"] = filename
    # sql = "insert into t_resource(resourceName,resourceType,resource," \
    #       "keywords, score, resourceDesc,user_id,upload_time,ext, resourceSize," \
    #       "content_type) values(%(resourceName)s, %(resourceType)s, %(resource)s, " \
    #       "%(keywords)s, %(score)s, %(resourceDesc)s,  %(user_id)s, now() ,  %(ext)s," \
    #       "%(resourceSize)s, %(content_type)s)"
    # db.update(sql, params=params)
    return redirect(to="/")


def personal(request):
    # 获取登陆用户的id
    user = request.session.get("LOGIN_LOCAL_FLAG")
    # 遍历该用户的注册信息
    sql = "select * from t_user_info where user_id = %s"
    new = db.query(sql, params=(user.id,))
    # 得到用户的头像
    photo = new.get("photo")
    photo = HttpResponse(photo)
    new.pop("photo")
    return render(request, "personal.html", {"new": new, "photo": photo})


def detail1(request, pk):
    resource = Resource.objects.get(pk=pk)
    ran = range(5)
    redis = get_redis_connection()
    if not redis.exists(f"resource:visit:{pk}"):
        redis.set(f"resource:visit:{pk}", 1)
    else:
        redis.incr(f"resource:visit:{pk}")
    # sql = """select t.*, f.nickname,
    # (select count(id) from t_resource_download d where d.res_id =t.id)as downloadnum
    # from t_resource t left join t_user_info f on t.user_id = f.user_id where t.id=%s"""
    # resource = db.query(sql, params=(pk,))

    # sql = "select t.*, f.nickname from t_resource_comment t left join t_user_info f on f.user_id=t.user_id " \
    #       "where t.res_id = %s"
    # comments = db.query_list(sql, params=(pk,))
    # resource["comments"] = comments

    # ran = range(5)
    # resource["ran"] = ran
    return render(request, "detail1.html", {"resource": resource, "ran": ran})


def photo(request, user_id):
    sql = "select photo from t_user_info where user_id =%s"
    photo_dict = db.query(sql, params=(user_id,))
    photo = photo_dict.get("photo")
    return HttpResponse(photo)


@auto_session
def download(request, id):
    user = request.session.get("LOGIN_LOCAL_FLAG")
    userid = user.get("id")
    sql = "insert into t_resource_download(res_id,user_id,down_time) value (%s,%s,now())"
    db.update(sql, params=(id, userid))
    sql = "select resource,resourceName,ext,content_type from t_resource where id = %s"
    resource = db.query(sql, params=(id,))
    if resource:
        resourcePath = resource.get("resource")
        resourceName = resource.get("resourceName")
        ext = resource.get("ext")
        content_type = resource.get("content_type")
        with open(os.path.join("upload", resourcePath), "rb") as f:
            response = HttpResponse(f.read())
            filename = f"{resourceName}.{ext}"
            filename = urlquote(filename)
            response["Content-Disposition"] = "attachment;filename=" + filename
            response["Content-type"] = content_type
            return response


@require_POST
@csrf_exempt
@auto_session
def comments(request):
    params = request.POST.dict()

    user = request.session.get("LOGIN_LOCAL_FLAG")
    userid = user.get("id")
    params["user_id"] = userid

    sql = "insert into t_resource_comment(content,star,comment_time,user_id,res_id)" \
          "values(%(content)s, %(star)s, now(), %(user_id)s, %(res_id)s)"

    pk = db.update(sql, params=params)

    sql = "select t.*, f.nickname from t_resource_comment t left join t_user_info f " \
          "on t.user_id=f.user_id where t.id=%s"
    comments = db.query(sql, params=(pk,))
    return JsonResponse(data=comments)
