from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.demo,name='demo'),
    path('ewaste/',views.ewaste,name='ewaste'),
    path('reg/',views.reg,name='reg'),
    path('login/',views.login,name='login'),
    path('customer/',views.customer,name='customer'),
    path('prof/',views.prof,name='prof'),
    path('profupdate/',views.prof_update,name='profupdate'),
    path('add_cart/',views.add_cart,name='add_cart'),
    path('view_cart/',views.view_cart,name='view_cart'),
    path('productsummary/',views.productsummary,name='productsummary'),
    path('plusqty/<int:id>/',views.plusqty,name='plusqty'),
    path('minusqty/<int:id>/',views.minusqty,name='minusqty'),
    path('de_cart/<int:id>/', views.de_cart, name='de_cart'),
    path('emptycart/', views.view_cart, name='emptycart'),
    path('pickup1/',views.pickup1,name='pickup1'),
    path('logout/',views.logout,name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('updateProfile/',views.updateProfile,name='updateProfile'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)   
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)