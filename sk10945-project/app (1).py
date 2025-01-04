import os
from flask import Flask, request, jsonify
from pyspark.ml.pipeline import PipelineModel
from pyspark.ml.regression import GBTRegressionModel
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.sql import SparkSession
from pyspark.sql import Row
from flask_cors import CORS
import traceback

app = Flask(__name__)

# Enable CORS for specific origins
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

# Path to models and pipeline
MODEL_PATH = "/Users/sumanthramesh/Documents/dev/big_data/movie-success-prediction-project/backend/models"

# Initialize Spark session
def create_spark_session():
    return SparkSession.builder \
        .appName("MovieModelInference") \
        .config("spark.executor.memory", "4g") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()

spark = create_spark_session()
print("SPARK VERSION:", spark.version)

# Load models and pipeline
try:
    print("Loading pipeline model...")
    pipeline_model = PipelineModel.load(os.path.join(MODEL_PATH, "pipeline"))
    print("Pipeline model loaded successfully.")

    print("Loading success model...")
    success_model = RandomForestClassificationModel.load(os.path.join(MODEL_PATH, "success_model"))
    print("Success model loaded successfully.")

    print("Loading ROI model...")
    roi_model = GBTRegressionModel.load(os.path.join(MODEL_PATH, "roi_model"))
    print("ROI model loaded successfully.")

    # Extract genre columns dynamically from the pipeline stage
    genre_columns = []
    for stage in pipeline_model.stages:
        if hasattr(stage, "getInputCols") and stage.getOutputCol() == "genre_features":
            genre_columns = stage.getInputCols()
            break
    print("Detected genre columns:", genre_columns)

except Exception as e:
    print("Error loading models:", str(e))
    print(traceback.format_exc())
    raise

@app.route('/model_inference', methods=["POST"])
def get_model_inference():
    try:
        # Parse input data
        data = request.json
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Validate required fields
        required_fields = [
            "budget_category", "is_summer_release", "is_holiday_release",
            "release_year", "release_month", "budget", "runtime",
            "production_company_count", "movies_in_same_month", "cost_per_minute", "genres"
        ]

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {missing_fields}"}), 400

        # Process genres into one-hot encoded values
        genre_encoding = {col: 0.0 for col in genre_columns}  # Initialize all genres as 0

        if "genres" in data:
            input_genres = data.pop("genres").split(",")
            for genre in input_genres:
                genre_key = f"is_{genre.strip().lower().replace(' ', '_')}"
                if genre_key in genre_encoding:
                    genre_encoding[genre_key] = 1.0
                else:
                    return jsonify({"error": f"Invalid genre: {genre}"}), 400

        # Combine input data with genre encoding
        data.update(genre_encoding)

        # Create a DataFrame from the input data
        input_df = spark.createDataFrame([Row(**data)])

        # Preprocess data using the pipeline
        preprocessed_data = pipeline_model.transform(input_df)

        # Make predictions
        roi_prediction = roi_model.transform(preprocessed_data).select("prediction").collect()[0][0]
        success_prediction = success_model.transform(preprocessed_data).select("probability", "prediction").collect()[0]

        # Prepare the response
        response = {
            "roi_prediction": float(roi_prediction),  # ROI is a regression prediction
            "success_probability": float(success_prediction["probability"][1]),  # Success probability (positive class)
            "success_prediction": int(success_prediction["prediction"])  # Success label (0 or 1)
        }

        return jsonify(response)

    except Exception as e:
        print("Error during inference:", str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
