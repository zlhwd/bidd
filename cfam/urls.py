from django.conf.urls import url
import views

app_name = 'cfam'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^molecules/?$',views.mols,name='mols'),
    url(r'^molecules/(?P<mol_id>[^/]+)/?$',views.mol,name='mol'),
    url(r'^families/?$',views.fams,name='fams'),
    url(r'^families/(?P<fam_id>[^/]+)/?$',views.fam,name='fam'),
]
