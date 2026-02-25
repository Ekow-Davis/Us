import api from "./axios"

export const createVaultApi = () => {
  return api.post("/vaults/create")
}

export const joinVaultApi = (inviteCode: string) => {
  return api.post(`/vaults/join/${inviteCode}`)
}

export const getMyVaultApi = () => {
  return api.get("/vaults/me")
}

export const getVaultDetailsApi = () => {
  return api.get(`/vaults/details`)
}

export const leaveVaultApi = () => {
  return api.post(`/vaults/leave`)
}