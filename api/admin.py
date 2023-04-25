from django.contrib import admin
from .models import Artist, Album, Track, PlaylistTrack, Playlist
from django.db.models import Count, F
from django.utils.html import format_html

class ArtistActiveListFilter(admin.SimpleListFilter):
    title = "year active"
    parameter_name = "year_active"
    
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples, where the first element in each
        tuple is the coded value for the option that will appear in
        the URL query. The second element is the human-readable name
        for the option that will appear in the right sidebar.
        """
        # Get a list of all the distinct years in the objects
        years = Album.objects.all().order_by("year")
        return [(year.year, year.year) for year in years]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value provided
        in the query string and retrievable via `self.value()`.
        """
        # Check if the filter has been applied
        try:
            year = int(self.value())
        except (TypeError, ValueError):
            return queryset
        return queryset.filter(albums__year=year)
    
class TrackInline(admin.TabularInline):
    model = Track
    fields = ("order", "name")
    extra = 0

class AlbumInline(admin.TabularInline):
    model = Album
    fields = ("name", "year", "tracks_cnt")
    readonly_fields = ("tracks_cnt",)
    extra = 0

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(track_count=Count("tracks"))

    def tracks_cnt(self, album):
        return format_html("{0}", album.track_count)

    tracks_cnt.short_description = "Tracks"

class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "albums_cnt")
    list_filter = (ArtistActiveListFilter,)
    search_fields = ("uuid", "name")
    fields = ("name", "uuid", "albums_cnt")
    readonly_fields = ("uuid", "albums_cnt",)
    inlines = [AlbumInline]
    
    def get_queryset(self, request):
        self.request = request
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("albums").annotate(album_count=Count("albums"))

    def albums_cnt(self, artist):
        return format_html("{0}", artist.album_count)

    albums_cnt.short_description = "Albums"

class AlbumAdmin(admin.ModelAdmin):
    list_display = ("name", "artist", "album_year", "tracks_cnt")
    list_filter = ("year",)
    search_fields = ("uuid", "name", "artist__name")
    fields = ("name", "year", "uuid", "artist", "tracks_cnt")
    readonly_fields = ("uuid", "artist", "tracks_cnt")
    inlines = [TrackInline]

    def get_queryset(self, request):
        self.request = request
        queryset = super().get_queryset(request)
        return queryset.annotate(track_count=Count("tracks"))
    
    def artist(self, album):
        return format_html("{0}", album.artist)

    artist.short_description = "Artist"
    artist.admin_order_field = "artist__name"

    def album_year(self, album):
        return format_html("{0}", album.year)
    
    album_year.short_description = "Year"
    album_year.admin_order_field = "year"

    def tracks_cnt(self, album):
        return format_html("{0}", album.track_count)

    tracks_cnt.short_description = "Tracks"
    tracks_cnt.admin_order_field = "track_count"

class TrackAdmin(admin.ModelAdmin):
    list_display = ("name", "artist", "album", "album_year")
    list_filter = ("album__year",)
    search_fields = ("uuid", "name", "album__name", "album__artist__name")
    fields = ("name", "uuid", "artist", "album", "album_year")
    readonly_fields = ("uuid", "artist", "album", "album_year")

    def get_queryset(self, request):
        self.request = request
        queryset = super().get_queryset(request)
        return queryset.annotate(album_year=F("album__year"))

    def artist(self, track):
        return format_html("{0}", track.album.artist)

    artist.short_description = "Artist"
    artist.admin_order_field = "album__artist__name"

    def album(self, track):
        return format_html("{0}", track.album)

    album.short_description = "Album"
    album.admin_order_field = "album__name"

    def album_year(self, track):
        return format_html("{0}", track.album_year)

    album_year.short_description = "Year"
    album_year.admin_order_field = "album__year"

class PlaylistTrackInline(admin.TabularInline):
    model = PlaylistTrack
    fields = ("order", "track")
    extra = 0

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "tracks_cnt")
    fields = ("name", "uuid", "tracks_cnt")
    readonly_fields = ("uuid", "tracks_cnt")
    search_fields = ("uuid", "name")
    inlines = [PlaylistTrackInline]

    def get_queryset(self, request):
        self.request = request
        queryset = super().get_queryset(request)
        return queryset.annotate(track_count=Count("tracks"))

    def tracks_cnt(self, playlist):
        return format_html("{0}", playlist.track_count)

    tracks_cnt.short_description = "Tracks"
    tracks_cnt.admin_order_field = "track_count"

class PlaylistTrackAdmin(admin.ModelAdmin):
    list_display = ("playlist", "track", "album", "artist")
    search_fields = ("playlist__name", "track __name", "album__name", "album__artist__name")
    fields = ("playlist", "track", "order")
    readonly_fields = ("playlist", "track")

    def get_queryset(self, request):
        self.request = request
        queryset = super().get_queryset(request)
        return queryset

    def playlist(self, playlisttrack):
        return format_html("{0}", playlisttrack.playlist.name)
    
    playlist.short_description = "Playlist"

    def track(self, playlisttrack):
        return format_html("{0}", playlisttrack.track.name)
    
    track.short_description = "Track"

    def album(self, playlisttrack):
        return format_html("{0}", playlisttrack.track.album)

    album.short_description = "Album"
    album.admin_order_field = "album__name"

    def artist(self, playlisttrack):
        return format_html("{0}", playlisttrack.track.album.artist)

    artist.short_description = "Artist"
    artist.admin_order_field = "album__artist__name"

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(PlaylistTrack, PlaylistTrackAdmin)