from django.urls import path, include
from rest_framework import routers
from .views import ArtistViewSet, AlbumViewSet, TrackViewSet, PlaylistViewSet, PlaylistTrackViewSet

router = routers.DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'tracks', TrackViewSet)
router.register(r'playlist', PlaylistViewSet)
router.register(r'playlisttrack', PlaylistTrackViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]