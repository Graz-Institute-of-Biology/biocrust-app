<template>
    <div class="signup">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Sign Up</h1>

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
                            <input class="input" type="password" placeholder="password" v-model="password">
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
                            <button class="button is-success">Sign up</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'SignUp',
    data () {
        return {
            username: '',
            password: '',
            errors: []
        }
    },

    methods: {
        submitForm () {
            const formData = {
                username: this.username,
                password: this.password
            }
            axios.interceptors.request.use(function (config) {
                const token = localStorage.getItem("token")
                config.headers.Authorization =  token ? `Token ${token}` : null
                return config;
            });
            axios.post('api/v1/users/', formData)
            .then(response => {
                this.$router.push('/login')
                console.log(response)
            })
            .catch(error => {
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