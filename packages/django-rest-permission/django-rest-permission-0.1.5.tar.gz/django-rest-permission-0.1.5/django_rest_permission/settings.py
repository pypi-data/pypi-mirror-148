# -*- coding: utf-8 -*-
"""
此配置文件在django settings.py中的配置项为REST_PERMISSION。
"""

# 缓存权限键样式
DEFAULT_USER_PERMISSIONS_CACHE_KEY_PATTERN = 'drp_user:permissions:{user_id}'

APP_LABEL_PATTERN = 'drp_{app_name}'
PERMISSION_CODENAME_PATTERN = 'view://{app_name}/{view_group}/{permission_code}'

VIEW_GROUP_PROP = 'view_group'
VIEW_ACCESS_PERMISSIONS_PROP = 'view_access_permissions'

# 这个配置项会混入到django的配置文件里面去
REST_PERMISSION = {
    'DEFAULT_USER_PERMISSIONS_CACHE_KEY_PATTERN': DEFAULT_USER_PERMISSIONS_CACHE_KEY_PATTERN,
    'APP_LABEL_PATTERN': APP_LABEL_PATTERN,
    'PERMISSION_CODENAME_PATTERN': PERMISSION_CODENAME_PATTERN,
    'VIEW_GROUP_PROP': VIEW_GROUP_PROP,
    'VIEW_ACCESS_PERMISSIONS_PROP': VIEW_ACCESS_PERMISSIONS_PROP
}
