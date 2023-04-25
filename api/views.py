from rest_framework import viewsets
from .filters import AlbumFilter, ArtistFilter, TrackFilter, PlaylistFilter
from .models import Album, Artist, Track, Playlist, PlaylistTrack
from .serializers import AlbumSerializer, ArtistSerializer, TrackSerializer, PlaylistSerializer, PlaylistTrackSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class BaseAPIViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
class ArtistViewSet(BaseAPIViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_class = ArtistFilter

class AlbumViewSet(BaseAPIViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_class = AlbumFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("artist").prefetch_related("tracks")

class TrackViewSet(BaseAPIViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filter_class = TrackFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("album", "album__artist")

class PlaylistViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    
class PlaylistTrackViewSet(viewsets.ModelViewSet):
    queryset = PlaylistTrack.objects.all()
    serializer_class = PlaylistTrackSerializer