import React from 'react';
import { GenreComparison as GenreComparisonType } from '../types/movie';
import { BarChart3 } from 'lucide-react';

interface GenreComparisonProps {
  comparisons: GenreComparisonType[];
}

export default function GenreComparison({ comparisons }: GenreComparisonProps) {
  const maxProbability = Math.max(...comparisons.map(c => c.successProbability));

  return (
    <div className="space-y-6">
      {/* <div className="flex items-center space-x-2">
        <BarChart3 className="h-6 w-6 text-gray-600" />
        <h2 className="text-xl font-semibold text-gray-900">Genre Comparison</h2>
      </div> */}

      <div className="space-y-4">
        {comparisons.map((comparison) => (
          <div key={comparison.genre} className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="font-medium">{comparison.genre}</span>
              <span>{comparison.successProbability.toFixed(1)}%</span>
            </div>
            <div className="h-2 bg-gray-200 rounded-full">
              <div
                className="h-full bg-blue-600 rounded-full transition-all duration-500"
                style={{
                  width: `${(comparison.successProbability / maxProbability) * 100}%`
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}