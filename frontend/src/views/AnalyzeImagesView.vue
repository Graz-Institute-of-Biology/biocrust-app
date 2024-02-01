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
                        <div class="button delete-button is-danger" @click="setDeleteAlert" v-if="!this.$store.loading">Delete dataset</div>
                    </div>
                    </div>
                </div>
            </div>
        <div v-if="!this.$store.loading">
            <div v-if="!this.setOverlay && !enlarged" class="image-container" @click="toggleEnlarge">
                <img :src="this.items[0]" class="image-small">
            </div>
            <div v-if="this.setOverlay && !enlarged" class="image-container" @click="toggleEnlarge">
                <img :src="this.mask_items[0]" class="overlay-mask">
                <img :src="this.items[0]" class="image-small">
            </div>
            <div v-if="!this.setOverlay && enlarged" class="image-container" @click="toggleEnlarge" @wheel="handleMouseWheel">
                <img :src="this.items[0]" class="image-large">
            </div>
            <div v-if="this.setOverlay && enlarged" class="image-container" @click="toggleEnlarge" @wheel="handleMouseWheel">
                <img :src="this.mask_items[0]" class="overlay-mask-large" :style="{ transform: `scale(${this.scale})` }">
                <img :src="this.items[0]" class="image-large" :style="{ transform: `scale(${this.scale})` }">
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
    },
    methods: {
        show () {
            const viewer = this.$el.querySelector('.images').$viewer
            viewer.show()
        },
        handleMouseWheel(event) {
        if (this.enlarged) {
            // Adjust the scale based on the wheel delta
            this.scale += event.deltaY > 0 ? -0.1 : 0.1;

            // Limit the scale to a reasonable range
            this.scale = Math.min(Math.max(this.scale, 0.5), 3);

            event.preventDefault();
            }
        },
        toggleEnlarge() {
            this.scale = 1; // Reset scale when toggling
            this.enlarged = !this.enlarged
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
                        this.items.push(img_items[i].img)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
                this.$store.commit('setLoading', false)
        },
        async addInfos() {
            this.mask.owner = localStorage.getItem('username')
            this.mask.name = this.Images[0].name.split('.')[0]
            this.mask.slug = this.mask.name.toLowerCase()
            this.mask.dataset = this.$route.params.id
            this.mask.ml_model_url = this.getModelUrl(this.$route.params.id)
            this.mask.source_image_url = this.Images[0].img
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
            await this.addInfos()
            await this.sendAnalysisRequest()
            .then(response => {
                this.message = 'Analysis request sent successfully!'
                this.mask = null
                this.progress = 0
                console.log(response)
            })
            .catch(error => {
                this.message = 'Analysis request Error!'
                this.mask = null
                this.progress = 0
                console.log(error)
            })                      
        },

        sendAnalysisRequest() {
            let formData = new FormData()
            formData.append('owner', this.mask.owner)
            formData.append('slug', this.mask.slug)
            formData.append('dataset', this.mask.dataset)
            formData.append('ml_model_url', this.mask.ml_model_url)
            formData.append('source_image_url', this.mask.source_image_url)
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
.page-dataset {
    margin-bottom: 10%;
}
.image-container {
    position: relative;
}
.image-small,
.overlay-mask {
    position: absolute;
    height: 500px;
    margin: 15px;
}
.image-large,
.overlay-mask-large {
    position: absolute;
    height: 1000px;
    width: auto;
    margin: 15px;
    transform-origin: top left; /* Set the origin for scaling */
}
.overlay-mask {
    z-index: 1;
    opacity: 0.6;
}
.overlay-mask-large {
    z-index: 1;
    opacity: 0.6;
    transform-origin: top left; /* Set the origin for scaling */
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