
<template>
    <div id="wrapper" class="body">
      <nav class="navbar is-dark" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
          <a role="button" class="navbar-burger burger"
            :class="{ 'is-active': isHamburgerOpen }"
            @click="openHamburgerMenu"
            data-target="navMenu">
              <span></span>
              <span></span>
              <span></span>
          </a>
        </div>
        <div id="navMenu"
            class="navbar-menu"
            :class="{ 'is-active': isHamburgerOpen }">
              <template v-if="$store.state.isAuthenticated">
                <div class="navbar-start">
                  <RouterLink to="/" class="navbar-item">Home</RouterLink>
                  <RouterLink to="/datasets" class="navbar-item">Datasets</RouterLink>
                  <RouterLink to="/models" class="navbar-item" v-if="!this.checkGuest">Models</RouterLink>
                  <RouterLink to="/about" class="navbar-item">About</RouterLink>
                </div>
                <div class="navbar-end">
                  <RouterLink to="/logout" class="navbar-item">Log out</RouterLink>
                </div>
            </template>
            <template v-else>
              <div class="navbar-start">
                <RouterLink to="/" class="navbar-item">Home</RouterLink>
              </div>
              <div class="navbar-end">
                <div class="navbar-item">
                  <RouterLink to="/signup" class="navbar-item">Sign Up</RouterLink>
                  <RouterLink to="/login" class="navbar-item">Log in</RouterLink>
                </div>
              </div>
            </template>
        </div>
      </nav>

        <div class="section">
            <router-view></router-view>
        </div>

        <!-- <footer class="footer is-fixed-bottom"> -->
          <footer class="footer">
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

  data() {
    return {
      isHamburgerOpen: false
    }
  },

  beforeCreate() {
    this.$store.commit('initializeStore')

    const token = this.$store.state.token

    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
  methods: {
    openHamburgerMenu() {
        this.isHamburgerOpen = !this.isHamburgerOpen;
        console.log("klicked")
      },
    checkGuest() {
      if (localStorage.getItem('username').includes('Guest')) {
        return true
      } else {
        return false
      }
      // return localStorage.getItem('username')
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')

      this.$store.commit('removeToken')
      this.$router.push('/')
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

.body {
  width: 100%;
  padding: 0;
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
.footer {
  height: 10px;
  width: 100%;
  // background-color: #333;
  color: #fff;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 30;
  padding: 1rem 0rem 3rem;
  line-height: 1
}

.footerbox-left {
  text-align: center;
  justify-content: center;
  flex: auto;
  padding: 0 0 0.5rem 0;
}
.footerbox-center {
  text-align: center;
  justify-content: center;
  flex: auto;
  padding: 0 0 0.5rem 0;
}
.footerbox-right {
  text-align: center;
  justify-content: center;
  flex: auto;
  padding: 0 0 1rem 0;
}
.wrapper {
  display: flex;
  // min-height: calc(100vh + 50px);
  flex-direction: column;
}
.section {
  padding: 0.5rem 5rem 10rem;
  min-height: calc(120vh - 10rem);
}

.footer .columns {
    background-color: #333;
  }

@media (max-width: 768px) {
  .section {
    padding: 0 0.5rem 0 0.5rem;
  }
  .footer {
    height: 40px;
  }
  .footerbox-left {
    padding: 0.5rem 0 0.5rem 0;
  }
}

</style>
