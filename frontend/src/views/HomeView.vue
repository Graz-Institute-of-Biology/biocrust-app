<template>
  <div class="container hero is-fullheight">
      <section class ="section" id="app">
          <h2 class="is-size-2 has-text-centered">Home</h2>
          <p> About this project some example text</p>
          <RouterLink @click="createDefaultDataset" to="/datasets" class="button is-link">Try</RouterLink>
      </section>
  </div>
</template>

<script>

import axios from 'axios'
import { defineComponent } from 'vue'
import 'viewerjs/dist/viewer.css'
import { directive as viewer } from "v-viewer"

export default defineComponent({
    name: 'HomeView',
    directives: {
      viewer: viewer({
        debug: true
      })
    },
    data () {
        return {
          dataset: {
                dataset_name: 'Guest_Dataset',
                coordinates: ' ',
                dataset_type: 'default',
                owner: localStorage.getItem('username'),
            }
        }
    },

    methods: {
      async createDefaultDataset() {
          this.addSlug();
          await axios.get('api/v1/datasets/')
          .then(response => {
              const existingDataset = response.data.find(dataset => dataset.dataset_name === this.dataset.dataset_name);
              if (existingDataset) {
                  console.log('Dataset already exists:', existingDataset);
                  return;
              }
              axios.post('api/v1/datasets/', this.dataset, { headers: { 'Content-Type': 'application/json' } })
              .then(createdResponse => {
                  console.log(createdResponse);
                  this.$router.push({ name: 'datasets' });
                  setTimeout(() => {
                    this.$router.go();
                  }, 100);
              })
              .catch(error => {
                  console.log(JSON.stringify(error));
              });
          })
          .catch(error => {
              console.log('Error fetching datasets:', error);
          });
      },
      addSlug() {
            this.dataset.slug = this.dataset.dataset_name.toLowerCase()
      }
    }
  })
    

</script>

<style scoped>

</style>