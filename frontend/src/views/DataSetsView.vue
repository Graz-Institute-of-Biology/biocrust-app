<template>
    <div class="is-fullheight">
        <div class="columns is-multiline">
            <div class="column is-10 header-col">
                <h2 class="is-size-2">Datasets</h2>
            </div>
            <div class="column is-2 button-col">
                <RouterLink :to="{ name: 'AddDataset' }" class="button is-primary">Add Dataset</RouterLink>
            </div>
        </div>
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

.header-col {
    text-align: center;
}
.button-col {
    text-align: right;
    margin-top: 10px;
}

.hero {
    min-height: 50hv;
}

</style>