import axios from 'axios'

export default {
    async setUploaderStatus({ commit }, status) {
        commit('setIsUploader', status)
    },

    async initializeStatus({ commit }) {
        try {
        const uploader = localStorage.getItem('is_uploader')
        const superuser = localStorage.getItem('is_superuser')
        if (uploader !== null && superuser !== null) {
            commit('setIsUploader', JSON.parse(uploader))
            commit('setIsSuperUser', JSON.parse(superuser))
        }
        if (localStorage.getItem('token')) {
            const userResponse = await axios.get('api/v1/users/me/', {
                headers: {
                    'Authorization': 'Token ' + localStorage.getItem('token'),
                    'Content-Type': 'application/json'
                }
            })        
            commit('setIsUploader', userResponse.is_uploader)
            commit('setIsSuperUser', userResponse.is_superuser)
         } else {
                commit('setPublicUser', true)
            } 
        } finally {
        commit('setUserLoaded', true)
        }
    },
    async resetStatus({ commit }) {
        commit('setIsUploader', false)
        commit('setUserLoaded', false)
        commit('setIsSuperUser', false)
    }
}
