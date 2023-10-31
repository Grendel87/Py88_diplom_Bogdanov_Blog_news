from django.test.testcases import TestCase

from django.contrib.auth import get_user_model

User = get_user_model()


class TestRegistration(TestCase):
    def setUp(self) -> None:
        self.registration_data = {
            'email': 'alex@mail.ru',
            'password': 'Hjkggghjd88s',
        }

    def test_registration_users(self):
        response = self.client.post('http://localhost:8000/sign-up/', data=self.registration_data)
        self.assertEqual(response.status_code, 302)

        alex = User.objects.first()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(alex.email, self.registration_data['email'])
