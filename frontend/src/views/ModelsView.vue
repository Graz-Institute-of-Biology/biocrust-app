<template>
    <div class="is-fullheight">
        <div class="columns is-multiline">
            <div class="column is-10 header-col">
                <h2 class="is-size-2">Models</h2>
            </div>
            <div class="column is-2 button-col">
                <RouterLink :to="{ name: 'AddModel' }" class="button is-primary">Add Model</RouterLink>
            </div>
        </div>
            <div class="columns is-multiline">
                <div 
                    class="column is-3"
                    v-for="model in models"
                    :key = model.id
                >
                <div class="box is-3">
                    <h3 class="is-size-2"> {{ model.model_name }} </h3>
                    <p> {{ model.model_type }} </p>
                    <RouterLink :to="{ name: 'ModelView', params: { id: model.id }}" class="button is-link">Details</RouterLink>
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
            models: [],
            Images: []
        }
    },
    components: {
    },
    created() {
        this.getModels()
    },
    methods : {
        getModels() {
            axios.get('api/v1/models/')
            .then(response => {
                for (let i = 0; i < response.data.length; i++) {
                    this.models.push(response.data[i])
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