pyi-makespec create_schedule_excel.py
pyinstaller --onefile --windowed create_schedule_excel.spec --clean

pyi-makespec create_master.py
pyinstaller --onefile --windowed create_master.spec --clean


pyi-makespec create_schedule.py
pyinstaller --onefile --windowed create_schedule.spec --clean

pyi-makespec enter_transactions.py
pyinstaller --onefile --windowed enter_transactions.spec --clean