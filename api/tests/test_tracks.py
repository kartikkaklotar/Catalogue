from rest_framework.test import APIClient
from rest_framework import status
from api.models import Artist, Album, Track
from django.urls import reverse
from furl import furl

from . import BaseAPITestCase

class TrackTests(BaseAPITestCase):
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

    def test_list_albums(self):
        url = reverse("track-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_search_albums(self):
        url = reverse("track-list")
        url = furl(url).set({"name": self.track_name}).url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], self.trc_object.uuid)
        self.assertEqual(response.data["results"][0]["album"]["uuid"], self.album_object.uuid)

    def test_get_album(self):
        url = reverse("track-detail", kwargs={"uuid": self.trc_object.uuid})
        response = self.client.get(url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.track_name)
        self.assertEqual(response.data["album"]["uuid"], self.album_object.uuid)
