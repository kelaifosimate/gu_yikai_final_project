from django.conf.urls import url, re_path
from django.views.static import serve
from fleamarket import settings
from .views import *

app_name = 'fm_user'

urlpatterns = [
    url(r'^register/$', register, name="register"),
    url(r'^register_handle/$', register_handle, name="register_handle"),
    url(r'^register_exist/$', register_exist, name="register_exist"),
    url(r'^login/$', login, name="login"),
    url(r'^login_handle/$', login_handle, name="login_handle"),
    url(r'^info/$', info, name="info"),
    url(r'^order/(\d+)$', order, name="order"),
    url(r'^site/$', site, name="site"),
    url(r'^publishers/$', publishers, name="publishers"),
    url(r'^changeInformation/$', changeInformation, name="changeInformation"),
    url(r'^check_user/$', check_user, name="check_user"),
    url('^myself_information/$', myself_information, name="myself_information"),
    url('^seller_information/(.+)/$', seller_information, name="seller_information"),
    url('^message/$', message, name="message"),
    url('^person_message/$', person_message, name="person_message"),
    url(r'^logout/$', logout, name="logout"),
    # 删除验证码相关路由
    # url(r'^verify_show/$', verify_show, name="verify_show"),
    # url(r'^verifycode/$', viewsUtil.verify_code, name="verifycode"),
    url(r'^changeInPwd/$', changeInPwd, name="changeInPwd"),
    url(r'^findpwdView/$', findpwdView, name="findpwdView"),
    url(r'^return_item/$', return_item, name="return_item"),
    re_path('^media/(?P<path>.*)/$', serve, {'document_root': settings.MEDIA_ROOT}),
]