from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # 읽기 권한 요청이 들어오면 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 요청자(request.user)가 객체(Blog)의 user와 동일한지 확인
        return obj.userID == request.user

class IsLeaderOrMemberReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.users.has_key[request.user]:
            if request.method in permissions.SAFE_METHODS:
                return True
            return obj.leader == request.user
        else:
            return False
            
class OwnerOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.userID == request.user
        