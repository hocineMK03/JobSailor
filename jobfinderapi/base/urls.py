from django.urls import path,include
from . import views
urlpatterns = [
    path('home',views.home,name="home"),
    path('acceuil',views.heropage,name="heropage"),
    path('log_view',views.log_view,name="log_view"),

    path('register_view',views.register_view,name="register_view"),
    path('api/render/paginatejob',views.paginatingforbrowser,name="paginatingforbrowser"),
    path('api/render/paginatepending',views.paginateforpendings,name="paginateforpendings"),
    path('api/validation/validthetype',views.validthetype,name="validthetype"),
    path('api/authentification/login',views.log,name="log"),
    path('api/getcsrf',views.get_csrf_token,name="get_csrf_token"),
    path('api/authentification/register',views.reg,name="reg"),
    path('api/authentification/logout',views.out,name="out"),
    path('api/joblisting/addjob',views.addjob,name="addjob"),
    path('api/joblisting/editjob',views.editjob,name="editjob"),
    path('api/joblisting/deletejob',views.deletejob,name="deletejob"),
    path('api/joblisting/acceptjoboffer',views.acceptjoboffer,name="acceptjoboffer"),
    path('api/joblisting/pendingjobapply',views.pendingjobapply,name="pendingjobapply"),
    path('api/joblisting/addordeletepending',views.addordeletepending,name="addordeletepending"),
    path('api/joblisting/deletependingandaccepts',views.deletependingandaccepts,name="deletependingandaccepts"),

    path('api/joblisting/showjobappliers',views.showjobappliers,name="showjobappliers"),
    path('api/messageconfig/messageadd',views.messageadd,name="messageadd"),
    path('api/messageconfig/messagedelete',views.messagedelete,name="messagedelete"),
    path('api/messageconfig/messagedisplay',views.messagedisplay,name="messagedisplay"),

    path('api/display/profil/<str:name>/',views.profildisplay,name="profildisplay"),
  ]
