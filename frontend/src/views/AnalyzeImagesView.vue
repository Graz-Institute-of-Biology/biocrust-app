<template>
    <div class="container page-dataset">
            <div class="columns">
                <div class="column">
                    <h1 class="title is-1">{{ dataset.dataset_name }}</h1>
                    <div class="columns is-mobile">
                        <div class="column is-half">
                        <div class="button is-success" @click="analyzeImage" v-if="!this.$store.loading">Analyze</div>
                        <!-- <div class="button is-success" @click="analyze" v-if="!this.$store.loading">Analyze images</div> -->
                        
                        </div>
                        <div class="column is-half">
                    </div>
                    </div>
                </div>
            </div>
            <div class="image-grid" v-if="!this.$store.loading">
                <div v-for="(item, index) in items" :key="index" class="image-container">
                    <div>
                        <div v-if="getAnalysisInfo(index) == 'error'" class="notification is-error">
                            Status: {{ getAnalysisInfo(index) }}
                        </div>
                        <div v-else-if="getAnalysisInfo(index) == 'processing'" class="notification is-info">
                            Status: {{ getAnalysisInfo(index) }}
                        </div>
                        <div v-else-if="getAnalysisInfo(index) == 'processed & saved' || getAnalysisInfo(index) == 'processed/sending result'" class="notification is-success">
                            Status: {{ getAnalysisInfo(index) }}
                        </div>
                        <div v-else class="notification is-warning">
                            Status: {{ getAnalysisInfo(index) }}
                        </div>
                        <div class="image-wrapper" 
                            @click="selectImage(index)" 
                            @wheel="handleMouseWheel(index, $event)"
                            :class="{ 'selected': isSelected(index) }"
                            :style="{ zIndex: isEnlarged(index) ? 1 : 0 }">
                            <img :src="item" class="image-small" v-if="!isEnlarged(index)">
                            <img :src="item" class="image-large" :style="{ transform: `scale(${getScale(index)})` }" v-if="isEnlarged(index)">
                            <img :src="getMaskUrl(item)" class="overlay-mask" @error="handleMaskImageError" v-if="setOverlay && !isEnlarged(index)">
                            <img :src="getMaskUrl(item)" class="overlay-mask-large" :style="{ transform: `scale(${getScale(index)})` }" @error="handleMaskImageError" v-if="setOverlay && isEnlarged(index)">
                        </div>
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
</template>


<script>
import axios from 'axios'
import { defineComponent } from 'vue'
import 'viewerjs/dist/viewer.css'
import { directive as viewer } from "v-viewer"

