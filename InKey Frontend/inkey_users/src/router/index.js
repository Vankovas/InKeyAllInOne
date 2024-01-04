import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

  const routes = [
    {
      name: 'home',
      path: '/',
      component: () => import('@/views/Home'),
    },
    {
      name: 'albums',
      path: '/albums',
      component: () => import('@/views/Albums'),
    },
    {
      name: 'album',
      path: '/albums/:id',
      component: () => import('@/views/AlbumDetails'),
    },
    {
      name: 'artist',
      path: '/artist/:id',
      component: () => import('@/views/ArtistDetails'),
    },
    {
      name: 'favourites',
      path: '/favourites',
      component: () => import('@/views/Favourites'),
    },
    {
      name: 'live',
      path: '/live',
      component: () => import('@/views/Live'),
    },
    {
      name: 'live-detail',
      path: '/stream/:id',
      component: () => import('@/views/LiveDetails'),
    },
    {
      name: 'playlists',
      path: '/playlists',
      component: () => import('@/views/Playlists'),
    },
    {
      name: 'playlist',
      path: '/playlist/:id',
      component: () => import('@/views/PlaylistDetails'),
    },
    {
      name: 'create_playlists',
      path: '/create_playlists',
      component: () => import('@/views/CreatePlaylists'),
    },
    {
      name: 'search',
      path: '/search/:input',
      component: () => import('@/views/Search'),
    },
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

export default router
