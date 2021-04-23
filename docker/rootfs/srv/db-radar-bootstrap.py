"""Will be executed by service-base -> django-migrate.sh"""
import os
import sys
import django
from datetime import timedelta
from django.utils import timezone

def create_default_users():
    from accounts.models import RadarUser

    ur = RadarUser.objects.create(
        username="root",
        email="root@localhost.invalid",
        first_name="Ruth",
        last_name="Robinson",
        is_superuser=True,
        is_staff=True,
    )
    ur.set_password("root")
    ur.save()
    # ur.userprofile.student_id = "<admin>"
    # ur.userprofile.save()

    # ut = RadarUser.objects.create(
    #     username="teacher",
    #     email="teacher@localhost.invalid",
    #     first_name="Terry",
    #     last_name="Teacher",
    # )
    # ut.set_password("teacher")
    # ut.save()
    # ut.userprofile.student_id = "<teacher>"
    # ut.userprofile.save()

    # ua = RadarUser.objects.create(
    #     username="assistant",
    #     email="assistant@localhost.invalid",
    #     first_name="Andy",
    #     last_name="Assistant",
    # )
    # ua.set_password("assistant")
    # ua.save()
    # ua.userprofile.student_id = "133701"
    # ua.userprofile.save()

    # us = RadarUser.objects.create(
    #     username="student",
    #     email="student@localhost.invalid",
    #     first_name="Stacy",
    #     last_name="Student",
    # )
    # us.set_password("student")
    # us.save()
    # us.userprofile.student_id = "123456"
    # us.userprofile.save()

    return {
        # 'root': ur.userprofile,
        # 'teacher': ut,
        # 'assistant': ua.userprofile,
        # 'student': us.userprofile
    }

def create_default_courses(users):
    from data.models import Course, URLKeyField
    from aplus_client.django.models import ApiNamespace as Site
    course_api = 'https://minus.cs.aalto.fi//api/v2/courses/194/'
    context_id = 'minus.cs.aalto.fi/laines5-test/i1/'

    site = Site.get_by_url(course_api)
    # user = users['teacher']
    # user.add_api_token(api_token, site) # will not add duplicates
    course_key = URLKeyField.safe_version(context_id)

    # apiclient = user.get_api_client(site)

    # course = Course.objects.using_namespace(site).create(
    course = Course.objects.create(
        name="Def. Course",
        # key="def000",
        #
    )
    # course.teachers.set([users['teacher']])

    # today = timezone.now()
    # instance = CourseInstance.objects.create(
    #     course=course,
    #     instance_name="Current",
    #     url="current",
    #     starting_time=today,
    #     ending_time=today + timedelta(days=365),
    #     configure_url="http://grader:8080/default/aplus-json",
    # )
    # instance.assistants.set([users['assistant']])

    # Enrollment.objects.get_or_create(course_instance=instance, user_profile=users['assistant'])
    # Enrollment.objects.get_or_create(course_instance=instance, user_profile=users['student'])

    return {'default': course}

def create_default_services():
    from external_services.models import LTIService

    services = {}

    services['rubyric+'] = LTIService.objects.create(
        url="http://localhost:8090/",
        menu_label="Rubyric+",
        menu_icon_class="save-file",
        consumer_key="foo",
        consumer_secret="bar",
    )

    services['rubyric'] = LTIService.objects.create(
        url="http://localhost:8091/",
        menu_label="Rubyric",
        menu_icon_class="save-file",
        consumer_key="foo",
        consumer_secret="bar",
    )

    return services

def add_lti_key():
    from django.core.exceptions import ValidationError
    from django_lti_login.models import LTIClient
    lticlient = LTIClient(key='lti-key')
    lticlient.secret = 'lti-secret'
    lticlient.description = 'aplus'

    lticlient.full_clean()

    lticlient.save()


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "radar.settings")
    sys.path.insert(0, '')
    django.setup()

    users = create_default_users()
    add_lti_key()
    # courses = create_default_courses(users)
    # services = create_default_services()
