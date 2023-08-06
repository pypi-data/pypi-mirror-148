from setuptools import setup, find_packages

setup(
    name='django-rest-permission',
    version='0.1.4',
    description="Access control for APIView of djangorestframework base on properties "
                "of request's method and view's action.",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='PyDa5',
    author_email='1174446068@qq.com',
    url='https://github.com/PyDa5/django-rest-permission',
    packages=find_packages(),
    license='MIT License',
    include_package_data=True,
    data_files=[
        ('.', ['LICENSE', 'README.md', 'requirements.txt', 'setup.py']),
    ],
    requires=['django', 'djangorestframework'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
    ]
)
