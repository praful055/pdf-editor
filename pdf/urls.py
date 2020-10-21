from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('',views.home,name='pdf-home'),
    path('home',views.home1,name='home'),
    path('about',views.about,name='pdf-about'),
    path('split',views.split,name="split"),
    path('split1',views.split1,name="split1"),
    path('download1',views.download1,name="download1"),
    path('download2',views.download2,name="download2"),
    path('web',views.web,name="web"),
    path('web1',views.web1,name="web1"),
    path('merge',views.merge,name="merge"),
    path('merge1',views.merge1,name="merge1"),
    path('compress',views.compress,name="compress"),
    path('compress1',views.compress1,name="compress1"),
    path('encrypt',views.encrypt,name="encrypt"),
    path('encrypt1',views.encrypt1,name="encrypt1"),
    path('image',views.image,name="image"),
    path('image1',views.image1,name="image1"),
    path('register',user_views.register,name="register"),
    path('login',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('profile',user_views.profile,name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)