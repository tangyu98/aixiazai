from django.db import models


# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="学校名称", blank=True)

    class Meta:
        db_table = "t_school"


class Student(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="姓名")
    _sex_type = (
        ("1", "男"),
        ("2", "女"),
        ("3", "保密")
    )
    sex = models.CharField(choices=_sex_type, max_length=1, null=True, blank=True, verbose_name="性别",
                           help_text="请输入（1：男，2：女，3：保密）")
    stuNo = models.AutoField(primary_key=True, auto_created=True, verbose_name="学号")
    birth = models.DateField(null=True, blank=True, verbose_name="出生日期")

    school = models.ForeignKey(to=School, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name + "," + self.sex + "," + str(self.birth)

    class Meta:
        db_table = "t_student"
        verbose_name = "学生"
        verbose_name_plural = "学生信息"


class Computer(models.Model):
    name = models.CharField(max_length=100, verbose_name="电脑名称", db_column="computer_name")
    stu = models.OneToOneField(to=Student, on_delete=models.CASCADE, blank=True)

    class Meta:
        db_table = "t_computer"


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(to=Student, db_table="t_tea_stu", blank=True)

    class Meta:
        db_table = "t_teacher"
