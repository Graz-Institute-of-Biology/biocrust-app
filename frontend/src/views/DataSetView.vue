<template>
    <div class="container page-dataset">
        <div class="columns">
            <div class="column">
                <h1 class="title is-1">{{ dataset.dataset_name }}</h1>
                <div class="columns is-mobile">
                    <div class="column is-half">
                        <RouterLink :to="{ name: 'AddImageView', params: { id: dataset.id }}" class="button is-link" v-if="!this.$store.loading">Add images</RouterLink>
                        <RouterLink :to="{ name: 'AddMaskView', params: { id: dataset.id }}" class="button is-link" v-if="!this.$store.loading">Add masks</RouterLink>
                        <RouterLink :to="{ name: 'AddModel', params: { id: dataset.id }}" class="button is-link">Add Model</RouterLink>
                    </div>
                    <div class="column is-half">
                        <RouterLink :to="{ name: 'AnalyzeImagesView', params: { id: dataset.id }}" class="button is-primary" v-if="!this.$store.loading">Analyze images</RouterLink>
                        <div class="button is-primary" @click="showOverlay" v-if="!this.$store.loading">Show Overlay</div>
                        <div class="button delete-button is-danger" @click="setDeleteAlert" v-if="!this.$store.loading">Delete dataset</div>
                        <!-- <div class="button is-success" @click="analyze" v-if="!this.$store.loading">Analyze images</div> -->
                    </div>
                </div>
            </div>
        </div>
        <div class="chart">
            <Bar
                id="my-chart-id"
                :options="chartOptions"
                :data="chartData"
            />
        </div>
        <div class="image-grid" v-if="!this.$store.loading">
            <div v-for="(item, index) in items" :key="index" class="image-container" >
                <!-- <div class="image-wrapper" @click="toggleEnlarge(index)" @wheel="handleMouseWheel(index, $event)"> -->
                <div class="image-wrapper" 
                        @click="toggleEnlarge(index)" 
                        @wheel="handleMouseWheel(index, $event)"
                        :style="{ zIndex: isEnlarged(index) ? 1 : 0 }">
                    <img :src="item" class="image-small" v-if="!isEnlarged(index)">
                    <img :src="item" class="image-large" :style="{ transform: `scale(${getScale(index)})` }" v-if="isEnlarged(index)">
                    <img :src="getMaskUrl(item)" class="overlay-mask" @error="handleMaskImageError" v-if="setOverlay && !isEnlarged(index)">
                    <img :src="getMaskUrl(item)" class="overlay-mask-large" :style="{ transform: `scale(${getScale(index)})` }" @error="handleMaskImageError" v-if="setOverlay && isEnlarged(index)">
                </div>
            </div>
        </div>
        <div v-else>
            <div class="columns is-multiline">
                <div class="column is-12">
                    <h1 class="title is-1">Loading...</h1>
                </div>
            </div>
        </div>
        <div class="modal is-active modal-background" v-if="deleteAlert">
            <div class="modal-background"></div>
            <div class="modal-card">
                <header class="modal-card-head">
                <p class="modal-card-title">Sure you want to delete dataset?</p>
                </header>
                <footer class="modal-card-foot">
                <button class="button is-danger" @click="deleteDataset">Delete</button>
                <button class="button" @click="setDeleteAlert">Cancel</button>
                </footer>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import { defineComponent } from 'vue'
