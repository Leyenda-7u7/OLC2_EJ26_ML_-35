from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as ReportImage,
    PageBreak,
)

from app.config import REPORTS_DIR
from app.services.model_store_service import (
    load_model_metadata,
    load_results_dataframe,
)


def get_report_dir(model_id: str) -> Path:
    """
    Crea y devuelve la carpeta de reportes de un modelo.
    """

    report_dir = REPORTS_DIR / model_id
    report_dir.mkdir(parents=True, exist_ok=True)

    return report_dir


def export_clustered_csv(model_id: str) -> Path:
    """
    Exporta el CSV de resultados del modelo.

    El CSV incluye:
    - columnas originales
    - cluster
    - pc1
    - pc2
    """

    results_df = load_results_dataframe(model_id)

    report_dir = get_report_dir(model_id)
    csv_path = report_dir / f"{model_id}_clusters.csv"

    results_df.to_csv(csv_path, index=False)

    return csv_path


def safe_value(value: Any) -> str:
    """
    Convierte valores a string de forma segura para PDF.
    """

    if pd.isna(value):
        return ""

    return str(value)


def build_simple_table(data: list[list[Any]]) -> Table:
    """
    Construye una tabla con estilo básico para ReportLab.
    """

    clean_data = [
        [safe_value(cell) for cell in row]
        for row in data
    ]

    table = Table(clean_data, hAlign="LEFT")

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ]
        )
    )

    return table


def create_pca_plot(model_id: str, results_df: pd.DataFrame) -> Path | None:
    """
    Genera una gráfica PCA/SVD 2D y la guarda como imagen PNG.

    Requiere que el dataframe tenga:
    - pc1
    - pc2
    - cluster
    """

    required_columns = {"pc1", "pc2", "cluster"}

    if not required_columns.issubset(set(results_df.columns)):
        return None

    report_dir = get_report_dir(model_id)
    plot_path = report_dir / f"{model_id}_pca_plot.png"

    plt.figure(figsize=(7, 5))

    plt.scatter(
        results_df["pc1"],
        results_df["pc2"],
        c=results_df["cluster"],
        alpha=0.75,
    )

    plt.title("Visualización de clusters en 2D")
    plt.xlabel("Componente 1")
    plt.ylabel("Componente 2")
    plt.tight_layout()
    plt.savefig(plot_path, dpi=150)
    plt.close()

    return plot_path


def build_metadata_table(metadata: dict[str, Any]) -> Table:
    """
    Tabla con información general del modelo.
    """

    data = [
        ["Campo", "Valor"],
        ["Model ID", metadata.get("model_id", "")],
        ["Dataset", metadata.get("dataset_type", "")],
        ["Archivo", metadata.get("filename", "")],
        ["Algoritmo", metadata.get("algorithm", "")],
        ["Registros", metadata.get("total_records", "")],
        ["Features", metadata.get("total_features", "")],
        ["Clusters encontrados", metadata.get("clusters_found", "")],
        ["Puntos ruido", metadata.get("noise_points", 0)],
        ["Método reducción", metadata.get("reduction_method", "")],
    ]

    return build_simple_table(data)


def build_metrics_table(metadata: dict[str, Any]) -> Table:
    """
    Tabla con métricas internas de clustering.
    """

    metrics = metadata.get("metrics", {})

    data = [
        ["Métrica", "Valor"],
        ["Silhouette Score", metrics.get("silhouette_score")],
        ["Davies-Bouldin Score", metrics.get("davies_bouldin_score")],
        ["Calinski-Harabasz Score", metrics.get("calinski_harabasz_score")],
    ]

    return build_simple_table(data)


def build_distribution_table(metadata: dict[str, Any]) -> Table:
    """
    Tabla de distribución de registros por cluster.
    """

    distribution = metadata.get("label_distribution", {})

    data = [["Cluster", "Cantidad"]]

    for cluster, count in distribution.items():
        data.append([cluster, count])

    return build_simple_table(data)


def build_cluster_profile_tables(results_df: pd.DataFrame) -> list[Table]:
    """
    Construye tablas resumen por cluster.

    Para cada cluster muestra:
    - cantidad de registros
    - promedio de columnas numéricas principales
    """

    tables: list[Table] = []

    if "cluster" not in results_df.columns:
        return tables

    ignored_columns = {"cluster", "pc1", "pc2"}

    numeric_columns = [
        column
        for column in results_df.select_dtypes(include=["number"]).columns.tolist()
        if column not in ignored_columns
    ]

    # Para que el PDF no se haga enorme, usamos máximo 6 variables numéricas.
    numeric_columns = numeric_columns[:6]

    for cluster_id, group_df in results_df.groupby("cluster"):
        data = [
            [f"Cluster {cluster_id}", ""],
            ["Cantidad de registros", len(group_df)],
        ]

        for column in numeric_columns:
            data.append(
                [
                    f"Promedio {column}",
                    round(float(group_df[column].mean()), 4),
                ]
            )

        tables.append(build_simple_table(data))

    return tables


def build_preview_table(results_df: pd.DataFrame, max_rows: int = 8) -> Table:
    """
    Crea una tabla pequeña con los primeros registros del resultado.
    """

    preview_df = results_df.head(max_rows).copy()

    # Evitamos tablas gigantes en PDF.
    max_columns = 8
    preview_df = preview_df.iloc[:, :max_columns]

    data = [preview_df.columns.tolist()]

    for _, row in preview_df.iterrows():
        data.append(row.tolist())

    return build_simple_table(data)


def export_pdf_report(model_id: str) -> Path:
    """
    Genera un reporte PDF del modelo entrenado.

    Incluye:
    - información general
    - métricas
    - interpretación
    - gráfica PCA/SVD
    - distribución por cluster
    - perfiles básicos por cluster
    - preview de resultados
    """

    metadata = load_model_metadata(model_id)
    results_df = load_results_dataframe(model_id)

    report_dir = get_report_dir(model_id)
    pdf_path = report_dir / f"{model_id}_report.pdf"

    plot_path = create_pca_plot(model_id, results_df)

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("TalentMosaic - Reporte de Segmentación", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Información general del modelo", styles["Heading2"]))
    story.append(build_metadata_table(metadata))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Métricas internas de evaluación", styles["Heading2"]))
    story.append(build_metrics_table(metadata))
    story.append(Spacer(1, 12))

    interpretation = metadata.get("interpretation")

    if interpretation:
        story.append(Paragraph("Interpretación", styles["Heading2"]))
        story.append(Paragraph(str(interpretation), styles["BodyText"]))
        story.append(Spacer(1, 12))

    story.append(Paragraph("Distribución de clusters", styles["Heading2"]))
    story.append(build_distribution_table(metadata))
    story.append(Spacer(1, 12))

    if plot_path is not None and plot_path.exists():
        story.append(Paragraph("Visualización PCA/SVD", styles["Heading2"]))
        story.append(ReportImage(str(plot_path), width=430, height=300))
        story.append(Spacer(1, 12))

    story.append(PageBreak())

    story.append(Paragraph("Perfiles básicos por cluster", styles["Heading2"]))
    profile_tables = build_cluster_profile_tables(results_df)

    if profile_tables:
        for table in profile_tables:
            story.append(table)
            story.append(Spacer(1, 10))
    else:
        story.append(
            Paragraph(
                "No fue posible generar perfiles por cluster.",
                styles["BodyText"],
            )
        )

    story.append(PageBreak())

    story.append(Paragraph("Vista previa de resultados", styles["Heading2"]))
    story.append(build_preview_table(results_df))

    doc.build(story)

    return pdf_path