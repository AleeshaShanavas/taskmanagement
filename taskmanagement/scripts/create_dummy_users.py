from v1.account.models import CustomUser
from v1.account.constants import UserType

# SuperAdmin
su = CustomUser.objects.create_user('super', 'pass', role=UserType.SUPER_ADMIN)
su.set_password('pass'); 
su.save()

# Admin
admin = CustomUser.objects.create_user('admin1', 'pass', role=UserType.ADMIN)
admin.set_password('pass'); 
admin.save()

# User (assigned to admin1)
user1 = CustomUser.objects.create_user('user1', 'pass', role=UserType.USER, assigned_admin=admin)
user1.set_password('pass'); 
user1.save()

user2 = CustomUser.objects.create_user('user2', 'pass', role=UserType.USER, assigned_admin=admin)
user2.set_password('pass'); 
user2.save()

user3 = CustomUser.objects.create_user('user3', 'pass', role=UserType.USER, assigned_admin=admin)
user3.set_password('pass'); 
user3.save()

