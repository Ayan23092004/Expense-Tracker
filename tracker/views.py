from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Sum
from .models import Expense
from .forms import ExpenseForm
from django.http import HttpResponse


# 1. User Registration View (New for Deployment)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after registration
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# 2. User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# 3. Dashboard View with Chart Analytics
@login_required
def dashboard(request):
    # Filter expenses belonging to the logged-in user
    expenses = Expense.objects.filter(user=request.user)

    # Calculate Grand Total using Django Aggregation
    total_data = expenses.aggregate(Sum('amount'))
    total = total_data['amount__sum'] or 0

    # Prepare Category-wise data for Chart.js
    category_qs = expenses.values('category').annotate(total_amount=Sum('amount'))
    labels = [item['category'] for item in category_qs]
    data = [float(item['total_amount']) for item in category_qs]

    # Handle Category Filtering
    category_filter = request.GET.get('category')
    if category_filter:
        expenses = expenses.filter(category=category_filter)

    return render(request, 'dashboard.html', {
        'expenses': expenses,
        'total': total,
        'labels': labels,
        'data': data
    })


# 4. Add Expense View
@login_required
def add_expense(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        return redirect('dashboard')
    return render(request, 'add_expense.html', {'form': form})


# 5. Edit Expense View
@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'edit_expense.html', {'form': form})


# 6. Delete Expense View
@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return redirect('dashboard')


# 7. Logout View
def user_logout(request):
    logout(request)
    return redirect('login')