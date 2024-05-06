
def Fin_venderbalance(request):
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

        vend = Fin_Vendors.objects.filter(Company=cmp)
        
        venders_data = []
        total_balance1 = 0 
        invoice_balance1=0
        recurring_invoice_balance1=0
        available_credits1=0
        total_invoice_balance1=0
        totCust = 0

        # Initialize total balance outside the loop
        for vendr in vend:
            vendrName = vendr.first_name +" "+vendr.last_name

            PurchaseBill = Fin_Purchase_Bill.objects.filter(vendor=vendr, status='Save')
            Recurring_Bills = Fin_Recurring_Bills.objects.filter(vendor=vendr, status='Save')
            Debit_Note = Fin_Debit_Note.objects.filter(Vendor=vendr, status='Saved')
            print(Debit_Note)
            
            bill_balance = sum(float(inv.balance) for inv in PurchaseBill)
            print(bill_balance)

            recurring_bill_balance = sum(float(rec_inv.balance) for rec_inv in Recurring_Bills)
            print(recurring_bill_balance)
            total_bill_balance = bill_balance + recurring_bill_balance
            print(total_bill_balance)

            available_debits = sum(float(credit_note.balance) for credit_note in Debit_Note)
            print(available_debits)
            
            total_balance = total_bill_balance - available_debits            
            # Update the total balance
            total_balance1 += total_balance
            totCust = len(vend)
            invoice_balance1 += bill_balance
            recurring_invoice_balance1 += recurring_bill_balance
            available_credits1 += available_debits
            total_invoice_balance1+=total_bill_balance
            print(available_credits1)



            venders_data.append({
                'name': vendrName,                
                'invoice_balance': total_bill_balance,
                'available_credits': available_debits,
                'total_balance': total_balance,
            })
        
        context = {
            'cust':vend,
            'customers': venders_data,
            'total_balance1': total_balance1,
            'cmp':cmp,
            'allmodules':allmodules,
            'com':com,
            'data':data,
            'totalCustomers':totCust,
            'totalInvoice':invoice_balance1,
            'totalRecInvoice':recurring_invoice_balance1, 
            'totalCreditNote': available_credits1,
            'invoice_balance':total_bill_balance,
            'available_credits': available_debits,
            'total_invoice_balance':total_invoice_balance1,
            'invoice_c_present': True,
            'cnote_c_present': True,

        }
        
        return render(request, 'company/reports/Fin_vender_balance.html', context)
    else:
        return redirect('/')

