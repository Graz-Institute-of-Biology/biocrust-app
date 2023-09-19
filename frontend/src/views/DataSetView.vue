<template>
    <div class="page-dataset">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title is-1">{{ dataset.dataset_name }}</h1>
                <RouterLink :to="{ name: 'AddImageView', params: { id: dataset.id }}" class="button is-link" v-if="!this.$store.loading">Add images</RouterLink>
            </div>
        </div>

        <div class="columns is-multiline" v-if="!this.$store.loading">
                <div
                    class="column is-3"
                    v-for="image in Images"
                    :key=image.id
                    >
                    <div class="box">
                        <h3 class="is-size-4"> {{ image.name }} </h3>
                        <figure class="image-mb-4">
                            <img :src="image.img" />
                        </figure>
                    </div>
                </div>
            </div>
        <div v-else>
            <div class="columns is-multiline">
                <div class="column is-12">
                    <h1 class="title is-1">Loading...</h1>
                </div>
            </div>
        </div>
    </div>

</template>


<script>
import axios from 'axios'

export default {
    name: 'DataSetView',

    data () {
        return {
            Images: [],
            dataset: {},
            dataset_name: this.$route.params.name
        }
    },
    created () {
        this.getDataset()
        this.getImages()
    },
    methods: {
        async getDataset() {
            this.$store.commit('setLoading', true)
            await axios.get(`api/v1/datasets/${this.$route.params.id}`)
            .then(response => {
                this.dataset = response.data
            })
            .catch(error => {
                console.log(error)
            })
            this.$store.commit('setLoading', false)
    },
        async getImages() {
                this.$store.commit('setLoading', true)
                await axios.get('api/v1/images/')
                .then(response => {
                    this.Images = response.data.filter(image => image.dataset == this.$route.params.id)
                })
                .catch(error => {
                    console.log(error)
                })
                this.$store.commit('setLoading', false)
            },
        getUrl(image) {
            const url = `${axios.defaults.baseURL}${image.img}`
            return url
        }
    }
}


</script>



<style scoped>

</style>