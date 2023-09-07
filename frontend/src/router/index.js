 import { createRouter, createWebHistory } from 'vue-router'
import homePage from '../views/homePage.vue'


const routes = [
    {
        path: '/',
        name: 'homePage',
        component: homePage
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes: routes
});


export default router;