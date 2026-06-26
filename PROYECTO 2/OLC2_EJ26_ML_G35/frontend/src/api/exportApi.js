import apiClient from "./axiosConfig";

export async function downloadCsvReport(modelId) {
  const response = await apiClient.get(`/export/csv/${modelId}`, {
    responseType: "blob",
  });

  return response.data;
}

export async function downloadPdfReport(modelId) {
  const response = await apiClient.get(`/export/pdf/${modelId}`, {
    responseType: "blob",
  });

  return response.data;
}

export function triggerFileDownload(blob, filename) {
  const url = window.URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = filename;

  document.body.appendChild(link);
  link.click();

  link.remove();
  window.URL.revokeObjectURL(url);
}