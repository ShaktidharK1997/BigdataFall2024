import React from 'react';
import { FormField } from './FormField';
import { LucideIcon } from 'lucide-react';

interface NumberInputProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  icon?: LucideIcon;
  allowEmpty?: boolean;
}

export default function NumberInput({
  label,
  value,
  onChange,
  min,
  max,
  icon: Icon,
  allowEmpty = false
}: NumberInputProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    if (newValue === '' && allowEmpty) {
      onChange(0);
    } else {
      onChange(Number(newValue));
    }
  };

  return (
    <FormField
      label={label}
      icon={Icon && <Icon className="h-5 w-5 text-gray-400" />}
    >
      <input
        type="number"
        min={min}
        max={max}
        className="w-full rounded-md border border-gray-300 pl-10 px-3 py-2"
        value={value}
        onChange={handleChange}
      />
    </FormField>
  );
}