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
                            <input class="input" type="text" placeholder="Model Type eg. Biocrust" v-model="model.dataset_type">
                        </div>
                    </div>
                </div>
                <div class="column is-12">
                    <div class="field">
                        <div class="control">
                            <button class="button is-success" @click="submitForm">Submit</button>
                        </div>
                    </div>
                </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'

export default {
    name: 'addModel',
    data () {
        return {
            model: {
                model_name: '',
                coordinates: '',
                model_type: ''
            }
        }
    },
    methods : {
        submitForm() {
            this.addSlug()
            axios.post('api/v1/models/', this.model, { headers: { 'Content-Type': 'application/json' } })
            .then(response => {
                console.log(response)
                this.$router.push({ name: 'models' })
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })
            
        },
        addSlug() {
            this.model.slug = this.model.model_name.toLowerCase()
        }
    }
}

</script>