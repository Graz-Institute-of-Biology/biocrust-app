<template>
    <div class="container">
        <section class ="section" id="app">
            <h1>
                Upload view
            </h1>
            <div class="columns is-multiline">
                <div class="columns is-12">
                    <h2 class="is-size-2 has-text-centered">Datasets:</h2>
                </div>
                <div
                    class="column is-3"
                    v-for="image in Images"
                    :key=image.id
                    >
                    <div class="box">
                        <h3 class="is-size-4"> {{ image.name }} </h3>
                        <figure class="image-mb-4">
                            <img :src="getUrl(image)" />
                        </figure>
                        <!-- <h3 class="is-size-4"> {{ image.name }} </h3> -->

                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'UploadView',
    data() {
        return {
            Images: []
        }
    },
    components: {
    },
    mounted() {
        this.getImages()
    },
    methods : {
        getImages() {
            axios.get('api/v1/images/')
            .then(response => {
                this.Images = response.data
            })
            .catch(error => {
                console.log(error)
            })
        },
        getUrl(image) {
            const url = `${axios.defaults.baseURL}${image.img}`
            return url
        }
    }
}

</script>


<style>
@import "https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css";

.container {
    margin-top: 50px;
    text-align: center;
}
.file {
    margin-top: 50px;
    text-align: center;
}
.section {
    margin-top: 50px;
    text-align: center;
}

.image {
    margin-top: -1.25rem;
    margin-bottom: -1.25rem;
    margin-right: -1.25rem;
}
</style>