<template>
    <div class="page-add-dataset">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title is-1">Add Model</h1>
            </div>
            <div class="column is-6">
                    <div class="field">
                        <label class="label">Model Name</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="Model Name" v-model="model.model_name">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label">Coordinates</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="Coordinates [Long / Lat]" v-model="model.coordinates">
                        </div>
                    </div>
            </div>
            <div class="column is-6">
                <div class="field">
                    <label class="label">Model Type</label>
                    <div class="control">
                        <input class="input" type="text" placeholder="Model Type eg. Biocrust" v-model="model.model_type">
                    </div>
                </div>
            </div>
            <div class="column is-6">
                <div class="field">
                    <label class="label">Belongs to Dataset ...</label>
                    <div class="control">
                        <input class="input" type="text" placeholder="Training Dataset" v-model="model.belongs_to_dset">
                    </div>
                </div>
            </div>
            <div class="column is-6">
                <div class="field">
                    <label class="label">Description</label>
                    <div class="control">
                        <input class="input" type="text" placeholder="Description" v-model="model.description">
                    </div>
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
            <div class="column is-12">
                <div class="field">
                    <div class="control">
                        <button class="button is-success" @click="modelUpload">Submit</button>
                    </div>
                </div>
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
            model_id: this.$route.params.id,
            model: {
                model_name: '',
                description: '',
                model_type: '',
                slug: '',
                belongs_to_dset: '',
                coordinates: ''
            },
            }
        },
    components: {
    },
    mounted() {
        this.getModels()
    },
    methods : {
        addInfos() {
            this.model.id = 1 //this.$route.params.id
            this.model.slug = this.model.model_name.toLowerCase()
            console.log(this.model)

        },
        selectFile() {
            this.document = this.$refs.file.files[0]
        },
        async getModels() {
            await axios.get('api/v1/models/')
            .then(response => {
                for (let i = 0; i < response.data.length; i++) {
                    if (response.data[i].id == this.model_id) {
                        this.models = response.data[i]
                        break
                    }
                }
            })
            .catch(error => {
                console.log(error)
            })
        },
        async modelUpload() {
            this.progress = 0
            this.addInfos()
            await this.performModelUpload(this.document, event => {
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
            //this.$store.commit('setModelsUploaded', 1)
            this.$router.push('models')            
        },
        performModelUpload(file, onUploadProgress) {
            console.log(this.model)
            console.log(file)            
            let formData = new FormData()
            formData.append('model_name', this.model.model_name)
            console.log(this.model.model_name)
            formData.append('slug', this.model.slug)
            console.log(this.model.slug)
            formData.append('coordinates', this.model.coordinates)
            formData.append('file', file)
            formData.append('description', this.model.description)
            formData.append('model_type', this.model.model_type)
            formData.append('belongs_to_dset', this.model.belongs_to_dset)
            console.log(formData)
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