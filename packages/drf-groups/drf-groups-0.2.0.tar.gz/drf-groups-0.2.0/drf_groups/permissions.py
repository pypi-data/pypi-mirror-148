from rest_framework import permissions


class GroupPermissionMixin:
    _groups_attribute: str

    def _is_group_qs_permitted(self, qs) -> bool:
        raise NotImplementedError()

    def has_permission(self, request, view):
        groups = getattr(view, self._groups_attribute, [])
        
        if not len(groups):
            return True

        matching_groups = request.user.groups.filter(name__in=groups)

        return self._is_group_qs_permitted(matching_groups)


class BelongsToGroups(permissions.BasePermission, GroupPermissionMixin):
    _groups_attribute = "allowed_groups"

    def _is_group_qs_permitted(self, qs):
        return qs.exists()


class DoesNotBelongToGroups(permissions.BasePermission, GroupPermissionMixin):
    _groups_attribute = "disallowed_groups"

    def _is_group_qs_permitted(self, qs):
        return not qs.exists()
