// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Social Insurance', {
	// refresh: function(frm) {

	// }

  employee:function(frm){
    var emp = frm.doc.employee ;

    frappe.call({
          method:'frappe.client.get' ,
          args:{
            'doctype' : 'Employee'  ,
            'name' : emp   ,

          },
            callback: function(r){

              frm.set_value("employee_name", r.message.employee_name)
            }


          })

          }


})
