import pandas as pd
from uuid import uuid4
# Crear DataFrame de Movimiento Transaccional
import pandas as pd
from uuid import uuid4
from random import choice
work_ids = [str(uuid4()) for _ in range(5)]
transaction_movement = pd.DataFrame({
    'id': [str(uuid4()) for _ in range(20)],
    'work_id': [choice(work_ids) for _ in range(20)],
    'description': [
        'Supplier payment', 'Material sale', 'Donation', 'Equipment purchase', 
        'Refund', 'Maintenance', 'Service payment', 'Grant', 'Project advance', 'Final settlement',
        'Training session', 'Research funding', 'Emergency repair', 'Software license',
        'Office supplies', 'Legal consultation', 'Sponsorship', 'Advertising campaign',
        'Employee bonus', 'Contractor fee'
    ],
    'category': ['monthly', 'one_time', 'one_time', 'monthly', 'one_time', 'monthly', 
                 'monthly', 'one_time', 'one_time', 'monthly', 'one_time', 'monthly', 
                 'one_time', 'monthly', 'one_time', 'monthly', 'one_time', 'monthly', 
                 'one_time', 'monthly'],
    'date': pd.to_datetime([
        '2024-07-01', '2024-08-15', '2024-09-10', '2024-10-05', '2024-11-20', 
        '2024-12-30', '2024-06-10', '2024-09-25', '2024-07-18', '2024-10-30',
        '2024-05-12', '2024-06-22', '2024-08-14', '2024-09-05', '2024-07-25',
        '2024-10-18', '2024-11-30', '2024-12-05', '2024-08-29', '2024-09-10'
    ]),
    'end_date': pd.to_datetime([pd.NaT, pd.NaT, pd.NaT, '2025-10-05', pd.NaT, '2025-12-30', 
                 '2025-06-10', pd.NaT, pd.NaT, '2025-10-30', pd.NaT, pd.NaT,
                 '2025-08-14', '2025-09-05', pd.NaT, '2025-10-18', '2025-11-30',
                 pd.NaT, pd.NaT, '2025-09-10']),
    'transaction_type': ['expense', 'income', 'income', 'expense', 'income', 'expense', 
                         'expense', 'income', 'income', 'expense', 'expense', 'income', 
                         'expense', 'expense', 'expense', 'income', 'income', 'expense',
                         'income', 'expense'],
    'amount': [500, 1500, 200, 800, 1000, 300, 1200, 250, 1800, 900, 600, 2000, 750, 
               1300, 400, 1100, 2200, 950, 1250, 1400],
    'stabilization_fund_percentage': [10, 20, 15, 5, 25, 8, 12, 18, 22, 10, 14, 30, 
                                      16, 7, 9, 21, 11, 19, 13, 17],
    'subject': [
        'John Doe', 'XYZ Corp', 'Red Cross', 'Tech Solutions', 'Jane Smith', 'ABC Ltd',
        'Facility Services', 'Government Grant', 'Green Energy Inc.', 'Final Account',
        'Training Dept.', 'University Fund', 'Repair Team', 'Software Provider',
        'Stationery Supplier', 'Legal Advisors', 'Event Sponsor', 'Marketing Agency',
        'HR Department', 'Independent Contractor'
    ]
})

transaction_movement.set_index('id', inplace=True)
# Crear DataFrame de Obra
work = pd.DataFrame({
    'work_id': work_ids,
    'name': ['Central Building', 'North Bridge', 'Rural School', 'Municipal Hospital', 'Tech Park'],
    'stipulated_payment': [50000, 75000, 30000, 100000, 120000],
    'start_date': pd.to_datetime(['2024-06-01', '2024-07-15', '2024-08-01', '2024-09-10', '2024-10-05']),
    'end_date': pd.to_datetime(['2025-06-01', '2025-07-15', '2025-08-01', '2025-09-10', '2025-12-31'])
})
work.set_index('work_id', inplace=True)