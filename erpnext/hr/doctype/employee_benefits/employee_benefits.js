// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee benefits', {
	// refresh: function(frm) {
  //
	// },
  contract: function(frm){
    var contract = frm.doc.contract
    var employee_data = frappe.get_doc('Employee contract',contract ) ;
    // var employee_data = frappe.get_doc('Employee contract',contract )
    // console.log(employee_data);
    frappe.call({
          method :"erpnext.hr.doctype.employee_benefits.employee_benefits.get_all_data" ,
          args:{
            'contract':contract
          },
             callback: function(r){
            console.log(r.message)
          }



      })


  } ,
  onload: function(frm){
   	if(frm.doc.contract){
      var contract = frm.doc.contract ;
      var employee_data = frappe.get_doc('Employee contract',contract ) ;

    }

  }
});
