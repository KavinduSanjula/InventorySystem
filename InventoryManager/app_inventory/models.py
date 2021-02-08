from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
	category_name = models.CharField(max_length=100,unique=True)

	def __str__(self):
		return self.category_name

class TransactionType(models.Model):
	transaction_type = models.CharField(max_length=10)

	def __str__(self):
		return self.transaction_type

class Item(models.Model):
	item_name = models.CharField(max_length=100)
	barcode_number = models.IntegerField(null=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
	purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
	sels_price = models.DecimalField(max_digits=12, decimal_places=2)

	def __str__(self):
		return self.item_name

class Stock(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	qty = models.IntegerField()

	def __str__(self):
		return self.item.item_name

class Transaction(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	qty = models.IntegerField()
	transaction_time = models.DateField(auto_now_add=True)
	transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	
	def __str__(self):
		return self.item.item_name + ' | ' + str(self.transaction_time)



