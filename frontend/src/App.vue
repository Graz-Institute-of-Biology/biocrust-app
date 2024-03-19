
<template>
    <div id="wrapper" class="body">
      <nav class="navbar is-dark is-fixed-top">
        <div class="navbar-brand">
          <RouterLink to="/" class="navbar-item">Home</RouterLink>
        </div>
          <div class="navbar-menu">
            <div class="navbar-end">
              <template v-if="$store.state.isAuthenticated">
                <RouterLink to="/datasets" class="navbar-item">Datasets</RouterLink>
                <RouterLink to="/models" class="navbar-item">Models</RouterLink>
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

        <div class="section">
            <router-view></router-view>
        </div>

        <footer class="footer is-fixed-bottom">
          <div class="columns is-multiline">
            <div class="col is-4 footerbox-left"> 
              <p>&copy; 2023</p>
              <p>CC-Explorer</p>
              <p>ccexplorerdemo@gmail.com</p>
            </div>
            <div class="col is-4 footerbox-center">
              <h1>Created by</h1>
              <p>stefan.herdy@uni-graz.at</p>
              <p>philipp.faulhammer@gmail.com</p>
            </div>
            <div class="col is-4 footerbox-right">
              <h1>Contact</h1>
              <p>Institut für Biologie</p>
              <p>Holteigasse 6 - 8010 Graz, Austria</p>
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
.is-fixed-bottom {
  height: 10px;
  width: 100%;
  background-color: #333;
  color: #fff;
  bottom: 0;
  left: 0;
  position: fixed;
  right: 0;
  z-index: 30;
  padding: 1rem 0rem 3rem;
  line-height: 1
}
.footerbox-left {
  text-align: center;
  justify-content: center;
  flex: auto;
}
.footerbox-center {
  text-align: center;
  justify-content: center;
  flex: auto;
}
.footerbox-right {
  text-align: center;
  justify-content: center;
  flex: auto;
}
.wrapper {
  display: flex;
  min-height: calc(100vh + 50px);
  flex-direction: column;
}
</style>
