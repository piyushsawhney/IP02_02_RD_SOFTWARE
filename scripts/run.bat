pyi-makespec processor/master.py
pyinstaller master.spec --clean

pyi-makespec processor/transactions.py
pyinstaller transactions.spec --clean

pyi-makespec processor/schedule_excel.py
pyinstaller schedule_excel.spec --clean

pyi-makespec processor/schedule.py
pyinstaller schedule.spec --clean

pyi-makespec processor/download_schedule.py
pyinstaller download_schedule.spec --clean