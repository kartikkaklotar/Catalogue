from rest_framework import serializers
from rest_framework.reverse import reverse as drf_reverse
from .models import Album, Artist, Track, PlaylistTrack, Playlist

class TrackAlbumArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    class Meta:
        model = Artist
        fields = ("uuid", "name")

class TrackAlbumSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    artist = TrackAlbumArtistSerializer()

    class Meta:
        model = Album
        fields = ("uuid", "name", "artist")

class TrackSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    album = TrackAlbumSerializer()

    class Meta:
        model = Track
        fields = ("uuid", "name", "order", "album")

class AlbumTrackSerializer(TrackSerializer):
    uuid = serializers.ReadOnlyField()

    class Meta:
        model = Track
        fields = ("uuid", "name", "order")

class AlbumArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()

    class Meta:
        model = Artist
        fields = ("uuid", "name")

class AlbumSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    artist = AlbumArtistSerializer()
    tracks = AlbumTrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ("uuid", "name", "year", "artist", "tracks")

class ArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()

    class Meta:
        model = Artist
        fields = ("uuid", "name")

class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer()

    class Meta:
        model = PlaylistTrack
        fields = ('id', 'track', 'order')

class PlaylistSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ("uuid", "name", "tracks")

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        playlist = Playlist.objects.create(**validated_data)

        for order, track_data in enumerate(tracks_data, start=1):
            album_data = track_data.pop('album')
            artist_data = album_data.pop('artist')
            artist, _ = Artist.objects.get_or_create(**artist_data)
            album, _ = Album.objects.get_or_create(artist=artist, **album_data)
            track, _ = Track.objects.get_or_create(album=album, **track_data)
            PlaylistTrack.objects.create(playlist=playlist, track=track, order=order)

        return playlist
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        tracks_data = validated_data.get('tracks')

        if tracks_data:
            existing_tracks = set(instance.tracks.all())

            for track_data in tracks_data:
                album_data = track_data.pop('album')
                artist_data = album_data.pop('artist')
                artist, _ = Artist.objects.get_or_create(**artist_data)
                album, _ = Album.objects.get_or_create(artist=artist, **album_data)
                track, _ = Track.objects.get_or_create(album=album, **track_data)

                track.name = track_data.get('name', track.name)
                track.album = album
                track.order = track_data.get('order', track.order)
                track.save()

                if track in existing_tracks:
                    existing_tracks.remove(track)

            for track in existing_tracks:
                instance.tracks.remove(track)

        instance.save()
        return instance

    