<template>
  <div class="is-fullheight">
    
        <div class="column is-10 header-col">
            <h2 class="is-size-2">Home</h2>
        </div>
        <p> Deep Learning Webpage for an image based Biomonitoring</p>
        <div class="column is-2 button-col">
          <div class="button is-primary" @click="createDefaultDataset" >Try demo dataset</div>
        </div>
    
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
                  const dataset_id = existingDataset.id;
                  this.$router.push({ name: 'DataSetView', params: {id: dataset_id } });
                  return;
              }
              axios.post('api/v1/datasets/', this.dataset, { headers: { 'Content-Type': 'application/json' } })
              .then(createdResponse => {
                  console.log(createdResponse);
                  const dataset_id = createdResponse.data.id;
                  this.$router.push({ name: 'DataSetView', params: { id: dataset_id } });
                  // setTimeout(() => {
                  //   this.$router.go();
                  // }, 100);
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

p {
  padding: 0.75rem;
}

.header-col {
    text-align: center;
}

</style>