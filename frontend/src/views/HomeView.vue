<template>
  <div class="is-fullheight">
        <div class="column is-12 header-col">
            <h1 class="is-size-1">Welcome to CC-Explorer</h1>
        </div>
        <!-- <div class="column is-12 button-col">
          <div class="button is-primary" @click="createDefaultDataset" >Try demo dataset</div>
        </div> -->
        <div class="container">
          <div class="left-column responsive-column">
              <img src="@/assets/Mock_Africa_1.png" alt="Landing Page" class="image" />
          </div>
          <div class="right-column responsive-column">
            <div class="text">
              <h1 class="header">Analyses Tools for Bio-Monitoring</h1>
              <ul class="features-list">
                <li>Segment your research image dataset.</li>
                <li>Use provided Machine Learning models.</li>
                <li>Visualise results & statistics.</li>
                <!-- Add more feature items as needed -->
              </ul>
              <RouterLink :to="{ name: 'DataSetView', params: { id: 9 }}" class="button is-primary">Browse sample dataset</RouterLink>

          </div>
          </div>
        </div>

        <div class="container">
          <div class="left-column responsive-column">
              <div class="text">
              <h1 class="header">Visualize & export statistics</h1>
              <ul class="features-list">
                <li>Upload your own data set.</li>
                <li>Analyse & assess your data.</li>
                <li>Export results as CSV file.</li>
                <!-- Add more feature items as needed -->
              </ul>
              <RouterLink :to="{ name: 'AddDataset' }" class="button is-primary">Add your Dataset</RouterLink>
            </div>
          </div>
          <div class="right-column responsive-column">
            <img src="@/assets/Mock_Data_Amazon.png" alt="Landing Page" class="image" />
          </div>
        </div>

        <!-- <div class="container">
          <div class="left-column">
              <img src="@/assets/USA_Mock.png" alt="Landing Page" class="image" />
          </div>
          <div class="right-column">
            <div class="text">
              <h1 class="header">Upload & analyse your own data</h1>
              <ul class="features-list">
                <li>Upload images.</li>
                <li>Use our ML-Models.</li>
                <li>Analyse & assess your own data.</li>
              </ul>
              <RouterLink :to="{ name: 'DataSetView', params: { id: 9 }}" class="button is-primary">Browse sample dataset</RouterLink>

          </div>
          </div>
        </div> -->
    
  </div>
</template>

<script>

import axios from 'axios'
import { defineComponent } from 'vue'
import 'viewerjs/dist/viewer.css'
import { directive as viewer } from "v-viewer"
import router from '@/router'

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
                router: router,
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

.button {
  margin-left: 35%;
}

.container {
  display: flex;
  flex-wrap: wrap;
  margin-top: 5%;
  width: 100%;
}

.features-list {
  font-size: 20px;
  list-style: none;
  margin-bottom: 30px;
  padding: 30px;
  text-align: center;
}

.features-list li {
  margin-bottom: 5px;
}

.header {
  font-size: 50px;
  margin-bottom: 10px;
  text-align: center;
}

.header-col {
  text-align: center;
}

.image {
  height: auto;
  width: 100%;
}

.left-column,
.right-column {
  flex: 1;
  width: 100%;
}

.p {
  padding: 0.8rem;
}

.responsive-column {
  flex: 1;
  padding: 10px;
  width: 100%;
}

.text {
  padding: 40px;
}

@media (max-width: 768px) {
  .button {
    width: 60%;
  }
  .container {
    flex-direction: column;
  }
  .responsive-column {
    flex-basis: 100%;
    padding: auto;
    width: 100%;
  }
}

</style>
