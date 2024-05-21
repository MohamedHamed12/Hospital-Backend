# -*- coding: utf-8 -*-
# permissions.py
from rest_framework.permissions import  BasePermission
from accounts.models import *
from rest_framework.permissions import SAFE_METHODS
class RelatedVisitPermission(BasePermission):
   

    def has_permission(self, request, view):
        # Check if the user is an admin
        # if request.user and request.user.is_superuser:
        if request.user and( request.user.is_staff or request.user.is_superuser):
            return True
        employee=Employee.objects.filter(user=request.user).first()
        if employee:
            return True
        if request.method in SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # if request.user and request.user.is_superuser:
        if request.user and( request.user.is_staff or request.user.is_superuser):
            return True
        employee=Employee.objects.filter(user=request.user).first()
        if employee:
            return True
        if request.method in SAFE_METHODS:
            return True
        return False