<template>
    <div class="page-dataset">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title is-1">{{ model.model_name }}</h1>
                <RouterLink :to="{ name: 'AddImageView', params: { id: model.id }}" class="button is-link" v-if="!this.$store.loading">Add images</RouterLink>
                <div class="button is-success" @click="analyze" v-if="!this.$store.loading">Analyze images</div>
            </div>
        </div>
        <div  v-if="!this.$store.loading">
        <div class="images" v-viewer="options">
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
    name: 'ModelView',
    directives: {
      viewer: viewer({
        debug: true
      })
 },
    data () {
        return {
            Images: [],
            items: [],
            model: {},
            model_name: this.$route.params.name,
            index: null,
            options: {
                        ready: () => {
                        this.$viewer = this.$el.querySelector(".images").$viewer;
                        },
                        inline: false,
                        toolbar: {
                                    oneToOne: true,
                                    movable: true,
                                    prev: () => {
                                    this.$viewer.prev(true);
                                    },
                                    play: false,
                                    next: () => {
                                    this.$viewer.next(true);
                                    },
                                    overlay: () => {
                                        const viewer = this.$viewer;
                                        const a = document.createElement("a");
                                        a.href = viewer.image.src;
                                        a.download = viewer.image.alt;
                                        
                                    }
                                },
   },
        }
    },
    created () {
        this.$store.commit('setLoading', true)
        this.getModel()
    },
    methods: {
        show () {
        const viewer = this.$el.querySelector('.images').$viewer
        viewer.show()
      },
        async getModel() {
            await axios.get(`api/v1/model/${this.$route.params.id}`)
            .then(response => {
                this.model = response.data
            })
            .catch(error => {
                console.log(error)
            })
            console.log("Model loaded")
            this.getImages()
    },
        async getImages() {
                await axios.get('api/v1/images/')
                .then(response => {
                    this.Images = response.data.filter(image => image.model == this.$route.params.id)
                    let img_items = response.data.filter(image => image.model == this.$route.params.id)
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
.page-model {
    margin-bottom: 10%;
}
.image-small {
    height: 500px;
    cursor:pointer;
    margin: 15px;
    display: inline-block;
    transition: .1s linear;
}
.image-small:hover {
    transform: scale(1.1);
}
.viewer-overlay::before {
  content: "download";
  color: transparent;
  display: block;
  font-size: 0;
  height: 20px;
  line-height: 0;
  width: 20px;
  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAXBJREFUOE/VlDFLlmEUhq9ra3HoT0RDCOIQEQnVkJRQU4QQJEKBICKmNFWEODRHUxJEaDT1ExxUJFLQpSEcxJ+gIE13PPa9H6+f72cSLr7j85xz3ec+57yPnPHnGfM4x8Ak88AD4ADYVO+dpj2NlpP8AH4CM0APMAX0A88rqLrUJHAMmGQWuK7erCckmQOutc76gA9qW6At1KmS5COwrr47yWKStIRX63FHKkxSlN8CL9T1fwAnChCYVbeOVZjkPvAZWFCfddi9AYyrDzvOR4t1YFktMX/3MMkVYBF40lRZkkZgBU/yFdhRpyvgBvBG/dZkswV8rD7tcj8EjKl3K+AucEv91SVhABhRR7rcvwQuqpMVcBIYVO909OgL8B0oQo+AfeBSfaWS9JbFB4bVxfaUk6wAe8Ca+rrWn/fAVWD7sOm1wST5BNwGXqllOEcfhySlist1YGtoJfFCw5THgHn1d9fFPs3/elLMOX6+/tf6HzsPjRVd/9/RAAAAAElFTkSuQmCC);
}

.button {
    margin-right: 10px;
}
</style>