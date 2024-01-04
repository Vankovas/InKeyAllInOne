export const mockUser = {
  username: 'Vankovas',
  fName: 'Ivan',
  lName: 'Vasilev',
  email: 'vannkovas@gmail.com',
  description: 'Some description',
  imageSrc: 'https://www.biography.com/.image/t_share/MTIwNjA4NjMzOTU5NTgxMTk2/bob-ross-9464216-1-402.jpg',
};

export const mockAlbums = [
  {
    id: 1,
    artistId: 1,
    name: 'Album 1',
    views: 10000,
    songs: [
      {
        name: 'Song 1',
        duration: 6.45,
      },
      {
        name: 'Song 2',
        duration: 4.19,
      },
    ],
  },
  {
    id: 2,
    artistId: 1,
    name: 'Album 2',
    views: 10000,
    songs: [
      {
        name: 'Song 1',
        duration: 6.45,
      },
      {
        name: 'Song 2',
        duration: 4.19,
      },
    ],
  },
];

export const mockPlaylists = [
  {
    id: 1,
    creatorId: 1,
    name: 'Playlist 1',
    songs: [
      {
        name: 'Song 1',
        duration: 6.45,
      },
      {
        name: 'Song 2',
        duration: 4.19,
      },
    ],
  },
  {
    id: 2,
    creatorId: 1,
    name: 'Playlist 2',
    songs: [
      {
        name: 'Song 1',
        duration: 6.45,
      },
      {
        name: 'Song 2',
        duration: 4.19,
      },
    ],
  },
];

export const mockSongs = [
  {
    name: 'Song 1',
    duration: 6.45,
  },
  {
    name: 'Song 2',
    duration: 4.19,
  },
];
