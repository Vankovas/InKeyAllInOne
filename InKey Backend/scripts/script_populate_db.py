import os
# -*- coding: utf-8 -*-
import os
import django
import eyed3

#  you have to set the correct path to you settings module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from account_management.models import User
from django.core.files.base import ContentFile
from creator.models import Album, Song


def get_all_first_lvl_dirs(dir=os.getcwd()):
    directory_list = []
    for root, dirs, files in os.walk(dir, topdown=True):
        for name in dirs:
            directory_list.append(os.path.join(root, name))
        break
    return directory_list


def remove_time_giberrish_from_folder_name(arr):
    for path in arr:
        all_parts = path.split("\\")
        new_path = "\\".join(all_parts[:-1]) + "\\" + "_".join(all_parts[-1].split("_")[:-3])
        os.rename(path, new_path)


def get_list_of_useremails(folders):
    emails = []
    for path in folders:
        relevant_path = path.split("\\")[-1]
        name = "_".join(relevant_path.split("_")[1:-2])
        site = ".".join(relevant_path.split("_")[-2:])
        email = name + "@" + site
        emails.append(email)
    return emails


def get_user_images(folders):
    images = []
    for path in folders:
        for filename in os.listdir(path):
            if "." in filename:
                images.append(path+"\\"+filename)
                break
    return images


def get_user_albums(folders):
    albums = []
    for path in folders:
        albums.append([])
        for filename in os.listdir(path):
            if "." not in filename:
                albums[-1].append(path+"\\"+filename)
    return albums


def get_album_cover(album):
    if "cover" in os.listdir(album):
        return album+"\\cover\\" + os.listdir(album+"\\cover")[0]
    return ""


def get_all_songs(album):
    songs = []
    for filename in os.listdir(album):
        if "." in filename:
            songs.append(album+"\\"+filename)
    return songs


def main():
    all_folders = get_all_first_lvl_dirs(os.getcwd() + "\\data_preset")
    all_users = get_list_of_useremails(all_folders)
    all_user_imgs = get_user_images(all_folders)
    all_albums = get_user_albums(all_folders)

    # for user, img in zip(all_users, all_user_imgs):
    #     u = User.objects.filter(email=user)
    #     if not u:
    #         u = User.objects.create_user(user, "password")
    #     else:
    #         u = u.first()
    #     first_name = user.split("@")[0].split("_")[0]
    #     u.firstname = first_name.capitalize()
    #     last_name = user.split("@")[0].split("_")[-1]
    #     if first_name != last_name:
    #         u.lastname = last_name.capitalize()
    #     else:
    #         u.lastname = ""
    #
    #     img_name = img.split('\\')[-1]
    #     with open(img, "rb") as file:
    #         u.profile_picture = ContentFile(file.read(), img_name)
    #     u.save()

    for i, albums in enumerate(all_albums):
        u = User.objects.get(email=all_users[i])
        for album in albums:
            album_name = album.split("\\")[-1]
            album_cover = get_album_cover(album)

            a, _ = Album.objects.get_or_create(artist=u, name=album_name)
            # img_name = album_cover.split('\\')[-1]
            # if album_cover:
            #     with open(album_cover, "rb") as file:
            #         a.cover_image = ContentFile(file.read(), img_name)
            # a.save()

            songs = get_all_songs(album)
            for song in songs:
                print(song)
                song_filename = song.split('\\')[-1]

                audio = eyed3.load(song)
                if audio.tag.title:
                    song_name = audio.tag.title
                else:
                    song_name = " ".join(song_filename.split("_"))
                    song_name = " ".join(song_name.split("-"))
                    song_name = song_name.split(".")[0]

                s, _ = Song.objects.get_or_create(album=a, name=song_name)
                with open(song, "rb") as file:
                    s.data = ContentFile(file.read(), song_filename)
                s.save()


if __name__ == '__main__':
    main()



