<template>
    <div class="is-fullheight">
        <div class="columns is-multiline">
            <div class="column is-10 header-col">
                <h2 class="is-size-2">Datasets</h2>
            </div>
            <div class="column is-2 button-col">
                <RouterLink :to="{ name: 'AddDataset' }" class="button is-primary">Add Dataset</RouterLink>
            </div>
        </div>
        <div class="columns">
            <!-- Datasets Grid Column -->
            <div class="column is-8">
                <div class="columns is-multiline">
                    <div 
                        class="column is-4"
                        v-for="dataset in datasets"
                        :key="dataset.id"
                    >
                        <div class="box dataset-box" @click="selectDataset(dataset)">
                            <h3 class="is-size-4"> {{ dataset.dataset_name }} </h3>
                            <p> {{ dataset.dataset_type }} </p>                            
                            <div class="buttons">
                                <RouterLink :to="{ name: 'DataSetView', params: { id: dataset.id }}" class="button is-link">Show</RouterLink>
                                <button class="button is-info" @click.stop="showDatasetDistribution(dataset.id)">
                                    Class Distribution
                                </button>
                            </div>
                        </div>                
                    </div>
                </div>
            </div>
            
            <!-- Chart Column -->
            <div class="column" v-if="selectedDataset">
                <h3 class="title is-3">Class Distribution</h3>
                <button class="button is-small is-primary" @click="downloadDatasetCSV" :disabled="!chartDataReady">
                        Download CSV
                    </button>
                <div v-if="loadingChart" class="has-text-centered">
                    <p class="is-size-5">Loading chart data...</p>
                </div>
                <div v-else-if="noDataAvailable" class="has-text-centered">
                    <p class="is-size-5">No class distribution data available for this dataset</p>
                </div>
                <div v-else class="chart-container">
                    <Doughnut 
                        :data="chartData" 
                        :options="chartOptions" 
                    />
                </div>
                <input type="checkbox" id="exclude-background" v-model="excludeBackground" @change="updateChartWithFilter">
                <label for="exclude-background">Exclude Background</label>
                <div class="table-container" v-if="chartDataReady">
                    <table class="table is-bordered is-striped is-narrow is-hoverable">
                        <thead>
                            <tr>
                                <th class="is-primary">Class Index</th>
                                <th class="is-primary">Coverage</th>
                                <th class="is-primary">Class</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(data, index) in chartData.datasets[0].data" :key="index">
                                <td>{{ index }}</td>
                                <td>{{ data.toFixed(2) }}%</td>
                                <td>{{ chartData.labels[index] }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { Chart as ChartJS, Title, Tooltip, Legend, DoughnutController, CategoryScale, ArcElement } from 'chart.js'
import { Doughnut } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, DoughnutController, CategoryScale, ArcElement)

