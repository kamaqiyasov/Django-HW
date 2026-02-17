import random
from django.urls import reverse
import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course


@pytest.fixture()
def client():
    return APIClient()

@pytest.fixture()
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture()
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    course = course_factory()

    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]['id'] == course.id
    
@pytest.mark.django_db
def test_get_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    
    response = client.get('/api/v1/courses/')
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert len(data) == len(courses)
    
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name
        
@pytest.mark.django_db
def test_get_filter_course(client, course_factory):
    course_factory(_quantity=5)
    course_ids = Course.objects.values_list('id', flat=True)
    random_id = random.choice(course_ids)
    
    response = client.get(f'/api/v1/courses/?id={random_id}')
    
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == random_id
    
@pytest.mark.django_db
def test_get_name_filter_course(client, course_factory):
    course_factory(_quantity=5)
    course_names = Course.objects.values_list('name', flat=True)
    random_name = random.choice(course_names)
    
    response = client.get(f'/api/v1/courses/?name={random_name}')
    
    assert response.status_code == 200
    data = response.json()

    assert data[0]['name'] != 'dawdaw'
    assert data[0]['name'] == random_name

@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    
    response = client.post('/api/v1/courses/', data={
        'name': 'Математика',
    })
    
    assert response.status_code == 201
    assert Course.objects.count() == count + 1
    
@pytest.mark.django_db
def test_update_course(client, course_factory, student_factory):
    courses = course_factory(_quantity=5)
    students = student_factory(_quantity=3)    
    course_id = random.choice(courses).id
    put_data = {
        'name': 'Физика',
        'students': [random.choice(students).id]
    }
    response = client.patch(f'/api/v1/courses/{course_id}/', data=put_data)
    assert response.status_code == 200
    data = response.json()
    assert put_data.items() <= data.items()
    
@pytest.mark.django_db
def test_destroy_course(client, course_factory):
    courses = course_factory(_quantity=5)
    course_id = random.choice(courses).id
    
    response = client.delete(f'/api/v1/courses/{course_id}/')
    
    assert response.status_code == 204
    assert len(courses) > Course.objects.count() 
    
    