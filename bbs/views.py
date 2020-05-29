from django.shortcuts import render
from django.shortcuts import render, redirect
from bbs.models import Student
from django.views.generic import ListView


# Create your views here.


# def students(request):
#     stu = Student.objects.all()
#
#     return render(request, "bbs/index.html", {"students": stu})

class StudentList(ListView):
    queryset = Student.objects.all()
    template_name = "bbs/index.html"
    context_object_name = "students"


# def detail(request, pk):
#     stu = Student.objects.get(pk=pk)
#     return render(request, "bbs/detail.html", {"student": stu})


class StudentDetailView(ListView):
    # queryset = Student.objects.all()
    # model = Student
    # template_name = "bbs/detail.html"
    # context_object_name = "stu"
    def get(self, request, pk):
        stu = Student.objects.get(pk=pk)
        return render(request, "bbs/detail.html", {"student": stu})
