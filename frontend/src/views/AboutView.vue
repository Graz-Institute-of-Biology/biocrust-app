<template>
  <div class="is-fullheight">
      <div class="columns is-multiline">
          <div class="column is-10 header-col">
              <h2 class="is-size-2">About</h2>
          </div>
      </div>
      <div class="container has-text-centered">
        <div class="abouttext">
            <p> {{aboutText}} </p>
        </div>
        <div class="container has-text-centered ">
            <header class="container">
            <img src="@/assets/logo.png" alt="Work Group" class="container logo" />
            </header>
            
            <h2 class="is-size-3 has-text-centered">Our Team</h2>
            <div class="center-vertically">
            <div class="column responsive-column">
                <div class="card">
                <img src="@/assets/stefanherdyprofile.jpg" alt="Stefan Herdy" style="width:100%;border-radius:15px">
                <div class="container">
                    <h2>Stefan Herdy</h2>
                    <p class="title">Co-Founder</p>
                    <p>PhD Student and Data Scientist</p>
                    <p>Institute of Biology, University of Graz</p>
                    <p><button class="button is-link" onclick="window.location.href='mailto:stefan.herdy@uni-graz.at';">Contact</button></p>
                </div>
                </div>
            </div>


            <div class="column responsive-column">
                <div class="card">
                <img src="@/assets/logo.png" alt="Philipp Faulhammer" style="width:100%;border-radius:15px">
                <div class="container">
                    <h2>Philipp Faulhammer</h2>
                    <p class="title">Co-Founder</p>
                    <p>PhD Student and Data Scientist</p>
                    <p>Institute of Biology, University of Graz</p>
                    <p><button class="button is-link" onclick="window.location.href='mailto:philipp.faulhammer@uni-graz.at';">Contact</button></p>
                </div>
                </div>
            </div>
            </div>
            <ul class="is-size-3 social-links">
            <li v-for="socialLink in socialLinks" :key="socialLink.name">
                <a :href="socialLink.url" target="_blank">{{ socialLink.name }}</a>
            </li>
            </ul>
        </div>
      </div>
  </div>
</template>

<script>
export default {
data() {
  return {
    workGroupImage: "work-group-image.jpg",
    aboutText: `The realm of image processing is witnessing a profound transformation propelled by advancements 
      in artificial intelligence, particularly within the domain of deep learning. This technological paradigm shift 
      is increasingly recognized for its pivotal role in various facets of remote sensing applications, notably in 
      biomonitoring endeavors. The development and deployment of deep learning models necessitate a deep understanding 
      of programming methodologies. \n\n
      In pursuit of democratizing access to cutting-edge advancements in the field, Stefan and Philipp have developed this 
      web application. This platform facilitates data management, model deployment, and the analysis of 
      biomonitoring data via an intuitive user interface. Leveraging state-of-the-art deep learning architectures, users 
      can harness the power of our computational infrastructure to analyze and derive insights from their datasets.`,

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

.about-section {
  background-color: #474e5d;
  color: white;
  padding: 50px;
  text-align: center;
}

.abouttext {
  font-size: 25px;
}

.button {
  background-color: #000;
  border: none;
  color: white;
  cursor: pointer;
  display: inline-block;
  outline: 0;
  padding: 8px;
  text-align: center;
  width: 100%;
}

.button:hover {
  background-color: #555;
}

.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  margin: 8px;
}

.center-vertically {
  align-items: center;
  display: flex;
  justify-content: center;
  margin: 0 auto;
  text-align: center;
  width: 80%;
}

.column {
  align-items: center;
  margin: auto;
  margin-bottom: 16px;
  margin-top: 16px;
  padding: 0 8px;
}

.container {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  margin-top: 5%;
  padding: 0 16px;
  width: 100%;
}

.container::after, .row::after {
  clear: both;
  content: "";
  display: table;
  margin: auto;
  padding: 10px;
  width: 100%;
}

.header-col {
  text-align: center;
}

.logo {
  height: auto;
  text-align: center;
  width: 100px;
}

.responsive-column {
  flex: 1;
  padding: 10px;
  width: 100%;
}

.title {
  color: grey;
}

@media (max-width: 768px) {
  .center-vertically {
    flex-direction: column; 
  }

  .container {
    flex-direction: column;
  }

  .responsive-column, .column {
    flex-basis: 100%;
    width: 100%;
  }
}

</style>
