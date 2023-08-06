from django.urls import path
from django.conf.urls import url
from .views import getToolPage, get_group_ajax, create_new_group, merge_groups, remove_member, get_singles, get_groups, get_single_ajax

app_name = "dubletten_tool"

urlpatterns = [
    path("start/", getToolPage.as_view(), name="tool_page"),
    path("create_group/", create_new_group, name="create_new_group"),
    path("get_singles/", get_singles, name="get_singles"),
    url(r"^get_single_ajax/(?P<s_id>[0-9]+)/$", get_single_ajax, name="get_single_ajax"),
    #url(r"^get_singles/(?P<val>[a-zA-Zäöüß#\-\_()]+)/(?P<type>[a-zA-Zäöüß#\_\-]+)/$", get_singles, name="get_singles"),
    url(r"^get_singles/(?P<val_name>[a-zA-Zäöüß#\-\_()]+)/(?P<val_first>[a-zA-Zäöüß#\_\-]+)/$", get_singles, name="get_singles"),
    url(r"^get_groups/(?P<val>[a-zA-Zäüöß_]+)/$", get_groups, name="get_groups"),
    path("merge_groups/", merge_groups, name="merge_groups"),
    url(r"^get_group/(?P<g_id>[0-9]+)/$", get_group_ajax, name="get_group_ajax"),
    url(r"^remove_member/(?P<group_id>[0-9]+)/(?P<per_id>[0-9]+)/$", remove_member, name="remove_member"),


]