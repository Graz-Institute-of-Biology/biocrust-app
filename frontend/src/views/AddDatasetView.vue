<template>
    <div class="page-add-dataset">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title is-1">Add Dataset</h1>
            </div>
            <form class="columns is-multiline" @submit.prevent="submitForm">
            <div class="column is-6">
                    <div class="field">
                        <label class="label">Dataset Name</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="Dataset Name" v-model="dataset.dataset_name" required>
                        </div>
                    </div>
                    <!-- <div class="field">
                        <label class="label">Coordinates</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="Coordinates [Long / Lat]" v-model="dataset.coordinates" required>
                        </div>
                    </div> -->
            </div>

                <div class="column is-6">
                    <div class="field">
                        <!-- <label class="label">Dataset Type</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="Dataset Type eg. Biocrust" v-model="dataset.dataset_type" required>
                        </div> -->
                        <label class="label">Select ontology</label>
                        <div class="select is-success">
                            <select class="is-focused" v-model="selectedOntology" @change="setOntology">
                                <option disabled value="">ontology...</option>
                                <option v-for="item in Ontology" :key="item">{{ item }}</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="column is-12">
                    <div class="field">
                        <div class="control">
                            <!-- <button class="button is-success" @click="submitForm">Submit</button> -->
                            <button class="button is-success" type="submit">Submit</button>
                        </div>
                    </div>
                </div>
                <div class="modal is-active modal-background" v-if="nameExists">
                    <div class="modal-background"></div>
                    <div class="modal-card">
                        <header class="modal-card-head">
                        <p class="modal-card-title">Dataset name already exists! Please choose a new name</p>
                        </header>
                        <footer class="modal-card-foot">
                        <button class="button is-success" @click="setNameExists">Ok</button>
                        </footer>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>


<script>
import axios from 'axios'

export default {
    name: 'addDataset',
    data () {
        return {
            dataset: {
                dataset_name: '',
                coordinates: '0/0',
                dataset_type: '',
                owner: localStorage.getItem('username'),
            },
            nameExists: false,
            Ontology: ['southafrica', 'amazon', 'usa'],
            selectedOntology: ''
        }
    },
    created() {
        this.getDatasets()
    },
    methods : {
        async getDatasets() {
            await axios.get('api/v1/datasets/')
            .then(response => {
                this.datasets = response.data
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })
            console.log(this.datasets)
        },
        setOntology() {
            this.dataset.dataset_type = this.selectedOntology
            console.log(this.dataset.dataset_type)
        },
        setNameExists() {
            this.nameExists = false
        },
        submitForm() {
            this.addSlug()
            if (this.checkDatasetName()) {
                return
            }
            axios.post('api/v1/datasets/', this.dataset, { headers: { 'Content-Type': 'application/json' } })
            .then(response => {
                console.log(response)
                this.$router.push({ name: 'datasets' })
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })
            
        },
        checkDatasetName() {
            for (let i = 0; i < this.datasets.length; i++) {
                if (this.datasets[i].dataset_name === this.dataset.dataset_name) {
                    this.nameExists = true
                    return true
                }
            }
        },
        addSlug() {
            this.dataset.slug = this.dataset.dataset_name.toLowerCase().replace(/ /g,"_")
        }
    }
}

</script>