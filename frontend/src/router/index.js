import Vue from 'vue';
import Router from 'vue-router';

import Settings from '@/components/settings';
import Callback from '@/components/callback';
import Dashboard from '@/components/dashboard';


Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard,
    },
    {
      path: '/settings',
      name: 'Settings',
      component: Settings,
    },
    {
      path: '/callback',
      component: Callback,
    },
  ],
});