export default defineComponent({
    name: 'DataSetView',
    directives: {
      viewer: viewer({
        debug: true
      })
    },
    data () {
        return {
            Images: [],
            Analyses: [],
            items: [],
            setOverlay: false,
            scale: 1,
            mask_items: [],
            enlarged: false,
            dataset: {},
            deleteAlert: false,
            dataset_name: this.$route.params.name,
            index: null,
            file: null,
            enlargedIndexes: [], 
            scales: {},
            selectedImage: null,
            mask: {
                name: '',
                owner: '',
                slug: '',
                dataset: '',
                source_image_url: '',
                ml_model_url: '',       
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
        this.getImages()
        this.getMasks()
        this.getModels()
        this.getAnalyses()
    },
    methods: {
        show () {
            const viewer = this.$el.querySelector('.images').$viewer
            viewer.show()
        },

        selectImage(index) {
        this.selectedImage = this.selectedImage === index ? null : index;
        },

        isSelected(index) {
            return this.selectedImage === index;
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
        showOverlay() {
            this.setOverlay = !this.setOverlay
            console.log(this.deleteAlert)
        },
        setDeleteAlert() {
            this.deleteAlert = !this.deleteAlert
            console.log(this.deleteAlert)
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
        },
        getAnalysisInfo(item) {
            console.log(this.Images[item].id)
            console.log(this.Analyses)
            const analysis = this.Analyses.filter(analysis => analysis.parent_img_id == this.Images[item].id)
            const status = analysis.length > 0 ? analysis[0].status : 'No analysis started'
                return status
        },
        async getModels() {
            await axios.get('api/v1/models/')
            .then(response => {
                this.Models = response.data
                console.log(this.Models)
            })
            .catch(error => {
                console.log(error)
            })
        },
        async getImages() {
                await axios.get('api/v1/images/')
                .then(response => {
                    this.Images = response.data.filter(image => image.dataset == this.$route.params.id)
                    let img_items = response.data.filter(image => image.dataset == this.$route.params.id)
                    for (let i = 0; i < img_items.length; i++) {
                        this.items.push(img_items[i].img.replace('http', 'https'))
                        this.items.push(img_items[i].img)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
                this.$store.commit('setLoading', false)
        },
        async getAnalyses() {
            await axios.get('api/v1/analyses/')
            .then(response => {
                this.Analyses = response.data.filter(analysis => analysis.dataset == this.$route.params.id)
            })
            .catch(error => {
                console.log(error)
            })
        },
        async addInfos(index) {
            this.mask.owner = localStorage.getItem('username')
            this.mask.name = this.Images[index].name.split('.')[0]
            this.mask.slug = this.mask.name.toLowerCase()
            this.mask.dataset = this.$route.params.id
            this.mask.ml_model_url = this.getModelUrl(this.$route.params.id)
            this.mask.source_image_url = this.Images[index].img
            this.mask.parent_image_id = this.Images[index].id
    },

        getModelUrl(id) {
            const model = this.Models.filter(model => model.dataset == id)
            console.log("MODEL URL")
            console.log(model[0].file)
            return model[0].file
        },

        createFileObjectFromUrl(fileUrl) {
            const fileName = fileUrl.substring(fileUrl.lastIndexOf('/') + 1)
            return new Promise((resolve, reject) => {
                fetch(fileUrl)
                    .then(response => response.blob())
                    .then(blob => {
                        const file = new File([blob], fileName)
                        resolve(file);
                    })
                    .catch(error => {
                        reject(error)
                    })
            })
        },

        async getMasks() {
            await axios.get('api/v1/masks/')
            .then(response => {
                this.Masks = response.data.filter(mask => mask.dataset == this.$route.params.id)
                let mask_items = response.data.filter(mask => mask.dataset == this.$route.params.id)
                for (let i = 0; i < mask_items.length; i++) {
                    this.mask_items.push(mask_items[i].mask)
                }
            })
            .catch(error => {
                console.log(error)
            })
            this.$store.commit('setLoading', false)
        },

        async analyzeImage() {
        if (this.selectedImage === null) {
            // No image selected, show error message or handle accordingly
            return;
        }

        await this.addInfos(this.selectedImage);
        await this.sendAnalysisRequest()
            .then(response => {
                this.message = 'Analysis request sent successfully!'
                console.log(response)
            })
            .catch(error => {
                this.message = 'Analysis request Error!'
                console.log(error)
            });
        },

        sendAnalysisRequest() {
            let formData = new FormData()
            formData.append('owner', this.mask.owner)
            formData.append('slug', this.mask.slug)
            formData.append('dataset', this.mask.dataset)
            formData.append('ml_model_url', this.mask.ml_model_url)
            formData.append('source_image_url', this.mask.source_image_url)
            formData.append('parent_img_id', this.mask.parent_image_id)
            formData.append('ml_model_id', this.Models[0].id)
            formData.append('token', localStorage.getItem('token'))
            console.log(formData)
            return axios.post('api/v1/analyses/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': '{{ csrftoken }}'
                },
            })
        },
        
        getUrl(image) {
            const url = `${axios.defaults.baseURL}${image.img}`
            return url
        }
    }
})
</script>

<style scoped>

.notification.is-success {
    margin-top: 10px;
    margin-bottom: 1px;
}

.notification.is-warning {
    margin-top: 10px;
    margin-bottom: 1px;
}

.notification.is-info {
    margin-top: 10px;
    margin-bottom: 1px;
}

.notification.is-error {
    margin-top: 10px;
    margin-bottom: 1px;
}

.selected {
    border: 1px solid rgb(44, 44, 47); /* Adjust border color and size as needed */
    box-shadow: 0 0 10px 0 rgb(51, 51, 55); /* Add shadow effect to the selected image */
    border-radius: 10px;
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
    margin-top: 1px;
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