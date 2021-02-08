from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ItemForm, StockForm, TransactionForm
from .models import Stock, Item, Transaction, TransactionType, Category


# Views

def index(request):
	return render(request, 'app_inventory/index.html')

def stock(request):
	if not request.session.get('user'):
		return redirect('/app_user/login')

	inventory = Stock.objects.all()
	return render(request, 'app_inventory/stock.html', {'inventory':inventory})

def delete_stock(request, id=0):
	stock = Stock.objects.get(pk=id)
	stock.delete()
	messages.add_message(request, messages.SUCCESS, 'Stock Deleted Succsesfully!')
	return redirect('/stock')


def add_item(request):
	if not request.session.get('user'):
		return redirect('/app_user/login')

	if request.method == 'POST':
		form = ItemForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request,messages.SUCCESS,'Item Added Sucsessfully!')
			return redirect('/')
	else:
		form = ItemForm()
		return render(request, 'app_inventory/add_item.html',{'form':form})

def add_stock(request, id=0):
	if not request.session.get('user'):
		return redirect('/app_user/login')

	if request.method == 'POST':
		if id == 0:
			form = StockForm(request.POST)
		else:
			stock = Stock.objects.get(pk=id)
			form = StockForm(request.POST, instance=stock)
			
		if form.is_valid():
			if id == 0:
				item = form.cleaned_data['item']
				try:
					stock = Stock.objects.get(item=item)
					stock.qty += form.cleaned_data['qty']
					stock.save()
				except:
					form.save()
			else:
				form.save()
			messages.add_message(request, messages.SUCCESS, 'Stock Updated!')
			return redirect('/inventory')
	else:
		if id == 0:
			form = StockForm()
		else:
			stock = Stock.objects.get(pk=id)
			form = StockForm(instance=stock)
		return render(request, 'app_inventory/add_stock.html', {'form':form})

def make_transaction(request):
	if not request.session.get('user'):
		return redirect('/app_user/login')

	if request.method == 'POST':
		form = TransactionForm(request.POST)
		if form.is_valid():

			stock = None
			item = form.cleaned_data['item']
			transaction_type = form.cleaned_data['transaction_type'].transaction_type
			quantity = form.cleaned_data['qty']
			transaction_status = False

			try:
				stock = Stock.objects.get(item=item)
			except:
				stock = Stock(item=item, qty=0)

			if transaction_type.lower() == 'buy':
				stock.qty += quantity
				stock.save()
				transaction_status  = True

			elif transaction_type.lower() == 'sell':
				if stock.qty >= quantity:
					stock.qty -= quantity
					stock.save()
					transaction_status  = True
				else:
					messages.add_message(request,messages.WARNING, 'No Stocks to Sell!')
					return redirect('/transactions')

			if transaction_status:
				user = User.objects.get(pk=request.session.get('user'))
				transaction = form.save(commit=False)
				transaction.user = user
				transaction.save()

			messages.add_message(request,messages.SUCCESS,'Transaction Created Sucsessfully!')
			return redirect('/transactions')
	else:
		form = TransactionForm()
		return render(request, 'app_inventory/make_transaction.html', {'form':form})

def delete_transaction(request, id=0):
	if not request.session.get('user'):
		return redirect('/app_user/login')

	transaction = Transaction.objects.get(pk=id)

	item = transaction.item
	quantity = transaction.qty
	transaction_type = transaction.transaction_type.transaction_type
	stock = Stock.objects.get(item=item)

	if transaction_type.lower() == 'buy':
		stock.qty -= quantity
		stock.save()

	elif transaction_type.lower() == 'sell':
		stock.qty += quantity
		stock.save()

	transaction.delete()
	messages.add_message(request,messages.SUCCESS,'Transaction Reverted Sucsessfully!')
	return redirect('/transactions')

def get_transactions(category='all', start_date='', end_date=''):
	if category != 'all':
		transactions = Transaction.objects.filter(item__category=Category.objects.get(category_name=category))
	else:
		transactions = Transaction.objects.all()
	return transactions
		

def transactions(request):
	if not request.session.get('user'):
		return redirect('/app_user/login')

	if request.method == 'POST':
		transactions = get_transactions(request.POST['category'],request.POST['start_date'],request.POST['end_date'])
		categories = Category.objects.all()
		return render(request, 'app_inventory/transactions.html', {'transactions':transactions, 'categories':categories})

	else:
		transactions = get_transactions()
		categories = Category.objects.all()
		return render(request, 'app_inventory/transactions.html', {'transactions':transactions, 'categories':categories})