export default {
    name: 'DataSets',
    components: {
        Doughnut
    },
    data() {
        return {
            datasets: [],
            Images: [],
            selectedDataset: null,
            loadingChart: false,
            noDataAvailable: false,
            excludeBackground: false,
            chartDataReady: false,
            allMasks: [],
            datasetImages: [],
            chartData: {
                labels: [],
                datasets: [{
                    backgroundColor: [],
                    data: []
                }]
            },
            chartOptions: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: "Class Distribution",
                    },
                    legend: {
                        display: true,
                        position: "bottom",
                    },
                },
            },
            rawDistributionData: null
        }
    },
    created() {
        this.getDatasets()
    },
    methods: {

        // Datasets section

        getDatasets() {
            axios.get('api/v1/datasets/')
            .then(response => {
                this.datasets = response.data
            })
            .catch(error => {
                console.log(error)
            })
        },
        
        selectDataset(dataset) {
            this.selectedDataset = dataset
        },
        
        // CSV download section

        downloadDatasetCSV() {
            if (!this.rawDistributionData) return
            
            const { distributions } = this.rawDistributionData
            const datasetName = this.selectedDataset.dataset_name || "dataset"
            const filteredDistributions = { ...distributions }
            
            if (this.excludeBackground) {
                for (const classKey in filteredDistributions) {
                    if (classKey.toLowerCase().includes('background')) {
                        delete filteredDistributions[classKey]
                    }
                }
            }
            
            const filteredTotalPixels = Object.values(filteredDistributions).reduce((sum, count) => sum + count, 0)
            
            const sortedKeys = Object.keys(filteredDistributions).sort((a, b) => {
                const numA = parseInt(a)
                const numB = parseInt(b)
                if (!isNaN(numA) && !isNaN(numB)) return numA - numB
                return a.localeCompare(b)
            })
            
            let csvContent = "DATASET CLASS DISTRIBUTION\n"
            csvContent += `Dataset Name,${datasetName}\n`
            csvContent += `Total Images,${this.datasetImages.length}\n`
            csvContent += `Total Masks Analyzed,${this.allMasks.length}\n`
            csvContent += `Export Date,${new Date().toISOString()}\n\n`
            
            csvContent += "Class Index,Class Name,Pixel Count,Coverage Percentage\n"
            
            for (const classKey of sortedKeys) {
                const pixelCount = filteredDistributions[classKey]
                const percentage = (pixelCount / filteredTotalPixels) * 100
                
                csvContent += `${classKey},${classKey},${pixelCount},${percentage.toFixed(2)}%\n`
            }
            
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
            const link = document.createElement('a')
            const url = URL.createObjectURL(blob)
            
            link.setAttribute('href', url)
            link.setAttribute('download', `${datasetName}_class_distribution.csv`)
            link.style.visibility = 'hidden'
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
        },

        // Class distribution section

        async showDatasetDistribution(datasetId) {
            this.loadingChart = true
            this.noDataAvailable = false
            this.chartDataReady = false
            
            try {
                const imagesResponse = await axios.get('api/v1/images/')
                this.datasetImages = imagesResponse.data.filter(image => image.dataset == datasetId)
                
                if (this.datasetImages.length === 0) {
                    this.loadingChart = false
                    this.noDataAvailable = true
                    return
                }
                
                const masksResponse = await axios.get('api/v1/masks/')
                this.allMasks = masksResponse.data.filter(mask => mask.dataset == datasetId)
                
                if (this.allMasks.length === 0) {
                    this.loadingChart = false
                    this.noDataAvailable = true
                    return
                }
                
                const foundDataset = this.datasets.find(d => d.id === datasetId)
                if (foundDataset) {
                    this.selectedDataset = foundDataset
                }
                
                await this.processDatasetDistributions()
                
            } catch (error) {
                console.error("Error loading dataset distribution:", error)
                this.loadingChart = false
                this.noDataAvailable = true
            }
        },
        
        async processDatasetDistributions() {
            const aggregatedDistributions = {}
            const classColors = {}
            let totalPixelsCounted = 0
            let masksWithDistributions = 0
            
            for (const mask of this.allMasks) {
                if (!mask.class_distributions) continue
                
                try {
                    const distributionData = JSON.parse(mask.class_distributions)
                    if (!distributionData || !distributionData.class_distributions) continue
                    
                    masksWithDistributions++
                    
                    for (const [classKey, pixelCount] of Object.entries(distributionData.class_distributions)) {
                        if (!aggregatedDistributions[classKey]) {
                            aggregatedDistributions[classKey] = 0
                        }
                        aggregatedDistributions[classKey] += pixelCount
                        totalPixelsCounted += pixelCount
                        
                        // Store color info for the class if we don't have it yet
                        if (!classColors[classKey] && distributionData.class_colors) {
                            const colorInfo = Object.values(distributionData.class_colors).find(
                                c => c.name === classKey || c.index?.toString() === classKey
                            )
                            if (colorInfo && colorInfo.color) {
                                classColors[classKey] = colorInfo.color
                            }
                        }
                    }
                } catch (error) {
                    console.warn(`Error parsing class distribution for mask ${mask.id}:`, error)
                }
            }
            
            if (masksWithDistributions === 0) {
                this.loadingChart = false
                this.noDataAvailable = true
                return
            }
            
            this.rawDistributionData = {
                distributions: aggregatedDistributions,
                colors: classColors,
                totalPixels: totalPixelsCounted
            }
            
            this.updateChartWithFilter()
        },
        
        updateChartWithFilter() {
            if (!this.rawDistributionData) return
            
            const { distributions, colors } = this.rawDistributionData
            const filteredDistributions = { ...distributions }
            
            if (this.excludeBackground) {
                for (const classKey in filteredDistributions) {
                    if (classKey.toLowerCase().includes('background')) {
                        delete filteredDistributions[classKey]
                    }
                }
            }
            
            const labels = []
            const data = []
            const backgroundColors = []
            
            const filteredTotalPixels = Object.values(filteredDistributions).reduce((sum, count) => sum + count, 0)
            
            const sortedKeys = Object.keys(filteredDistributions).sort((a, b) => {
                const numA = parseInt(a)
                const numB = parseInt(b)
                if (!isNaN(numA) && !isNaN(numB)) return numA - numB
                return a.localeCompare(b)
            })
            
            for (const classKey of sortedKeys) {
                const pixelCount = filteredDistributions[classKey]
                const percentage = (pixelCount / filteredTotalPixels) * 100
                
                labels.push(classKey)
                data.push(percentage)
                
                if (colors[classKey]) {
                    const rgbColor = colors[classKey]
                    backgroundColors.push(`rgba(${rgbColor.join(',')}, 0.7)`)
                } else {
                    const r = Math.floor(Math.random() * 200)
                    const g = Math.floor(Math.random() * 200)
                    const b = Math.floor(Math.random() * 200)
                    backgroundColors.push(`rgba(${r}, ${g}, ${b}, 0.7)`)
                }
            }
            
            this.chartData = {
                labels: labels,
                datasets: [{
                    backgroundColor: backgroundColors,
                    data: data
                }]
            }
            
            this.chartOptions = {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                            display: true,
                            text: this.selectedDataset.dataset_name
                    },
                    legend: {
                        display: true,
                        position: "bottom"
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const label = context.label || ''
                                const value = context.parsed || 0
                                return `${label}: ${value.toFixed(2)}%`
                            }
                        }
                    }
                }
            }
            
            this.loadingChart = false
            this.chartDataReady = true
        }
    }
}
</script>

