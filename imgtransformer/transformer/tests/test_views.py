from io import BytesIO
from PIL import Image

from django.test import SimpleTestCase
from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile


class IndexViewTest(SimpleTestCase):

    def test_view_template(self):
        response = self.client.get(reverse('transformer:index'))
        self.assertTemplateUsed(response, 'index.html')


class RezizeViewTest(SimpleTestCase):

    def test_view_template(self):
        response = self.client.get(reverse('transformer:resize', args=(50,)))
        self.assertTemplateUsed(response, 'transform.html')

    def test_image_resize(self):
        data_list = [
            {
                'original_size': (100, 100),
                'percent': 50,
                'expected_size': (50, 50),
            },
            {
                'original_size': (10, 10),
                'percent': 1,
                'expected_size': (1, 1),
            }
        ]
        for entry in data_list:
            stream = BytesIO()
            Image.new('RGB', entry['original_size']).save(stream, 'JPEG')
            stream.seek(0)
            upload_file = SimpleUploadedFile(
                'image.png', stream.read(), content_type='image/jpeg')
            response = self.client.post(
                reverse('transformer:resize', args=(entry['percent'],)),
                {'file': upload_file}
            )
            img = Image.open(BytesIO(response.content))
            self.assertEqual(entry['expected_size'], img.size)


class RotateViewTest(SimpleTestCase):

    def test_view_template(self):
        response = self.client.get(
            reverse('transformer:rotate', args=('cw', 90)))
        self.assertTemplateUsed(response, 'transform.html')

    def test_image_rotate(self):
        data_list = [
            {
                'original_size': (30, 40),
                'direction': 'cw',
                'degree': 90,
                'expected_size': (40, 30),
            },
            {
                'original_size': (100, 100),
                'direction': 'ccw',
                'degree': 45,
                'expected_size': (142, 142),
            }
        ]
        for entry in data_list:
            stream = BytesIO()
            Image.new('RGB', entry['original_size']).save(stream, 'JPEG')
            stream.seek(0)
            upload_file = SimpleUploadedFile(
                'image.png', stream.read(), content_type='image/jpeg')
            response = self.client.post(
                reverse('transformer:rotate', args=(entry['direction'], entry['degree'],)),
                {'file': upload_file}
            )
            img = Image.open(BytesIO(response.content))
            self.assertEqual(entry['expected_size'], img.size)


class BWViewTest(SimpleTestCase):

    def test_view_template(self):
        response = self.client.get(reverse('transformer:bw'))
        self.assertTemplateUsed(response, 'transform.html')

    def test_bandw_convertion(self):
        stream = BytesIO()
        Image.new('RGB', (100, 100)).save(stream, 'JPEG')
        stream.seek(0)
        upload_file = SimpleUploadedFile(
            'image.png', stream.read(), content_type='image/jpeg')
        response = self.client.post(
            reverse('transformer:bw'),
            {'file': upload_file}
        )
        img = Image.open(BytesIO(response.content))
        self.assertEqual(img.getbands(), ('L',))


class TransformViewTest(SimpleTestCase):

    def test_unsupported_format(self):
        stream = BytesIO()
        Image.new('RGB', (100, 100)).save(stream, 'JPEG')
        stream.seek(0)
        upload_file = SimpleUploadedFile(
            'image.zip', stream.read(), content_type='image/jpeg')
        response = self.client.post(
            reverse('transformer:bw'),
            {'file': upload_file}
        )
        self.assertEqual(response.context['error'], 'This format is not supported')

    def test_jpg_instead_of_jpeg(self):
        stream = BytesIO()
        Image.new('RGB', (100, 100)).save(stream, 'JPEG')
        stream.seek(0)
        upload_file = SimpleUploadedFile(
            'image.jpg', stream.read(), content_type='image/jpeg')
        response = self.client.post(
            reverse('transformer:bw'),
            {'file': upload_file}
        )
        img = Image.open(BytesIO(response.content))
        self.assertEqual(img.getbands(), ('L',))
