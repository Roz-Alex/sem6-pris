import os
import sys
import uuid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count, isnan
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.types import DoubleType


def analyze_dataset(input_path: str, result_dir: str, spark_master_url: str = "local[*]") -> dict:
    spark = SparkSession.builder \
        .appName("HousePricePrediction") \
        .master(spark_master_url) \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()


    try:
        # === 1. Загрузка данных ===
        df = spark.read.option("header", "true").csv(input_path)  # inferSchema=False — будем сами управлять типами

        schema = df.dtypes
        row_count = df.count()
        column_count = len(df.columns)

        plot_filename = None

        numeric_columns = [
            "OverallQual", "GrLivArea", "GarageCars", "TotalBsmtSF",
            "1stFlrSF", "FullBath", "TotRmsAbvGrd", "YearBuilt", "SalePrice"
        ]

        print(f"Initial rows: {row_count}", flush=True)

        for col_name in numeric_columns:
            if col_name in df.columns:
                df = df.withColumn(col_name, col(col_name).cast(DoubleType()))

        df = df.filter(col("SalePrice").isNotNull())

        print(f"After filtering SalePrice not null: {df.count()}", flush=True)

        sample_pdf = df.limit(10).toPandas()
        summary_pdf = df.describe().toPandas()
        summary_filename = "summary.csv"
        summary_pdf.to_csv(os.path.join(result_dir, summary_filename), index=False)

        numeric_cols = [name for name, typ in df.dtypes
                        if typ == 'double' and name != 'SalePrice']

        if not numeric_cols:
            return {
                "model_metrics": {"error": f"После преобразования не найдено числовых признаков. Типы: {df.dtypes}"}
            }

        feature_cols = numeric_cols
        assembler = VectorAssembler(inputCols=feature_cols, outputCol="features", handleInvalid="skip")
        df_model = assembler.transform(df).select("features", "SalePrice")

        print(f"After VectorAssembler (non-null features): {df_model.count()}", flush=True)

        train_data, test_data = df_model.randomSplit([0.8, 0.2], seed=42)

        print(f"Train size: {train_data.count()}, Test size: {test_data.count()}", flush=True)

        lr = LinearRegression(featuresCol="features", labelCol="SalePrice")
        lr_model = lr.fit(train_data)

        predictions = lr_model.transform(test_data)

        evaluator = RegressionEvaluator(labelCol="SalePrice", predictionCol="prediction", metricName="rmse")
        rmse = evaluator.evaluate(predictions)
        r2 = RegressionEvaluator(labelCol="SalePrice", predictionCol="prediction", metricName="r2").evaluate(predictions)

        saleprice_pdf = df.select("SalePrice").dropna().toPandas()
        if not saleprice_pdf.empty and len(saleprice_pdf) > 0:
            plt.figure(figsize=(8, 5))
            plt.hist(saleprice_pdf["SalePrice"], bins=30, color='skyblue', edgecolor='black')
            plt.title("Распределение целевой переменной (SalePrice)")
            plt.xlabel("Цена продажи")
            plt.ylabel("Частота")
            plot_filename = f"{uuid.uuid4().hex}_saleprice_hist.png"
            plt.savefig(os.path.join(result_dir, plot_filename), bbox_inches='tight')
            plt.close()
        else:
            plot_filename = None

        pred_pdf = predictions.select("SalePrice", "prediction").dropna().limit(200).toPandas()
        pred_plot_filename = None
        if not pred_pdf.empty:
            plt.figure(figsize=(8, 6))
            plt.scatter(pred_pdf["SalePrice"], pred_pdf["prediction"], alpha=0.6, color='purple')
            min_val = min(pred_pdf["SalePrice"].min(), pred_pdf["prediction"].min())
            max_val = max(pred_pdf["SalePrice"].max(), pred_pdf["prediction"].max())
            plt.plot([min_val, max_val], [min_val, max_val], 'r--')
            plt.xlabel("Реальная цена")
            plt.ylabel("Предсказанная цена")
            plt.title(f"Предсказания модели (RMSE: {rmse:.2f}, R²: {r2:.2f})")
            pred_plot_filename = f"{uuid.uuid4().hex}_pred.png"
            plt.savefig(os.path.join(result_dir, pred_plot_filename), bbox_inches='tight')
            plt.close()

        return {
            "schema": schema,
            "row_count": row_count,
            "column_count": column_count,
            "sample_html": sample_pdf.to_html(classes='table table-striped', escape=False),
            "summary_file": summary_filename,
            "plot_file": plot_filename,
            "model_metrics": {
                "rmse": round(rmse, 2),
                "r2": round(r2, 2)
            },
            "prediction_plot": pred_plot_filename
        }

    finally:
        spark.stop()