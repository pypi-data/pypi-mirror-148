import markdown
from django.shortcuts import render
from django.template.loader import get_template
from jinja2 import Environment, PackageLoader
from rest_framework.decorators import action

from .generators import filter_to_vue, viewset_to_vue


class VueMixin(object):
    """
     VIEWSET的mixin 返回一个vue的模板文件
    """

    @action(detail=False, methods=["GET"])
    def vue(self, request, *args, **kwargs):
        filter_content = filter_to_vue(self)
        detail_content = viewset_to_vue(self)
        env = Environment(loader=PackageLoader('vue', 'templates'))
        content = env.get_template('vue_example.md').render(filter_content=filter_content,
                                                            detail_content=detail_content)

        md = markdown.Markdown(
            extensions=[
                # 包含 缩写、表格等常用扩展
                'markdown.extensions.extra',
                # 语法高亮扩展
                'markdown.extensions.codehilite',
                # 目录扩展
                'markdown.extensions.toc',
            ]
        )

        body = md.convert(content)

        # 新增了md.toc对象
        context = {'content': body}

        return render(request, 'vue_example.html', context)
