
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
        totCust = 0

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

def Fin_shareCustomerBalenceReportToEmail(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id = s_id)
        if data.User_Type == 'Company':
            com = Fin_Company_Details.objects.get(Login_Id=s_id)
        else:
            com = Fin_Staff_Details.objects.get(Login_Id = s_id).company_id
        
        try:
            if request.method == 'POST':
                emails_string = request.POST['email_ids']

                # Split the string by commas and remove any leading or trailing whitespace
                emails_list = [email.strip() for email in emails_string.split(',')]
                email_message = request.POST['email_message']
                # print(emails_list)
            
                startDate = request.POST['start']
                endDate = request.POST['end']
                if startDate == "":
                    startDate = None
                if endDate == "":
                    endDate = None
                cust = Fin_Customers.objects.filter(Company=com)
                print(cust)
        
                customers_data = []
                total_balance1 = 0 
                invoice_balance1=0
                recurring_invoice_balance1=0
                available_credits1=0
                total_invoice_balance1=0

                # Initialize total balance outside the loop
                for customer in cust:
                    customerName = customer.first_name +" "+customer.last_name
                    print(customerName)

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
                        'customers': customers_data,
                        'total_balance1': total_balance1,
                        'cmp':com,
                        'com':com,
                        'data':data,
                        'totalCustomers':totCust,
                        'totalInvoice':invoice_balance1,
                        'totalRecInvoice':recurring_invoice_balance1, 
                        'totalCreditNote': available_credits1,
                        'invoice_balance':total_invoice_balance,
                        'available_credits': available_credits,
                        'total_invoice_balance':total_invoice_balance1,
                        'startDate':startDate, 
                        'endDate':endDate,

                    }
            

                template_path = 'company/reports/Fin_salesBalancePdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'Report_CustomerBalance'
                subject = f"Report_CustomerBalance"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Report for - Report CustomerBalance. \n{email_message}\n\n--\nRegards,\n{com.Company_name}\n{com.Address}\n{com.State} - {com.Country}\n{com.Contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Report has been shared via email successfully..!')
                return redirect(Fin_customerbalence)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(Fin_customerbalence)


def Fin_customerbalence_report_customized(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id=s_id)
        if data.User_Type == "Company":
            com = Fin_Company_Details.objects.get(Login_Id=s_id)
            cmp = com
        else:
            com = Fin_Staff_Details.objects.get(Login_Id=s_id)
            cmp = com.company_id

        allmodules = Fin_Modules_List.objects.get(company_id=cmp, status='New')

        cust = Fin_Customers.objects.filter(Company=cmp)

        customers_data = []
        total_balance1 = 0
        invoice_balance1 = 0
        recurring_invoice_balance1 = 0
        available_credits1 = 0
        total_invoice_balance1 = 0
        totCust = 0
        recurring_invoice_balance = 0
        total_invoice_balance = 0
        available_credits = 0

        # Get the start date from POST data with a default value of None
     
        if 'from_date' in request.POST:
            start_date_str = request.POST['from_date']
        else:
            start_date_str = None
        print(start_date_str)
        if 'to_date' in request.POST:
            end_date_str = request.POST['to_date']
        else:
            end_date_str = None
        
        print(end_date_str)
        

        # Check if 'bills' is present in POST data
        if 'bills' in request.POST:
            invoice_c = request.POST['bills']
        else:
            invoice_c = ''

        # Check if 'dnote' is present in POST data
        if 'dnote' in request.POST:
            cnote_c = request.POST['dnote']
        else:
            cnote_c = ''

        # Check if 'transactions' is present in POST data
        if 'transactions' in request.POST:
            name = request.POST['transactions']
        else:
            name = None
        print(name)

        # Convert start_date and end_date strings to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
        print(start_date)
        print(end_date)
        if name == 'all':
            for customer in cust:
                customerName = customer.first_name + " " + customer.last_name
                print(customerName)
                invoices = Fin_Invoice.objects.filter(Customer=customer, status='Saved')
                recurring_invoices = Fin_Recurring_Invoice.objects.filter(Customer=customer, status='Saved')
                credit_notes = Fin_CreditNote.objects.filter(Customer=customer, status='Saved')

                # Filter invoices based on start_date and end_date if provided
                if start_date and end_date:
                    print("ok")
                    invoices = invoices.filter(invoice_date__range=[start_date, end_date])
                    print(invoices)
                    recurring_invoices = recurring_invoices.filter(start_date__range=[start_date, end_date])
                    print(recurring_invoices)
                    credit_notes = credit_notes.filter(creditnote_date__range=[start_date, end_date])

                # Calculate invoice balance only if 'invoice_c_present' is true
                if invoice_c:
                    invoice_balance = sum(float(inv.balance) for inv in invoices)
                    
                    recurring_invoice_balance = sum(float(rec_inv.balance) for rec_inv in recurring_invoices)
                    total_invoice_balance = invoice_balance + recurring_invoice_balance
                    available_credits = 0 
                    total_balance = total_invoice_balance - available_credits

                if cnote_c:
                    available_credits = sum(float(credit_note.balance) for credit_note in credit_notes)
                    invoice_balance = 0  # Set invoice balance to 0
                    recurring_invoice_balance = 0
                    total_invoice_balance = 0
                    total_balance = total_invoice_balance - available_credits

                if  invoice_c and cnote_c:
                    print("cnote_c andinv2")
                    invoice_balance = sum(float(inv.balance) for inv in invoices)
                    
                    recurring_invoice_balance = sum(float(rec_inv.balance) for rec_inv in recurring_invoices)
                    available_credits = sum(float(credit_note.balance) for credit_note in credit_notes)
                    total_invoice_balance = invoice_balance + recurring_invoice_balance
                    total_balance = total_invoice_balance - available_credits

                    # Update the total balance
                total_balance1 += total_balance
                totCust = len(cust)
                invoice_balance1 += invoice_balance
                recurring_invoice_balance1 += recurring_invoice_balance
                available_credits1 += available_credits
                total_invoice_balance1 += total_invoice_balance

                

                customers_data.append({
                        'name': customerName,
                        'invoice_balance': total_invoice_balance,
                        'available_credits': available_credits,
                        'total_balance': total_balance,
                    })

        else:
            for customer in cust:
                customerName = customer.first_name + " " + customer.last_name
                print(customerName)

                # Check if the name matches the filter, if provided
                if name and name != customerName:
                    print(name)
                    continue


                # Initialize total balance outside the loop
                for customer in cust:
                    customerName = customer.first_name + " " + customer.last_name

                    # Check if the name matches the filter, if provided
                    if name and name != customerName:
                        continue

                    invoices = Fin_Invoice.objects.filter(Customer=customer, status='Saved')
                    recurring_invoices = Fin_Recurring_Invoice.objects.filter(Customer=customer, status='Saved')
                    credit_notes = Fin_CreditNote.objects.filter(Customer=customer, status='Saved')

                    # Filter invoices based on start_date and end_date if provided
                    if start_date and end_date:
                        invoices = invoices.filter(invoice_date__range=[start_date, end_date])
                        recurring_invoices = recurring_invoices.filter(start_date__range=[start_date, end_date])
                        credit_notes = credit_notes.filter(creditnote_date__range=[start_date, end_date])

                    # Calculate invoice balance only if 'bills' is true
                    if invoice_c:
                        print("invc")
                        invoice_balance = sum(float(inv.balance) for inv in invoices)
                        recurring_invoice_balance = sum(float(rec_inv.balance) for rec_inv in recurring_invoices)
                        total_invoice_balance = invoice_balance + recurring_invoice_balance
                        available_credits = 0  # Set credit note balance to 0
                    if cnote_c:
                        print("cnote_c")
                        available_credits = sum(float(credit_note.balance) for credit_note in credit_notes)
                        invoice_balance = 0  # Set invoice balance to 0
                        recurring_invoice_balance = 0
                        total_invoice_balance = 0
                    if cnote_c and invoice_c:
                        print("cnote_c andinv")
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
                    total_invoice_balance1 += total_invoice_balance

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
            'cmp': cmp,
            'allmodules': allmodules,
            'com': com,
            'data': data,
            'totalCustomers': totCust,
            'totalInvoice': invoice_balance1,
            'totalRecInvoice': recurring_invoice_balance1,
            'totalCreditNote': available_credits1,
            'invoice_balance': total_invoice_balance,
            'available_credits': available_credits,
            'total_invoice_balance': total_invoice_balance1,
            'start_date': start_date_str,  # Pass start_date to the template
            'end_date': end_date_str,  # Pass end_date to the template
            'name': name,  # Pass name to the template
            'invoice_c_present': bool(invoice_c),
            'cnote_c_present': bool(cnote_c),
        }

        return render(request, 'company/reports/Fin_customerbalence_report.html', context)
    else:
        return redirect('/')
