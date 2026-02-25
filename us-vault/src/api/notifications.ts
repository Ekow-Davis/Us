import api from "./axios"

// Get paginated notifications
export const getNotificationsApi = (
  page: number = 1,
  page_size: number = 10
) => {
  return api.get("/notifications", {
    params: { page, page_size }
  })
}

// Mark single notification as read
export const markNotificationAsReadApi = (
  notificationId: string
) => {
  return api.patch(`/notifications/${notificationId}/read`)
}

// Get unread count
export const getUnreadNotificationsCountApi = () => {
  return api.get("/notifications/unread-count")
}

// Cleanup (delete all read notifications)
export const cleanupNotificationsApi = () => {
  return api.delete("/notifications/cleanup")
}