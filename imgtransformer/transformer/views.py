from PIL import Image

from django.views.generic import TemplateView
from django.http import HttpResponse

from .forms import UploadImgForm


class IndexView(TemplateView):
    template_name = 'index.html'


class TransformView(TemplateView):
    template_name = 'transform.html'
    ACCEPTED_FORMATS = ('gif', 'jpeg', 'png', 'tiff')
    AVAILABLE_TRANSFORMATIONS = ('rotate', 'resize', 'bw')
    VIEW_DESCRIPTION = None

    def transform(self, source, destination, **kwargs):
        # Override this method to perform custom transformation
        pass

    def get(self, request, *args, **kwargs):
        img_form = UploadImgForm()
        err = kwargs.get('error', None)
        description = self.VIEW_DESCRIPTION
        kwargs.update({
            'form': img_form,
            'description': description,
            'error': err,
        })
        return super(TransformView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES['file']
        extension = uploaded_file.name.split('.')[-1]
        if extension == 'jpg':
            extension = 'jpeg'
        if extension not in self.ACCEPTED_FORMATS:
            kwargs['error'] = 'This format is not supported'
            return self.get(request, *args, **kwargs)
        response = HttpResponse(content_type="image/{}".format(extension))
        self.transform(source=uploaded_file, destination=response, extension=extension, **kwargs)
        return response


class RotateView(TransformView):

    def transform(self, source, destination, extension, direction, degree):
        if direction == 'cw':
            degree = -1 * int(degree)
        else:
            degree = int(degree)
        img = Image.open(source)
        img.rotate(degree, expand=True).save(destination, extension)

    def get(self, request, direction, degree, *args, **kwargs):
        self.VIEW_DESCRIPTION = 'Rotate by {}° {}.'.format(
            degree,
            'clockwise' if direction == 'cw' else 'counterclockwise'
        )
        return super(RotateView, self).get(request, direction, degree, *args, **kwargs)


class BWView(TransformView):
    VIEW_DESCRIPTION = 'Transform RGB to Black and White'

    def transform(self, source, destination, extension):
        img = Image.open(source)
        img.convert('L').save(destination, extension)


class ResizeView(TransformView):

    def transform(self, source, destination, extension, pct):
        img = Image.open(source)
        sizex = img.width * int(pct) // 100
        if sizex == 0:
            sizex = 1
        sizey = img.height * int(pct) // 100
        if sizey == 0:
            sizey = 1
        img.resize((sizex, sizey)).save(destination, extension)

    def get(self, request, pct, *args, **kwargs):
        self.VIEW_DESCRIPTION = 'Resize image to {}%.'.format(pct)
        return super(ResizeView, self).get(request, pct, *args, **kwargs)
