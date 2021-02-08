from django.urls import path
from .views import *

urlpatterns = [
	path('',index, name='index'),
	path('stock/', stock, name='stock'),
	path('stock/delete/<int:id>', delete_stock, name='delete-stock'),
	path('add-product/', add_item, name='add-item'),
	path('add-stock/', add_stock, name='add-stock'),
	path('add-stock/<int:id>/', add_stock, name='update-stock'),
	path('transactions/', transactions, name='transactions'),
	path('make-transaction/', make_transaction, name='make-transaction'),
	path('transactions/delete/<int:id>/', delete_transaction, name='delete-transaction'),

]