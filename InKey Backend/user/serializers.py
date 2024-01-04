from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account_management.serializers import UserSerializer
from core.utils import is_user_auth
from core.abstract_serializers import AbstractVoteSerializer
from creator.models import Song, Album
from creator.serializers import SongSerializer
from user.models import Comment, Playlist, CommentSong, CommentAlbum, Stream, PlaylistTrack, PlaylistVote


class StreamSerializer(serializers.ModelSerializer):
    artist = UserSerializer(read_only=True)

    class Meta:
        model = Stream
        fields = ["artist", "uuid", "created_at"]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if is_user_auth(request):
            user = request.user
            stream, exists = Stream.objects.get_or_create(artist=user)
            return stream
        raise ValidationError("You need to be logged in to create a stream!")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'date_of_creation': {'read_only': True},
            'last_edited': {'read_only': True},
            'message': {'required': True},
            'user': {'read_only': True,
                     'required': True},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if is_user_auth(request):
            user = request.user
            comment = Comment.objects.create(user=user, **self.validated_data)
            return comment
        raise ValidationError("You need to be logged in to create a comment!")


class CommentSongSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(required=True)
    song_id = serializers.IntegerField(read_only=False)

    class Meta:
        model = CommentSong
        fields = ['song_id', 'comment']

    def create(self, validated_data):
        request = self.context.get("request")
        if is_user_auth(request):
            userpk = request.user if request.user.is_authenticated else -1
            qs = Song.objects.filter(Q(album__artist=userpk) | Q(album__is_private=False))
            song = validated_data.pop('song_id', None)
            song = qs.filter(id=song)
            if len(song) == 0:
                raise ValidationError("Enter a correct song id!!!")
            song = song[0]
            comment_serializer = CommentSerializer(data=validated_data.get("comment"), context=self.context)
            comment_serializer.is_valid(raise_exception=True)
            comment = comment_serializer.save()
            cs = CommentSong.objects.create(comment=comment, song=song)
            return cs
        raise ValidationError("You need to be logged in to create a comment!")

    def update(self, instance, validated_data):
        return instance


class CommentAlbumSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(required=True)
    album_id = serializers.IntegerField(read_only=False)

    class Meta:
        model = CommentAlbum
        fields = ['album_id', 'comment']

    def create(self, validated_data):
        request = self.context.get("request")
        if is_user_auth(request):
            userpk = request.user if request.user.is_authenticated else -1
            qs = Album.objects.filter(Q(artist=userpk) | Q(is_private=False))
            album = validated_data.pop('album_id', None)
            album = qs.filter(id=album)
            if len(album) == 0:
                raise ValidationError("Enter a correct album id!!!")
            album = album[0]
            comment_serializer = CommentSerializer(data=validated_data.get("comment"), context=self.context)
            comment_serializer.is_valid(raise_exception=True)
            comment = comment_serializer.save()
            cs = CommentAlbum.objects.create(comment=comment, album=album)
            return cs
        raise ValidationError("You need to be logged in to create a comment!")

    def update(self, instance, validated_data):
        return instance


class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)
    add_songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), many=True, write_only=True)
    delete_songs = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), many=True, write_only=True)
    user_name = serializers.SerializerMethodField(read_only=True)

    def get_user_name(self, obj):
        return obj.user.firstname

    class Meta:
        model = Playlist
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True},
            'user': {'read_only': True,
                     'required': True},
            'description': {'required': False, 'default': ''},
            'views': {'read_only': True},
            'rating': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def add_and_remove_songs(self, playlist, add_songs, delete_songs):
        if add_songs:
            for song in add_songs:
                new_position = PlaylistTrack.last_position(playlist)+1
                if PlaylistTrack.objects.filter(playlist=playlist, song=song).count() == 0:
                    PlaylistTrack.objects.create(playlist=playlist, song=song, position=new_position)
        if delete_songs:
            for song in delete_songs:
                PlaylistTrack.objects.filter(playlist=playlist, song=song).delete()

    def create(self, validated_data):
        request = self.context.get("request")
        if is_user_auth(request):
            user = request.user
            add_songs = validated_data.pop("add_songs", None)
            delete_songs = validated_data.pop("delete_songs", None)
            playlist = Playlist.objects.create(user=user, **validated_data)
            self.add_and_remove_songs(playlist, add_songs, delete_songs)
            return playlist
        raise ValidationError("You need to be logged in to create a playlist!")

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if is_user_auth(request):
            user = request.user
            if instance.user != user:
                raise ValidationError("You cannot edit another person's playlist!")
            add_songs = validated_data.pop("add_songs", None)
            delete_songs = validated_data.pop("delete_songs", None)
            self.add_and_remove_songs(instance, add_songs, delete_songs)
            return super(PlaylistSerializer, self).update(instance, validated_data)
        raise ValidationError("You need to be logged in to update a playlist!")


class PlaylistVoteSerializer(AbstractVoteSerializer):
    class Meta:
        model = PlaylistVote
        exclude = ['user']
        key_containing_rating = "playlist"
