from . import views
from django.urls import path

urlpatterns = [
    path('',views.demo,name='demo'),
    path('ewaste/',views.ewaste,name='ewaste'),
    path('reg/',views.reg,name='reg'),
    path('login/',views.login,name='login'),
    path('customer/',views.customer,name='customer'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('pluscart/',views.pluscart,name='pluscart'),
    path('minuscart/',views.minuscart,name='minuscart'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('emptycart/', views.show_cart, name='emptycart'),
    # path('cart/',views.cart,name='cart'),
    # path('checkout/',views.checkout,name='checkout'),
    path('pickup/',views.pickup,name='pickup'),
    path('logout/',views.logout,name='logout'),
    path('base/',views.base,name='base'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('updateProfile/',views.updateProfile,name='updateProfile'),
    # path('logout/',views.logout,name='login')

]
