import { MoviePredictionRequest, PredictionResponse, PredictionResult } from '../types/movie';

const API_URL = 'http://127.0.0.1:5001';

export const predictionService = {
  predictSuccess: async (request: MoviePredictionRequest): Promise<PredictionResult> => {
    try {
      const response = await fetch(`${API_URL}/model_inference`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error('Prediction request failed');
      }

      const data: PredictionResponse = await response.json();
      
      return {
        successProbability: (data.success_probability * 100),
        roi: (data.roi_prediction * 100)-70,
        successPrediction: data.success_prediction
      };
    } catch (error) {
      console.error('Error making prediction:', error);
      throw error;
    }
  }
};