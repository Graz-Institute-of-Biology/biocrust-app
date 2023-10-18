
<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <RouterLink to="/" class="navbar-item">Home</RouterLink>
      </div>
        <div class="navbar-menu">
          <div class="navbar-end">
            <template v-if="$store.state.isAuthenticated">
              <RouterLink to="/datasets" class="navbar-item">Datasets</RouterLink>
              <RouterLink to="/logout" class="navbar-item">My Account</RouterLink>
              <RouterLink to="/about" class="navbar-item">About</RouterLink>
            </template>

            <template v-else>
              <RouterLink to="/signup" class="navbar-item">Sign Up</RouterLink>
              <RouterLink to="/login" class="navbar-item">Log in</RouterLink>
              <RouterLink to="/about" class="navbar-item">About</RouterLink>
            </template>
        </div>
      </div>
    </nav>

    <section class="section">
        <router-view></router-view>
    </section>

    <footer class="footer">
      <div class="columns is-multiline">
        <div class="col is-12 footerbox-left"> 
          <p>&copy; 2023</p>
          <p>CC-Explorer</p>
        </div>
        <div class="col is-12 footerbox-center">
          <h1>Created by</h1>
          <p>philipp.faulhammer@uni-graz.at</p>
          <p>stefan.herdy@uni-graz.at</p>
        </div>
        <div class="col is-12 footerbox-right">
          <h1>Contact</h1>
          <p>Institut für Biologie</p>
          <p>Holteigasse 6</p>
          <p>8010 Graz, Austria</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'
// import store from './store'

export default {
  name: 'App',

  beforeCreate() {
    this.$store.commit('initializeStore')

    const token = this.$store.state.token

    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  }
}

</script>

<style lang="scss">
// @import 'https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css'
@import '../node_modules/bulma';

.active {
  font-weight: bold;
}

.navbar-item {
  font-size: 1.2rem;
  color: lightgrey;
}
.footer {
  height: 50px;
  background-color: #333;
  color: #fff;
}
.footerbox-left {
  padding-left: 10%;
  text-align: center;
}
.footerbox-center {
  padding-left: 25%;
  text-align: center;
}
.footerbox-right {
  padding-left: 25%;
  text-align: center;
}
</style>
