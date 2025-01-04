import React, { ReactNode } from 'react';

interface FormFieldProps {
  label: string;
  icon?: ReactNode;
  children: ReactNode;
}

export function FormField({ label, icon, children }: FormFieldProps) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <div className="mt-1 relative">
        {icon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            {icon}
          </div>
        )}
        {children}
      </div>
    </div>
  );
}