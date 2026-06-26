import apiClient from "./axiosConfig";

export async function uploadDataset(datasetType, file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post("/data/upload", formData, {
    params: {
      dataset_type: datasetType,
    },
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}

export async function cleanDataset(datasetType, filename) {
  const response = await apiClient.post("/data/clean", null, {
    params: {
      dataset_type: datasetType,
      filename,
    },
  });

  return response.data;
}

export async function getDatasetPreview(datasetType, filename, preferClean = true) {
  const response = await apiClient.get("/data/preview", {
    params: {
      dataset_type: datasetType,
      filename,
      prefer_clean: preferClean,
    },
  });

  return response.data;
}