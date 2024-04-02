from django.contrib import admin
from django.urls import path
from socoldapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',views.home),
    path('pdetails/<pid>',views.pdetails),
    path('cartt',views.cart),
    path('orderr',views.order),
    path('aboutt',views.about),
    path('contactt',views.contact),
    path('registerr',views.register),
    path('loginn',views.user_login),
    path('logoutt',views.user_logout),
    path('password_reset_view',views.password_reset_view),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('viewcart',views.viewcart),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment/', views.makepayment),
    path('search/',views.search_view),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)