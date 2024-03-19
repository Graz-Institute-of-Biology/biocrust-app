<template>
    <div class="container">
        <div class="page-add-dataset">
            <div class="columns is-multiline">
                <div class="column is-12">
                    <h1 class="title is-1">Add Image(s)</h1>
                </div>
                <div class="column is-6">
                        <div class="field">
                            <label class="label">Description</label>
                            <div class="control">
                                <input class="input" type="text" placeholder="Description" v-model="image.description">
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
            </label>
        </div>
        <button class="button is-primary mt-2" v-if="document" @click="imageUpload">Upload</button>
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
            file_extension: '',
            document: null,
            dataset_id: this.$route.params.id,
            dataset: {},
            image: {
                name: '',
                description: '',
                slug: '',
                dataset: ''
            },
            }
        },
    components: {
    },
    mounted() {
        this.getDatasets()
    },
    methods : {
        addInfos() {
            this.image.dataset = this.$route.params.id
            this.image.name = this.document.name.split('.')[0] // remove file extension and add filename as image name
            this.image.slug = this.image.name.toLowerCase()
            console.log(this.image)

        },
        selectFile() {
            this.document = this.$refs.file.files[0]
            this.file_extension = this.document.name.split('.')[1]
            if (this.file_extension.toLowerCase() == 'png' || this.file_extension.toLowerCase() == 'jpg') {
                this.message = "File is valid!";
            } else {
                this.message = "File is invalid";
                this.document = null
            }
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
        async imageUpload() {
            this.progress = 0
            this.addInfos()
            if (this.file_extension.toLowerCase() == 'png' || this.file_extension.toLowerCase() == 'jpg') {
                this.message = "File is valid!";
                await this.performImageUpload(this.document, event => {
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
                this.$store.commit('setImagesUploaded', 1)
                this.$router.push({ name: 'DataSetView', params: { id: this.dataset_id } })       
            } else {
                this.message = "File extension is invalid. Supported file types are '.png' or '.jpg'!" ;
                this.document = null
            }     
        },
        performImageUpload(file, onUploadProgress) {
            let formData = new FormData()
            formData.append('img', file)
            formData.append('name', this.image.name)
            formData.append('owner', localStorage.getItem('username'))
            formData.append('description', this.image.description)
            formData.append('slug', this.image.slug)
            formData.append('dataset', this.image.dataset)
            return axios.post('api/v1/images/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-CSRFToken': '{{ csrftoken }}'
                },
                onUploadProgress
            })
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