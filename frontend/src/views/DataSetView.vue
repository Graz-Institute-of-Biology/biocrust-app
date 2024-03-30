<template>
    <div class="is-fullheight">
        <div class="columns">
            <div class="column">
                <h1 class="title is-1">{{ dataset.dataset_name }}</h1>
                <div class="columns is-mobile">
                    <div class="column is-half">
                        <RouterLink :to="{ name: 'AddImageView', params: { id: dataset.id }}" class="button is-link" v-if="!this.$store.loading && this.allowActions">Add images</RouterLink>
                        <RouterLink :to="{ name: 'AddMaskView', params: { id: dataset.id }}" class="button is-link" v-if="!this.$store.loading && this.allowActions">Add masks</RouterLink>
                        <RouterLink :to="{ name: 'AddModel', params: { id: dataset.id }}" class="button is-link" v-if="this.allowActions">Add Model</RouterLink>
                    </div>
                    <div class="column is-half">
                        <div class="select is-success" :class="{ 'blinking': selectModelWarning }" v-if="this.allowActions">
                            <select class="is-focused" v-model="selectedMlModel" >
                                <option disabled value="">Select ML-Model</option>
                                <option v-for="(item, index) in Models" :key="index">{{ item.model_name }}</option>
                            </select>
                        </div>
                        <div class="button is-primary" @click="handleAnalyses" v-if="!this.$store.loading && this.allowActions">Analyze Images ({{ this.items.length }})</div>
                        <div class="button is-primary" @click="showOverlay" v-if="!this.$store.loading && this.mask_items.length > 0">Show Overlay</div>
                        <div class="button delete-button is-danger" @click="setDeleteAlert" v-if="!this.$store.loading && this.allowActions">Delete dataset</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="columns">
            <!-- Image Grid Column -->
            <div class="column is-two-thirds">
                <div class="image-grid-container">
                    <div class="image-grid" v-if="!this.$store.loading">
                        <div v-for="(item, index) in Images" :key="index" class="image-container" >
                            <div class="image-wrapper" 
                                    @click="() => { toggleEnlarge(index); handleImageClick(item); }"
                                    @wheel="handleMouseWheel(index, $event)"
                                    :style="{ zIndex: isEnlarged(index) ? 1 : 0 }">
                                <img :src="item.img" class="image-small" v-if="!isEnlarged(index)">
                                <img :src="item.img" class="image-large" :style="{ transform: `scale(${getScale(index)})` }" v-if="isEnlarged(index)">
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
                </div>
            </div>
            
            <!-- Chart Column -->
            <div class="column">
                <h1 class="title is-3">Class Distribution</h1>
                <input v-if="this.showChart" type="checkbox" id="checkbox" v-model="checkExcludeBackground" @change="excludeBackground" />
                <label v-if="this.showChart" for="checkbox">Exclude Background</label>
                <div class="chart-container">
                    <Doughnut :data="chartData" :options="chartOptions" />
                </div>
                <div v-if="this.showChart" class="chart-table">
                    <button class="button is-primary" @click="downloadCSV" style="margin-bottom: 10px;">Download CSV </button>
                        <table class="table is-bordered is-striped is-narrow is-hoverable">
                            <thead>
                                <tr>
                                    <th class="is-primary">Index</th>
                                    <th class="is-primary">Data</th>
                                    <th class="is-primary">Label</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(data, label) in chartData.datasets[0].data" :key="label">
                                    <td>{{ label }}</td>
                                    <td>{{ data }}</td>
                                    <td>{{ chartData.labels[label] }}</td>
                                </tr>
                            </tbody>
                        </table>
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
        <info-window v-if="getShowProcessingQueue" :processingList="imageProcessingList"></info-window>
    </div>
</template>


<script>
import axios from 'axios'
import { defineComponent } from 'vue'
import 'viewerjs/dist/viewer.css'
import { directive as viewer } from "v-viewer"
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, DoughnutController, CategoryScale, ArcElement } from 'chart.js'
import InfoWindow from './InfoWindow.vue'; // Import the InfoWindow component
import { mapGetters } from 'vuex'

