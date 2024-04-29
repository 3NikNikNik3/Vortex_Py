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


def load_file(path):
    with open(path, 'rb') as file:
        ans = SimpleUploadedFile('file', file.read())
    return ans


class TestCaseFileTxt(TestCase):
    fixtures = ['bd.json']

    def setUp(self):
        self.c = Client()
        res = self.c.get('/load')
        self.cook = {'key_user': res.client.cookies['key_user'],
                     'csrftoken': res.client.cookies['csrftoken']}

    def test_load(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/load', {'File': load_file('project/main/tests/1'),
                                    'Type': ''})
        res = self.c.get('/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('text', res.context)
        self.assertEqual(res.context['text'], '\ntest1\n    test2\n   test3')

    def test_save(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/load', {'File': load_file('project/main/tests/1'),
                                    'Type': ''})

        res = self.c.post('/edit', {'save': '', 'text': 'test000', 'sinte': 'none'})
        self.assertEqual(res.status_code, 200)

        res = self.c.get('/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('text', res.context)
        self.assertEqual(res.context['text'], '\ntest000')


class TestCaseFileHtml(TestCase):
    fixtures = ['bd.json']

    def setUp(self):
        self.c = Client()
        res = self.c.get('/load')
        self.cook = {'key_user': res.client.cookies['key_user'],
                     'csrftoken': res.client.cookies['csrftoken']}

    def test_load(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/load', {'File': load_file('project/main/tests/2'),
                                    'Type': 'txt/html'})
        res = self.c.get('/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('text', res.context)
        self.assertEqual(res.context['text'], '''
<html>
    <body>
        <p>test</p>
    </body>
</html>''')

    def test_save(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/load', {'File': load_file('project/main/tests/2'),
                                    'Type': '.html'})

        res = self.c.post('/edit', {'save': '', 'text': 'test000'})
        self.assertEqual(res.status_code, 200)

        res = self.c.get('/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('text', res.context)
        self.assertEqual(res.context['text'], '\ntest000')


class TestCaseFileByte(TestCase):
    fixtures = ['bd.json']

    def setUp(self):
        self.c = Client()
        res = self.c.get('/load')
        self.cook = {'key_user': res.client.cookies['key_user'],
                     'csrftoken': res.client.cookies['csrftoken']}

    def test_load(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/load', {'File': load_file('project/main/tests/3'),
                                    'Type': '(bytes)'})
        res = self.c.get('/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('data', res.context)
        self.assertEqual(res.context['data'], '303031')

    def test_save(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/load', {'File': load_file('project/main/tests/1'),
                                    'Type': '(bytes)'})

        res = self.c.post('/edit', {'save': '', 'bin': 'AAAA'})
        self.assertEqual(res.status_code, 200)

        res = self.c.get('/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('data', res.context)
        self.assertEqual(res.context['data'], 'AAAA')


class TestCaseNewFile(TestCase):
    fixtures = ['bd.json']

    def setUp(self):
        self.c = Client()
        res = self.c.get('/load')
        self.cook = {'key_user': res.client.cookies['key_user'],
                     'csrftoken': res.client.cookies['csrftoken']}

    def test_new(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.get('/new')
        self.assertEqual(res.status_code, 200)

    def test_new_txt(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/new', {'type': 'txt/text'})
        self.assertRedirects(res, '/edit')

        res = self.c.get('/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('text', res.context)
        self.assertEqual(res.context['text'], '\n')

    def test_new_html(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/new', {'type': 'txt/html'})
        self.assertRedirects(res, '/edit')

        res = self.c.get('/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('text', res.context)
        self.assertEqual(res.context['text'], '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Page</title>
</head>
<body>

</body>
</html>''')

    def test_new_bin(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/new', {'type': 'bin/bin'})
        self.assertRedirects(res, '/edit')

        res = self.c.get('/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('data', res.context)
        self.assertEqual(res.context['data'], '00')

    def test_new_jup(self):
        self.c.cookies = SimpleCookie(self.cook)
        res = self.c.post('/new', {'type': 'jup/jup'})
        self.assertRedirects(res, '/edit')

        res = self.c.get('/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('count', res.context)
        self.assertEqual(res.context['count'], 1)
        self.assertIn('metadata', res.context)
        self.assertEqual(res.context['metadata'], {})
        self.assertIn('type', res.context)
        self.assertEqual(res.context['type'], 'none')
        self.assertIn('blocks', res.context)
        self.assertEqual(res.context['blocks'], [{'id': 0, 'value': ''}])
