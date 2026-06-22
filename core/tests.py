from unittest.mock import patch

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from .models import User


class DashboardRoutingTests(TestCase):
    def test_admin_is_sent_to_admin_dashboard(self):
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password123",
            role=User.Role.ADMIN,
        )
        self.client.force_login(admin)

        response = self.client.get(reverse("dashboard"))

        self.assertRedirects(response, reverse("admin:index"), fetch_redirect_response=False)

    def test_faculty_still_sees_faculty_dashboard(self):
        faculty = User.objects.create_user(
            username="faculty",
            password="password123",
            role=User.Role.FACULTY,
        )
        self.client.force_login(faculty)

        with patch("core.views.render", return_value=HttpResponse()) as render_mock:
            response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(render_mock.call_args.args[1], "faculty/dashboard.html")
