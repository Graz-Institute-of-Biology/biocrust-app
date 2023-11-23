<template>
  <div class="container hero is-fullheight">
      <section class ="section" id="app">
          <h2 class="is-size-2 has-text-centered">Home</h2>
          <p> About this project some example text</p>
      </section>
  </div>
</template>

<script setup>

// import { computed } from 'vue'
// import store from '../store'
import imageData from '../data.json'
import { useRoute } from 'vue-router'
import { ref, watch, onMounted } from 'vue'

const dataset = ref(imageData)
const continent = ref("")
// const router = useRouter()
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
})

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