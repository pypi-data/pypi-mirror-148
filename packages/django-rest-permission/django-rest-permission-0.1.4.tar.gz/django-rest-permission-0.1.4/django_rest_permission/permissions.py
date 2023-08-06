# -*- coding: utf-8 -*-
"""
用于在APP的permissions.py中创建通用权限校验类GenericViewPermission，如下：
from django_rest_permission.permissions import getGenericViewPermission

GenericViewPermission = getGenericViewPermission()
...
"""

import inspect
from importlib import import_module
from os.path import dirname, basename, join, exists

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.conf import settings
from django.views.generic.base import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from django_rest_permission.settings import REST_PERMISSION

if not hasattr(settings, 'REST_PERMISSION'):
    setattr(settings, 'REST_PERMISSION', REST_PERMISSION)
else:
    for item_key in REST_PERMISSION:
        if item_key not in settings.REST_PERMISSION:
            settings.REST_PERMISSION[item_key] = REST_PERMISSION[item_key]

DEFAULT_USER_PERMISSIONS_CACHE_KEY_PATTERN = settings.REST_PERMISSION['DEFAULT_USER_PERMISSIONS_CACHE_KEY_PATTERN']
APP_LABEL_PATTERN = settings.REST_PERMISSION['APP_LABEL_PATTERN']
PERMISSION_CODENAME_PATTERN = settings.REST_PERMISSION['PERMISSION_CODENAME_PATTERN']
VIEW_GROUP_PROP = settings.REST_PERMISSION['VIEW_GROUP_PROP']
VIEW_ACCESS_PERMISSIONS_PROP = settings.REST_PERMISSION['VIEW_ACCESS_PERMISSIONS_PROP']

User = get_user_model()


def get_user_permissions_from_cache(request: Request, view: View, perm_cache_key_pattern=None) -> set:
    """
    从缓存获取用户权限集合
    :request 请求对象
    :view 视图函数
    :perm_cache_key_pattern 缓存权限的键名，默认'drp_user:permissions:{user_id}'，pattern需包含{user_id}
    return: 从缓存读取用户权限并返回
    """
    user = request.user

    if isinstance(user, AnonymousUser):
        return set()

    user_id = user.id
    if perm_cache_key_pattern is None:
        cache_key = DEFAULT_USER_PERMISSIONS_CACHE_KEY_PATTERN.format(user_id=user_id)
    else:
        cache_key = perm_cache_key_pattern.format(user_id=user_id)

    perms = cache.get(cache_key, None)
    if perms:
        return perms

    return set()


def cache_user_permissions(request: Request, view: View, max_age, perm_cache_key_pattern=None) -> set:
    """
    从数据库读取用户权限，写入缓存并返回用户权限
    :request 请求对象
    :view 视图函数
    :max_age 权限缓存的时长
    :perm_cache_key_pattern 缓存权限的键名，默认'drp_user:permissions:{user_id}'，pattern需包含{user_id}
    return: 从缓存读取用户权限并返回
    """
    user = request.user

    if isinstance(user, AnonymousUser):
        return set()

    user_permissions = set(request.user.get_user_permissions())
    if not user_permissions:
        return set()

    user_id = user.id
    if perm_cache_key_pattern is None:
        cache_key = DEFAULT_USER_PERMISSIONS_CACHE_KEY_PATTERN.format(user_id=user_id)
    else:
        cache_key = perm_cache_key_pattern.format(user_id=user_id)
    cache.set(cache_key, user_permissions, max_age)

    return user_permissions


def get_and_cache_user_permissions(request: Request, view: View, max_age, perm_cache_key_pattern=None) -> set:
    """
    从缓存读取用户权限，缓存没有，再从数据库读
    :request 请求对象
    :view 视图函数
    :max_age 权限缓存的时长
    :perm_cache_key_pattern 缓存权限的键名，默认'drp_user:permissions:{user_id}'，pattern需包含{user_id}
    return: 从缓存读取用户权限并返回
    """
    user_permissions = get_user_permissions_from_cache(request, view, perm_cache_key_pattern)
    if not user_permissions:
        user_permissions = cache_user_permissions(request, view, max_age)  # 获取用户权限
    return user_permissions


def clear_cache_of_user_permissions(request: Request, view: View, perm_cache_key_pattern=None):
    """
    工具函数，主要用于用户退出、注销
    :request 请求对象
    :view 视图对象
    :perm_cache_key_pattern 缓存键的格式
    """
    user = request.user

    if isinstance(user, AnonymousUser):
        return

    user_id = user.id
    if perm_cache_key_pattern is None:
        cache_key = DEFAULT_USER_PERMISSIONS_CACHE_KEY_PATTERN.format(user_id=user_id)
    else:
        cache_key = perm_cache_key_pattern.format(user_id=user_id)
    cache.delete(cache_key)


