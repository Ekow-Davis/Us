import api from "./axios"

export const registerApi = (data: {
  email: string
  password: string
  display_name: string
}) => {
  return api.post("/auth/register", data)
}

export const loginApi = (data: {
  email: string
  password: string
}) => {
  const form = new URLSearchParams()
  form.append("username", data.email)
  form.append("password", data.password)

  return api.post("/auth/login", form, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
}

export const refreshApi = () => {
  return api.post("/auth/refresh")
}

export const getMeApi = () => {
  return api.get("/auth/me")
}

export const logoutApi = () => {
  return api.post("/auth/logout")
}