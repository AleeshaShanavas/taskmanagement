from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

from v1.account.constants import UserType

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Authenticate user and return JWT tokens along with user ID and role.
    Expects 'username' and 'password' in the request data.
    Returns refresh and access tokens, user ID, and role on success.
    """

    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        if user.role != UserType.USER:
            return Response({
                'error': 'You are not allowed to login via API.'},
                status=status.HTTP_403_FORBIDDEN)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh), 'access': str(refresh.access_token),
            'user_id': user.id, 'role': user.role})
    return Response({
        'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


def panel_login(request):
    """Render login form and authenticate admin users for admin panel access."""

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'admin/login.html', {'form': form})