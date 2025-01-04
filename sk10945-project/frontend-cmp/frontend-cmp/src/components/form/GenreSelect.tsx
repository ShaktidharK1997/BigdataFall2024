import React from 'react';
import { Film } from 'lucide-react';
import { FormField } from './FormField';

interface GenreSelectProps {
  value: string;
  onChange: (value: string) => void;
}

export default function GenreSelect({ value, onChange }: GenreSelectProps) {
  const genres = ['action', 'comedy', 'drama', 'horror', 'romance', 'western', 'documentary', 'history'];

  return (
    <FormField
      label="Genre"
      icon={<Film className="h-5 w-5 text-gray-400" />}
    >
      <select
        className="w-full rounded-md border border-gray-300 pl-10 px-3 py-2"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {genres.map((genre) => (
          <option key={genre} value={genre}>
            {genre.charAt(0).toUpperCase() + genre.slice(1)}
          </option>
        ))}
      </select>
    </FormField>
  );
}