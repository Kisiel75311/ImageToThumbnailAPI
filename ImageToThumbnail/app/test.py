# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Image, UserProfile, Tier
from .serializers import ImageSerializer, UserProfileSerializer, TierSerializer
from PIL import Image as Img
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import tempfile
from datetime import timedelta
from django.utils import timezone


class ViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='testpassword')
        self.client.login(username='test', password='testpassword')
        self.tier = Tier.objects.create(name='Premium', thumbnail_sizes=[200, 200], has_original=True, can_expire=False)
        self.user_profile = UserProfile.objects.create(user=self.user, tier=self.tier)
        self.image = Image.objects.create(user=self.user, image='dummy_image.jpg')
        self.upload_url = reverse('upload')

    def test_image_upload_view(self):
        with open('ImageToThumbnail/app/test_image.jpg', 'rb') as img:
            response = self.client.post(self.upload_url, {'image': img, 'user': self.user.id}, format='multipart')
        self.assertEqual(response.status_code, 201)

        self._check_basic_plan_functionality(response)
        self._check_premium_plan_functionality(response)
        self._check_enterprise_plan_functionality(response)
        self._check_expiring_link_functionality(response)

    def _check_basic_plan_functionality(self, response):
        basic_thumbnail_url = response.data['thumbnail_200']
        self.assertIsNotNone(basic_thumbnail_url)

    def _check_premium_plan_functionality(self, response):
        self.user_profile.tier = Tier.objects.create(
            name='Premium', thumbnail_sizes=[200, 200, 400], has_original=True, can_expire=False
        )
        self.user_profile.save()
        response = self.client.post(self.upload_url, {'image': img, 'user': self.user.id}, format='multipart')
        self.assertEqual(response.status_code, 201)
        premium_thumbnail_200_url = response.data['thumbnail_200']
        self.assertIsNotNone(premium_thumbnail_200_url)
        premium_thumbnail_400_url = response.data['thumbnail_400']
        self.assertIsNotNone(premium_thumbnail_400_url)
        original_image_url = response.data['image']
        self.assertIsNotNone(original_image_url)

    def _check_enterprise_plan_functionality(self, response):
        self.user_profile.tier = Tier.objects.create(
            name='Enterprise', thumbnail_sizes=[200, 200, 400], has_original=True, can_expire=True
        )
        self.user_profile.save()
        response = self.client.post(self.upload_url, {'image': img, 'user': self.user.id}, format='multipart')
        self.assertEqual(response.status_code, 201)
        enterprise_thumbnail_200_url = response.data['thumbnail_200']
        self.assertIsNotNone(enterprise_thumbnail_200_url)
        enterprise_thumbnail_400_url = response.data['thumbnail_400']
        self.assertIsNotNone(enterprise_thumbnail_400_url)
        enterprise_original_image_url = response.data['image']
        self.assertIsNotNone(enterprise_original_image_url)

    def _check_expiring_link_functionality(self, response):
        expiry_seconds = 600  # Example: Link expires after 10 minutes
        image_id = response.data['id']
        expiry_url = f'/images/{image_id}/expiring-link/?expires_in={expiry_seconds}'
        response = self.client.get(expiry_url)
        self.assertEqual(response.status_code, 200)
        expiry_date = timezone.now() + timedelta(seconds=expiry_seconds)
        self.assertEqual(response.data['expires_at'], expiry_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))


class ModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testpassword')
        self.tier = Tier.objects.create(name='Premium', thumbnail_sizes=[200, 200], has_original=True, can_expire=False)
        self.user_profile = UserProfile.objects.create(user=self.user, tier=self.tier)
        self.image = Image.objects.create(user=self.user, image='dummy_image.jpg')

    def test_model_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(Tier.objects.count(), 1)
        self.assertEqual(Image.objects.count(), 1)

    def test_model_str_method(self):
        self.assertEqual(str(self.user), 'test')
        self.assertEqual(str(self.user_profile), 'test')
        self.assertEqual(str(self.tier), 'Premium')
        self.assertEqual(str(self.image), 'test: ' + str(self.image.created_at))

class SerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testpassword')
        self.tier = Tier.objects.create(name='Premium', thumbnail_sizes=[200, 200], has_original=True, can_expire=False)
        self.user_profile = UserProfile.objects.create(user=self.user, tier=self.tier)
        self.image = Image.objects.create(user=self.user, image='dummy_image.jpg')

    def test_serializers(self):
        serializer_data = ImageSerializer(instance=self.image).data
        self.assertEqual(serializer_data['user'], self.image.user.id)

        serializer_data = UserProfileSerializer(instance=self.user_profile).data
        self.assertEqual(serializer_data['user'], self.user_profile.user.id)

class ViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='testpassword')
        self.client.login(username='test', password='testpassword')
        self.tier = Tier.objects.create(name='Premium', thumbnail_sizes=[200, 200], has_original=True, can_expire=False)
        self.user_profile = UserProfile.objects.create(user=self.user, tier=self.tier)
        self.image = Image.objects.create(user=self.user, image='dummy_image.jpg')
        self.upload_url = reverse('upload')

    def test_image_upload_view(self):
        with open('ImageToThumbnail/app/test_image.jpg', 'rb') as img:
            response = self.client.post(self.upload_url, {'image': img, 'user': self.user.id}, format='multipart')
        print(response.content)  # Wydrukuj treść odpowiedzi
        self.assertEqual(response.status_code, 201)

    def test_image_list_view(self):
        response = self.client.get('/images/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_user_profile_view(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user'], self.user.id)

