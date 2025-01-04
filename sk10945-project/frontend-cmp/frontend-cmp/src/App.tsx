import React, { useState } from 'react';
import { MovieDetails, PredictionResult, GenreComparison } from './types/movie';
import { predictionService } from './services/predictionService';
import PredictionForm from './components/PredictionForm';
import PredictionResults from './components/PredictionResults';
import GenreComparisonChart from './components/GenreComparison';
import { Sparkles } from 'lucide-react';

function App() {
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [genreComparisons, setGenreComparisons] = useState<GenreComparison[]>([]);

  const handlePrediction = async (details: MovieDetails) => {
    const result = await predictionService.predictSuccess(details);
    setPrediction(result);
    
    const comparisons = await predictionService.compareGenres(details);
    setGenreComparisons(comparisons);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <Sparkles className="h-10 w-10 text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-900">Movie Success Predictor</h1>
          </div>
          <p className="text-xl text-gray-600">
            Predict your movie's success using big data analysis
          </p>
        </div>

        <div className="flex flex-col space-y-8">
          <div className="bg-white p-8 rounded-xl shadow-md">
            <PredictionForm onSubmit={handlePrediction} />
          </div>

          {prediction && (
            <div className="bg-white p-8 rounded-xl shadow-md space-y-12">
              <PredictionResults result={prediction} />
              <GenreComparisonChart comparisons={genreComparisons} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;