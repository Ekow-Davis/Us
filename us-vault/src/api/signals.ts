import api from "./axios"

export const getUnreadSignalCountApi = () => {
  return api.get("/signals/unread-count")
}

export const markSignalsSeenApi = () => {
  return api.post("/signals/mark-seen")
}

export const sendSignalApi = () => {
  return api.post("/signals/send")
}