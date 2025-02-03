
export default {
    getImagesUploaded(state) {
        return state.imagesUploaded
    },
    getShowProcessingQueue(state) {
        return state.showProcessingQueue
    },
    isUploader(state) {
        return state.is_uploader
    },
    isSuperUser(state) {
        return state.is_superuser
    },
    getUserLoaded(state) {
        return state.userLoaded
    }
}
