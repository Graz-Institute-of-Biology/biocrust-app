<template>
    <div class="is-fullheight">
      
          <div class="column is-10 header-col">
              <h2 class="is-size-2">Account activation</h2>
          </div>
          <p> Hello, please click here to activate your account</p>
          <div class="column is-2 button-col">
            <div class="button is-info" @click="sendActivationToBackend" >Activate</div>
          </div>
      
    </div>
  </template>

  <script>
import { defineComponent } from 'vue'
import axios from 'axios'

export default defineComponent({
    name: 'DataSetView',
    methods: {
        async sendActivationToBackend() {
            console.log("sending...");
            try {
                const response = await axios.get(`users/activate/${this.$route.params.id}/${this.$route.params.token}`);
                console.log(response)
                this.$router.push('/login')
            } catch (error) {
                console.error("Error with account activation:", error);
            }
            return null;
        },
    }
})
  </script>
  