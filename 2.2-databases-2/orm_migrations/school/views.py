from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


def students_list(request):
    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = 'group'
    
    students = Student.objects.order_by(ordering).all().prefetch_related('teachers')
    template = 'school/students_list.html'
    context = {
        'students': students
    }

    return render(request, template, context)
