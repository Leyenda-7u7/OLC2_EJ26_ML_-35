export const API_BASE_URL = "http://127.0.0.1:8000";

export const DATASET_TYPES = [
  {
    value: "freelancers",
    label: "Freelancers",
  },
  {
    value: "reviews",
    label: "Reseñas de clientes",
  },
];

export const ALGORITHMS = [
  {
    value: "kmeans",
    label: "K-Means",
  },
  {
    value: "dbscan",
    label: "DBSCAN",
  },
  {
    value: "agglomerative",
    label: "Clustering jerárquico",
  },
  {
    value: "gmm",
    label: "GMM",
  },
];

export const VECTORIZERS = [
  {
    value: "tfidf",
    label: "TF-IDF",
  },
  {
    value: "bow",
    label: "Bag of Words",
  },
];

export const NAV_ITEMS = [
  {
    path: "/",
    label: "Carga y preprocesamiento",
  },
  {
    path: "/training",
    label: "Configuración y entrenamiento",
  },
  {
    path: "/interpretation",
    label: "Interpretación de los segmentos",
  },
  {
    path: "/evaluation",
    label: "Evaluación y validación",
  },
  {
    path: "/classification",
    label: "Clasificación de nuevo registro",
  },
  {
    path: "/export",
    label: "Exportación de reportes",
  },
];