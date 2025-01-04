export const getBudgetCategory = (budget: number): 'low' | 'medium' | 'high' => {
  if (budget < 50000000) return 'low';
  if (budget < 150000000) return 'medium';
  return 'high';
};

export const formatBudget = (budget: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    notation: 'compact',
    maximumFractionDigits: 1
  }).format(budget);
};