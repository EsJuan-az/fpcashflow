from utils.store import work as w, transaction_movement as tm
import pandas as pd
from datetime import datetime, timedelta


def stabilization_fund_historic() -> pd.Series:
    # Tener fecha, income * sf, expense * sf en un dataframe
    df = tm.copy()
    is_expense = df['transaction_type'] == 'expense'
    df.loc[is_expense, 'amount'] *= -1
    df['stabilization_fund_amount'] = df['amount'] * df['stabilization_fund_percentage'] * 0.01
    df = df[['date', 'stabilization_fund_amount']].sort_values('date').groupby('date').aggregate('sum')
    return df['stabilization_fund_amount'].cumsum().round(2)
    
def required_for_stabilization_historic() -> pd.Series:
    df = tm.copy()
    df = df.sort_values('date').set_index('date')
    is_expense = df['transaction_type'] == 'expense'
    df.loc[~is_expense, 'amount'] = 0
    df.loc[is_expense, 'last_6month_expense'] = df.loc[is_expense, 'amount'].rolling(f'{6*30}D').sum()
    df['last_6month_expense'].ffill(inplace=True, axis=0)

    df.loc[is_expense, 'last_6month_expense_dev'] = df.loc[is_expense, 'amount'].rolling(f'{6*30}D').std()
    df['last_6month_expense_dev'] = df['last_6month_expense_dev'].ffill(axis=0).fillna(0)
    calculation = df['last_6month_expense'] + df['last_6month_expense_dev'] * 0.3
    calculation.name = 'required_stabilization_fund'
    return calculation.round(2)

def recommended_destination_percentage(amount) -> float:
    amount = max(amount, 1)
    sf = stabilization_fund_historic().iloc[-1]
    required = required_for_stabilization_historic().iloc[-1]
    if required <= sf:
        return 0
    
    needed = required - sf 
    needed = 50 * needed // 50 
    percentage = min(needed / amount, 0.6) * 100
    return round(max(0, percentage), 2)

def pending_expenses() -> pd.DataFrame:
    current_date = datetime.now()
    five_days_from_now = current_date + timedelta(days=5) 

    is_expense = tm['transaction_type'] == 'expense'
    
    # Filtrar los pagos one_time cuyo 'date' esté dentro de los próximos 5 días
    one_time_upcoming = (tm['category'] == 'one_time') & (tm['date'] > current_date) & (tm['date'] <= five_days_from_now)
    
    # Filtrar pagos "monthly" cuyo `end_date` no haya pasado
    monthly_upcoming = (tm['category'] == 'monthly') & (tm['end_date'] >= current_date)
    
    # Para los pagos "monthly", verificar que el día del mes de `start_date` esté a menos de 5 días de la fecha actual
    monthly_upcoming_5_days = monthly_upcoming & \
                               (tm['date'].dt.day >= current_date.day) & \
                               (tm['date'].dt.day <= (current_date.day + 5))
    
    # Combinamos los filtros para one_time y monthly
    df = tm.copy()
    df = df[is_expense & (one_time_upcoming | monthly_upcoming_5_days)]
    
    merged_df = df.merge(w, how='left', left_on='work_id', right_index=True)
    
    return merged_df