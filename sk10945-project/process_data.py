from pyspark.sql import SparkSession
from pyspark.sql.functions import (col, when, regexp_replace, to_date, year, month, 
                                 size, split, explode, array_contains, count, isnan,
                                 isnull)
from pyspark.sql.types import DoubleType
from pyspark.sql.window import Window

def create_spark_session():
    return SparkSession.builder \
        .appName("MovieDataProcessing") \
        .config("spark.executor.memory", "16g") \
        .config("spark.driver.memory", "16g") \
        .config("spark.executor.cores", "4") \
        .config("spark.executor.instances", "8") \
        .config("spark.yarn.maxAppAttempts", "3") \
        .config("spark.sql.shuffle.partitions", "200") \
        .config("spark.default.parallelism", "200") \
        .getOrCreate()

def process_movie_data(spark):
    """Process movie data with enhanced feature engineering and validation"""
    try:
        # Read the data
        df = spark.read.format('csv') \
            .options(header='true', inferSchema='true', quote='"', escape='"') \
            .load("hdfs:/user/sk10945_nyu_edu/big_data_project/IMDB_movie_dataset.csv")
        
        print("Initial row count:", df.count())
        
        # Remove unwanted columns
        columns_to_drop = ['overview', 'homepage', 'backdrop_path', 'poster_path', 
                          'tagline', 'id', 'adult', 'imdb_id']
        df = df.drop(*columns_to_drop)
        
        # Enhanced validation: Drop nulls and validate numerical columns
        df = df.na.drop(subset=["release_date", "title", 'vote_count', 
                               'vote_average', 'budget', 'runtime', 'revenue'])
        
        # Validate numerical columns
        df = df.filter(
            (col("budget").isNotNull()) &
            (col("runtime").isNotNull()) &
            (col("revenue").isNotNull()) &
            (col("budget") > 0) &
            (col("runtime") > 0) &
            (~isnan(col("budget"))) &
            (~isnan(col("runtime"))) &
            (~isnan(col("revenue")))
        )
        
        print("Row count after dropping nulls and validation:", df.count())
        
        # Convert and filter dates
        df = df.withColumn("release_date", to_date("release_date"))
        df = df.filter(
            (col("release_date").between("1980-01-01", "2023-12-31")) &
            (col("runtime") > 20) &
            ~((col("vote_average") == 0) & (col("vote_count") > 0)) &
            (col("revenue") >= 0) &
            (col("budget") >= 0)
        )
        
        print("Row count after filtering:", df.count())
        
        # Add temporal features
        df = df.withColumn("release_year", year("release_date"))
        df = df.withColumn("release_month", month("release_date"))
        df = df.withColumn("is_summer_release", 
            when((month("release_date").between(6, 8)), 1.0).otherwise(0.0))
        df = df.withColumn("is_holiday_release", 
            when((month("release_date").isin(11, 12)), 1.0).otherwise(0.0))
        
        # Add budget categories
        df = df.withColumn("budget_category", 
            when(col("budget") < 5000000, "low")
            .when(col("budget") < 40000000, "medium")
            .when(col("budget") < 100000000, "high")
            .otherwise("blockbuster"))
        
        # Process genres with validation
        df = df.filter(col("genres").isNotNull())  # Ensure genres are not null
        df = df.withColumn("genres_array", split("genres", ","))
        genres_list = df.select(explode("genres_array").alias("genre")).distinct().collect()
        for genre in genres_list:
            df = df.withColumn(f"is_{genre.genre.lower()}", 
                array_contains(col("genres_array"), genre.genre).cast("double"))
        
        # Add production company features with validation
        df = df.withColumn("production_company_count", 
            when(col("production_companies").isNull(), 1)
            .otherwise(size(split("production_companies", ","))))
        
        # Add language features
        df = df.withColumn("is_english", 
            when(col("original_language") == "en", 1.0).otherwise(0.0))
        
        # Add derived metrics with validation against division by zero
        df = df.withColumn("cost_per_minute", 
            when(col("runtime") > 0, col("budget") / col("runtime"))
            .otherwise(0.0))
        
        # Add competition metrics
        window_spec = Window.partitionBy("release_year", "release_month")
        df = df.withColumn("movies_in_same_month", count("*").over(window_spec))
        
        # Calculate ROI and success with validation
        df = df.withColumn(
            "roi", 
            when(col("budget") > 0, 
                 (col("revenue") - col("budget")) / col("budget")
            ).otherwise(0.0)
        )
        
        # Cap extreme ROI values
        df = df.withColumn(
            "roi",
            when(col("roi") > 10.0, 10.0)  # Cap at 1000% ROI
            .when(col("roi") < -1.0, -1.0)  # Cap at -100% loss
            .otherwise(col("roi"))
        )
        
        df = df.withColumn(
            "success",
            when(col("roi") > 0.5, 1.0).otherwise(0.0)
        )
        
        # Final validation to remove any remaining invalid values
        df = df.filter(
            (~isnan(col("roi"))) &
            (~isnan(col("cost_per_minute"))) &
            (col("cost_per_minute").isNotNull()) &
            (col("roi").isNotNull())
        )
        
        # Show summary statistics
        print("\nSummary Statistics:")
        numeric_cols = ["budget", "revenue", "runtime", "roi", "cost_per_minute"]
        df.select(numeric_cols).summary().show()
        
        # Save processed data
        output_path = "hdfs:/user/sk10945_nyu_edu/big_data_project/processed_movie_data"
        df.write.mode("overwrite").parquet(output_path)
        print(f"\nProcessed data saved to: {output_path}")
        
        # Show schema of processed data
        print("\nProcessed Data Schema:")
        df.printSchema()
        
        return df
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    spark = create_spark_session()
    try:
        print("Starting data processing...")
        processed_df = process_movie_data(spark)
        print("Data processing completed successfully!")
    except Exception as e:
        print(f"Error during processing: {str(e)}")
    finally:
        spark.stop()