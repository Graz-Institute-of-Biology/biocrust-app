<template>
  <div class="container">
    <div class="container">
        <section class ="section" id="app">
            <h2 class="is-size-2 has-text-centered">About</h2>
            <p> About this project some example text</p>
        </section>
    </div>
    <div class="container has-text-centered">
        <header class="container">
        <img src="@/assets/logo.png" alt="Work Group" class="container" />
        </header>

        <div class="container">
        <p>{{ description }}</p>d
        </div>

        <ul class="social-links">
        <li v-for="socialLink in socialLinks" :key="socialLink.name">
            <a :href="socialLink.url" target="_blank">{{ socialLink.name }}</a>
        </li>
        </ul>

        
        <h2 style="text-align:center">Our Team</h2>
        <div class="center-vertically">
        <div class="column">
            <div class="card">
            <img src="@/assets/logo.png" alt="Stefan Herdy" style="width:100%">
            <div class="container">
                <h2>Stefan Herdy</h2>
                <p class="title">Co-Founder</p>
                <p>Some text that describes me lorem ipsum ipsum lorem.</p>
                <p><button class="button" onclick="window.location.href='mailto:stefan.herdy@uni-graz.at';">Contact</button></p>
            </div>
            </div>
        </div>


        <div class="column">
            <div class="card">
            <img src="@/assets/logo.png" alt="Philipp Faulhammer" style="width:100%">
            <div class="container">
                <h2>Philipp Faulhammer</h2>
                <p class="title">Co-Founder</p>
                <p>Some text that describes me lorem ipsum ipsum lorem.</p>
                <p><button class="button" onclick="window.location.href='mailto:philipp.faulhammer@uni-graz.at';">Contact</button></p>
            </div>
            </div>
        </div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      workGroupImage: "work-group-image.jpg",
      description: "Welcome to our website! We are a passionate group of individuals dedicated to excellence in our field. Our mission is to provide the best solutions for your needs.",
      socialLinks: [
        { name: "GitHub", url: "https://github.com/Graz-Institute-of-Biology" },
      ],
      formData: {
        name: "",
        email: "",
        message: "",
      },
    };
  },
  methods: {
    submitForm() {
      // Handle form submission, e.g., send data to the server
      console.log("Form submitted with data:", this.formData);
    },
  },
};
</script>

<style scoped>
body {
  font-family: Arial, Helvetica, sans-serif;
  margin: 0;
}

html {
  box-sizing: border-box;
}

*, *:before, *:after {
  box-sizing: inherit;
}

.center-vertically {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80%;
  margin: 0 auto;
}

.column {
  float: left;
  width: 30%;
  margin: auto;
  margin-bottom: 16px;
  padding: 0 8px;
}

.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  margin: 8px;
}

.about-section {
  padding: 50px;
  text-align: center;
  background-color: #474e5d;
  color: white;
}

.container {
  padding: 0 16px;
}

.container::after, .row::after {
  margin: auto;
  width: 100%;
  padding: 10px;
  content: "";
  clear: both;
  display: table;
}

.title {
  color: grey;
}

.button {
  border: none;
  outline: 0;
  display: inline-block;
  padding: 8px;
  color: white;
  background-color: #000;
  text-align: center;
  cursor: pointer;
  width: 100%;
}

.button:hover {
  background-color: #555;
}

@media screen and (max-width: 650px) {
  .column {
    width: 100%;
    display: block;
  }
}
</style>
