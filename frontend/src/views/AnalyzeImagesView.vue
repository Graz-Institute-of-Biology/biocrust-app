<template>
    <div class="container page-dataset">
            <div class="columns">
                <div class="column">
                    <h1 class="title is-1">{{ dataset.dataset_name }}</h1>
                    <div class="columns is-mobile">
                        <div class="column is-half">
                        <div class="button is-success" @click="maskUpload" v-if="!this.$store.loading">Analyze</div>
                        <!-- <div class="button is-success" @click="analyze" v-if="!this.$store.loading">Analyze images</div> -->
                        </div>
                        <div class="column is-half">
                        <div class="button delete-button is-danger" @click="setDeleteAlert" v-if="!this.$store.loading">Delete dataset</div>
                    </div>
                    </div>
                </div>
            </div>
        <div v-if="!this.$store.loading">
            <div v-if="!this.setOverly && !enlarged" class="image-container" @click="toggleEnlarge">
                <img :src="this.items[0]" class="image-small">
            </div>
            <div v-if="this.setOverly && !enlarged" class="image-container" @click="toggleEnlarge">
                <img :src="this.mask_items[0]" class="overlay-mask">
                <img :src="this.items[0]" class="image-small">
            </div>
            <div v-if="!this.setOverly && enlarged" class="image-container" @click="toggleEnlarge" @wheel="handleMouseWheel">
                <img :src="this.items[0]" class="image-large">
            </div>
            <div v-if="this.setOverly && enlarged" class="image-container" @click="toggleEnlarge" @wheel="handleMouseWheel">
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
            setOverly: false,
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
                description: '',
                parentImage: '',
                source: '',            
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
            this.enlarged != this.enlarged
        },
        showOverlay() {
            this.setOverly != this.setOverly
        },
        setDeleteAlert() {
            this.deleteAlert != this.deleteAlert
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
        async addInfos() {
            if (!this.mask) {
            this.mask = {}
            }
            await this.getImages()
            this.mask.owner = localStorage.getItem('username')
            this.mask.name = this.Images[0].name.split('.')[0]
            this.mask.slug = this.mask.name.toLowerCase()
            this.mask.dataset = this.$route.params.id
            this.mask.parentImage = this.Images[0].id
            this.mask.source = 'analyzed image' 
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

        async maskUpload() {
            this.progress = 0
            await this.addInfos()
            await this.createFileObjectFromUrl(this.Images[0].img)
            .then(file => {
                this.file = file
                console.log('file')
                console.log(file)
            })
            .catch(error => {
                console.error(error)
            })
            await this.performMaskUpload(this.file, event => {
                this.progress = Math.round((100 * event.loaded) / event.total)
            })
            .then(response => {
                this.message = 'File uploaded successfully!'
                this.mask = null
                this.progress = 0
                console.log(response)
            })
            .catch(error => {
                this.message = 'Could not upload file!'
                this.mask = null
                this.progress = 0
                console.log(error)
            })                      
        },

        performMaskUpload(file, onUploadProgress) {
            console.log('upload')
            console.log(file)
            let formData = new FormData()
            formData.append('mask', file)
            formData.append('name', this.mask.name)
            formData.append('parent_image', this.mask.parentImage)
            formData.append('owner', this.mask.owner)
            formData.append('description', this.mask.description)
            formData.append('slug', this.mask.slug)
            formData.append('dataset', this.mask.dataset)
            formData.append('source', this.mask.source)
            return axios.post('api/v1/masks/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': '{{ csrftoken }}'
                },
                onUploadProgress
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