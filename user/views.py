from django.shortcuts import render, redirect
from untitled import db
from django.http import HttpResponse, JsonResponse
from untitled.decorators import auto_session
from django.http.response import JsonResponse


# Create your views here.
def find(request, pk):
    sql = "select * from usernew where name1 = %s"
    user = db.query(sql, params=(pk,))
    return render(request, "detail.html", user)


def del_user(request, pk):
    sql = "delete from usernew where name1 = %s"
    db.update(sql, params=(pk,))
    return redirect(to="/")


def change(request, pk):
    sql = "select * from usernew where name1 = %s"
    user = db.query(sql, params=(pk,))
    return render(request, "change.html", user)


def change_new(request, pk):
    param = request.POST.dict()
    sql = "update usernew set name1=param[name1],pwd=param[pwd],tel=param[tel] where name1 = param[name1]"
    db.query(sql, param)
    return render(request, "change_new.html", param)


def show_photo(request):
    user = request.session.get("LOGIN_LOCAL_FLAG")
    current_user_id = user.get("id")
    sql = "select photo from t_user_info where user_id =%s"
    photo_dict = db.query(sql, params=(current_user_id,))
    photo = photo_dict.get("photo")
    response = HttpResponse(photo)
    response.setdefault("Content-Disposition", "attachment;filename=a.png")
    response["Content-Type"] = "image/jp"
    return response


@auto_session
def my_friends(request):
    user = request.session.get("LOGIN_LOCAL_FLAG")
    current_user_id = user.get("id")
    sql = """
        select user_id, nickname from t_user_info k where exists 
            (
            select 1 from (
                select friend_id from t_user_friend where user_id = %s
                union 
                select user_id from t_user_friend where  friend_id =%s 
                ) m where m.friend_id=k.user_id);
    """
    data = db.query_list(sql, params=(current_user_id, current_user_id))
    return JsonResponse(data, safe=False)
