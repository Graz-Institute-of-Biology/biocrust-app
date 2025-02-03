
export default {
    initializeStore(state) {
        if (localStorage.getItem('token')) {
            state.token = localStorage.getItem('token')
            state.isAuthenticated = true
        } else {
            state.token = ''
            state.isAuthenticated = false
        }
    },
    setToken(state, token) {
        state.token = token
        state.isAuthenticated = true
    },
    removeToken(state) {
        state.token = ''
        state.isAuthenticated = false
    },
    setLoading(state, loading) {
        state.loading = loading
    },
    setImagesUploaded(state, imagesUploaded) {
        state.imagesUploaded = state.imagesUploaded + imagesUploaded
    },
    setShowProcessingQueue(state, showProcessingQueue) {
        state.showProcessingQueue = showProcessingQueue
    },
    setIsUploader(state) {
        state.is_uploader = JSON.parse(localStorage.getItem('is_uploader'))
        console.log("SET UPLOADER")
        console.log(state.is_uploader)
    },
    setUserLoaded(state, userLoaded) {
        state.userLoaded = userLoaded
    },
}