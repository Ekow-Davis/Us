import axios from "axios"
import { useAuthStore } from "../stores/auth"

const api = axios.create({
  baseURL: "https://us-vault-v1.up.railway.app",
  withCredentials: true,
})

api.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const auth = useAuthStore()

    if (error.response?.status === 401 && auth.accessToken) {
      const refreshed = await auth.refresh()
      if (refreshed) {
        error.config.headers.Authorization = `Bearer ${auth.accessToken}`
        return api.request(error.config)
      }
    }

    return Promise.reject(error)
  }
)

export default api