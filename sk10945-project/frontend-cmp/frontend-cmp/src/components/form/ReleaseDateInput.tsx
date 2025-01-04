import React from 'react';
import { Calendar } from 'lucide-react';
import { FormField } from './FormField';

interface ReleaseDateInputProps {
  month: number;
  year: number;
  onMonthChange: (value: number) => void;
  onYearChange: (value: number) => void;
}

export default function ReleaseDateInput({
  month,
  year,
  onMonthChange,
  onYearChange
}: ReleaseDateInputProps) {
  return (
    <FormField
      label="Release Date"
      icon={<Calendar className="h-5 w-5 text-gray-400" />}
    >
      <div className="grid grid-cols-2 gap-4">
        <select
          className="rounded-md border border-gray-300 pl-10 px-3 py-2"
          value={month}
          onChange={(e) => onMonthChange(Number(e.target.value))}
        >
          {Array.from({ length: 12 }, (_, i) => (
            <option key={i + 1} value={i + 1}>
              {new Date(2000, i).toLocaleString('default', { month: 'long' })}
            </option>
          ))}
        </select>
        <input
          type="number"
          className="rounded-md border border-gray-300 px-3 py-2"
          value={year}
          onChange={(e) => onYearChange(Number(e.target.value))}
          min="2000"
          max="2030"
        />
      </div>
    </FormField>
  );
}