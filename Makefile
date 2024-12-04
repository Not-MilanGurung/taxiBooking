.PHONY: customer driver main_customer initialise

main_customer: 
	python main_customer.py

customer: customer
	python UI/customer_UI.py

driver: driver
	python UI/driver_UI.py

admin: admin
	python UI/admin_UI.py

initialise: 
	python databaseInitialise.py