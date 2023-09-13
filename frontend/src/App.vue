
<template>
  <main class="container">
    <div class="links">
      <nav class="navbar is-dark">
        <div class="navbar-brand">
          <RouterLink class="navbar-item" to="/"><strong>Home</strong></RouterLink>
          <RouterLink class="navbar-item" to="/upload">Upload</RouterLink>
          <RouterLink class="navbar-item" to="/about">About</RouterLink>
          <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          </a>
        </div>
      </nav>
    </div>
  </main>
  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'

</script>

<style scoped>
@import 'https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css';

.active {
  font-weight: bold;
}

.navbar-item {
  font-size: 1.2rem;
  color: lightgrey;
}
</style>
