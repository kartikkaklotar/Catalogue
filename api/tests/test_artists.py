from rest_framework.test import APIClient
from rest_framework import status
from api.models import Artist
from django.urls import reverse
from furl import furl

from . import BaseAPITestCase

class ArtistTest(BaseAPITestCase):
    def setUp(self):
        self.client = APIClient()
        self.artist_name = 'Demo artist'
        self.payload = {
            'name': self.artist_name,
        }
        
        # create a test object
        self.test_object = Artist.objects.create(**self.payload)

    def test_list(self):
        response = self.client.get(reverse("artist-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_search_artists(self):
        url = reverse("artist-list")
        url = furl(url).set({"name": self.artist_name}).url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["uuid"], self.test_object.uuid)

    def test_get_artist(self):
        url = reverse("artist-detail", kwargs={"uuid": self.test_object.uuid})
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["name"], self.artist_name)
