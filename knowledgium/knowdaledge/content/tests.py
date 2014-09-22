from django.test import TestCase
from django.core.urlresolvers import reverse


from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


from coder.tests import TestCoderMixin
from coder.models import Coder


from .models import Content, Category


class ContentTest(TestCoderMixin):

    category_url = reverse('category_list_create')
    content_url = reverse('content_list_create')
    content_detail_url = lambda s, pk: reverse('content_detail', args=[pk])

    coder_jesus = {
     'email': 'iam@theway.com',
     'password': 'konamicode'
    }

    category_1 = {
        'title': "backend coding"
    }

    category_2 = {
        'title': "frontend coding"
    }

    def setUp(self):
        self.client = APIClient()
        self.yhwh = Coder.objects.create_superuser(self.coder_jesus['email'],
            password=self.coder_jesus['password'])
        self.yhwh_t = Token.objects.create(user=self.yhwh)

        self.client.post(self.create_url, self.kouga, format='json')
        self.client.post(self.create_url, self.rei, format='json')

        self.garo = Coder.objects.get(email=self.kouga['email'])
        self.zero = Coder.objects.get(email=self.rei['email'])

    def test_admin_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.yhwh_t.key)
        response = self.client.get(self.current_coder_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_categories(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.yhwh_t.key)

        response = self.client.post(self.category_url, self.category_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.category_url, self.category_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Category.objects.all().count(), 2)

    def test_create_categories_failure(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.garo.auth_token.key)

        response = self.client.post(self.category_url, self.category_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertFalse(Category.objects.all())

    def test_create_content(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.yhwh_t.key)

        response = self.client.post(self.category_url, self.category_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.category_url, self.category_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Category.objects.all().count(), 2)

        be = Category.objects.get(title=self.category_1['title'])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.garo.auth_token.key)
        response = self.client.post(self.content_url, {
            'title': "Python is dope.",
            'message': "I love python. Do you love python? PYTHON PYTHON PYTHON.",
            'category': be.pk
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.zero.auth_token.key)
        response = self.client.post(self.content_url, {
            'title': "Python",
            'message': "LALALALALALALALAL PYTHON",
            'category': be.pk
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.content_url)

    def test_patch_content(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.yhwh_t.key)

        response = self.client.post(self.category_url, self.category_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.category_url, self.category_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Category.objects.all().count(), 2)

        be = Category.objects.get(title=self.category_1['title'])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.garo.auth_token.key)
        response = self.client.post(self.content_url, {
            'title': "Python is dope.",
            'message': "I love python. Do you love python? PYTHON PYTHON PYTHON.",
            'category': be.pk
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.zero.auth_token.key)
        response = self.client.post(self.content_url, {
            'title': "Python",
            'message': "LALALALALALALALAL PYTHON",
            'category': be.pk
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        garo_post = Content.objects.get(author=self.garo, title='Python is dope.')
        zero_post = Content.objects.get(author=self.zero, title='Python')

        # Kouga tries to update his post.

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.garo.auth_token.key)
        response = self.client.patch(self.content_detail_url(garo_post.pk), {
            'message': "My python skills are mad sick, yo!"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.content_detail_url(garo_post.pk))
        self.assertEqual(response.data['message'], "My python skills are mad sick, yo!")

        # Kouga tries to update Rei's post.

        response = self.client.patch(self.content_detail_url(zero_post.pk), {
            'message': "Zero can't code for shit.",
            'title': "Kouga's the better coder."
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Yhwh updates Kouga's post

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.yhwh_t.key)
        response = self.client.patch(self.content_detail_url(garo_post.pk), {
            'message': "This is Yhwh. Stop being so vain, Kouga.\n -End Transmission."
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.content_detail_url(garo_post.pk))
        self.assertEqual(response.data['message'],
            "This is Yhwh. Stop being so vain, Kouga.\n -End Transmission.")

    def test_destroy_content(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.yhwh_t.key)

        response = self.client.post(self.category_url, self.category_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.category_url, self.category_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Category.objects.all().count(), 2)

        be = Category.objects.get(title=self.category_1['title'])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.garo.auth_token.key)
        response = self.client.post(self.content_url, {
            'title': "Python is dope.",
            'message': "I love python. Do you love python? PYTHON PYTHON PYTHON.",
            'category': be.pk
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.zero.auth_token.key)
        response = self.client.post(self.content_url, {
            'title': "Python",
            'message': "LALALALALALALALAL PYTHON",
            'category': be.pk
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        garo_post = Content.objects.get(author=self.garo, title='Python is dope.')
        zero_post = Content.objects.get(author=self.zero, title='Python')

        # Kouga tries to delete his post.

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.garo.auth_token.key)
        response = self.client.delete(self.content_detail_url(garo_post.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Kouga tries to delete Rei's post.

        response = self.client.delete(self.content_detail_url(zero_post.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Yhwh deletes Rei's post

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.yhwh_t.key)
        response = self.client.delete(self.content_detail_url(zero_post.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Content.objects.all())
