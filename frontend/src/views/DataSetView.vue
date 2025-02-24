<template>
    <div class="is-fullheight">
        <div class="columns">
            <div class="column">
                <h1 class="title is-1">{{ dataset.dataset_name }}</h1>
                <div class="columns is-mobile">
                    <div class="column is-half">
                        <RouterLink :to="{ name: 'AddImageView', params: { id: dataset.id }}" class="button is-link" v-if="!this.$store.loading && isSuperUser || allowActions">Add images</RouterLink>
                        <RouterLink :to="{ name: 'AddMaskView', params: { id: dataset.id }}" class="button is-link" v-if="!this.$store.loading && isSuperUser">Add masks</RouterLink>
                        <RouterLink :to="{ name: 'AddModel', params: { id: dataset.id }}" class="button is-link" v-if="isSuperUser">Add Model</RouterLink>
                    </div>
                    <div class="column is-half right">
                        <div class="button is-primary" @click="handleAnalyses" v-if="!this.$store.loading && isSuperUser || this.allowActions">Analyze Images ({{ this.items.length }})</div>
                        <div class="button is-primary" @click="showOverlay" v-if="!this.$store.loading && isSuperUser || this.mask_items.length > 0">Show Overlay</div>
                        <div class="button delete-button is-danger" @click="setDeleteAlert" v-if="!this.$store.loading && isSuperUser">Delete dataset</div>
                    </div>
                </div>
                <div class="columns is-mobile">
                    <div class="select is-success" :class="{ 'blinking': selectModelWarning }" v-if="isSuperUser || this.allowActions">
                        <select class="is-focused" v-model="selectedMlModel" >
                            <option disabled value="">Select ML-Model</option>
                            <option v-for="(item, index) in Models" :key="index">{{ item.model_name }}</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
        <div class="columns">
            <!-- Image Grid Column -->
            <div class="column is-two-thirds">
                <div class="image-grid-container">
                    <!-- Popup Modal -->
                    <div v-if="this.zoomedImage" class="modal-overlay" 
                        @dblclick="closeModal"
                        @wheel="handleModalMouseWheel($event)">
                        <div class="modal-content" 
                            @mousedown="startDrag($event)"
                            @mousemove="handleDrag($event)"
                            @mouseup="stopDrag"
                            @mouseleave="stopDrag">
                            <img :src="this.zoomedImage.img" class="image-large" 
                                :style="{ transform: `scale(${getModalScale()}) translate(${modalPosition.x}px, ${modalPosition.y}px)` }">
                            <img :src="getMaskUrl(this.zoomedImage)" class="overlay-mask-large" 
                                :style="{ transform: `scale(${getModalScale()}) translate(${modalPosition.x}px, ${modalPosition.y}px)` }" 
                                @error="handleMaskImageError" v-if="setOverlay">
                        </div>
                    </div>
                    <div v-else>
                        <div class="image-grid" v-if="!this.$store.loading">
                            <div v-for="(item, index) in Images" :key="index" class="image-container" >
                                <!-- <div class="image-wrapper" 
                                        @click="() => { toggleEnlarge(index); handleImageClick(item); openModal(item) }"
                                        @wheel="handleMouseWheel(index, $event)"
                                        :style="{ zIndex: isEnlarged(index) ? 1 : 0 }">
                                    <img :src="item.img" class="image-small" v-if="!isEnlarged(index)">
                                    <img :src="item.img" class="image-large" :style="{ transform: `scale(${getScale(index)})` }" v-if="isEnlarged(index)">
                                    <img :src="getMaskUrl(item)" class="overlay-mask" @error="handleMaskImageError" v-if="setOverlay && !isEnlarged(index)">
                                    <img :src="getMaskUrl(item)" class="overlay-mask-large" :style="{ transform: `scale(${getScale(index)})` }" @error="handleMaskImageError" v-if="setOverlay && isEnlarged(index)">
                                </div> -->
                                <div class="image-wrapper" 
                                        @dblclick="() => { openModal(item) }"
                                        @click="() => { handleImageClick(item) }">
                                    <img :src="item.img" class="image-small" v-if="!isEnlarged(index)">
                                    <img :src="getMaskUrl(item)" class="overlay-mask" @error="handleMaskImageError" v-if="setOverlay && !isEnlarged(index)">
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
            </div>

            <!-- Chart Column -->
            <div v-if="this.clickedImage" class="column">
                <h1 class="title is-3">Class Distribution</h1>
                <div v-if="this.showChart" class="chart-table">
                    <button class="button is-primary" @click="downloadAllImagesCSV" style="margin-bottom: 10px;">Download CSV </button>
                </div>
                <div class="chart-container">
                    <Doughnut :data="chartData" :options="chartOptions" />
                </div>
                <input v-if="this.showChart" type="checkbox" class="checkbox" id="checkbox" v-model="checkExcludeBackground" @change="excludeBackground" />
                <label v-if="this.showChart" for="checkbox">Exclude Background</label>
                <div v-if="this.showChart" class="table-container">
                    <table class="table is-bordered is-striped is-narrow is-hoverable">
                        <thead>
                            <tr>
                                <th class="is-primary">Class Index</th>
                                <th class="is-primary">Coverage</th>
                                <th class="is-primary">Class</th>
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
            <div v-else>
                <div class="column has-text-centered">
                    <h1 class="title is-4">Select image to see analysis results</h1>
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
import { mapGetters, mapActions } from 'vuex'

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
            allowActions: true,
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
            zoomedImage: null,
            modalPosition: { x: 0, y: 0 },
            isDragging: false,
            startDragPosition: { x: 0, y: 0 },
            chartData: {
                labels: [],
                datasets: [{
                    backgroundColor: [],
                    data: []
                }]
            },
            chartOptions: {
                responsive: false,
                skipNull: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Class Distribution.'
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
        this.initializeStatus()
        this.getImages()
        this.getDataset()
        this.getMasks()
        this.getModels()
        this.getAnalyses()
    },
    computed: {
        ...mapGetters(['getShowProcessingQueue', 'isSuperUser'])
    },
    methods: {
        show () {
        const viewer = this.$el.querySelector('.images').$viewer
        viewer.show()
        },
        ...mapActions(['initializeStatus']),
        openModal(imageSrc) {
        this.zoomedImage = imageSrc;
        this.scale = 1;
        this.modalPosition = { x: 0, y: 0 };
        },
        closeModal() {
        this.zoomedImage = null;
        },
        async getDataset() {
            console.log("SU")
            console.log(this.isSuperUser)
            await axios.get(`api/v1/datasets/${this.$route.params.id}/`)
            .then(response => {
                this.dataset = response.data

                if (this.dataset.owner == localStorage.getItem('username')) {
                    this.allowActions = true
                } else {
                    this.allowActions = false
                }
            })
            .catch(error => {
                console.log(error)
            })
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
                console.log(this.Analyses)
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
                        for (let i = 0; i < class_names.length; i++) {
                            if (class_names[i].includes('background')) {
                                delete classDistributions.class_distributions[class_names[i]];
                            }
                            if (classDistributions.class_colors[i].name.includes('background')) {
                                delete classDistributions.class_colors[i];
                            }
                        }
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
                    this.selectModelWarning = false; 
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
                    this.message = 'Error sending analysis request!'
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
                            text: 'Select image to see class distribution.'
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

        getScale(index) {
            return this.scales[index] || 1; 
        },

        handleMouseWheel(index, event) {
            if (this.isEnlarged(index)) {
                this.scales[index] = this.scales[index] || 1; 
                this.scales[index] += event.deltaY > 0 ? -0.1 : 0.1;

                this.scales[index] = Math.min(Math.max(this.scales[index], 0.5), 3);

                event.preventDefault();
            }
        },

        getModalScale() {
            return this.scale || 1; 
        },

        handleModalMouseWheel(event) {
            
            this.scale = this.scale || 1; 
            this.scale += event.deltaY > 0 ? -0.1 : 0.1;

            this.scale = Math.min(Math.max(this.scale, 0.5), 3);

            event.preventDefault();
            
        },

        startDrag(event) {
            if (this.scale > 1) {
                this.isDragging = true;
                this.startDragPosition = {
                    x: event.clientX - this.modalPosition.x,
                    y: event.clientY - this.modalPosition.y
                };
                event.preventDefault();
            }
        },
        
        handleDrag(event) {
            if (this.isDragging && this.scale > 1) {
                this.modalPosition = {
                    x: event.clientX - this.startDragPosition.x,
                    y: event.clientY - this.startDragPosition.y
                };
                event.preventDefault();
            }
        },
        
        stopDrag() {
            this.isDragging = false;
        },
        

        getMaskUrl(item) {
            for (let mask_item of this.mask_items) {
                // if (mask_item.parent_image_url.includes('django'))
                //     item = item.replace('127.0.0.1', 'django')
                if (mask_item.parent_image === item.id) {
                    return mask_item.mask //.replace('https', 'http'); // only for local development
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
                        this.items.push(img_items[i].img) //.replace('http', 'https'))
                        // this.items.push(img_items[i].img)
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
                    // mask_items[i].parent_image_url = mask_items[i].parent_image_url.replace('http', 'https')
                    // mask_items[i].mask = mask_items[i].mask.replace('http', 'https')
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
        },

        downloadAllImagesCSV() {
            this.$store.commit('setLoading', true);
            
            this.collectAllImageData()
                .then(allData => {
                    console.log("Data collection done:", {
                        imageCount: allData.imageData.length,
                        classCount: allData.classColumns.length,
                        hasMetadata: !!allData.metadata
                    });
                    
                    const csvContent = this.generateAllImagesCSVContent(allData);
                    console.log("CSV content, length:", csvContent.length);
                    
                    if (!csvContent.trim()) {
                        console.error("CSV content empty!");
                        this.$store.commit('setLoading', false);
                        return;
                    }
                    
                    const datasetName = this.dataset.dataset_name || "dataset";
                    const fileName = `${datasetName}_all_images_data.csv`;
                    
                    try {
                        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                        if (window.navigator.msSaveOrOpenBlob) {
                            window.navigator.msSaveBlob(blob, fileName);
                        } else {
                            const link = document.createElement('a');
                            const url = URL.createObjectURL(blob);
                            link.setAttribute('href', url);
                            link.setAttribute('download', fileName);
                            link.style.visibility = 'hidden';
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                        }
                        console.log("CSV download started");
                    } catch (error) {
                        console.error("Error during file download:", error);
                    }
                    
                    this.$store.commit('setLoading', false);
                })
                .catch(error => {
                    console.error("Error in data collection process:", error);
                    alert("Error generating CSV. Check console for details.");
                    this.$store.commit('setLoading', false);
                });
        },
        
        async collectAllImageData() {
            console.log(`No. images: ${this.Images.length} images`);
            const allImageData = [];
            const uniqueClasses = new Map();
            
            for (const image of this.Images) {
                try {
                    console.log(`${image.name || image.img}`);
                    const classDistribution = await this.fetchClassDistribution(image);
                    
                    if (!classDistribution) {
                        console.warn(`No class distribution for: ${image.name || image.img}`);
                        continue;
                    }
                    
                    if (!classDistribution.class_distributions) {
                        console.warn(`Invalid class distribution for: ${image.name || image.img}`, classDistribution);
                        continue;
                    }
                    
                    const labelIndices = Object.keys(classDistribution.class_distributions);
                    console.log(`No. classes: ${labelIndices.length}`);
                    
                    labelIndices.forEach((label, index) => {
                        const indexNumber = parseInt(label, 10) || index;
                        uniqueClasses.set(label, {
                            name: label,
                            index: indexNumber,
                            label: `${indexNumber} ${label}` // convention - to be discussed
                        });
                    });
                    
                    allImageData.push({
                        imageName: this.getImageName(image.img),
                        distribution: classDistribution.class_distributions
                    });
                } catch (error) {
                    console.error(`Error processing: ${image.img}:`, error);
                }
            }
                        
            const sortedClasses = Array.from(uniqueClasses.values())
                .sort((a, b) => a.index - b.index);
            
            console.log("Sorted class list:", sortedClasses);
            
            const metadata = this.collectDatasetMetadata();
            console.log("Metadata:", metadata);
            
            return {
                imageData: allImageData,
                classColumns: sortedClasses,
                metadata: metadata
            };
        },
        
        collectDatasetMetadata() {
            const totalImages = this.Images.length;
            const totalMasks = this.mask_items.length;
            const modelCount = this.Models.length;
            const analysesCount = this.Analyses.length;
            
            const datasetInfo = {
                "Dataset Name": this.dataset.dataset_name || "Unnamed Dataset",
                "Dataset ID": this.dataset.id || "Unknown",
                "Owner": this.dataset.owner || "Unknown",
                "Creation Date": this.dataset.created_at || new Date().toISOString(),
                "Last Modified": this.dataset.updated_at || new Date().toISOString(),
                "Total Images": totalImages,
                "Total Masks": totalMasks,
                "Available Models": modelCount,
                "Analyses Performed": analysesCount,
                "Export Date": new Date().toISOString()
            };
            
            if (this.selectedMlModel) {
                if (typeof this.selectedMlModel === 'string') {
                    datasetInfo["Analysis Model"] = this.selectedMlModel;
                } else if (this.selectedMlModel.model_name) {
                    datasetInfo["Analysis Model"] = this.selectedMlModel.model_name;
                }
            }
            
            return datasetInfo;
        },
        
        generateAllImagesCSVContent({ imageData, classColumns, metadata }) {
            console.log("Starting CSV generation");
            
            if (!imageData || imageData.length === 0) {
                console.warn("No image data available for CSV generation");
                return "No image data available\n";
            }
            
            if (!classColumns || classColumns.length === 0) {
                console.warn("No class columns available for CSV generation");
                return "No class data available\n";
            }
            
            let csvContent = "";
            
            try {
                csvContent += "DATASET METADATA\n";
                Object.entries(metadata || {}).forEach(([key, value]) => {
                    csvContent += `${key},${value}\n`;
                });
                csvContent += "\n";
                
                if (imageData.length > 0 && classColumns.length > 0) {
                    csvContent += "CLASS SUMMARY\n";
                    classColumns.forEach(classInfo => {
                        let totalCoverage = 0;
                        let imagesWithClass = 0;
                        
                        imageData.forEach(image => {
                            if (image.distribution && classInfo.name in image.distribution) {
                                const value = image.distribution[classInfo.name] || 0;
                                if (value > 0) {
                                    totalCoverage += value;
                                    imagesWithClass++;
                                }
                            }
                        });
                        
                        const avgCoverage = imagesWithClass > 0 ? totalCoverage / imagesWithClass : 0;
                        const percentImagesWithClass = (imagesWithClass / imageData.length) * 100;
                        console.log('Class info:');
                        console.log({classInfo});
                        csvContent += `${classInfo.index},${classInfo.name},Avg Coverage: ${avgCoverage.toFixed(2)}%,Present in: ${percentImagesWithClass.toFixed(2)}% of images\n`;
                    });
                    csvContent += "\n";
                    
                    csvContent += "Image";
                    classColumns.forEach(classInfo => {
                        csvContent += `,${classInfo.label}`;
                    });
                    csvContent += "\n";
                    
                    imageData.forEach(image => {
                        if (!image.distribution) {
                            console.warn(`Missing distribution data for image: ${image.imageName}`);
                            return;
                        }
                        
                        csvContent += `${image.imageName}`;
                        
                        classColumns.forEach(classInfo => {
                            const value = image.distribution[classInfo.name] || 0;
                            csvContent += `,${value}`;
                        });
                        
                        csvContent += "\n";
                    });
                } else {
                    csvContent += "Insufficient data to generate class summary\n";
                }
                
                console.log(`CSV generation done!`);
                return csvContent;
                
            } catch (error) {
                console.error("Error writing CSV:", error);
                return `ERROR WRITING CSV: ${error.message}\n`;
            }
        },
    }
})
</script>

<style scoped>
.blinking {
    animation: blink 0.2s infinite;
}

.button {
    margin-bottom: 2%;
    /* margin-left: 10px; */
    margin-right: 10px;
    width: 140px;
}

.canvas {
    height: 100% !important;
    margin: 0 auto;
}

.chart {
    margin-left: auto;
    margin-right: auto;
    padding-bottom: 5%;
    padding-top: 5%;
}

.chart-container {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
    height: 0;
    margin-bottom: 20px;
    overflow: hidden;
    padding-bottom: 20px;
    padding-top: 100%;
    position: relative;
    width: 100%;
}

.chart-container canvas {
    height: 100% !important;
    left: 0;
    position: absolute;
    top: 0;
    width: 100% !important;
}

.column.is-half {
    align-items: center;
    display: flex;
    padding-left: 0px;
    padding-right: 0px;
}

.columns.is-mobile {
    display: flex;
    justify-content: space-between;
}

.checkbox {
    margin-right: 10px;
}

.image-container {
    position: relative;
}

.image-grid {
    display: grid;
    grid-gap: 10px;
    grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
}

.image-grid-container {
    border-radius: 10px;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
    height: 100vh;
    margin: 0 auto;
    max-height: 100%;
    max-width: 100%;
    overflow-y: auto;
    padding-bottom: 5%;
    padding-left: 5%;
    padding-right: 5%;
    padding-top: 5%;
    scrollbar-width: none;
    width: 100vw;
}

.image-large,
.image-small {
    border-radius: 10px;
    height: 100%;
    object-fit: cover;
    width: 100%;
}

.image-wrapper {
    height: 100%;
    position: relative;
    width: 100%;
}

.image-wrapper:hover {
    transform: scale(1.01);
    z-index: 10;
}

.modal-overlay {
    /* position: fixed; */
    margin: auto;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgb(256, 256, 256);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    border-radius: 10px;
}

.modal-content {
    background: rgb(256, 256, 256);
    padding: 10px;
    border-radius: 10px;
    max-width: 90%;
    max-height: 90%;
    overflow: visible;
    cursor: move;
}

.modal-content.dragging {
    cursor: grabbing;
}

.overlay-mask,
.overlay-mask-large {
    border-radius: 10px;
    height: 100%;
    left: 0;
    opacity: 0.6;
    position: absolute;
    top: 0;
    width: 100%;
}

.page-dataset {
    margin-bottom: 10%;
}

.right {
    justify-content: flex-end;
}

.right .button {
    margin-right: 0px;
    margin-left: 10px;
}

.select {
    margin-left: 0;
    margin-right: 10px;
}

.table-container {
    margin-top: 1rem;
    overflow-y: auto;
    max-height: 400px;
}

.title {
    margin-bottom: 1rem;
}

@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
}

@media (max-width: 768px) {
    .button {
        width: 85%;
        /* margin-left: 5px; */
    }
    .canvas {
        height: 70% !important;
    }
    .column {
        flex-direction: column;
        width: 100%;
    }
    .column.is-half {
        align-items: flex-start;
    }
    .column.is-half.right{
        padding-right: 0;
        padding-left: 10px;
        align-items: flex-end;
    }
    .image-wrapper {
        width: 30%;
    }
    .image-grid-container {
        height: 50vh;
    }
    .right .button{
        margin-right: 0;
    }
}

</style>
