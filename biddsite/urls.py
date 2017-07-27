from django.conf.urls import url
import views

app_name = 'biddsite'

urlpatterns = [
    url(r'^$',views.index,name='index'),
]
