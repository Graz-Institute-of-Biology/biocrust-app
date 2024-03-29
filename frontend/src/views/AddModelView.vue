<template>
    <div class="page-add-dataset">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title is-1">Add Model</h1>
            </div>
            <form class="columns is-multiline" @submit.prevent="modelUpload">
            <div class="column is-6">
                    <div class="field">
                        <label class="label">Model Name</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="Model Name" v-model="model.model_name" required>
                        </div>
                    </div>
            </div>
            <div class="column is-6">
                <div class="field">
                    <label class="label">Description</label>
                    <div class="control">
                        <input class="input" type="text" placeholder="Description" v-model="model.description" required>
                    </div>
                </div>
            </div>
            <div class="file">
            <label class="file-label">
                <input type="file" ref="file" class="file-input" @change="selectFile" required>

                <span class="file-cta">
                    <span class="file-label">Choose a file...</span>
                </span>
            </label>
            </div>
            <div class="column is-12">
                <div class="field">
                    <div class="control">
                        <button class="button is-success" type="submit">Submit</button>
                    </div>
                </div>
            </div>
            <div class="notification mt-6" v-if="message">
            {{ message }}
        </div>
        </form>
        <div v-if="document" class="progress mb-6">
                <progress class="progress is-primary" :value="progress" max="100">50%</progress>
        </div>
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
            datasets: {},
            file_extension: '',
            model: {
                model_name: '',
                description: '',
                slug: '',
                dataset: '',
                coordinates: 'dummy',
            },
            }
        },
    components: {
    },
    methods : {
        addInfos() {
            this.model.dataset = this.$route.params.id
            this.model.slug = this.model.model_name.toLowerCase().replace(/ /g,"_")

        },
        selectFile() {
            this.document = this.$refs.file.files[0]
            this.file_extension = this.document.name.split('.')[1]
            if (this.file_extension.toLocaleLowerCase() == 'pth' || this.file_extension.toLocaleLowerCase() == 'pt') {
                this.message = "File is valid!";
            } else {
                this.message = "File is invalid";
                this.document = null
            }

        },
        async modelUpload() {
            this.progress = 0
            this.addInfos()
            if (this.file_extension.toLocaleLowerCase() == 'pth' || this.file_extension.toLocaleLowerCase() == 'pt') {
                this.message = "File is valid!";
            
                await this.performModelUpload(this.document, event => {
                    this.progress = Math.round((100 * event.loaded) / event.total)
                })
                .then(response => {
                    this.message = 'File uploaded successfully!'
                    this.document = null
                    this.progress = 0
                    console.log(response)
                    this.$router.push('models')  
                })
                .catch(error => {
                    this.message = 'Could not upload file!'
                    this.document = null
                    this.progress = 0
                    console.log(error)
                })
            } else {
                this.message = "File extension is invalid. Supported file types are '.pt' or '.pth'!" ;
                this.document = null
            }
            //this.$store.commit('setModelsUploaded', 1)
            this.$router.push({ name: 'ModelsView' })       
        },
        performModelUpload(file, onUploadProgress) {
            let formData = new FormData()
            formData.append('model_name', this.model.model_name)
            formData.append('slug', this.model.slug)
            formData.append('coordinates', this.model.coordinates)
            formData.append('file', file)
            formData.append('description', this.model.description)
            formData.append('model_type', this.model.model_type)
            formData.append('dataset', this.model.dataset)
            return axios.post('api/v1/models/', formData, {
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