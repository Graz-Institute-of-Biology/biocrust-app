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
                    <div class="field">
                        <label class="label">Coordinates</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="Coordinates [Long / Lat]" v-model="dataset.coordinates" required>
                        </div>
                    </div>
            </div>

                <div class="column is-6">
                    <div class="field">
                        <label class="label">Dataset Type</label>
                        <div class="control">
                            <input class="input" type="text" placeholder="Dataset Type eg. Biocrust" v-model="dataset.dataset_type" required>
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
                coordinates: '',
                dataset_type: ''
            }
        }
    },
    methods : {
        submitForm() {
            this.addSlug()
            axios.post('api/v1/datasets/', this.dataset, { headers: { 'Content-Type': 'application/json' } })
            .then(response => {
                console.log(response)
                this.$router.push({ name: 'datasets' })
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })
            
        },
        addSlug() {
            this.dataset.slug = this.dataset.dataset_name.toLowerCase()
        }
    }
}

</script>