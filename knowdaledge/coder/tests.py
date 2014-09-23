from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

from .models import Coder


class TestCoderMixin(TestCase):

    create_url = reverse('create_coder')
    current_coder_url = reverse('current_coder')
    login_url = reverse('login_coder')

    kouga = {
        'email': 'saejima.kouga@gmail.com',
        'password': 'ougonkishii',
        'first_name': 'Kouga',
        'last_name': 'Saejima'
    }

    rei = {
        'email': 'zero.rei@gmail.com',
        'password': 'ginnokishii',
        'first_name': 'Rei',
        'last_name': 'Zero'
    }

    def setUp(self):
        self.client = APIClient()


class CoderTests(TestCoderMixin):

    def test_create_coders(self):
        response = self.client.post(self.create_url, self.kouga, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.create_url, self.rei, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Coder.objects.all().count(), 2)

    def test_create_coders_conflict(self):
        response = self.client.post(self.create_url, self.kouga, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.create_url, {
            'email': self.kouga['email'],
            'password': 'this should totally work'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(Coder.objects.all().count(), 1)

    def test_create_coders_bad_request(self):
        response = self.client.post(self.create_url, {
            'email': 'whoomp.thereitaint.',
            'password': 'shackalocka',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Coder.objects.all())

    def test_cuurent_stakeholder(self):
        response = self.client.post(self.create_url, self.kouga, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        garo = Coder.objects.get(email=self.kouga['email'])
        garo_t = garo.auth_token.key

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + garo_t)
        response = self.client.get(self.current_coder_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.kouga['email'])

    def test_current_stakeholder_fail(self):

        response = self.client.get(self.current_coder_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_coder_success(self):
        response = self.client.post(self.create_url, self.kouga, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        garo = Coder.objects.get(email=self.kouga['email'])

        # Have Kouga login

        response = self.client.post(self.login_url, {
            'email': self.kouga['email'],
            'password': self.kouga['password']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], garo.pk)
        self.assertEqual(response.data['token'], garo.auth_token.key)

    def test_login_coder_success_fail(self):
        response = self.client.post(self.create_url, self.kouga, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        garo = Coder.objects.get(email=self.kouga['email'])

        # Have Kouga login

        response = self.client.post(self.login_url, {
            'email': self.kouga['email'],
            'password': 'rainbowponysprinklesson'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
