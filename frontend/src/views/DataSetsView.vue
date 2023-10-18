<template>
    <div class="page-dataset">
        <h2 class="is-size-2 has-text-centered">Datasets</h2>
        <RouterLink :to="{ name: 'AddDataset' }" class="button is-primary">Add Dataset</RouterLink>
            <div class="columns is-multiline">
                <div 
                    class="column is-3"
                    v-for="dataset in datasets"
                    :key = dataset.id
                >
                <div class="box is-3">
                        <h3 class="is-size-2"> {{ dataset.dataset_name }} </h3>
                        <p> {{ dataset.dataset_type }} </p>
                        <RouterLink :to="{ name: 'DataSetView', params: { id: dataset.id }}" class="button is-link">Details</RouterLink>
                </div>                
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'DataSets',
    data() {
        return {
            datasets: [],
            Images: []
        }
    },
    components: {
    },
    created() {
        this.getDatasets()
    },
    methods : {
        getDatasets() {
            axios.get('api/v1/datasets/')
            .then(response => {
                for (let i = 0; i < response.data.length; i++) {
                    this.datasets.push(response.data[i])
                }
            })
            .catch(error => {
                console.log(error)
            })
        }
    }
}

</script>


<style scoped>

page-dataset {
    display: grid;
}


</style>