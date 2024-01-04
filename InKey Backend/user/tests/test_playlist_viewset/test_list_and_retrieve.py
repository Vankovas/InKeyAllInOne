from django.urls import reverse
from user.tests.test_playlist_viewset.playlist_mixin import TestPlaylistMixin


class TestPlaylistListAndRetrieveViewSet(TestPlaylistMixin):
    def test_list_works_correctly(self):
        response = self.client.get(reverse('playlist-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        print(response.json())
        for i in range(0, len(response.json())):
            if response.json()[i]["description"] == "haha":
                self.assertEqual(response.json()[i]["user"], self.user.id)
                self.assertEqual(len(response.json()[i]["songs"]), 2)
                self.assertEqual(response.json()[i]["songs"][0]["id"], self.songs[2].id)
                self.assertEqual(response.json()[i]["songs"][1]["id"], self.songs[1].id)
            elif response.json()[i]["description"] == "hihi":
                self.assertEqual(response.json()[i]["user"], self.user_other.id)
                self.assertEqual(response.json()[i]["name"], "Name 2")
                self.assertEqual(len(response.json()[i]["songs"]), 0)
            elif response.json()[i]["description"] == "huhu":
                self.assertEqual(response.json()[i]["user"], self.user.id)
                self.assertEqual(response.json()[i]["name"], "Name 3")
                self.assertEqual(len(response.json()[i]["songs"]), 0)
            else:
                self.fail("You have a playlist which wasnt defined in the set up!")

    def test_list_gets_all_playlists_whatever_the_user(self):
        response = self.client.get(reverse('playlist-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        response = self.client_other.get(reverse('playlist-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        response = self.client_unauthenticated.get(reverse('playlist-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_retrieve_works_and_gets_user_name(self):
        self.user.firstname = "new name"
        self.user.save()
        response = self.client.get(reverse('playlist-detail', kwargs={"pk": self.playlists[0].id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"], self.user.id)
        self.assertEqual(response.json()["user_name"], self.user.firstname)
        self.assertEqual(len(response.json()["songs"]), 2)
        self.assertEqual(response.json()["songs"][0]["id"], self.songs[2].id)
        self.assertEqual(response.json()["songs"][1]["id"], self.songs[1].id)

    def test_retrieve_other_users_playlist_works(self):
        response = self.client.get(reverse('playlist-detail', kwargs={"pk": self.playlists[1].id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"], self.user_other.id)
        self.assertEqual(response.json()["user_name"], self.user_other.firstname)
        self.assertEqual(len(response.json()["songs"]), 0)

    def test_retrieve_unathenticated_user_works(self):
        response = self.client_unauthenticated.get(reverse('playlist-detail', kwargs={"pk": self.playlists[1].id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"], self.user_other.id)
        self.assertEqual(response.json()["user_name"], self.user_other.firstname)
        self.assertEqual(len(response.json()["songs"]), 0)