<style scoped>
.button-col {
    margin-top: 10px;
    text-align: right;
}

.buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 1rem;
}

.canvas {
    height: 100% !important;
    margin: 0 auto;
}

.chart {
    margin-left: auto;
    margin-right: auto;
    padding-bottom: 5%;
    padding-top: 5%;
}

.chart-container {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
    height: 0;
    margin-bottom: 20px;
    overflow: hidden;
    padding-bottom: 20px;
    padding-top: 100%;
    position: relative;
    width: 100%;
}

.chart-container canvas {
    height: 100% !important;
    left: 0;
    position: absolute;
    top: 0;
    width: 100% !important;
}

.chart-controls {
    align-items: center;
    display: flex;
    justify-content: space-between;
    margin: 1rem 0;
}

.chart-wrapper {
    display: flex;
    flex: 1;
    flex-direction: column;
    position: relative;
}

.dataset-box {
    height: 100%;
    transition: all 0.3s ease;
}

.dataset-box:hover {
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}

.header-col {
    text-align: center;
}

.hero {
    min-height: 50hv;
}

.table-container {
    margin-top: 1rem;
    max-height: 400px;
    overflow-y: auto;
}


@media (max-width: 768px) {
    .canvas {
        height: 70% !important;
    }
    .column {
        flex-direction: column;
        width: 100%;
    }
}
</style>