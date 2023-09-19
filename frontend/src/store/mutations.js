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
}