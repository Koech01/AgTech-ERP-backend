import io
import uuid
from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class AuthTestCase(APITestCase):
    def setUp(self):
        self.user_password = 'Testpass@123'
        self.user = User.objects.create_user(
            username=f"user_{uuid.uuid4().hex[:6]}",
            email=f"{uuid.uuid4().hex}@example.com",
            password=self.user_password,
            role=User.Role.FARMER
        )

        login_url = reverse('login_view')
        response = self.client.post(login_url, {
            'email': self.user.email,
            'password': self.user_password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.accessToken = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.accessToken}')


class SignupViewTestCase(APITestCase):
    def setUp(self):
        User.objects.all().delete()
        self.url = reverse('signup_view')

    def generate_unique_payload(self):
        return {
            "username": f"user_{uuid.uuid4().hex[:6]}",
            "email": f"{uuid.uuid4().hex}@example.com",
            "password": "Testpass@123",
        }

    def test_signup_success(self):
        payload = self.generate_unique_payload()
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)

    def test_signup_duplicate_email(self):
        payload = self.generate_unique_payload()
        self.client.post(self.url, payload)
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileViewsTestCase(AuthTestCase):
    def setUp(self):
        super().setUp()
        self.profile_url = reverse('user_profile_view')
        self.update_url = reverse('user_profile_update_view')

    def test_profile_retrieve_success(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_profile_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_success(self):
        file = io.BytesIO()
        image = Image.new("RGB", (100, 100))
        image.save(file, 'PNG')
        file.name = 'test.png'
        file.seek(0)

        payload = {
            "username": "updatedusername",
            "email": f"{uuid.uuid4().hex}@example.com",
            "profileIcon": SimpleUploadedFile(file.name, file.read(), content_type='image/png')
        }

        response = self.client.patch(self.update_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "updatedusername")