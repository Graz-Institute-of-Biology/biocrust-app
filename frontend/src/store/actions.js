import axios from 'axios'

export default {
    async setUploaderStatus({ commit }, status) {
        commit('setIsUploader', status)
    },

    async initializeStatus({ commit }) {
        try {
        const stored = localStorage.getItem('is_uploader')
        if (stored !== null) {
            commit('setIsUploader', JSON.parse(stored))
        } else {
            const userResponse = await axios.get('api/v1/users/me/', {
                headers: {
                    'Authorization': 'Token ' + localStorage.getItem('token'),
                    'Content-Type': 'application/json'
                }
            })        
            commit('setIsUploader', userResponse.is_uploader)
        }
        } finally {
        commit('setUserLoaded', true)
        }
    },
    async resetStatus({ commit }) {
        commit('setIsUploader', false)
        commit('setUserLoaded', false)
    }
}
