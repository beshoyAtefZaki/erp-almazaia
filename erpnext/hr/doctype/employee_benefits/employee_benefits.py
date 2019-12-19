# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Employeebenefits(Document):
	pass




@frappe.whitelist()
def get_all_data(contract) :
	res = frappe.db.sql('''
	SELECT   employee, contract_type, contract_start_date, total_earnings, total_deductions  FROM  `tabEmployee contract`  WHERE name = '%s'

	'''%contract, as_dict=1)
	return(res)