def Fin_share_vendor_BalenceReportToEmail(request):
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
                vend = Fin_Vendors.objects.filter(Company=com)
        
                venders_data = []
                total_balance1 = 0 
                invoice_balance1=0
                recurring_invoice_balance1=0
                available_credits1=0
                total_invoice_balance1=0
                totCust = 0

                # Initialize total balance outside the loop
                for vendr in vend:
                    vendrName = vendr.first_name +" "+vendr.last_name

                    PurchaseBill = Fin_Purchase_Bill.objects.filter(vendor=vendr, status='Save')
                    Recurring_Bills = Fin_Recurring_Bills.objects.filter(vendor=vendr, status='Save')
                    Debit_Note = Fin_Debit_Note.objects.filter(Vendor=vendr, status='Saved')
                    print(Debit_Note)
                    
                    bill_balance = sum(float(inv.balance) for inv in PurchaseBill)
                    print(bill_balance)

                    recurring_bill_balance = sum(float(rec_inv.balance) for rec_inv in Recurring_Bills)
                    print(recurring_bill_balance)
                    total_bill_balance = bill_balance + recurring_bill_balance
                    print(total_bill_balance)

                    available_debits = sum(float(credit_note.balance) for credit_note in Debit_Note)
                    print(available_debits)
                    
                    total_balance = total_bill_balance - available_debits            
                    # Update the total balance
                    total_balance1 += total_balance
                    totCust = len(vend)
                    invoice_balance1 += bill_balance
                    recurring_invoice_balance1 += recurring_bill_balance
                    available_credits1 += available_debits
                    total_invoice_balance1+=total_bill_balance
                    print(available_credits1)



                    venders_data.append({
                        'name': vendrName,                
                        'invoice_balance': total_bill_balance,
                        'available_credits': available_debits,
                        'total_balance': total_balance,
                    })
                
                context = {
                        'cust':vend,
                        'customers': venders_data,
                        'total_balance1': total_balance1,
                        'cmp':com,
                        'data':data,
                        'totalCustomers':totCust,
                        'totalInvoice':invoice_balance1,
                        'totalRecInvoice':recurring_invoice_balance1, 
                        'totalCreditNote': available_credits1,
                        'invoice_balance':total_bill_balance,
                        'available_credits': available_debits,
                        'total_invoice_balance':total_invoice_balance1,
                        'invoice_c_present': True,
                        'cnote_c_present': True,

                    }
            

                template_path = 'company/reports/Fin_vender_balence_pdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'Report_VendorBalance'
                subject = f"Report_VendorBalance"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Report for - Report VendorBalance. \n{email_message}\n\n--\nRegards,\n{com.Company_name}\n{com.Address}\n{com.State} - {com.Country}\n{com.Contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Report has been shared via email successfully..!')
                return redirect(Fin_venderbalance)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(Fin_venderbalance)


def Fin_vendorbalence_report_customized(request):
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

        vend = Fin_Vendors.objects.filter(Company=cmp)
        
        venders_data = []
        total_balance1 = 0 
        invoice_balance1=0
        recurring_invoice_balance1=0
        available_credits1=0
        total_invoice_balance1=0
        totCust = 0
        recurring_bill_balance = 0
        total_bill_balance = 0
        available_debits = 0

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
            for vendr in vend:
                vendrName = vendr.first_name +" "+vendr.last_name

                PurchaseBill = Fin_Purchase_Bill.objects.filter(vendor=vendr, status='Save')
                Recurring_Bills = Fin_Recurring_Bills.objects.filter(vendor=vendr, status='Save')
                Debit_Note = Fin_Debit_Note.objects.filter(Vendor=vendr, status='Saved')

                # Filter invoices based on start_date and end_date if provided
                if start_date and end_date:
                    print("ok")
                    PurchaseBill = PurchaseBill.filter( bill_date__range=[start_date, end_date])
                    Recurring_Bills = Recurring_Bills.filter(date__range=[start_date, end_date])
                    Debit_Note = Debit_Note.filter( debit_note_date__range=[start_date, end_date])

                # Calculate invoice balance only if 'invoice_c_present' is true
                if invoice_c:
                    bill_balance = sum(float(inv.balance) for inv in PurchaseBill)
                    
                    recurring_bill_balance = sum(float(rec_inv.balance) for rec_inv in Recurring_Bills)
                    total_bill_balance = bill_balance + recurring_bill_balance
                    available_debits = 0 
                    total_balance = total_bill_balance - available_debits

                if cnote_c:
                    available_debits = sum(float(credit_note.balance) for credit_note in Debit_Note)
                    bill_balance = 0  # Set invoice balance to 0
                    recurring_bill_balance = 0
                    total_bill_balance = 0
                    total_balance = total_bill_balance - available_debits

                if  invoice_c and cnote_c:
                    print("cnote_c andinv2")
                    bill_balance = sum(float(inv.balance) for inv in PurchaseBill)
                    
                    recurring_bill_balance = sum(float(rec_inv.balance) for rec_inv in Recurring_Bills)
                    available_debits = sum(float(credit_note.balance) for credit_note in Debit_Note)
                    total_bill_balance = bill_balance + recurring_bill_balance

                    total_balance = total_bill_balance - available_debits

                    # Update the total balance
                total_balance1 += total_balance
                totCust = len(vend)
                invoice_balance1 += bill_balance
                recurring_invoice_balance1 += recurring_bill_balance
                available_credits1 += available_debits
                total_invoice_balance1 += total_bill_balance

                

                venders_data.append({
                        'name': vendrName,
                        'invoice_balance': total_bill_balance,
                        'available_credits': available_debits,
                        'total_balance': total_balance,
                    })

        else:
            for vendr in vend:
                vendrName = vendr.first_name +" "+vendr.last_name

                print(vendrName)

                # Check if the name matches the filter, if provided
                if name and name != vendrName:
                    print(name)
                    continue


                # Initialize total balance outside the loop
                for vendr in vend:
                    vendrName = vendr.first_name +" "+vendr.last_name

                    # Check if the name matches the filter, if provided
                    if name and name != vendrName:
                        continue

                    PurchaseBill = Fin_Purchase_Bill.objects.filter(vendor=vendr, status='Save')
                    Recurring_Bills = Fin_Recurring_Bills.objects.filter(vendor=vendr, status='Save')
                    Debit_Note = Fin_Debit_Note.objects.filter(Vendor=vendr, status='Saved')
                    print(Debit_Note)

                    # Filter invoices based on start_date and end_date if provided
                    if start_date and end_date:
                        print("ok")
                        PurchaseBill = PurchaseBill.filter( bill_date__range=[start_date, end_date])
                        Recurring_Bills = Recurring_Bills.filter(date__range=[start_date, end_date])
                        Debit_Note = Debit_Note.filter( debit_note_date__range=[start_date, end_date])

                    # Calculate invoice balance only if 'bills' is true
                    if invoice_c:
                        print("invc")
                        bill_balance = sum(float(inv.balance) for inv in PurchaseBill)
                        recurring_bill_balance = sum(float(rec_inv.balance) for rec_inv in Recurring_Bills)
                        total_bill_balance = bill_balance + recurring_bill_balance
                        available_debits = 0  # Set credit note balance to 0
                    if cnote_c:
                        print("cnote_c")
                        available_debits = sum(float(credit_note.balance) for credit_note in Debit_Note)
                        bill_balance = 0  # Set invoice balance to 0
                        recurring_bill_balance = 0
                        total_bill_balance = 0
                    if cnote_c and invoice_c:
                        print("cnote_c andinv")
                        bill_balance = sum(float(inv.balance) for inv in PurchaseBill)
                        recurring_bill_balance = sum(float(rec_inv.balance) for rec_inv in Recurring_Bills)
                        total_bill_balance = bill_balance + recurring_bill_balance

                        available_debits = sum(float(credit_note.balance) for credit_note in Debit_Note)

                    total_balance = total_bill_balance - available_debits

                    # Update the total balance
                    total_balance1 += total_balance
                    totCust = len(vend)
                    invoice_balance1 += bill_balance
                    recurring_invoice_balance1 += recurring_bill_balance
                    available_credits1 += available_debits
                    total_invoice_balance1 += total_bill_balance

                    venders_data.append({
                        'name': vendrName,
                        'invoice_balance': total_bill_balance,
                        'available_credits': available_debits,
                        'total_balance': total_balance,
                    })

        context = {
            'cust':vend,
            'customers': venders_data,
            'total_balance1': total_balance1,
            'cmp': cmp,
            'allmodules': allmodules,
            'com': com,
            'data': data,
            'totalCustomers': totCust,
            'totalInvoice': invoice_balance1,
            'totalRecInvoice': recurring_invoice_balance1,
            'totalCreditNote': available_credits1,
            'invoice_balance': total_bill_balance,
            'available_credits': available_debits,
            'total_invoice_balance': total_invoice_balance1,
            'start_date': start_date_str,  # Pass start_date to the template
            'end_date': end_date_str,  # Pass end_date to the template
            'name': name,  # Pass name to the template
            'invoice_c_present': bool(invoice_c),
            'cnote_c_present': bool(cnote_c),
        }

        return render(request, 'company/reports/Fin_vender_balance.html', context)
    else:
        return redirect('/')
    
    