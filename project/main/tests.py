from django.test import TestCase, Client
from http.cookies import SimpleCookie
from django.core.files.uploadedfile import SimpleUploadedFile


class TestCaseNotFile(TestCase):
    fixtures = ['bd.json']

    def setUp(self):
        self.c = Client()

    def test_page_main(self):
        res = self.c.get('/')
        self.assertEqual(res.status_code, 200)

    def test_page_save(self):
        res = self.c.get('/save')
        self.assertRedirects(res, '/load')

    def test_page_edit(self):
        res = self.c.get('/edit')
        self.assertRedirects(res, '/load')

    def test_page_transform(self):
        res = self.c.get('/transform')
        self.assertRedirects(res, '/load')

    def test_page_load(self):
        res = self.c.get('/load')
        self.assertEqual(res.status_code, 200)
        self.assertIn('key_user', res.client.cookies)


class TestCaseLoad(TestCase):
    fixtures = ['bd.json']
    def setUp(self):
        self.c = Client()
        res = self.c.get('/load')
        self.cook = {'key_user': res.client.cookies['key_user'],
                     'csrftoken': res.client.cookies['csrftoken']}

    def test_page_load(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/load', {'File': SimpleUploadedFile('tests/1', b'file_content'),
                                    'Type': ''})
        self.assertRedirects(res, '/edit')

    def test_bad_load_1(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/load', {'File': SimpleUploadedFile('tests/1', b'file_content')})
        self.assertNotEqual(res.status_code, 302)

    def test_bad_load_2(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/load', {'Type': ''})
        self.assertNotEqual(res.status_code, 302)

    def test_bad_load_3(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/load', {})
        self.assertNotEqual(res.status_code, 302)

class TestCaseFileTxt(TestCase):
    fixtures = ['bd.json']

    def setUp(self):
        self.c = Client()
        res = self.c.get('/load')
        self.cook = {'key_user': res.client.cookies['key_user'],
                     'csrftoken': res.client.cookies['csrftoken']}

    def test_load(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/load', {'File': SimpleUploadedFile('tests/1', b'file_content'),
                                    'Type': ''})
        res = self.c.get('/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('text', res.context)
        self.assertEqual(res.context['text'], '\ntest1\ttest2   test3')

    def test_save(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/load', {'File': SimpleUploadedFile('tests/1', b'file_content'),
                                    'Type': ''})

        res = self.c.post('/edit', {'save': '', 'text': 'test000', 'sinte': 'none'})
        self.assertEqual(res.status_code, 200)

        res = self.c.get('/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('text', res.context)
        self.assertEqual(res.context['text'], 'test000')