import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import DataSetView from '../views/DataSetView.vue'
import PageNotFoundView from '../views/PageNotFoundView.vue'
import AddImageView from '../views/AddImageView.vue'
import DataSetsView from '../views/DataSetsView.vue'
import AddDatasetView from '../views/AddDatasetView.vue'
import SignUpView from '../views/SignUpView.vue'
import LogInView from '../views/LogInView.vue'
import LogOutView from '../views/LogOutView.vue'
import store from '../store'

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
        path: '/signup',
        name: 'Signup',
        component: SignUpView
    },
    {
        path: '/logout',
        name: 'Logout',
        component: LogOutView
    },
    {
        path: '/login',
        name: 'Login',
        component: LogInView
    },
    {
        path: '/AddDataset',
        name: 'AddDataset',
        component: AddDatasetView
    },
    {
        path: '/datasets',
        name: 'datasets',
        component: DataSetsView
    },
    {
        path: '/dataset/:id',
        name: 'DataSetView',
        component: DataSetView
    },
    {
        path: '/addImage/:id',
        name: 'AddImageView',
        component: AddImageView
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
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
        next('/login')
    } else {
        next()
    }
})

export default router;