ChartJS.register(Title, Tooltip, Legend, DoughnutController, CategoryScale, ArcElement)

export default defineComponent({
    name: 'DataSetView',
    components: { 
                    Doughnut,
                    InfoWindow 
                },
    directives: {
      viewer: viewer({
        debug: true
      })
    },
    data () {
        return {
            Analyses: [],
            analysesStarted: false,
            info: "This is some information to display.",
            selectModelWarning : false,
            blinkDuration: 1000,
            imageProcessingList: [],
            Images: [],
            items: [],
            Models: [],
            selectedMlModel: '',
            selectedMlModelId: null,
            setOverlay: false,
            allowActions: false,
            scale: 1,
            mask_items: [],
            enlarged: false,
            dataset: {},
            deleteAlert: false,
            dataset_name: this.$route.params.name,
            index: null,
            enlargedIndexes: [], 
            scales: {},
            showChart: false,
            checkExcludeBackground: false,
            clickedImage: null,
            chartData: {
                labels: [ ' ', ' ', ' ' ],
                datasets: [{
                    backgroundColor: 'white',
                    label: " ",
                    data: [null, null, null]
                    }, {
                    backgroundColor: 'white',
                    label: " ",
                    data: [null, null, null]
                    }, {
                    backgroundColor: 'white',
                    label: " ",
                    data: [null, null, null]
                    }]
            },
            chartOptions: {
                responsive: false,
                skipNull: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Click on image to see class distribution.'
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
        this.$store.commit('setShowProcessingQueue', false)
        this.getImages()
        this.getDataset()
        this.getMasks()
        this.getModels()
        this.getAnalyses()
    },
    computed: {
        ...mapGetters(['getShowProcessingQueue'])
    },
    methods: {
        show () {
        const viewer = this.$el.querySelector('.images').$viewer
        viewer.show()
        },
        async getDataset() {
            await axios.get(`api/v1/datasets/${this.$route.params.id}/`)
            .then(response => {
                this.dataset = response.data
                if (localStorage.getItem('username').includes('Guest') && this.dataset.owner == localStorage.getItem('username')) {
                    this.allowActions = true
                } else if (localStorage.getItem('username').includes('Admin')) {
                    this.allowActions = true
                }
            })
            .catch(error => {
                console.log(error)
            })
        },
        downloadCSV() {
            const datasetName = this.dataset.dataset_name;
            const imageName = this.clickedImage ? this.clickedImage.name : 'data';
            const fileName = `${datasetName}_${imageName}_data.csv`;
            const csvContent = this.generateCSVContent();
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement('a');
            link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodedUri);
            link.setAttribute('download', fileName);
            document.body.appendChild(link);
            link.click();
        },
        generateCSVContent() {
            let csvContent = "Index,Data,Label\n";
            this.chartData.datasets[0].data.forEach((data, index) => {
                csvContent += `${index},${data},${this.chartData.labels[index]}\n`;
            });
            return csvContent;
        },
        setSelectedMlModel() {
             this.selectedMlModel = this.Models.filter(model => model.model_name == this.selectedMlModel)[0]
        },
        setModelWarningFalse() {
            this.selectModelWarning = false
        },
        async getAnalyses() {
            await axios.get('api/v1/analyses/')
            .then(response => {
                this.Analyses = response.data.filter(analysis => analysis.dataset == this.$route.params.id)
            })
            .catch(error => {
                console.log(error)
            })
            let processingAnalyses = this.Analyses.filter(analysis => analysis.status == "processing")
            if (processingAnalyses.length > 0) {
                this.$store.commit('setShowProcessingQueue', true)
            }
        },
        async getModels() {
            await axios.get('api/v1/models/')
            .then(response => {
                this.Models = response.data
            })
            .catch(error => {
                console.log(error)
            })
        },
        async fetchClassDistribution(image) {
            const imageUrl = image; 
            const maskUrl = this.getMaskUrl(imageUrl); 
            try {
                const response = await axios.get('api/v1/masks/');
                const maskData = response.data;

                const matchingMask = maskData.find(mask => mask.mask === maskUrl);

                if (matchingMask && matchingMask.class_distributions) {
                    if (this.checkExcludeBackground) {
                        const classDistributions = JSON.parse(matchingMask.class_distributions);
                        const class_names = Object.keys(classDistributions.class_distributions)
                        // const backgroundIndexDist = 0;
                        for (let i = 0; i < class_names.length; i++) {
                            if (class_names[i].includes('background')) {
                                delete classDistributions.class_distributions[class_names[i]];
                            }
                            if (classDistributions.class_colors[i].name.includes('background')) {
                                delete classDistributions.class_colors[i];
                            }
                        }
                        // const backgroundIndexColor = null;

                        // delete classDistributions.class_colors[backgroundIndexColor]
                        console.log(classDistributions.class_distributions)
                        return classDistributions;
                    } else {
                        console.log(JSON.parse(matchingMask.class_distributions))
                        return JSON.parse(matchingMask.class_distributions);
                    }
                }
            } catch (error) {
                console.error("Error fetching class distribution:", error);
            }
            return null;
        },

        getImageName(imageUrl) {
            const parts = imageUrl.split('/');
            const filename = parts[parts.length - 1];
            return filename;
        },
        async handleAnalyses() {
            if (this.selectedMlModel == '') {
                this.selectModelWarning = true
                setTimeout(() => {
                    this.selectModelWarning = false; // Remove the blinking effect after the specified duration
                }, this.blinkDuration);
                return
            } else {
                this.setSelectedMlModel()
            }
            this.$store.commit('setShowProcessingQueue', true)
            for (let i = 0; i < this.Images.length; i++) {
                await this.analyzeImage(this.Images[i])
                this.imageProcessingList.push(this.Images[i].name)
            }
        },
        async analyzeImage(image) {

            await this.sendAnalysisRequest(image)
                .then(response => {
                    this.message = 'Analysis request sent successfully!'
                    console.log(response)
                })
                .catch(error => {
                    this.message = 'Analysis request Error!'
                    console.log(error)
                });
            },

        async sendAnalysisRequest(image) {
            let formData = new FormData()
            formData.append('owner', localStorage.getItem('username'))
            formData.append('slug', image.slug)
            formData.append('dataset', image.dataset)
            formData.append('ml_model_url', this.selectedMlModel.file) // USE HTTPS URL!
            formData.append('source_image_url', image.img) // USE HTTPS URL!
            formData.append('parent_img_id', image.id)
            formData.append('ml_model_id', this.selectedMlModel.id)
            formData.append('token', localStorage.getItem('token'))
            
            return axios.post('api/v1/analyses/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': '{{ csrftoken }}'
                },
            })
        },
        excludeBackground() {
            if (this.checkExcludeBackground) {
                this.handleImageClick(this.clickedImage)
            } else {
                this.handleImageClick(this.clickedImage)
            }
        },

        async handleImageClick(image) {
            this.clickedImage = image;
            const classDistribution = await this.fetchClassDistribution(image);
            this.showChart = true;
            if (classDistribution) {
                const labels = Object.keys(classDistribution.class_distributions);
                const data = Object.values(classDistribution.class_distributions);
                const colors = Object.values(classDistribution.class_colors).map(color => color.color);
                // const colors = Object.values(classDistribution.class_colors).map(colorStr => {
                //     return colorStr.replace(/\[|\]/g, '').split(',').map(Number);
                // });
                
                this.chartData = {
                    labels: labels,
                    datasets: [{
                        label: labels,
                        data: data,
                        backgroundColor: colors.map(color => `rgba(${color.join(',')}, 0.6)`), // Construct RGBA values
                    }]
                };
                this.chartOptions = {
                    responsive: false,
                    skipNull: true,
                    plugins: {
                        title: {
                            display: true,
                            text: this.getImageName(image.img)
                        },
                        legend: {
                            display: true,
                            position: "bottom",
                            labels: {
                                generateLabels: (chart) => {
                                    const data = chart.data;
                                    if (data.labels.length && data.datasets.length) {
                                        return data.labels.map((label, i) => {
                                            const backgroundColor = data.datasets[0].backgroundColor[i];
                                            return {
                                                text: label,
                                                fillStyle: backgroundColor
                                            };
                                        });
                                    }
                                    return [];
                                }
                            }
                        },
                    },
                };
            } else {
                // temporary default data
                this.chartData = { 
                    labels: [ ' ', ' ', ' ' ],
                    datasets: [{
                        backgroundColor: 'white',
                        label: " ",
                        data: [null, null, null]
                    }, {
                        backgroundColor: 'white',
                        label: " ",
                        data: [null, null, null]
                    }, {
                        backgroundColor: 'white',
                        label: " ",
                        data: [null, null, null]
                    }]
                };
                this.chartOptions = {
                    responsive: false,
                    skipNull: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Click on image to see class distribution.'
                        },
                        legend: {
                            display: true,
                            position: "bottom",
                        },
                    },
                };
            }
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
            for (let mask_item of this.mask_items) {
                if (mask_item.parent_image_url.includes('django'))
                    item = item.replace('127.0.0.1', 'django')
                if (mask_item.parent_image === item.id) {
                    return mask_item.mask.replace('https', 'http'); // only for local development
                }
            }
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

        async getImages() {
                await axios.get('api/v1/images/')
                .then(response => {
                    this.Images = response.data.filter(image => image.dataset == this.$route.params.id)
                    let img_items = response.data.filter(image => image.dataset == this.$route.params.id)
                    for (let i = 0; i < img_items.length; i++) {
                        this.items.push(img_items[i].img.replace('http', 'https'))
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
                // this.Masks = response.data.filter(mask => mask.dataset == this.$route.params.id)
                let mask_items = response.data.filter(mask => mask.dataset == this.$route.params.id)
                for (let i = 0; i < mask_items.length; i++) {
                    mask_items[i].parent_image_url = mask_items[i].parent_image_url.replace('http', 'https')
                    mask_items[i].mask = mask_items[i].mask.replace('http', 'https')
                    this.mask_items.push(mask_items[i])
                }
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

.chart-container {
    width: 100%; /* Set width to any desired value */
    height: 0;
    padding-top: 100%; /* This ensures 1:1 aspect ratio */
    padding-bottom: 20px; /* Optional: Add padding to create some space */
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    background-color: #ffffff;
    margin-bottom: 20px; 
    position: relative;
    overflow: hidden; /* Hide overflow to prevent scrollbars */
}

.chart-container canvas {
    width: 100% !important;
    height: 100% !important;
    position: absolute;
    top: 0;
    left: 0;
}

.page-dataset {
    margin-bottom: 10%;
}

@media (max-width: 768px) {
    .column {
        width: 100%;
    }
}

.image-grid-container { 
    overflow-y: auto;
    padding-bottom: 5%; 
    padding-left: 5%;
    padding-right: 5%;
    padding-top: 5%;
    scrollbar-width: none;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
    border-radius: 10px;
}

.chart {
  margin-left: auto;
  margin-right: auto;
  padding-top: 5%;
  padding-bottom: 5%;
} 

canvas {
    /* width: 100% !important; */
    height: 100% !important;
    margin: 0 auto;
}
.page-dataset {
    margin-bottom: 10%;
}

.image-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
    grid-gap: 10px;
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

@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0; }
  100% { opacity: 1; }
}

.blinking {
  animation: blink 0.2s infinite;
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

.select {
    margin-right: 10px;
}

.column-header {
    text-align: center;
}

.delete-button {
    float: right;
}
</style>