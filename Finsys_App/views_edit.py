def Fin_customerbalence(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id = s_id)
        if data.User_Type == "Company":
            com = Fin_Company_Details.objects.get(Login_Id = s_id)
            cmp = com
        else:
            com = Fin_Staff_Details.objects.get(Login_Id = s_id)
            cmp = com.company_id
        
        allmodules = Fin_Modules_List.objects.get(company_id = cmp,status = 'New')

        cust = Fin_Customers.objects.filter(Company=cmp)
        
        customers_data = []
        total_balance1 = 0 
        invoice_balance1=0
        recurring_invoice_balance1=0
        available_credits1=0
        total_invoice_balance1=0

        # Initialize total balance outside the loop
        for customer in cust:
            customerName = customer.first_name +" "+customer.last_name

            invoices = Fin_Invoice.objects.filter(Customer=customer, status='Saved')
            recurring_invoices = Fin_Recurring_Invoice.objects.filter(Customer=customer, status='Saved')
            credit_notes = Fin_CreditNote.objects.filter(Customer=customer, status='Saved')
            
            invoice_balance = sum(float(inv.balance) for inv in invoices)
            recurring_invoice_balance = sum(float(rec_inv.balance) for rec_inv in recurring_invoices)
            total_invoice_balance = invoice_balance + recurring_invoice_balance
            
            available_credits = sum(float(credit_note.balance) for credit_note in credit_notes)
            
            total_balance = total_invoice_balance - available_credits
            
            # Update the total balance
            total_balance1 += total_balance
            totCust = len(cust)
            invoice_balance1 += invoice_balance
            recurring_invoice_balance1 += recurring_invoice_balance
            available_credits1 += available_credits
            total_invoice_balance1+=total_invoice_balance



            customers_data.append({
                'name': customerName,                
                'invoice_balance': total_invoice_balance,
                'available_credits': available_credits,
                'total_balance': total_balance,
            })
        
        context = {
            'cust':cust,
            'customers': customers_data,
            'total_balance1': total_balance1,
            'cmp':cmp,
            'allmodules':allmodules,
            'com':com,
             'data':data,
             'totalCustomers':totCust,
             'totalInvoice':invoice_balance1,
             'totalRecInvoice':recurring_invoice_balance1, 
             'totalCreditNote': available_credits1,
             'invoice_balance':total_invoice_balance,
            'available_credits': available_credits,
            'total_invoice_balance':total_invoice_balance1,
            'invoice_c_present': True,
            'cnote_c_present': True,

        }
        
        return render(request, 'company/reports/Fin_customerbalence_report.html', context)
    else:
        return redirect('/')

