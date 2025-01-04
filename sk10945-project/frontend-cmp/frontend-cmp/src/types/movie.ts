export interface MoviePredictionRequest {
  budget_category: 'low' | 'medium' | 'high';
  is_summer_release: boolean;
  is_holiday_release: boolean;
  release_year: number;
  release_month: number;
  budget: number;
  runtime: number;
  production_company_count: number;
  movies_in_same_month: number;
  cost_per_minute: number;
  genres: string;
}

export interface PredictionResponse {
  roi_prediction: number;
  success_prediction: number;
  success_probability: number;
}

export interface PredictionResult {
  successProbability: number;
  roi: number;
  successPrediction: number;
}