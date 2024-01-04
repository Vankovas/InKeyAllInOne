from rest_framework.exceptions import ValidationError

from core.utils import is_user_auth
from core.abstract_serializers import AbstractVoteSerializer
from creator.models import Album, Song, AlbumVote, SongVote
from rest_framework import serializers


class AlbumSerializer(serializers.ModelSerializer):
    artist_name = serializers.SerializerMethodField(read_only=True)

    def get_artist_name(self, obj):
        return obj.artist.firstname

    class Meta:
        model = Album
        fields = '__all__'
        extra_kwargs = {
            'views': {'read_only': True},
            'artist': {'read_only': True},
            'name': {'required': True},
            'created_at': {'read_only': True},
            'rating': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if is_user_auth(request):
            user = request.user
            album = Album.objects.create(artist=user, **self.validated_data)
            return album
        raise ValidationError("You need to be logged in to create an album!")


class SongSerializer(serializers.ModelSerializer):
    artist_name = serializers.SerializerMethodField(read_only=True)

    def get_artist_name(self, obj):
        return obj.album.artist.firstname

    class Meta:
        model = Song
        fields = '__all__'
        extra_kwargs = {
            'views': {'read_only': True},
            'name': {'required': True},
            'data': {'required': True},
            'album': {'required': True},
            'created_at': {'read_only': True},
            'rating': {'read_only': True},
        }


class AlbumVoteSerializer(AbstractVoteSerializer):
    class Meta:
        model = AlbumVote
        exclude = ['user']
        key_containing_rating = "album"


class SongVoteSerializer(AbstractVoteSerializer):
    class Meta:
        model = SongVote
        exclude = ['user']
        key_containing_rating = "song"
