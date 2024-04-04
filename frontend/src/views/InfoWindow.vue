<template>
    <div class="info-window">
      <div class="content">
        <ul>
          <div>
            <table class="table table-striped">
                <thead>
                    <th>Image</th>
                    <th>Status</th>
                </thead>
                <tbody>
                    <tr v-for="item in Analyses" :key="item">
                    <th scope="row">{{ getImageName(item.source_image_url)  }}</th>
                    <th scope="row" v-if="getLoading(item.status)"><clip-loader :loading="getLoading(item.status)" :color="color" :size="size"></clip-loader></th>
                    <th scope="row" v-else> {{ getStatusText(item.status) }}</th>
                    <!-- <div v-for="item in this.Analyses" :key="item">{{ getImageName(item.source_image_url) }}</div> -->
                    </tr>
                </tbody>
                </table>
        </div>
        </ul>
      </div>
    </div>
  </template>
  
<script>
import axios from 'axios'
// import PulseLoader from 'vue-spinner/src/PulseLoader.vue'
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'



  export default {
    components: {
        // PulseLoader,
        ClipLoader,
    },
    data() {
      return {
        Analyses: [],
        timer: null,
        intervallTime: 6000,
        timerCalls: 0,
        loading: true,
        size: '20px',
        color: '#3B8070'
      }
    },
    created () {
        this.getAnalyses()
    },
    mounted: function() {
        this.timer = setInterval(() => {
            this.getAnalyses()
            this.timerCalls++
        }, this.intervallTime)
    },
    props: {
      processingList: Array // Define a prop to accept an array
    },
    methods: {
        async getAnalyses() {
            console.log(this.Analyses)
            await axios.get('api/v1/analyses/')
            .then(response => {
                this.Analyses = response.data.filter(analysis => analysis.dataset == this.$route.params.id && analysis.completed == false)
            })
            .catch(error => {
                console.log(error)
            })
            if (this.Analyses.length == 0) {
                this.$store.commit('setShowProcessingQueue', false)
                clearInterval(this.timer)
            }
        },
        getStatusText(status) {
            if (status == 'processing') {
                return ''
            }
            else {
                return status
            }
        },
        getLoading(status) {
            if (status == 'processing') {
                return true
            }
            else {
                return false
            }
        },
        getImageName(image) {
            return image.split('/')[6]
        }
    },
    beforeUnmount() {
        clearInterval(this.timer)
    }
  }
  </script>
  
  <style scoped>
  ul {
    list-style: none;
    padding: 0;
  }

  .info-window {
  position: fixed;
  bottom: 10%; /* Adjust as needed */
  right: 5%; /* Adjust as needed */
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
}
  
  </style>
  