from django.urls import path
from . import views

urlpatterns = [
    path('drugs/', views.drug_search, name='drug_search'),
    path('drugs/<str:set_id>/', views.product_detail, name='product_detail'),
    path('distinct-values/', views.distinct_values, name='distinct_values'),
    # Drug-Drug interactions
    path('check-drug-interactions/', views.check_drug_interactions, name='check-drug-interactions'),

    # DISEASES SEARCH
    path('diseases/', views.disease_search, name='disease_search'),

    # CPT
    path('cpt/', views.cpt_search, name='cpt_search'),
]