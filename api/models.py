from uuid import uuid4
from django.db import models
from rest_framework import viewsets, status
from rest_framework.response import Response

class Artist(models.Model):
    uuid = models.UUIDField(verbose_name="uuid", default=uuid4, unique=True)
    name = models.CharField(max_length=100, )

    class Meta:
        ordering = ("name",)
        indexes = (models.Index(fields=("name",)),)

    def __str__(self):
        return self.name

class Album(models.Model):
    uuid = models.UUIDField(verbose_name="uuid", default=uuid4, unique=True)
    name = models.CharField(max_length=100, )
    year = models.IntegerField()
    artist = models.ForeignKey(Artist, related_name="albums", on_delete=models.CASCADE)

    class Meta:
        ordering = ("artist", "year", "name")
        indexes = (models.Index(fields=("artist", "year", "name")),)

    def __str__(self):
        return self.name
    
class Track(models.Model):
    uuid = models.UUIDField(verbose_name="uuid", default=uuid4, unique=True)
    name = models.CharField(max_length=100)
    album = models.ForeignKey(Album, related_name="tracks", on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        ordering = ("order", "name")
        indexes = (models.Index(fields=("order", "name")),)
        constraints = (
            models.UniqueConstraint(
                fields=("album", "order"), name="unique_album_order"
            ),
        )

    def __str__(self):
        return self.name

class Playlist(models.Model):
    uuid = models.UUIDField(verbose_name="uuid", default=uuid4, unique=True)
    name = models.CharField(max_length=100)
    tracks = models.ManyToManyField(Track, related_name='playlists', through='PlaylistTrack', blank=True)

    def __str__(self):
        return self.name

class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, related_name='playlisttracks', on_delete=models.CASCADE)
    track = models.ForeignKey(Track, related_name='playlisttracks', on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        ordering = ('order',)
        indexes = (models.Index(fields=("playlist", "track")),)
        constraints = (
            models.UniqueConstraint(
                fields=("playlist", "track", "order"), name="unique_playlist_track_order"
            ),
        )

    def __str__(self):
        return f'{self.playlist} - {self.track}'