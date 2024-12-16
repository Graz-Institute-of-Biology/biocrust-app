<template>
    <div class="signup">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Sign Up</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label class="label">Account name</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="Name" v-model="username">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Email</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="email@example.com" v-model="email">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Password</label>
                        <div class="control">
                            <input class="input" type="password" placeholder="password" v-model="password">
                        </div>
                    </div>

                    <div class="space-y-4">
                        <div class="flex items-center">
                        <input
                            id="terms"
                            v-model="acceptedTerms"
                            type="checkbox"
                            class="w-4 h-4 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                            required
                        />
                        <label for="terms" class="ml-2 text-sm font-medium text-gray-700">
                            I accept the
                            <a href="/terms" class="text-blue-600 hover:text-blue-500 underline">
                            Terms and Conditions
                            </a>
                        </label>
                        </div>

                        <div class="flex items-center">
                        <input
                            id="privacy"
                            v-model="acceptedPrivacy"
                            type="checkbox"
                            class="w-4 h-4 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                            required
                        />
                        <label for="privacy" class="ml-2 text-sm font-medium text-gray-700">
                            I agree to the
                            <a href="/privacy" class="text-blue-600 hover:text-blue-500 underline">
                            Privacy Policy
                            </a>
                        </label>
                        </div>
                    </div>
                    <div class="notification is-danger" v-if="errors.length" style="position: relative;">
                        <button class="delete" 
                                style="position: absolute; right: 0.5rem; top: 0.5rem;"
                                @click="clearErrors"
                                aria-label="close">
                        </button>
                        <p v-for="error in errors"
                        :key="error">
                            {{ error }}
                        </p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-success">Sign up</button>
                        </div>
                    </div>
                </form>
                <!-- <VueRecaptcha
                    :sitekey="siteKey"
                    :load-recaptcha-script="true"
                    @verify="captchaSuccess"
                    @error="captchaError"
                ></VueRecaptcha> -->
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios'
// import { computed } from 'vue';
// import { VueRecaptcha } from 'vue-recaptcha';

export default {
    name: 'SignUp',
    // components: {
    //     VueRecaptcha
    // },
    // created() {
    //     this.siteKey = computed(() => {
    //     return 'yourSiteAPIKey';
    //     })
    // },
    data () {
        return {
            username: '',
            email: '',
            password: '',
            captchaDone: false,
            siteKey: '',
            errors: [],
            acceptedTerms: false,
            acceptedPrivacy: false
        }
    },

    methods: {
        captchaSuccess () {
            this.captchaDone = true
        },
        clearErrors() {
            this.errors = [];
            },
        submitForm () {
            const formData = {
                username: this.username,
                email: this.email,
                password: this.password
            }
            if (!this.acceptedTerms || !this.acceptedPrivacy) {
                this.errors.push('You must accept the terms and privacy policy')
                return
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
    ,
  watch: {
    acceptedTerms(newVal) {
      this.$emit('terms-updated', newVal)
    },
    acceptedPrivacy(newVal) {
      this.$emit('privacy-updated', newVal)
    }
  } 
}

</script>