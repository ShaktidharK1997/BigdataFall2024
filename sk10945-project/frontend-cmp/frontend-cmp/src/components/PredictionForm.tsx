import React, { useState } from 'react';
import { MoviePredictionRequest } from '../types/movie';
import { Clock, Building2, Film } from 'lucide-react';
import { getBudgetCategory } from '../utils/budgetUtils';
import { isHolidayMonth, isSummerMonth } from '../utils/dateUtils';
import BudgetSlider from './form/BudgetSlider';
import NumberInput from './form/NumberInput';
import GenreSelect from './form/GenreSelect';
import ReleaseDateInput from './form/ReleaseDateInput';

interface PredictionFormProps {
  onSubmit: (request: MoviePredictionRequest) => void;
}

export default function PredictionForm({ onSubmit }: PredictionFormProps) {
  const [formData, setFormData] = useState({
    budget: 100000000,
    runtime: 120,
    release_month: new Date().getMonth() + 1,
    release_year: new Date().getFullYear(),
    production_company_count: 3,
    movies_in_same_month: 12,
    genres: 'drama'
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const request: MoviePredictionRequest = {
      ...formData,
      budget_category: getBudgetCategory(formData.budget),
      is_summer_release: isSummerMonth(formData.release_month),
      is_holiday_release: isHolidayMonth(formData.release_month),
      cost_per_minute: formData.budget / formData.runtime
    };
    onSubmit(request);
  };

  const updateField = (field: string, value: number | string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <BudgetSlider
        value={formData.budget}
        onChange={(value) => updateField('budget', value)}
      />

      <div className="grid gap-6">
        <NumberInput
          label="Runtime (minutes)"
          value={formData.runtime}
          onChange={(value) => updateField('runtime', value)}
          min={30}
          max={300}
          icon={Clock}
        />

        <ReleaseDateInput
          month={formData.release_month}
          year={formData.release_year}
          onMonthChange={(value) => updateField('release_month', value)}
          onYearChange={(value) => updateField('release_year', value)}
        />

        <NumberInput
          label="Production Companies"
          value={formData.production_company_count}
          onChange={(value) => updateField('production_company_count', value)}
          min={1}
          max={10}
          icon={Building2}
        />

        {/* <NumberInput
          label="Movies in Same Month"
          value={formData.movies_in_same_month}
          onChange={(value) => updateField('movies_in_same_month', value)}
          icon={Film}
          allowEmpty={true}
        /> */}

        <GenreSelect
          value={formData.genres}
          onChange={(value) => updateField('genres', value)}
        />
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium"
      >
        Predict Success
      </button>
    </form>
  );
}