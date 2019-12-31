# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
#create contract for existing employee
from __future__ import unicode_literals
import frappe
import datetime
import calendar
from dateutil.relativedelta import relativedelta
from frappe.model.document import Document
import json


class Employeecontract(Document):
	def validate(self):
		self.validate_dates()
	def validate_dates(self):
		check = validate_contract_date(self.employee, self.contract_start_date)
		earnings   = self.earnings
		create_Liquidation(self.employee,earnings ,self.contract_start_date ,self.contratc_end_date,self.liquidation_type ,self.total_earnings ,self.employee_full_name, self.yearly_vacation)

		if not check :
			frappe.throw(("You can not add tow contract to this active employee contract."))
	def on_submit(self):
		earnings   = self.earnings
		deductions = self.deductions
		create_salary_structure(self.name ,earnings,deductions,self.employee,self.contract_start_date)

	def on_cancel(self):
		frappe.db.sql('''
		DELETE FROM `tabSalary Structure Assignment` WHERE employee ='%s'
		'''%self.employee)
		frappe.db.commit()
		res = frappe.db.sql('''
		DELETE FROM `tabSalary Structure` WHERE parent ='%s'
		'''%self.name)
		frappe.db.commit()
		frappe.msgprint("Cancelled")

def create_Liquidation(employee ,earnings,start , end,type_l,total_earnings,full_name ,yearly_vacation):
	habit = 0
	basic = 0
	doc = frappe.new_doc("Liquidation")
	doc.employee = employee
	doc.employee_name = full_name
	doc.employee_start_date = start
	doc.employee_end_contract_date=end
	if type_l == "Full":
		doc.employee_receivables =(float(total_earnings)/11)*(float(yearly_vacation)/30.0) * 11.00
	for i in earnings :
		if i.salary_component == "Basic":
			basic +=  float(i.amount)
		if i.salary_component == "Housing allowance":
			habit += float(i.amount)
		if i.salary_component == u"بدل سكن":
			habit += float(i.amount)
	if type_l == "Basic" :
		doc.employee_receivables =(float(basic)/11)*(float(yearly_vacation)/30.0) * 11.00
	if type_l == "Basic + Housing allowance" :
		doc.employee_receivables =((float(basic)+float(habit))/11)*(float(yearly_vacation)/30.0) * 11.00
	doc.insert()
	doc.save()
	frappe.db.commit()



@frappe.whitelist()
def validate_contract_date(employee , start_date):
	date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
	# date = datetime.date.today()
	grant_date    = datetime.datetime.today() - relativedelta(months =+ 2)
	if date < grant_date :
		frappe.msgprint("Unvalid Contract date !")
		return False
	res = frappe.db.sql('''
	SELECT   contratc_end_date  FROM `tabEmployee contract` WHERE employee ='%s' and docstatus = 1
	'''%employee, as_dict=1)


	for i in res:
		if  i.contratc_end_date >  date.date()  :
				return False
		else :
			return True
	return True

@frappe.whitelist()
def get_contract_end_date(duration , start_date,  employee ):
	date        = datetime.datetime.strptime(start_date, "%Y-%m-%d")
	end_date    = date + relativedelta(months =+ int(duration))
	check_dates = validate_contract_date(employee , start_date)
	if check_dates :
		return(end_date.date() )
	else :
		frappe.msgprint("You can not add tow contract to this active employee contract")
	return(end_date.date() )



@frappe.whitelist()
def v_integer(number):
	try :
		int(number)
		return("1")
	except:
		return("0")


#create  salary structure on submit
#assign employee to salary structure
@frappe.whitelist()
def create_salary_structure(parent,item ,deductions,employee ,contract_start_date):
	company               = frappe.db.get_single_value("Global Defaults", "default_company")
	doc                   = frappe.new_doc("Salary Structure")
	doc.is_active         = "Yes"
	doc.parent 			  = parent
	doc.payroll_frequency = "Monthly"
	doc.company           = company
	for i in item :
		doc.append("earnings" ,{
		"salary_component":i.salary_component ,
		"amount" : i.amount
		})

	for i in deductions :
		doc.append("deductions" ,{
		"salary_component":i.salary_component ,
		"amount" : i.amount
		})
	doc.insert()
	doc.docstatus= 1
	doc.save()
	frappe.db.commit()
	create_salary_structure_assignment(doc.name ,employee,contract_start_date)
	return doc.name



def create_salary_structure_assignment(salary_structure,employee ,contract_start_date):
	doc = frappe.new_doc("Salary Structure Assignment")
	doc.employee         = employee
	doc.salary_structure = salary_structure
	doc.from_date        = contract_start_date
	doc.docstatus        = 1
	doc.save()
	frappe.db.commit()
