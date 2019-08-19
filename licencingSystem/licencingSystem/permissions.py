from rest_framework import permissions


class StaffPermission(permissions.BasePermission):
	
	def has_permission(self, request, view):
		safe_method = request.method in permissions.SAFE_METHODS
		perm = safe_method or request.user.is_staff
		return perm

