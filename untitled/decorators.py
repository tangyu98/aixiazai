from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse


def auto_session(func):
    def auto_session_warpper(request, *args, **kwargs):
        user = request.session.get("LOGIN_LOCAL_FLAG")
        if user is None:
            referer = request.headers.get("Referer", None)
            if "X-Requested-With" in request.headers:
                if referer is None:
                    path = "/"
                else:
                    path = referer
                return JsonResponse(data={"status": False, "msg": "用户未登录", "referer": path}, status=318)
            else:
                if referer is None:
                    return redirect(to="/?url=/")
                return redirect(to="/?url=" + referer)
        return func(request, *args, **kwargs)

    return auto_session_warpper
