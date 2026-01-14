from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from v1.account.models import CustomUser
from v1.account.constants import UserType
from v1.task.models import Task


class TaskAssignmentForm(forms.ModelForm):
    """Form for assigning tasks to users."""

    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        """Extract custom kwarg for user queryset"""

        user_queryset = kwargs.pop('user_queryset', None)
        super().__init__(*args, **kwargs)

        if user_queryset is not None:
            self.fields['assigned_to'].queryset = user_queryset
            if not user_queryset.exists():
                self.fields['assigned_to'].widget = forms.HiddenInput()
                self.fields['assigned_to'].required = False
        else:
            self.fields['assigned_to'].queryset = CustomUser.objects.none()

    def clean_assigned_to(self):
        """Ensure assigned_to is provided unless hidden."""
        assigned_to = self.cleaned_data.get('assigned_to')
        if not assigned_to and \
            self.fields['assigned_to'].widget.__class__ != forms.HiddenInput:
            raise forms.ValidationError("You must assign this task to a user.")
        return assigned_to


class CustomUserCreateForm(UserCreationForm):
    """Form for creating users with role and assigned_admin."""

    role = forms.ChoiceField(choices=UserType.choices)
    assigned_admin = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role=UserType.ADMIN),
        required=False, help_text="Required if role is 'User'")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')

    def clean(self):
        """Validate assigned_admin based on role."""
        cleaned_data = super().clean()
        role = int(cleaned_data.get('role'))
        assigned_admin = cleaned_data.get('assigned_admin')
        if role == UserType.USER and not assigned_admin:
            self.add_error(
                'assigned_admin', "User must be assigned to an Admin.")
        return cleaned_data

    def save(self, commit=True):
        """Save user with role and assigned_admin."""
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if user.role == UserType.USER:
            user.assigned_admin = self.cleaned_data['assigned_admin']
        else:
            user.assigned_admin = None
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(UserChangeForm):
    """Form for updating users with role and assigned_admin."""

    password = None
    role = forms.ChoiceField(choices=UserType.choices)
    assigned_admin = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role=UserType.ADMIN), required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'assigned_admin')

    def __init__(self, *args, **kwargs):
        """Hide assigned_admin field for non-User roles."""
        super().__init__(*args, **kwargs)
        if self.instance.role != UserType.USER:
            self.fields['assigned_admin'].widget = forms.HiddenInput()

    def clean(self):
        """Validate assigned_admin based on role."""
        cleaned_data = super().clean()
        role = int(cleaned_data.get('role'))
        assigned_admin = cleaned_data.get('assigned_admin')
        if role == UserType.USER and not assigned_admin:
            self.add_error(
                'assigned_admin', "User must be assigned to an Admin.")
        if role != UserType.USER:
            cleaned_data['assigned_admin'] = None
        return cleaned_data

    def save(self, commit=True):
        """Save user with role and assigned_admin."""
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if user.role == UserType.USER:
            user.assigned_admin = self.cleaned_data['assigned_admin']
        else:
            user.assigned_admin = None
        if commit:
            user.save()
        return user