from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("submissions", views.SubmissionViewSet, basename="submission")
router.register("questions", views.QuestionViewSet, basename="question-api")
router.register("progress", views.ProgressViewSet, basename="progress")

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.AppLoginView.as_view(), name="login"),
    path("logout/", views.AppLogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("modules/<int:module_id>/", views.module_detail, name="module_detail"),
    path("questions/<int:question_id>/", views.question_detail, name="question_detail"),
    path("submissions/<int:submission_id>/", views.submission_detail, name="submission_detail"),
    path("certificates/generate/", views.certificate_create, name="certificate_create"),
    path("certificates/<int:certificate_id>/", views.certificate_detail, name="certificate_detail"),
    path("verify/<str:verification_hash>/", views.certificate_verify, name="certificate_verify"),
    path("faculty/modules/new/", views.faculty_module_form, name="faculty_module_new"),
    path("faculty/modules/<int:module_id>/", views.faculty_module_form, name="faculty_module_edit"),
    path("faculty/questions/new/", views.faculty_question_form, name="faculty_question_new"),
    path("faculty/questions/<int:question_id>/", views.faculty_question_form, name="faculty_question_edit"),
    path("faculty/questions/<int:question_id>/tests/new/", views.faculty_testcase_form, name="faculty_testcase_new"),
    path("api/", include(router.urls)),
]
