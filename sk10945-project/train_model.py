from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
from pyspark.ml import Pipeline
from pyspark.ml.regression import GBTRegressor, RandomForestRegressor
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator, RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
import sys

def create_spark_session():
    return SparkSession.builder \
        .appName("MovieModelTraining") \
        .config("spark.executor.memory", "16g") \
        .config("spark.driver.memory", "16g") \
        .config("spark.executor.cores", "4") \
        .config("spark.executor.instances", "8") \
        .getOrCreate()

def create_pipeline(df):
    """Create enhanced feature engineering pipeline"""
    
    # Categorical Features with improved handling
    budget_cat_indexer = StringIndexer(inputCol="budget_category", outputCol="budget_category_index", handleInvalid="keep")
    budget_cat_encoder = OneHotEncoder(inputCols=["budget_category_index"], outputCols=["budget_category_vec"])
    
    # Enhanced date features assembly
    date_assembler = VectorAssembler(
        inputCols=[
            "is_summer_release", 
            "is_holiday_release",
            "release_year",
            "release_month"  # Added month as feature
        ], 
        outputCol="date_features",
        handleInvalid="keep"
    )
    
    # Genre features
    genre_cols = [col for col in df.columns if col.startswith("is_")]
    genre_assembler = VectorAssembler(inputCols=genre_cols, outputCol="genre_features", handleInvalid="keep")
    
    # Numerical features (pre-release only)
    num_assembler = VectorAssembler(
        inputCols=[
            "budget", 
            "runtime", 
            "production_company_count",
            "movies_in_same_month",
            "cost_per_minute"
        ],
        outputCol="num_features",
        handleInvalid="keep"
    )
    num_scaler = StandardScaler(inputCol="num_features", outputCol="scaled_num_features", withStd=True, withMean=True)
    
    # Final assembly with all features
    final_assembler = VectorAssembler(
        inputCols=[
            "budget_category_vec",
            "date_features",
            "genre_features",
            "scaled_num_features"
        ],
        outputCol="features",
        handleInvalid="keep"
    )
    
    return Pipeline(stages=[
        budget_cat_indexer,
        budget_cat_encoder,
        date_assembler,
        genre_assembler,
        num_assembler,
        num_scaler,
        final_assembler
    ])

def train_and_evaluate_models(train_data_transformed, test_data_transformed):
    """Train models with balanced complexity"""
    
    # ROI Prediction Model (GBTRegressor with moderate complexity)
    roi_model = GBTRegressor(
        featuresCol="features",
        labelCol="roi",
        maxDepth=8,  # Moderate tree depth
        maxBins=64,
        maxIter=50,
        stepSize=0.1
    )
    
    # Parameter grid for ROI model
    roi_param_grid = ParamGridBuilder() \
        .addGrid(GBTRegressor.maxDepth, [6, 8, 10]) \
        .addGrid(GBTRegressor.maxBins, [48, 64]) \
        .addGrid(GBTRegressor.stepSize, [0.05, 0.1]) \
        .build()
    
    # Success Prediction Model (RandomForestClassifier for better stability)
    success_model = RandomForestClassifier(
        featuresCol="features",
        labelCol="success",
        numTrees=100,
        maxDepth=8,
        maxBins=64
    )
    
    # Parameter grid for success model
    success_param_grid = ParamGridBuilder() \
        .addGrid(RandomForestClassifier.maxDepth, [6, 8]) \
        .addGrid(RandomForestClassifier.numTrees, [80, 100]) \
        .addGrid(RandomForestClassifier.maxBins, [48, 64]) \
        .build()
    
    # Cross validation setup
    roi_cv = CrossValidator(
        estimator=roi_model,
        estimatorParamMaps=roi_param_grid,
        evaluator=RegressionEvaluator(labelCol="roi", predictionCol="prediction"),
        numFolds=4,
        parallelism=4
    )
    
    success_cv = CrossValidator(
        estimator=success_model,
        estimatorParamMaps=success_param_grid,
        evaluator=BinaryClassificationEvaluator(labelCol="success"),
        numFolds=4,
        parallelism=4
    )
    
    print("Training ROI model...")
    trained_roi_model = roi_cv.fit(train_data_transformed)
    
    print("Training Success model...")
    trained_success_model = success_cv.fit(train_data_transformed)
    
    # Model evaluation
    roi_predictions = trained_roi_model.transform(test_data_transformed)
    success_predictions = trained_success_model.transform(test_data_transformed)
    
    roi_evaluator = RegressionEvaluator(labelCol="roi", predictionCol="prediction")
    roi_rmse = roi_evaluator.evaluate(roi_predictions)
    
    success_evaluator = BinaryClassificationEvaluator(labelCol="success")
    auc = success_evaluator.evaluate(success_predictions)
    
    print(f"ROI Model RMSE: {roi_rmse}")
    print(f"Success Model AUC: {auc}")
    
    return trained_roi_model.bestModel, trained_success_model.bestModel

def main():
    spark = create_spark_session()
    
    try:
        # Load processed data
        input_path = "/user/sk10945_nyu_edu/big_data_project/processed_movie_data"
        df = spark.read.parquet(input_path)
        
        # Create and fit pipeline
        pipeline = create_pipeline(df)
        train_data, test_data = df.randomSplit([0.8, 0.2], seed=42)
        
        pipeline_model = pipeline.fit(train_data)
        train_data_transformed = pipeline_model.transform(train_data)
        test_data_transformed = pipeline_model.transform(test_data)
        
        # Train models
        roi_model, success_model = train_and_evaluate_models(
            train_data_transformed, 
            test_data_transformed
        )
        
        # Save models with overwrite option
        output_path = "/user/sk10945_nyu_edu/big_data_project/models"
        
        # Save pipeline model
        pipeline_model.write().overwrite().save(f"{output_path}/pipeline")
        
        # Save ROI model
        roi_model.write().overwrite().save(f"{output_path}/roi_model")
        
        # Save success model
        success_model.write().overwrite().save(f"{output_path}/success_model")
        
        print("Models saved successfully with overwrite option.")
        
    finally:
        spark.stop()

if __name__ == "__main__":
    main()