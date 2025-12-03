from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    """
    Allows access only to users with role='student'.
    Assumes the custom User model has a 'role' field.
    """
    message = "You must be a student to access this resource."

    def has_permission(self, request, view):
        # request.user is available here if the user is authenticated (JWT is valid)
        
        # 1. Ensure the user is authenticated first
        if not request.user or not request.user.is_authenticated:
            return False
            
        # 2. Check the user's role field
        # The role field should be a string/char field on your custom user model
        return request.user.role == 'STUDENT'

class IsAdmin(BasePermission):
    """
    Allows access only to users with role='admin'.
    """
    message = "You must be an administrator to access this resource."

    def has_permission(self, request, view):
        # ... (similar logic for 'admin' role)
        return request.user.role == 'ADMIN'