from rest_framework.exceptions import ParseError
from rest_framework.permissions import BasePermission


class SongBelongsToUserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.album.artist == request.user
        else:
            return False

    def has_permission(self, request, view):
        if request.method == 'POST':
            album = request.data.get('album')
            from creator.models import Album
            instance = Album.objects.filter(pk=album).first()
            if not instance:
                raise ParseError(detail={"album": ["This field is required."]})
            return instance.artist == request.user
        return super(SongBelongsToUserPermission, self).has_permission(request, view)


class BelongsToArtistPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.artist == request.user
        else:
            return False
