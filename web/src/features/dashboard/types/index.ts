export type AdoptionStatsRead = {
  current_month_total: number;
  average_days_to_adoption?: number | null;
  return_rate: number;
};

export type ExpensesHighlightRead = {
  current_month_total: number;       // Decimal → número no JSON
  previous_month_total: number;
  variation_percentage: number;      // ex.: -15.5
};

export type ExpensesByCategoryRead = {
  category_id: string;
  category_name: string;
  total: number;                      // Decimal → número
};

export type DashboardSummaryRead = {
  active_animals: number;
  adoptions: AdoptionStatsRead;
  volunteers_active: number;
  expenses: ExpensesHighlightRead;
  expenses_by_category: ExpensesByCategoryRead[];
};
