import pandas as pd
from uuid import uuid4
# Crear DataFrame de Movimiento Transaccional
import pandas as pd
from uuid import uuid4
from random import choice
work_ids = [
    'bfe72e46-c1ed-4919-9295-63e100622a2a',
    '24770055-ceb8-448a-86d9-e58873fb990c',
    '80f191db-1801-44aa-81e3-fd946aec5e4c',
    '1e2e1795-1d1b-468b-beab-e66d1ce853c5',
    '4e866962-c2ad-4a24-a529-ae651bcb68e8',
]
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

import pandas as pd

# Datos fijos para proveedores
suppliers_data = {
    'id': [
        'a1b2c3d4-1234-5678-9101-112131415161',
        'b2c3d4e5-2345-6789-1011-121314151617',
        'c3d4e5f6-3456-7891-0111-213141516171',
        'd4e5f6g7-4567-8910-1112-131415161718',
        'e5f6g7h8-5678-9101-1121-314151617181',
        'f6g7h8i9-6789-1011-1213-141516171819',
        'g7h8i9j0-7891-0111-2131-415161718192',
        'h8i9j0k1-8910-1112-1314-151617181920',
        'i9j0k1l2-9101-1121-3141-516171819212',
        'j0k1l2m3-1011-1213-1415-161718192122'
    ],
    'name': ['Depot 1', 'Depot 2', 'Depot 3', 'Depot 4', 'Depot 5', 'Depot 6', 'Depot 7', 'Depot 8', 'Depot 9', 'Depot 10'],
    'contact': ['1483615247', '2654253158', '3615815835', '4725836152', '5836152471', '6152478361', '7247158362', '8361524715', '9471583624', '1583624715'],
    'nit': ['123456789-1', '234567890-2', '345678901-3', '456789012-4', '567890123-5', '678901234-6', '789012345-7', '890123456-8', '901234567-9', '012345678-0'],
    'location': ['Cali', 'Bogotá', 'Medellín', 'Barranquilla', 'Cartagena', 'Pereira', 'Manizales', 'Bucaramanga', 'Cúcuta', 'Santa Marta']
}

# Crear DataFrame de proveedores
suppliers = pd.DataFrame(suppliers_data)
suppliers.set_index('id', inplace=True)

# Datos fijos para productos
products_data = {
    'id': [
        'p1q2r3s4-1234-5678-9101-112131415161',
        'q2r3s4t5-2345-6789-1011-121314151617',
        'r3s4t5u6-3456-7891-0111-213141516171',
        's4t5u6v7-4567-8910-1112-131415161718',
        't5u6v7w8-5678-9101-1121-314151617181',
        'u6v7w8x9-6789-1011-1213-141516171819',
        'v7w8x9y0-7891-0111-2131-415161718192',
        'w8x9y0z1-8910-1112-1314-151617181920',
        'x9y0z1a2-9101-1121-3141-516171819212',
        'y0z1a2b3-1011-1213-1415-161718192122'
    ],
    'name': ['Concrete', 'Wood Planks', 'Sand', 'Steel Beams', 'Bricks', 'Cement', 'Glass Panels', 'Roof Tiles', 'PVC Pipes', 'Electrical Wires'],
    'stack_price': [100, 1234, 152, 1200, 160, 97, 148, 107, 1184, 200],
    'stack_amount': [500, 200, 1000, 300, 800, 600, 400, 700, 900, 1200],
    'supplier_id': [
        'a1b2c3d4-1234-5678-9101-112131415161',
        'b2c3d4e5-2345-6789-1011-121314151617',
        'c3d4e5f6-3456-7891-0111-213141516171',
        'd4e5f6g7-4567-8910-1112-131415161718',
        'e5f6g7h8-5678-9101-1121-314151617181',
        'f6g7h8i9-6789-1011-1213-141516171819',
        'g7h8i9j0-7891-0111-2131-415161718192',
        'h8i9j0k1-8910-1112-1314-151617181920',
        'i9j0k1l2-9101-1121-3141-516171819212',
        'j0k1l2m3-1011-1213-1415-161718192122'
    ],
    'category': ['Construction', 'Construction', 'Construction', 'Construction', 'Construction', 'Construction', 'Construction', 'Construction', 'Plumbing', 'Electrical'],
    'unit': ['kg', 'units', 'kg', 'units', 'units', 'kg', 'units', 'units', 'meters', 'meters']
}

# Crear DataFrame de productos
products = pd.DataFrame(products_data)
products.set_index('id', inplace=True)

import pandas as pd

# Datos fijos para empleados
employees_data = {
    'id': [
        'e1f2g3h4-1234-5678-9101-112131415161',
        'f2g3h4i5-2345-6789-1011-121314151617',
        'g3h4i5j6-3456-7891-0111-213141516171',
        'h4i5j6k7-4567-8910-1112-131415161718',
        'i5j6k7l8-5678-9101-1121-314151617181',
        'j6k7l8m9-6789-1011-1213-141516171819',
        'k7l8m9n0-7891-0111-2131-415161718192',
        'l8m9n0o1-8910-1112-1314-151617181920',
        'm9n0o1p2-9101-1121-3141-516171819212',
        'n0o1p2q3-1011-1213-1415-161718192122'
    ],
    'name': [
        'Juan Pérez', 'María Gómez', 'Carlos López', 'Ana Rodríguez', 'Luis Martínez',
        'Sofía Hernández', 'Diego García', 'Laura Díaz', 'Jorge Sánchez', 'Carmen Ruiz'
    ],
    'contact': [
        '3001234567', '3102345678', '3203456789', '3304567890', '3405678901',
        '3506789012', '3607890123', '3708901234', '3809012345', '3900123456'
    ],
    'role': [
        'Manager', 'Accountant', 'Engineer', 'Supervisor', 'Technician',
        'Analyst', 'Engineer', 'Technician', 'Supervisor', 'Accountant'
    ],
    'monthly_salary': [
        5000, 4500, 4000, 4200, 3800, 4100, 3900, 3700, 4300, 4400
    ],
    'entered_date': [
        '2020-01-15', '2019-05-20', '2021-03-10', '2018-11-01', '2022-02-25',
        '2020-07-12', '2021-09-05', '2019-12-18', '2022-04-30', '2023-01-10'
    ],
    'contract_type': [
        'Permanent', 'Temporary', 'Permanent', 'Permanent', 'Temporary',
        'Permanent', 'Temporary', 'Permanent', 'Permanent', 'Temporary'
    ],
    'end_contract_date': [
        None, '2024-05-20', None, None, '2023-02-25',
        None, '2023-09-05', None, None, '2024-01-10'
    ],
    'department': [
        'Finance', 'Finance', 'Engineering', 'Operations', 'Engineering',
        'Analytics', 'Engineering', 'Operations', 'Operations', 'Finance'
    ],
    'status': [
        'Active', 'Active', 'Active', 'Active', 'Active',
        'Active', 'Active', 'Active', 'Active', 'Active'
    ]
}

# Crear DataFrame de empleados
employees = pd.DataFrame(employees_data)

# Convertir fechas a tipo datetime
employees['entered_date'] = pd.to_datetime(employees['entered_date'])
employees['end_contract_date'] = pd.to_datetime(employees['end_contract_date'])

# Establecer 'id' como índice
employees.set_index('id', inplace=True)

