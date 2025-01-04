import React from 'react';
import { formatBudget } from '../../utils/budgetUtils';

interface BudgetSliderProps {
  value: number;
  onChange: (value: number) => void;
}

export default function BudgetSlider({ value, onChange }: BudgetSliderProps) {
  const maxBudget = 2800000000;

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700">
        Budget: {formatBudget(value)}
      </label>
      <div className="mt-1">
        <input
          type="range"
          min="1000000"
          max={maxBudget}
          step="1000000"
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>{formatBudget(1000000)}</span>
          <span>{formatBudget(maxBudget)}</span>
        </div>
      </div>
    </div>
  );
}