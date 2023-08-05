import uuid

import requests
import six
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import URLValidator
from drf_extra_fields.fields import Base64ImageField
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError


class CustomBase64ImageField(Base64ImageField):
    def __init__(self, *args, **kwargs):
        self.url_validator = URLValidator()
        super(CustomBase64ImageField, self).__init__(*args, **kwargs)

    def to_internal_value(self, base64_data):
        if isinstance(base64_data, six.string_types) and base64_data.rsplit(
                '.', 1)[-1] in Base64ImageField.ALLOWED_TYPES:

            request = self.context.get('request')
            media_url = settings.MEDIA_URL
            if request is not None:
                host = '{scheme}://{host}'.format(scheme=request.scheme, host=request.get_host())
                if not media_url.startswith(host):
                    media_url = host + media_url

            if self._verify_local_url(base64_data) and base64_data.startswith(media_url):
                return base64_data.split(settings.MEDIA_URL)[-1]

            return self.to_local_img_path(base64_data).split(settings.MEDIA_URL)[-1]

        return super(CustomBase64ImageField, self).to_internal_value(base64_data)

    def to_local_img_path(self, url):
        """第三方图片路径转为本地图片路径"""

        url = self._valid_url(url)
        if not url:
            raise exceptions.ValidationError('图片路径不正确，请检查上传的图片路径是否正确')

        try:
            data = requests.get(url, timeout=3)
        except (requests.ConnectionError, requests.Timeout):
            raise exceptions.ValidationError('连接超时，无法获取第三方的图片数据，请检查上传的图片路径是否正确')
        except Exception as e:
            raise exceptions.ValidationError('未知错误，无法获取第三方的图片数据，请检查上传的图片路径是否正确')

        img = SimpleUploadedFile(
            '%s.%s' % (''.join(str(uuid.uuid1()).split('-')), url.rsplit('.')[-1]), data.content)

        return default_storage.url(default_storage.save(img.name, img))

    def _valid_url(self, url):
        try:
            self.url_validator(url)
        except ValidationError as e:
            return
        return url

    def _verify_local_url(self, url):
        """验证图片路径是否为本地路径"""

        if '*' in settings.ALLOWED_HOSTS:
            return True

        request = self.context.get('request')
        if request is None:
            return False

        scheme = '{scheme}://'.format(scheme=request.scheme)

        is_local_url = False

        for host in settings.ALLOWED_HOSTS:
            if url.startswith('%s%s' % (scheme, host)):
                is_local_url = True
        return is_local_url
