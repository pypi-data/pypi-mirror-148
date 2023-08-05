###  使用方法
> 1.安装
```cmd
pip install drf-vue
```

> 2 . 在setting.py引入 vue
```python
INSTALLED_APPS = [
    ....
    'vue'
]
```
> 3.在viewset中使用
```python
from vue.mixins import VueMixin
class xxViewSet( VueMixin): 

```

> 4.访问url获取示例代码
只需要在路由后面加上/vue即可查看示例代码
eg: http://127.0.0.1:8000/api/xx/xxservice/vue/

