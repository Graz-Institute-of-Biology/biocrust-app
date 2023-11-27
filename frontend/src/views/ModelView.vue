<template>
    <div class="container page-dataset">
            <div class="columns">
                <div class="column">
                    <h1 class="title is-1">{{ model.model_name }}</h1>
                <div class="columns is-mobile">
                    <div class="column is-half">
                    <div class="column is-12">
                        <h1 class="title is-3">Coordinates:         {{ model.coordinates }}</h1>
                        <h1 class="title is-3">Description:         {{ model.description }}</h1>
                        <h1 class="title is-3">Training Dataset:    {{ model.belongs_to_dset }}</h1>
                        <h1 class="title is-3">Created:             {{ date }} {{ time }}</h1>
                        <h1 class="title is-3">Model Type:          {{ model.model_type }}</h1>
                        <button class="button" @click="downloadImage(model.file)"><img class= "svg-icon" src="@/assets/download.png" alt="Download Model" /></button> 
                    </div>
                    </div>
                    <div class="column is-half">
                    <div class="button delete-button is-danger" @click="setDeleteAlert" v-if="!this.$store.loading">Delete model</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal is-active modal-background" v-if="deleteAlert">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
            <p class="modal-card-title">Sure you want to delete dataset?</p>
            </header>
            <footer class="modal-card-foot">
            <button class="button is-danger" @click="deleteModel">Delete</button>
            <button class="button" @click="setDeleteAlert">Cancel</button>
            </footer>
        </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { defineComponent } from 'vue'
import 'viewerjs/dist/viewer.css'

export default defineComponent({
    name: 'ModelView',
    directives: {
 },
    data () {
        return {
            Images: [],
            deleteAlert: false,
            model: {},
            model_name: this.$route.params.name,
            index: null,
            date: '',
            time: '',
        }
    },
    created () {
        this.$store.commit('setLoading', true)
        this.getModel()
    },
    methods: {
        setDeleteAlert() {
            if (this.deleteAlert == true) {
                this.deleteAlert = false
            } else {
                this.deleteAlert = true
            }
        },
        async deleteModel() {
            await axios.delete(`api/v1/models/${this.$route.params.id}/`, 
                        { headers: {
                        'X-CSRFToken': '{{ csrftoken }}'
                                    } 
                        },
                        )
            .then(response => {
                console.log(response)
                this.$router.push('/models')
            })
        },
        async getModel() {
            await axios.get(`api/v1/models/${this.$route.params.id}`)
            .then(response => {
                this.model = response.data
                //console.log(this.model.model_created)
                this.date = this.model.model_created.split('T')[0]
                this.time = this.model.model_created.split('T')[1].split('.')[0]

            })
            .catch(error => {
                console.log(error)
            })
            console.log("Model loaded")
    },
        getUrl(image) {
            const url = `${axios.defaults.baseURL}${image.img}`
            return url
        },
        getFilename(path) {
        console.log(path)
        var filename = path.replace(/^.*[\\]/, '')
        return filename
        },
        downloadImage(url) {
        fetch(url)
          .then(response => response.blob())
          .then(blob => {
            const objectURL = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = objectURL;
            link.download = this.model.model_name;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            link.click();
          })
        },
    }
})
</script>

<style scoped>
.svg-icon {
    width: 60px;
    display: inline-block;
    fill: rgb(71, 62, 62);
    background: white;
}

.button {
    background: white;
    border: none;
}

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
.delete-button {
    float: right;
}
</style>