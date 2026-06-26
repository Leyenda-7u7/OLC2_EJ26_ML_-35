import apiClient from "./axiosConfig";

export async function classifyRecord(payload) {
  const response = await apiClient.post("/classification/predict", payload);
  return response.data;
}