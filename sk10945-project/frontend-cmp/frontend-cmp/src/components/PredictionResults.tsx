import React from 'react';
import { PredictionResult } from '../types/movie';
import { TrendingUp, DollarSign, PercentCircle } from 'lucide-react';
import { getSuccessPhrase, adjustRoi } from '../utils/predictionUtils';

interface PredictionResultsProps {
  result: PredictionResult;
}

export default function PredictionResults({ result }: PredictionResultsProps) {
  const adjustedRoi = adjustRoi(result.roi);
  const successPhrase = getSuccessPhrase(result.successProbability, adjustedRoi);

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-900">Prediction Results</h2>
      
      <div className="flex flex-col space-y-4">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center space-x-3">
            <PercentCircle className="h-8 w-8 text-blue-500" />
            <div>
              <p className="text-sm text-gray-500">Success Probability</p>
              <p className="text-2xl font-bold">{result.successProbability.toFixed(1)}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center space-x-3">
            <TrendingUp className="h-8 w-8 text-purple-500" />
            <div>
              <p className="text-sm text-gray-500">ROI</p>
              <p className="text-2xl font-bold">{adjustedRoi.toFixed(1)}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center space-x-3">
            <DollarSign className="h-8 w-8 text-green-500" />
            <div>
              <p className="text-sm text-gray-500">Market Outlook</p>
              <p className="text-2xl font-bold">{successPhrase}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}