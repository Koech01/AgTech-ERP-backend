import io
from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

# Helper for image uploads
def generate_test_image(name='test.png'):
    img = Image.new('RGB', (100, 100), color=(73, 109, 137))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return SimpleUploadedFile(name, buf.read(), content_type='image/png')


# Base auth class
class AuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Testpass@123',
            role='farmer'
        )
        self.accessToken = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.accessToken}')


class AuthViewsTestCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse('signup_view')
        self.login_url = reverse('login_view')
        self.user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Testpass@123',
        }

    def test_signup_success(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], self.user_data['username'])

    def test_signup_duplicate_email(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_login_success(self):
        user = User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['role'], user.role)

    def test_login_fail_wrong_password(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': 'WrongPass123'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileViewsTestCase(AuthTestCase):
    def setUp(self):
        super().setUp()
        self.profile_url = reverse('user_profile_view')
        self.update_url = reverse('user_profile_update_view')

    def test_get_profile_success(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_profile_invalid_email(self):
        payload = {'email': 'not-an-email'}
        response = self.client.patch(self.update_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_update_profile_duplicate_email(self):
        other_user = User.objects.create_user(username='other', email='other@example.com', password='Testpass@123')
        payload = {'email': 'other@example.com'}
        response = self.client.patch(self.update_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_profile_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FarmerViewsTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', email='admin@example.com', password='Testpass@123', role='admin')
        self.farmer = User.objects.create_user(username='farmer1', email='farmer1@example.com', password='Testpass@123', role='farmer')
        self.accessToken = str(RefreshToken.for_user(self.admin).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.accessToken}')
        self.list_url = reverse('farmer_list_create_view')
        self.detail_url = reverse('farmer_detail_view', kwargs={'pk': self.farmer.id})

    def test_list_farmers(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(f['username'] == self.farmer.username for f in response.data))

    def test_create_farmer_success(self):
        payload = {'username': 'newfarmer', 'email': 'newfarmer@example.com', 'password': 'Testpass@123'}
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='newfarmer').count(), 1)

    def test_create_farmer_unauth_for_non_admin(self):
        non_admin_token = str(RefreshToken.for_user(self.farmer).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {non_admin_token}')
        payload = {'username': 'failfarmer', 'email': 'failfarmer@example.com', 'password': 'Testpass@123'}
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_farmer_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.farmer.username)

    def test_update_farmer(self):
        payload = {'username': 'updatedfarmer'}
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.farmer.refresh_from_db()
        self.assertEqual(self.farmer.username, payload['username'])

    def test_delete_farmer(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.farmer.id).exists())


class LogoutViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@example.com', password='Testpass@123')
        self.logout_url = reverse('logout_view')
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.client.cookies['refreshToken'] = self.refresh_token

    def test_logout_success(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Successfully logged out!')
        self.assertEqual(response.cookies['refreshToken'].value, '')


class TokenRefreshTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user2', email='user2@example.com', password='Testpass@123')
        self.refresh_url = reverse('token_refresh')
        self.refresh_token = str(RefreshToken.for_user(self.user))

    def test_token_refresh_success(self):
        response = self.client.post(self.refresh_url, {'refresh': self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)