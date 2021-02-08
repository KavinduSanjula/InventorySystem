from django import forms
from .models import Item, Stock, Transaction

class ItemForm(forms.ModelForm):
	barcode_number = forms.IntegerField(required=False)
	class Meta:
		model = Item
		fields = ['item_name', 'barcode_number', 'category', 'purchase_price', 'sels_price']

class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['item','qty']

class TransactionForm(forms.ModelForm):
	class Meta:
		model = Transaction
		fields = ['item', 'qty', 'transaction_type']