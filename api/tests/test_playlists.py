from rest_framework.test import APIClient
from rest_framework import status
from api.models import Playlist, Track, Artist, Album, PlaylistTrack
from django.urls import reverse
from furl import furl

from . import BaseAPITestCase

class PlaylistTest(BaseAPITestCase):
    def setUp(self):
        self.client = APIClient()
        self.artist_name = 'Demo artist'
        self.album_name = "Desi Kalakar"
        self.track_name = "Testing"

        self.art_payload = {
            'name': self.artist_name,
        }
        self.artist_object = Artist.objects.create(**self.art_payload)

        self.alb_payload = {
            'name': self.album_name,
            'year': 2012,
            'artist': self.artist_object
        }
        self.album_object = Album.objects.create(**self.alb_payload)

        self.trc_payload = {
            'name':self.track_name,
            'album':self.album_object,
            'order':1
        }
        self.trc_object = Track.objects.create(**self.trc_payload)
        self.playlist1 = Playlist.objects.create(name='Playlist 1')
        PlaylistTrack.objects.create(playlist=self.playlist1, track=self.trc_object, order=1)

    def test_get_all_playlists(self):
        url = reverse('playlist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_single_playlist(self):
        url = reverse('playlist-detail', kwargs={'uuid': str(self.playlist1.uuid)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.playlist1.name)

    def test_create_playlist(self):
        url = reverse('playlist-list')
        data = {
            "name": "Playlist 2",
            "tracks": [
                {
                    "name": "Testing",
                    "order": 1,
                    "album": {
                        "name": "Desi Kalakar",
                        "year":2022,
                        "artist": {
                            "name": "Demo artist"
                        }
                    }
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Playlist.objects.count(), 2)
        self.assertEqual(Playlist.objects.get(name='Playlist 2').name, 'Playlist 2')

    def test_update_playlist(self):
        url = reverse('playlist-detail', kwargs={'uuid': str(self.playlist1.uuid)})
        data = {
            "name": "Updated Playlist",
            "tracks": [
                {
                    "name": "Testing",
                    "order": 1,
                    "album": {
                        "name": "Desi Kalakar",
                        "year":2022,
                        "artist": {
                            "name": "Demo artist"
                        }
                    }
                }
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Playlist.objects.get(pk=self.playlist1.pk).name, 'Updated Playlist')

    def test_delete_playlist(self):
        url = reverse('playlist-detail', kwargs={'uuid': str(self.playlist1.uuid)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Playlist.objects.count(), 0)