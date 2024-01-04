import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    name: 'home',
    path: '/',
    component: () => import('@/views/Home'),
  },
  {
    name: 'login',
    path: '/login',
    component: () => import('@/views/Login'),
  },
  {
    name: 'register',
    path: '/register',
    component: () => import('@/views/Register'),
  },
  {
    name: 'profile',
    path: '/profile/:id',
    component: () => import('@/views/UserProfile'),
  },

  // Commented routes to be used in the future possibly

  // {
  //   name: "about",
  //   path: "/about",
  //   component: () => import("@/views/Home")
  // },
  // {
  //   path: "/user/:id",
  //   component: UserProfile,
  //   children: [
  //     {
  //       name: "albums",
  //       path: "albums",
  //       component: Albums
  //     },
  //     {
  //       name: "playlists",
  //       path: "playlists",
  //       component: Playlists
  //     },
  //     {
  //       name: "messages",
  //       path: "messages",
  //       component: Messages
  //     },
  //   ]
  // },
  // {
  //   name: "track",
  //   path: "/track/:id",
  //   component: Track,
  // },
  {
    name: "stream",
    path: "/stream",
    component: () => import("@/views/Stream")
  },
];

const router = new VueRouter({
  routes,
});

export default router;
