<template>
    <div class="container">
        <h1>DataSet</h1>
        <p>Country: {{ dataset.country }}</p>
    </div>

</template>


<script setup>
import { useRoute } from 'vue-router'
import { ref, onBeforeMount } from 'vue'
import datasets from '../data.json'

const dataset = ref(null)
const route = useRoute()
const {id} = route.params

onBeforeMount(() => {
    dataset.value = datasets.find(c => c.id === parseInt(id))
})


</script>



<style scoped>

</style>