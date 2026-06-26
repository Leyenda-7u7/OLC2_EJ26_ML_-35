import apiClient from "./axiosConfig";

export async function getPcaAnalysis(modelId) {
  const response = await apiClient.get(`/analysis/pca/${modelId}`);
  return response.data;
}

export async function getClusterProfiles(modelId) {
  const response = await apiClient.get(`/analysis/profiles/${modelId}`);
  return response.data;
}

export async function getCrossSegmentTable(freelancerModelId, reviewsModelId) {
  const response = await apiClient.get("/analysis/cross-table", {
    params: {
      freelancer_model_id: freelancerModelId,
      reviews_model_id: reviewsModelId,
    },
  });

  return response.data;
}