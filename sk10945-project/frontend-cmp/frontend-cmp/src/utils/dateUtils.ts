export const isHolidayMonth = (month: number): boolean => {
  return [11, 12].includes(month); // November and December
};

export const isSummerMonth = (month: number): boolean => {
  return [6, 7, 8].includes(month); // June, July, August
};