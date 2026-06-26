import apiClient from "./axiosConfig";

export async function trainModel(payload) {
  const response = await apiClient.post("/training/train", payload);
  return response.data;
}