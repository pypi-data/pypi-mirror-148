from setuptools import setup, find_packages

setup(
    name='django-rest-permission',
    version='0.1.2',
    description='DRF之APIView视图访问权限控制',
    long_description=open('django_rest_permission/README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='PyDa5',
    author_email='1174446068@qq.com',
    url='https://github.com/PyDa5/django-rest-permission',
    packages=find_packages(),
    license='MIT',
    include_package_data=True,
    requires=['django', 'djangorestframework'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
    ]
)