def update_cache_of_user_permissions(request: Request, view: View, max_age, perm_cache_key_pattern=None):
    """
    工具函数，主要用于用户登陆重新获取权限
    :request 请求对象
    :view 视图对象
    :max_age 权限缓存多长时间，可以从GenericViewPermission获取permission_max_age赋值给它
    :perm_cache_key_pattern 缓存键的格式
    """
    cache_user_permissions(request, view, max_age, perm_cache_key_pattern=perm_cache_key_pattern)


class _GenericViewPermission(BasePermission):
    """
    视图级别的权限控制，在视图类中定义view_group和view_access_permissions来声明访问视图所需要的权限
    :view_group 在视图中定义的属性，表示权限分组名称（必须）
    :view_access_permissions 在视图中定义的属性，用于表示请求方法对应的权限名称映射关系，取值例如：
                            1、{'GET': (perm_code, perm_name), 'POST': (perm_code, perm_name),...}
                            2、{'GET': perm_code, 'POST': perm_code,...}，value为字符串时，perm_name=perm_code
    """

    def has_permission(self, request: Request, view: View):
        use_cache = getattr(self, 'use_cache')
        permission_max_age = getattr(self, 'permission_max_age')
        perm_cache_key_pattern = getattr(self, 'perm_cache_key_pattern')
        db_app_label_pattern = getattr(self, 'db_app_label_pattern')
        db_permissions_code_pattern = getattr(self, 'db_permissions_code_pattern')
        view_group_name = getattr(self, 'view_group_name')
        view_access_permissions_name = getattr(self, 'view_access_permissions_name')

        view_group = getattr(view, view_group_name)  # 视图名称(对应django_content_type中的model名称)
        view_access_permissions: dict = getattr(view, view_access_permissions_name)  # 映射：请求方法 ==> 权限名称

        method = request.method
        if hasattr(view, 'action'):
            method = getattr(view, 'action')

        # 当前请求所需权限
        if method not in view_access_permissions.keys():
            return True

        user: User = request.user

        # 匿名用户不许登陆
        if isinstance(user, AnonymousUser):
            return False

        # 从缓存读用户权限，缓存无则从数据库读取
        if use_cache:
            user_permissions = get_and_cache_user_permissions(request, view, permission_max_age, perm_cache_key_pattern)
        else:
            user_permissions = user.get_user_permissions()

        # 不存在用户权限不允许访问
        if not user_permissions:
            return False

        app_name = getattr(self, 'app_name')  # 当前视图所在APP名称，从执行gerGenericViewPermission()，从上下文获取

        # 鉴权
        if type(view_access_permissions[method]) == str:
            perm_code = view_access_permissions[method]  # method:perm_code
        else:
            perm_code, perm_name = view_access_permissions[method]  # method: (perm_code, perm_name)
        expected_permission = db_app_label_pattern.format(app_name=app_name) \
                              + '.' \
                              + db_permissions_code_pattern.format(app_name=app_name, view_group=view_group,
                                                                   permission_code=perm_code)
        if expected_permission in user_permissions:
            return True
        return False


def getGenericViewPermission(
        use_cache=True,
        permission_max_age=60 * 60 * 24 * 15,
        perm_cache_key_pattern='drp_user:permissions:{user_id}',
        **kwargs
) -> type:
    """
    返回GenericViewPermission
    """
    # 从配置文件读取
    db_app_label_pattern = APP_LABEL_PATTERN
    db_permissions_code_pattern = PERMISSION_CODENAME_PATTERN
    view_group_name = VIEW_GROUP_PROP
    view_access_permissions_name = VIEW_ACCESS_PERMISSIONS_PROP
    # 校验参数是否正确
    db_app_label_pattern.format(app_name='')
    db_permissions_code_pattern.format(app_name='', view_group='', permission_code='')
    perm_cache_key_pattern.format(user_id='')

    # 获取调用方信息
    previous_frame = inspect.currentframe().f_back
    filename, line_number, function_name, lines, index = inspect.getframeinfo(previous_frame)

    # 获取调用方app.py所在的包名
    fp = filename
    current_dir_path = dirname(fp)
    current_dir_name = basename(current_dir_path)
    while not (exists(join(current_dir_path, '__init__.py')) and exists(join(current_dir_path, 'apps.py'))):
        fp = current_dir_path
        current_dir_path = dirname(fp)
        current_dir_name = basename(current_dir_path)
    caller_package_name = current_dir_name
    try:
        module = import_module(f'{caller_package_name}.apps')
        app_config = getattr(module, f'{caller_package_name[0].upper()+ caller_package_name[1:]}Config')
    except ImportError:
        ImportError('请在app目录下的permissions.py中导入此模块')

    # 构建GenericViewPermission
    klass = _GenericViewPermission

    app_name = getattr(app_config, 'name')
    klass.app_name = app_name

    klass.db_app_label_pattern = db_app_label_pattern
    klass.db_permissions_code_pattern = db_permissions_code_pattern

    klass.view_group_name = view_group_name
    klass.view_access_permissions_name = view_access_permissions_name

    klass.use_cache = use_cache
    klass.permission_max_age = permission_max_age
    klass.perm_cache_key_pattern = perm_cache_key_pattern

    for key in kwargs:
        setattr(klass, key, kwargs[key])

    return klass
