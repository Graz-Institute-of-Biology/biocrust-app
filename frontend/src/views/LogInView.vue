<template>
    <div class="signup">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Log in</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label class="label">Name</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="Name" v-model="username">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Password</label>
                        <div class="control">
                            <input class="input" type="password" placeholder="Email" v-model="password">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p 
                            v-for="error in errors"
                            :key="error"
                        >
                            {{ error }}
                        </p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-success">Log in</button>
                        </div>
                    </div>
                    <div class="modal is-active modal-background" v-if="loginAlert">
                        <div class="modal-background"></div>
                        <div class="modal-card">
                            <header class="modal-card-head">
                            <p class="modal-card-title">Login Error</p>
                            </header>
                            <section class="modal-card-body">
                                <p>Please check username and password</p>
                                <p>Have you already activated your account?</p>
                            </section>
                            <footer class="modal-card-foot">
                                <button class="button is-success" @click="setLoginAlert">Ok</button>
                            </footer>
                        </div>
                    </div>
                </form>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios'
import store from '../store'

export default {
    name: 'LogIn',
    data () {
        return {
            username: '',
            password: '',
            errors: [],
            loginAlert: false
        }
    },
    methods: {
        clearFields() {
            this.username = ''
            this.password = ''
            this.errors = []
        },
        setLoginAlert() {
            if (this.loginAlert) {
                this.clearFields()
                this.loginAlert = false
            } else {
                this.loginAlert = true
            }
        },
        redirect() {
            this.clearFields()
            this.$router.push('/login')
        },
        async setUserPermissions(token) {
            const userResponse = await axios.get('api/v1/users/me/', {
            headers: {
                'Authorization': 'Token ' + token,
                'Content-Type': 'application/json'
            }
        })        
        const isUploader = userResponse.data.is_uploader
        console.log(isUploader)
        store.commit('setIsUploader', isUploader)
        localStorage.setItem('is_uploader', JSON.stringify(isUploader))
        },
        async submitForm() {
            axios.defaults.headers.common['Authorization'] = ''

            localStorage.removeItem('token')

            const formData = {
                username: this.username,
                password: this.password
            }

            await axios.post('api/v1/token/login/', formData, { headers: { 'Content-Type': 'application/json' } })
            .then(response => {
                const token = response.data.auth_token
                store.commit('setToken', token)
                axios.defaults.headers.common['Authorization'] = 'Token ' + token
                localStorage.setItem('token', token)
                localStorage.setItem('username', this.username)
                this.setUserPermissions(token)
                this.$router.push('/datasets')
            })
            .catch(error => {
                this.setLoginAlert()
                if (error.response) {
                    for (let key in error.response.data) {
                        this.errors.push(`${key}: ${error.response.data[key]}`)
                    }
                    console.log(JSON.stringify(error.response.data))
                } else if (error.message) {
                    console.log(JSON.stringify(error.message))
                } else {
                    console.log(JSON.stringify(error))
                }
            })

        }
    }
}

</script>

<style>

.enable-line-break {
    white-space: pre-wrap;
}

</style>