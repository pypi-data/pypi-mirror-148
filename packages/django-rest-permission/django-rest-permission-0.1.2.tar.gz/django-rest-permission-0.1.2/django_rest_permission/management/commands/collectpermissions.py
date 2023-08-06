# -*- coding: utf-8 -*-
"""
视图权限入库
python manage.py collectpermissions
python manage.py collectpermissions app_name
"""
import os
import re
from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction
from django.views.generic.base import View

from django_rest_permission.apps import DrfPermConfig


def validate_perm_code(codename: str):
    """
    权限名称命名必须以字母开头，且只能包含小写字母、数字和下划线
    """
    pattern = r'[a-z\u4e00-\u9fa5][a-z0-9_\u4e00-\u9fa5]*'
    match_result = re.compile(pattern).fullmatch(codename)
    if not match_result:
        raise ValueError('权限名称命名必须以字母开头，且只能包含小写字母、数字、下划线或中文字符')


def get_app_installed_modules(app_name):
    """
    遍历获取APP中的所有模块
    :app_name settings.py中加载的app名称
    """
    _modules = []

    # 不查找APP中这些目录中的模块
    exclude_dirs = ['static', 'templates', 'templatetags', 'migrations', 'management']
    # 不查找APP中的这些模块
    exclude_modules = ['admin.py', 'apps.py', 'models.py', 'serializers.py', 'permissions', 'forms.py']

    # 确保包存在
    try:
        app = __import__(app_name)
    except:
        raise ModuleNotFoundError(f'the app "{app_name}" not found')
    app_path = str(app.__path__[0])

    # 遍历获取包中所有的模块
    current_pkg_path = ''
    for root, dns, fns in os.walk(app_path):
        dn = os.path.basename(root)  # 遍历到的文件夹名称
        if root == app_path:
            current_pkg_path = app_name
        else:
            current_pkg_path = '.'.join([app_name, root[len(app_path) + 1:].replace('\\', '.').replace('/', '')])
        if dn in exclude_dirs:  # 排除肯定不包含视图的文件夹
            continue
        if '..' in current_pkg_path:  # 排除隐藏文件夹
            continue
        if '__' in current_pkg_path:  # 排除双下划线的目录
            continue
        for fn in fns:
            if not fn.endswith('.py'):  # 排除非py文件
                continue
            if fn.startswith('__'):  # 排除双下划线文件
                continue
            if fn in exclude_modules:  # 排除不可能是视图文件的文件
                continue
            # 去掉后缀的文件名
            fn_no_sfx = fn[:-3]
            # 获取APP中模块的实例
            _module_path = '.'.join([current_pkg_path, fn_no_sfx])
            _module = import_module(_module_path)
            _modules.append(_module)
    return _modules


def get_all_apps_installed_modules():
    """
    获取所有已加载APP中的所有模块
    """
    _all_modules = []
    installed_apps = [
        app_name for app_name in settings.INSTALLED_APPS
        if not app_name.startswith(('django.', 'rest_framework', DrfPermConfig.name))
    ]
    for installed_app in installed_apps:
        app_modules = get_app_installed_modules(installed_app)
        _all_modules.extend(app_modules)
    return _all_modules


def collect_modules_permissions(modules: list):
    """权限收集入库"""
    with transaction.atomic():
        for module in modules:
            for module_prop_name in dir(module):
                # 双下划线开头的跳过
                if module_prop_name.startswith('__'):
                    continue
                module_prop = getattr(module, module_prop_name)
                # 不是类的跳过
                if not isinstance(module_prop, type):
                    continue
                # 不继承View的跳过
                if View not in module_prop.__mro__:
                    continue
                # 不包含view_name和view_actions的跳过
                if VIEW_GROUP_PROP not in dir(module_prop):
                    continue
                if VIEW_ACCESS_PERMISSIONS_PROP not in dir(module_prop):
                    continue

                app_name = str(module_prop.__module__).split('.')[0]
                view_group = getattr(module_prop, VIEW_GROUP_PROP)
                view_access_permissions = getattr(module_prop, VIEW_ACCESS_PERMISSIONS_PROP)

                # 往django_content_type表存放app_label、model_name
                content_type = {
                    'app_label': APP_LABEL_PATTERN.format(app_name=app_name),
                    'model': str(view_group).strip()
                }
                obj: ContentType = ContentType.objects.filter(**content_type).first()
                if obj is None:
                    obj = ContentType()
                    obj.app_label = APP_LABEL_PATTERN.format(app_name=app_name)
                    obj.model = str(view_group).strip()
                    obj.save()
                content_type_id = obj.pk

                # 往auth_permissions表存放name、content_id、codename
                for request_method in view_access_permissions:
                    perm_desc = view_access_permissions[request_method]
                    if isinstance(perm_desc, str):
                        perm_code = perm_name = perm_desc
                    else:
                        perm_code, perm_name = perm_desc
                    validate_perm_code(perm_code)
                    codename = PERMISSION_CODENAME_PATTERN.format(
                            app_name=app_name,
                            view_group=view_group,
                            permission_code=perm_code
                        )
                    perm = {
                        'name': perm_name,
                        'content_type_id': content_type_id,
                        'codename': codename
                    }

                    obj: Permission = Permission.objects.filter(**perm).first()
                    if obj is None:
                        Permission.objects.create(**perm)
                        print(f'{app_name} ==> {codename}')
    print('ok')


def collect_all_installed_apps_access_permissions():
    """收集所有APP的视图访问权限"""
    collect_modules_permissions(get_all_apps_installed_modules())


def collect_installed_app_access_permissions(app_name):
    """收集特定app的视图访问权限"""
    collect_modules_permissions(get_app_installed_modules(app_name))


class Command(BaseCommand):
    help = 'collect custom permissions from all View from all installed apps'
    requires_migrations_checks = True
    requires_system_checks = []

    def add_arguments(self, parser):
        parser.add_argument(
            'app_name',
            nargs='?',
            help='为指定的APP做权限迁移'
        )

    def handle(self, *args, **options):
        if options['app_name'] is None:
            collect_all_installed_apps_access_permissions()
        else:
            collect_installed_app_access_permissions(options['app_name'])
