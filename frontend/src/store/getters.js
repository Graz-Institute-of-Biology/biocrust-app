
export default {
    getImagesUploaded(state) {
        return state.imagesUploaded
    },
    getShowProcessingQueue(state) {
        return state.showProcessingQueue
    },
    isUploader(state) {
        console.log("GET_USER_UPLOADER")
        return state.is_uploader
    },
    getUserLoaded(state) {
        console.log("GET_USER_LOADED")
        return state.userLoaded
    }
}
