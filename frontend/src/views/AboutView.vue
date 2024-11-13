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

.header-col {
  text-align: center;
}

.abouttext {
font-size: 25px;

}

.column {
  margin: auto;
  margin-top: 16px;
  margin-bottom: 16px;
  padding: 0 8px;
  align-items: center;
}

.container {
  display: flex;
  width: 100%;
  margin-top: 5%;
  flex-wrap: wrap;
  flex-direction: column;
}

.responsive-column {
  flex: 1;
  padding: 10px;
  width: 100%;
}

.center-vertically {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80%;
  margin: 0 auto;
  text-align: center;
}

.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  margin: 8px;
}

@media (max-width: 768px) {
  .responsive-column, .column {
    flex-basis: 100%;
    width: 100%;
  }

  .container {
    flex-direction: column;
  }

  .center-vertically {
    flex-direction: column; 
  }
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

.logo {
text-align: center;
width: 100px; 
height: auto;
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

</style>