import 'viewerjs/dist/viewer.css'
import { directive as viewer } from "v-viewer"
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default defineComponent({
    name: 'DataSetView',
    components: { Bar },
    directives: {
      viewer: viewer({
        debug: true
      })
    },
    data () {
        return {
            Images: [],
            items: [],
            setOverlay: false,
            scale: 1,
            mask_items: [],
            enlarged: false,
            dataset: {},
            deleteAlert: false,
            dataset_name: this.$route.params.name,
            index: null,
            enlargedIndexes: [], 
            scales: {}, 
            chartData: {
                labels: [ 'Taxon 1', 'Taxon 2', 'Taxon 2' ],
                datasets: [{
                    backgroundColor: 'aqua',
                    label: "Taxon 1",
                    data: [123, null, null]
                    }, {
                    backgroundColor: 'lightgreen',
                    label: "Taxon 2",
                    data: [null, 321, null]
                    }, {
                    backgroundColor: 'pink',
                    label: "Taxon 2",
                    data: [null, null, 213]
                    }]
            },
            chartOptions: {
                responsive: false,
                skipNull: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Test Chart'
                    },
                    legend: {
                        display: true,
                        position: "bottom",
                    },
                },
            },
            options: {
                        ready: () => {
                        this.$viewer = this.$el.querySelector(".images").$viewer;
                        },
                        inline: false,
                        toolbar: {
                                    oneToOne: true,
                                    movable: true,
                                    prev: () => {
                                    this.$viewer.prev(true);
                                    },
                                    play: false,
                                    next: () => {
                                    this.$viewer.next(true);
                                    },
                                    overlay: () => {
                                        const viewer = this.$viewer;
                                        const a = document.createElement("a");
                                        a.href = viewer.image.src;
                                        a.download = viewer.image.alt;
                                        
                                    }
                        },
            },
        }
    },
    created () {
        this.$store.commit('setLoading', true)
        this.getDataset()
    },
    methods: {
        show () {
        const viewer = this.$el.querySelector('.images').$viewer
        viewer.show()
        },

        toggleEnlarge(index) {        
            if (this.enlargedIndexes.includes(index)) {
                this.enlargedIndexes = this.enlargedIndexes.filter(i => i !== index);
            } else {
                this.scales = {};
                this.enlargedIndexes = [];
                this.enlargedIndexes.push(index);
            }
        },

        isEnlarged(index) {
            return this.enlargedIndexes.includes(index);
        },

        handleMouseWheel(index, event) {
            if (this.isEnlarged(index)) {
                this.scales[index] = this.scales[index] || 1; 
                this.scales[index] += event.deltaY > 0 ? -0.1 : 0.1;

                this.scales[index] = Math.min(Math.max(this.scales[index], 0.5), 3);

                event.preventDefault();
            }
        },

        getScale(index) {
            return this.scales[index] || 1; 
        },

        getMaskUrl(item) {
            console.log(item)
        return this.mask_item.mask;
        },

        handleMaskImageError(event) {
            event.target.style.display = 'none';
        },

        showOverlay() {
            this.setOverlay = !this.setOverlay
        },

        setDeleteAlert() {
            this.deleteAlert = !this.deleteAlert
        },

        async deleteDataset() {
            await axios.delete(`api/v1/datasets/${this.$route.params.id}/`, 
                        { headers: {
                        'X-CSRFToken': '{{ csrftoken }}'
                                    } 
                        },
                        )
            .then(
                this.$router.push('/datasets')
            )
        },

        async getDataset() {
            await axios.get(`api/v1/datasets/${this.$route.params.id}/`)
            .then(response => {
                this.dataset = response.data
            })
            .catch(error => {
                console.log(error)
            })
            console.log("Dataset loaded")
            this.getImages()
            this.getMasks()
        },

        async getImages() {
                await axios.get('api/v1/images/')
                .then(response => {
                    this.Images = response.data.filter(image => image.dataset == this.$route.params.id)
                    let img_items = response.data.filter(image => image.dataset == this.$route.params.id)
                    for (let i = 0; i < img_items.length; i++) {
                        this.items.push(img_items[i].img)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
                this.$store.commit('setLoading', false)
        },

        async getMasks() {
            await axios.get('api/v1/masks/')
            .then(response => {
                this.Masks = response.data.filter(mask => mask.dataset == this.$route.params.id)
                let mask_items = response.data.filter(mask => mask.dataset == this.$route.params.id)
                for (let i = 0; i < mask_items.length; i++) {
                    this.mask_items.push(mask_items[i])
                }
                this.mask_item = this.mask_items[0]
            })
            .catch(error => {
                console.log(error)
            })
            this.$store.commit('setLoading', false)
        },

        getUrl(image) {
            const url = `${axios.defaults.baseURL}${image.img}`
            return url
        }
    }
})
</script>

<style scoped>

.chart {
  margin-left: auto;
  margin-right: auto;
  padding-top: 5%;
  padding-bottom: 5%;
} 

canvas {
    width: 40% !important;
    height: 40% !important;
    margin: 0 auto;
}
.page-dataset {
    margin-bottom: 10%;
}

.image-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(500px, 1fr)); /* Adjust the size as needed */
    grid-gap: 10px; /* Adjust the gap between images */
}

.image-container {
    position: relative;
}

.image-wrapper {
    position: relative;
    width: 100%;
    height: 100%;
}



.image-small,
.image-large {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 10px;
}

.overlay-mask,
.overlay-mask-large {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0.6;
    border-radius: 10px;
}

.button {
    margin-right: 10px;
}

.column-header {
    text-align: center;
}

.delete-button {
    float: right;
}
</style>