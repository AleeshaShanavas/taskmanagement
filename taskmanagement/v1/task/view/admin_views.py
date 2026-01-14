# task/admin_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

from v1.account.models import CustomUser
from v1.account.constants import UserType
from v1.task.models import Task
from v1.task.forms import CustomUserCreateForm, CustomUserUpdateForm, \
    TaskAssignmentForm


@login_required
def admin_dashboard(request):
    """Dashboard view for Admins and SuperAdmins.
    Shows users and tasks based on role."""

    user = request.user
    if user.role == UserType.USER:
        return HttpResponseForbidden("Admin access required.")

    context = {
        'is_superadmin': user.role == UserType.SUPER_ADMIN,
        'UserType': UserType
    }
    if user.role == UserType.SUPER_ADMIN:
        users = CustomUser.objects.all()
        tasks = Task.objects.all()
    else:
        users = CustomUser.objects.filter(assigned_admin=user)
        tasks = Task.objects.filter(assigned_to__assigned_admin=user)

    context.update({'users': users, 'tasks': tasks})
    return render(request, 'admin/dashboard.html', context)


@login_required
def view_task_report(request, task_id):
    if request.user.role not in [UserType.ADMIN, UserType.SUPER_ADMIN]:
        return redirect('admin_dashboard')
    
    task = get_object_or_404(Task, id=task_id)
    if task.status != 'COMPLETED':
        return redirect('admin_dashboard')
    
    return render(request, 'admin/task_report.html', {'task': task})

@login_required
def assign_user_to_admin(request, user_id):
    """Assign a User to an Admin (SuperAdmin only).
    Only SuperAdmins can assign users to admins."""

    if request.user.role != UserType.SUPER_ADMIN:
        return redirect('admin_dashboard')
    
    user = get_object_or_404(CustomUser, id=user_id, role=UserType.USER)
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        admin = get_object_or_404(CustomUser, id=admin_id, role=UserType.ADMIN)
        user.assigned_admin = admin
        user.save()
        return redirect('admin_dashboard')
    
    admins = CustomUser.objects.filter(role=UserType.ADMIN)
    return render(
        request, 'admin/assign_user.html', {'user': user, 'admins': admins})


@login_required
def assign_task(request):
    """Assign a task to a user (Admin only).
    Only Admins can assign tasks. They can only assign tasks to users
    assigned to them."""

    if request.user.role != UserType.ADMIN:
        return HttpResponseForbidden("Only Admins can assign tasks.")

    eligible_users = CustomUser.objects.filter(
        assigned_admin=request.user, role=UserType.USER)

    if not eligible_users.exists():
        messages.error(
            request, 
            "You have no users assigned to you. Please contact SuperAdmin.")
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = TaskAssignmentForm(request.POST, user_queryset=eligible_users)
        if form.is_valid():
            form.save()
            messages.success(request, "Task assigned successfully!")
            return redirect('admin_dashboard')
    else:
        form = TaskAssignmentForm(user_queryset=eligible_users)

    return render(request, 'admin/assign_task.html', {'form': form})


@login_required
def create_user(request):
    """Create a new user (SuperAdmin only).
    Only SuperAdmins can create new users."""

    if request.user.role != UserType.SUPER_ADMIN:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('admin_dashboard')
    else:
        form = CustomUserCreateForm()
    admins = CustomUser.objects.filter(role=UserType.ADMIN)
    return render(request, 'admin/create_user.html', {
        'form': form, 'admins': admins, 'USER_TYPE_USER': UserType.USER})


@login_required
def update_user(request, user_id):
    """Update an existing user (SuperAdmin only).
    Only SuperAdmins can update users."""

    if request.user.role != UserType.SUPER_ADMIN:
        return HttpResponseForbidden()
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User '{user.username}' updated!")
            return redirect('admin_dashboard')
    else:
        form = CustomUserUpdateForm(instance=user)
    admins = CustomUser.objects.filter(role=UserType.ADMIN)
    return render(request, 'admin/update_user.html', {
        'form': form, 'user_obj': user, 'admins': admins, 
        'USER_TYPE_USER': UserType.USER
    })

@login_required
def delete_user(request, user_id):
    """Delete a user (SuperAdmin only).
    Only SuperAdmins can delete users."""
    
    if request.user.role != UserType.SUPER_ADMIN:
        return HttpResponseForbidden()
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' deleted!")
        return redirect('admin_dashboard')
    return render(request, 'admin/confirm_delete.html', {'user': user})