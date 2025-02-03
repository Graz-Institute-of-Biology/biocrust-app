<template>
    <div class="page-my-account">
        <div class="columns is-multiline">
            <h1 class="title is-1">My Account</h1>
        </div>
        <div class="column is-12">
            <button @click="logout()" class="button is-danger">Log out</button>
        </div>
    </div>
    
</template>

<script>

import { mapActions } from 'vuex'

export default {
    name: 'LogOut',
    methods: {
        ...mapActions(['resetStatus']),
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('username')
            localStorage.removeItem('is_uploader')

            this.$store.commit('removeToken')
            this.$router.push('/')
    },
    mounted() {
        this.logout()
        this.resetStatus()
    }
}
}
</script>
