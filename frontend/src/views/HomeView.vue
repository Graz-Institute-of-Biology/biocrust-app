<template>
    Home view
    <h1>Data Set</h1>
        <select @change="handleChange" v-model="continent">
            <option value="All">All</option>
            <option value="Europe">Europe</option>
            <option value="Africa">Africa</option>
            <option value="Asia">Asia</option>
            <option value="North America">North America</option>
            <option value="South America">South America</option>
        </select>
    <div class="cards">
      <div 
        v-for="data in dataset"
        :key="data.id"
        class="card"
        @click="router.push(`/dataset/${data.id}`)">
        <h1>{{data.id}}</h1>
        <p>{{data.country}}</p>
        <p>{{data.images}}</p>
      </div>

    </div>
</template>

<script setup>

// import { computed } from 'vue'
// import store from '../store'
import imageData from '../data.json'
import { useRouter, useRoute } from 'vue-router'
import { ref, watch, onMounted } from 'vue'

const dataset = ref(imageData)
const continent = ref("")
const router = useRouter()
const route = useRoute()


onMounted(() => {
    continent.value = route.query.continent || "All"
})

watch(continent, () => {
    if (continent.value === "All") {
        dataset.value = imageData
    } else {
        dataset.value = imageData.filter(data => data.continent === continent.value)
    }
    console.log(continent.value)
})


const handleChange = () => {
    router.push({query: {continent: continent.value}})
}

// const data_set = computed(() => store.state.data_set)
</script>

<style scoped>
.cards {
  display: flex;
  width: 1000px;
  flex-wrap: wrap;
  margin-top: 50px;
  justify-content: center;
}

.card {
  box-shadow: 1px 1px 10px rgba(0, 0, 0, 0.207);
  padding: 15px;
  width: 150px;
  margin-right: 15px;
  cursor: pointer;
  margin-bottom: 20px;

}
</style>