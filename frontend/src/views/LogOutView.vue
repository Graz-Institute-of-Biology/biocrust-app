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

export default {
    name: 'LogOut',
    created() {
        this.logout()
    },
    methods: {
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('username')

            this.$store.commit('removeToken')
            this.$router.push('/')
    }
}
}
</script>
