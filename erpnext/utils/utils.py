# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

import frappe
import calendar

from frappe import _
from frappe.utils import getdate,money_in_words
from datetime import datetime
from collections import namedtuple

def Overlab_Dates(R1_Start_Date,R1_End_date,R2_Start_Date,R2_End_date):
	
    a,b,c,d = \
	datetime.strptime(R1_Start_Date, '%Y-%m-%d'),\
	datetime.strptime(R1_End_date, '%Y-%m-%d'),\
	datetime.strptime(R2_Start_Date, '%Y-%m-%d'),\
	datetime.strptime(R2_End_date, '%Y-%m-%d')
	
    Range = namedtuple('Range', ['start', 'end'])

    r1 = Range(start=datetime(a.year, a.month, a.day), end=datetime(b.year, b.month, b.day))
    r2 = Range(start=datetime(c.year, c.month, c.day), end=datetime(d.year, d.month, d.day))
    
    latest_start = max(r1.start, r2.start)
    earliest_end = min(r1.end, r2.end)
    delta = (earliest_end - latest_start).days + 1
    overlap = max(0, delta)
    
    return overlap

def get_month_days(start_date):
    MonthDays = int(frappe.db.get_single_value("HR Settings", "calculate_on_month_days"))
    if not MonthDays:
        MonthDays = calendar.monthrange(int(getdate(start_date).year),int(getdate(start_date).month))[1]
    return MonthDays

def get_over_time_hour_range():
	over_time_hour_range = float(frappe.db.get_single_value("HR Settings", "over_time_hour_range")) or 1.5
	return  over_time_hour_range

def get_daily_work_hours():
	daily_work_hours = float(frappe.db.get_single_value("HR Settings", "daily_work_hours")) or 8
	return  daily_work_hours

def validate_Percentage(input,min=0,max=100):
    try:
        input = float(input)
        if(input < min):
            frappe.throw(_("Sorry....Would you please enter a valid number bigger than "+_(money_in_words(min).replace("only","").replace("SAR",""))+""))
        elif(input > float(max)):
            frappe.throw(_("Sorry....Would you please enter a valid number lower than "+_(money_in_words(max).replace("only","").replace("SAR",""))+""))
    except ValueError as e:
        raise e

@frappe.whitelist()
def Get_current_company_logo(current_user):
	current_company = frappe.defaults.get_user_default("company")
	logo_path = frappe.db.sql(
		"""
		select logo
		from  tabCompany where name = '{current_company}'
		""".format(current_company= current_company.encode('utf-8'))
	)
	return logo_path