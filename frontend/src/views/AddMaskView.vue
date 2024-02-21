<template>
    <div class="container">
        <div class="page-add-dataset">
            <div class="columns is-multiline">
                <div class="column is-12">
                    <h1 class="title is-1">Add Mask(s)</h1>
                </div>
                <div class="column is-6">
                    <div class="field">
                        <label class="label">Description</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="Description" v-model="mask.description">
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="document" class="progress mb-6">
                <progress class="progress is-primary" :value="progress" max="100">50%</progress>
            </div>
        </div>
        <div class="file">
            <label class="file-label">
                <input type="file" ref="file" class="file-input" @change="selectFile">
                <span class="file-cta">
                    <span class="file-label">Choose a file...</span>
                </span>
                <!-- <button class="button is-primary mt-2" @click="searchParent">Search</button> -->
            </label>
        </div>
        <button class="button is-primary mt-2" v-if="document" @click="maskUpload">Upload</button>
        <div class="notification mt-6" v-if="message">
            {{ message }}
        </div>
    </div>
</template>

<script>
import axios from 'axios'


export default {
    name: 'UploadView',
    data() {
        return {
            progress: 0,
            message: '',
            document: null,
            dataset_id: this.$route.params.id,
            dataset: {},
            Images: [],
            img_names : [],
            mask: {
                name: '',
                owner: '',
                slug: '',
                dataset: '',
                description: '',
                parentImage: '',
                source: '',            
            },
            }
        },
    components: {
    },
    mounted() {
        this.getDatasets()
        this.getImages()
    },
    methods : {
        addInfos() {
            this.mask.name = this.document.name.split('.')[0] // remove file extension and add filename as image name
            this.mask.owner = localStorage.getItem('username')
            this.mask.slug = this.mask.name.toLowerCase()
            this.mask.dataset = this.$route.params.id
            this.mask.parentImage = this.searchParent()
            this.mask.source_manual = true

        },

        selectFile() {
            this.document = this.$refs.file.files[0]
        },

        async getDatasets() {
            await axios.get('api/v1/datasets/')
            .then(response => {
                for (let i = 0; i < response.data.length; i++) {
                    if (response.data[i].id == this.dataset_id) {
                        this.datasets = response.data[i]
                        break
                    }
                }
            })
            .catch(error => {
                console.log(error)
            })
        },

        async maskUpload() {
            this.progress = 0
            this.addInfos()
            await this.performMaskUpload(this.document, event => {
                this.progress = Math.round((100 * event.loaded) / event.total)
            })
            .then(response => {
                this.message = 'File uploaded successfully!'
                this.document = null
                this.progress = 0
                console.log(response)
            })
            .catch(error => {
                this.message = 'Could not upload file!'
                this.document = null
                this.progress = 0
                console.log(error)
            })
            // this.$store.commit('setMasksUploaded', 1)
            this.$router.push({ name: 'DataSetView', params: { id: this.dataset_id } })            
        },
        // "name" : 'test',
        // "owner" : 'admin',
        // "description" : "test description",
        // "slug" : 'test',
        // "dataset" : dataset,
        // "parent_image" : parent_img_id,
        // "source_model" : ml_model_id,
        // "source_model_url" : source_model_url,

        performMaskUpload(file, onUploadProgress) {
            console.log(file)
            console.log("HERE")
            console.log(this.Images)
            let formData = new FormData()
            formData.append('mask', file)
            formData.append('name', this.mask.name)
            formData.append('parent_image', this.mask.parentImage.id)
            formData.append('parent_image_url', this.mask.parentImage.img)
            formData.append('owner', this.mask.owner)
            formData.append('description', this.mask.description)
            formData.append('slug', this.mask.slug)
            formData.append('dataset', this.mask.dataset)
            formData.append('source_manual', true)
            formData.append('dataset', this.dataset_id)
            //formData.append('source_model', null)
            console.log(formData)
            return axios.post('api/v1/masks/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': '{{ csrftoken }}'
                },
                onUploadProgress
            })
        },

        getParentImageName(name) {
            var mask_name = name.split('.')[0]
            return mask_name
        },

        searchParent() {
            var mask_name = this.getParentImageName(this.document.name)
            console.log(mask_name)
            console.log("searching...")
            for (let image of this.Images) {
                console.log(image)
                if (mask_name.includes(image.name)) {
                    console.log("found")
                    return image
                }
            }
        },

        async getImages() {
                await axios.get('api/v1/images/')
                .then(response => {
                    this.Images = response.data.filter(image => image.dataset == this.$route.params.id)
                    let img_items = response.data.filter(image => image.dataset == this.$route.params.id)
                    for (let i = 0; i < img_items.length; i++) {
                        this.img_names.push(img_items[i].name)
                    }
                })
                .catch(error => {
                    console.log(error)
                })
                this.$store.commit('setLoading', false)
        },
    }
}
</script>


<style>
@import "https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css";

.file {
    text-align: center;
}

</style>