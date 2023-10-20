<template>
    <div class="page-dataset">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title is-1">{{ dataset.dataset_name }}</h1>
                <RouterLink :to="{ name: 'AddImageView', params: { id: dataset.id }}" class="button is-link" v-if="!this.$store.loading">Add images</RouterLink>
            </div>
        </div>
        <div  v-if="!this.$store.loading">
        <div class="images" v-viewer="{movable: true}">
            <img class="image-small" v-for="src in items" :src="src" :key="src">
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
import { defineComponent } from 'vue'
import 'viewerjs/dist/viewer.css'
import { directive as viewer } from "v-viewer"


export default defineComponent({
    name: 'DataSetView',
    directives: {
      viewer: viewer({
        debug: true
      })
    },
    data () {
        return {
            Images: [],
            items: [],
            dataset: {},
            dataset_name: this.$route.params.name,
            index: null
        }
    },
    created () {
        this.$store.commit('setLoading', true)
        this.getDataset()
    },
    methods: {
        show () {
        const viewer = this.$el.querySelector('.images').$viewer
        viewer.show()
      },
        async getDataset() {
            await axios.get(`api/v1/datasets/${this.$route.params.id}`)
            .then(response => {
                this.dataset = response.data
            })
            .catch(error => {
                console.log(error)
            })
            console.log("Dataset loaded")
            this.getImages()
    },
        async getImages() {
                await axios.get('api/v1/images/')
                .then(response => {
                    this.Images = response.data.filter(image => image.dataset == this.$route.params.id)
                    let img_items = response.data.filter(image => image.dataset == this.$route.params.id)
                    for (let i = 0; i < img_items.length; i++) {
                        this.items.push(img_items[i].img)
                    }
                    console.log(this.items)
                })
                .catch(error => {
                    console.log(error)
                })
                console.log("Images loaded")
                this.$store.commit('setLoading', false)
            },
        getUrl(image) {
            const url = `${axios.defaults.baseURL}${image.img}`
            return url
        }
    }
})


</script>



<style scoped>
.page-dataset {
    margin-bottom: 10%;
}
.image-small {
    height: 200px;
    cursor:pointer;
    margin: 15px;
    display: inline-block;
    transition: .1s linear;
}
.image-small:hover {
    transform: scale(1.1);
}

</style>