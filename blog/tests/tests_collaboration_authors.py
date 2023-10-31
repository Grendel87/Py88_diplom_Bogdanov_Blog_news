from django.test.testcases import TestCase

from django.contrib.auth import get_user_model

from blog.models import Article

User = get_user_model()


class TestRegistration(TestCase):
    def setUp(self) -> None:
        self.user_first = {
            'email': 'alex@mail.ru',
            'password': 'Hjkggghjd88s',
        }
        self.user_second = {
            'email': 'dima@mail.ru',
            'password': 'Hjkggghjd88s',
        }

        self.article = {
            'title': 'This is good new',
            'content': 'This is good content'
        }

    def test_registration_users(self):
        self.client.post('http://localhost:8000/sign-up/', data=self.user_first)
        self.client.post('http://localhost:8000/sign-up/', data=self.user_second)

        self.client.login(email=self.user_second['email'], password=self.user_second['password'])
        self.client.post('http://localhost:8000/create-article/', self.article)

        art = Article.objects.first()
        response = self.client.post('http://localhost:8000/create-collaboration/', {
            'collaborate_email': self.user_first['email'],
            'article_id': art.id,
        })

        self.assertEqual(response.status_code, 302)

        user_first = User.objects.get(email=self.user_first['email'])
        self.assertEqual(user_first.article_set.get_queryset().count(), 1)
