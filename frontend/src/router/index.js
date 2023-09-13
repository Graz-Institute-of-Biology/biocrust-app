import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import DataSetView from '../views/DataSetView.vue'
import PageNotFoundView from '../views/PageNotFoundView.vue'
import UploadView from '../views/UploadView.vue'

const routes = [
    {
        path: '/',
        name: 'HomeView',
        component: HomeView
    },
    {
        path: '/about',
        name: 'about',
        component: AboutView
    },
    {
        path: '/dataset/:id',
        name: 'dataset',
        component: DataSetView
    },
    {
        path: '/upload',
        name: 'upload',
        component: UploadView
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'PageNotFound',
        component: PageNotFoundView
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes: routes
});


export default router;