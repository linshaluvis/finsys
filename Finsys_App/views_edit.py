    
    
def Fin_PaymentReceived_report(request):
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
        reportData = []
        totalSales = 0
        totvendr=0
        totalbalance=0

        payRec = Fin_Payment_Invoice.objects.filter(company=cmp)
       
        if payRec:
            for s in payRec:
                partyName = s.payment.customer.first_name +" "+s.payment.customer.last_name
                date = s.pdate
                method=s.payment.payment_method
                payno=s.payment.payment_no
                
                invno =s.pinvoice_no
                total = s.pinvoice_amount
                balance=s.p_invoice_balance
                totalSales += float(s.pinvoice_amount)
                totalbalance += float(s.p_invoice_balance)

                details = {
                    'date': date,
                    'name': partyName,
                    'payno':payno,
                    'invno':invno,
                    'method':method,
                    'total':total,
                    'balance':balance,
                    
                    
                    
                }
                reportData.append(details)


        context = {
            'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data, 'reportData':reportData,'totalbalance':totalbalance, 'totalSales':totalSales,'totcust':totvendr,
            'startDate':None, 'endDate':None
        }
        return render(request,'company/reports/Fin_payments_received.html', context)
    else:
        return redirect('/')
    

def Fin_payments_receivedCustomized(request):
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

        startDate = request.GET.get('start_date', None)
        endDate = request.GET.get('end_date', None)
       

        print(startDate)
        print(endDate)
        reportData = []
        totalSales = 0
        totvendr=0
        totalbalance=0

        payRec = Fin_Payment_Invoice.objects.filter(company=cmp)
        vendr = Fin_Vendors.objects.filter(Company=cmp)
       
        
        if startDate and endDate:
            payRec = payRec.filter(pdate__range=[startDate, endDate])
            print("1")
        

        if payRec:
            for s in payRec:
                partyName = s.payment.customer.first_name +" "+s.payment.customer.last_name
                date = s.pdate
                method=s.payment.payment_method
                payno=s.payment.payment_no
                
                invno =s.pinvoice_no
                total = s.pinvoice_amount
                balance=s.p_invoice_balance
                totalSales += float(s.pinvoice_amount)
                totalbalance += float(s.p_invoice_balance)

                details = {
                    'date': date,
                    'name': partyName,
                    'payno':payno,
                    'invno':invno,
                    'method':method,
                    'total':total,
                    'balance':balance,
                    
                    
                    
                }
                reportData.append(details)

        context = {
            'allmodules': allmodules, 'com': com, 'cmp': cmp, 'data': data, 'reportData': reportData,'totalbalance':totalbalance,
            'totalSales': totalSales, 'totcust': totvendr, 'startDate': startDate, 'endDate': endDate, 
        }
        return render(request, 'company/reports/Fin_payments_received.html', context)
    else:
        return redirect('/')

def Fin_sharePaymentsReceivedReportToEmail(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id = s_id)
        if data.User_Type == 'Company':
            cmp = Fin_Company_Details.objects.get(Login_Id=s_id)
        else:
            cmp = Fin_Staff_Details.objects.get(Login_Id = s_id).company_id
        
        try:
            if request.method == 'POST':
                emails_string = request.POST['email_ids']

                # Split the string by commas and remove any leading or trailing whitespace
                emails_list = [email.strip() for email in emails_string.split(',')]
                email_message = request.POST['email_message']
                # print(emails_list)
                cust = Fin_Customers.objects.filter(Company=cmp)
            
                cust = Fin_Customers.objects.filter(Company=cmp)
                startDate = request.POST['start']
                endDate = request.POST['end']
                status = request.POST['status']
                if startDate == "":
                    startDate = None
                if endDate == "":
                    endDate = None
                
                reportData = []
                totalSales = 0
                totvendr=0
                totalbalance=0

                payRec = Fin_Payment_Invoice.objects.filter(company=cmp)
            
                if payRec:
                    for s in payRec:
                        partyName = s.payment.customer.first_name +" "+s.payment.customer.last_name
                        date = s.pdate
                        method=s.payment.payment_method
                        payno=s.payment.payment_no
                        
                        invno =s.pinvoice_no
                        total = s.pinvoice_amount
                        balance=s.p_invoice_balance
                        totalSales += float(s.pinvoice_amount)
                        totalbalance += float(s.p_invoice_balance)

                        details = {
                            'date': date,
                            'name': partyName,
                            'payno':payno,
                            'invno':invno,
                            'method':method,
                            'total':total,
                            'balance':balance,
                            
                            
                            
                        }
                        reportData.append(details)

                context = {'cmp': cmp, 'reportData': reportData,'totalbalance':totalbalance,'totalSales': totalSales,'startDate': startDate, 'endDate': endDate, 'status': status}
                template_path = 'company/reports/Fin_paymentsReceivedPdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'Report_paymentsReceived_Details'
                subject = f"Report_paymentsReceived_Details"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Report for - payments Received Details. \n{email_message}\n\n--\nRegards,\n{cmp.Company_name}\n{cmp.Address}\n{cmp.State} - {cmp.Country}\n{cmp.Contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Report has been shared via email successfully..!')
                return redirect(Fin_PaymentReceived_report)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(Fin_PaymentReceived_report)
            
#End



    
def Fin_Paymentmade_report(request):
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

        currentDate = datetime.today()

        reportData = []
        totalSales = 0
        totvendr=0
        totalbalance=0

        payRec = Fin_PaymentMadeDetails.objects.filter(Company=cmp)
       
        if payRec:
            for s in payRec:
                partyName = s.paymentmade.vendor.first_name +" "+s.paymentmade.vendor.last_name
                date = s.date
                method=s.paymentmade.payment_method
                payno=s.paymentmade.payment_number
                
                invno =s.bill_number
                total = s.payment
                balance=s.balance_amount
                totalSales += float(s.payment)
                totalbalance += float(s.balance_amount)

                details = {
                    'date': date,
                    'name': partyName,
                    'payno':payno,
                    'invno':invno,
                    'method': method,
                    'total':total,
                    'balance':balance,
                    
                    
                    
                }
                reportData.append(details)


        context = {
            'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data, 'reportData':reportData,'totalbalance':totalbalance, 'totalSales':totalSales,'totcust':totvendr,
            'startDate':None, 'endDate':None
        }
        return render(request,'company/reports/Fin_payments_made.html', context)
    else:
        return redirect('/')


def Fin_payments_madeCustomized(request):
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

        startDate = request.GET.get('start_date', None)
        endDate = request.GET.get('end_date', None)
       

        print(startDate)
        print(endDate)
        reportData = []
        totalSales = 0
        totvendr=0
        totalbalance=0

        payRec = Fin_PaymentMadeDetails.objects.filter(Company=cmp)

        vendr = Fin_Vendors.objects.filter(Company=cmp)
       
        
        if startDate and endDate:
            payRec = payRec.filter(date__range=[startDate, endDate])
            print("1")
        

        if payRec:
            for s in payRec:
                partyName = s.paymentmade.vendor.first_name +" "+s.paymentmade.vendor.last_name
                date = s.date
                method=s.paymentmade.payment_method
                payno=s.paymentmade.payment_number
                
                invno =s.bill_number
                total = s.payment
                balance=s.balance_amount
                totalSales += float(s.payment)
                totalbalance += float(s.balance_amount)

                details = {
                    'date': date,
                    'name': partyName,
                    'payno':payno,
                    'invno':invno,
                    'method': method,
                    'total':total,
                    'balance':balance,
                    
                    
                    
                }
                reportData.append(details)

        context = {
            'allmodules': allmodules, 'com': com, 'cmp': cmp, 'data': data, 'reportData': reportData,'totalbalance':totalbalance,
            'totalSales': totalSales, 'totcust': totvendr, 'startDate': startDate, 'endDate': endDate, 
        }
        return render(request, 'company/reports/Fin_payments_made.html', context)
    else:
        return redirect('/')
    

def Fin_sharePaymentsmadeReportToEmail(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id = s_id)
        if data.User_Type == 'Company':
            cmp = Fin_Company_Details.objects.get(Login_Id=s_id)
        else:
            cmp = Fin_Staff_Details.objects.get(Login_Id = s_id).company_id
        
        try:
            if request.method == 'POST':
                emails_string = request.POST['email_ids']

                # Split the string by commas and remove any leading or trailing whitespace
                emails_list = [email.strip() for email in emails_string.split(',')]
                email_message = request.POST['email_message']
                # print(emails_list)
                cust = Fin_Customers.objects.filter(Company=cmp)
            
                cust = Fin_Customers.objects.filter(Company=cmp)
                startDate = request.POST['start']
                endDate = request.POST['end']
                status = request.POST['status']
                if startDate == "":
                    startDate = None
                if endDate == "":
                    endDate = None
                
                reportData = []
                totalSales = 0
                totvendr=0
                totalbalance=0

                payRec = Fin_PaymentMadeDetails.objects.filter(Company=cmp)
       
                if payRec:
                    for s in payRec:
                        partyName = s.paymentmade.vendor.first_name +" "+s.paymentmade.vendor.last_name
                        date = s.date
                        method=s.paymentmade.payment_method
                        payno=s.paymentmade.payment_number
                        
                        invno =s.bill_number
                        total = s.payment
                        balance=s.balance_amount
                        totalSales += float(s.payment)
                        totalbalance += float(s.balance_amount)

                        details = {
                            'date': date,
                            'name': partyName,
                            'payno':payno,
                            'invno':invno,
                            'method': method,
                            'total':total,
                            'balance':balance,
                            
                            
                            
                        }
                        reportData.append(details)

                context = {'cmp': cmp, 'reportData': reportData,'totalbalance':totalbalance,'totalSales': totalSales,'startDate': startDate, 'endDate': endDate, 'status': status}
                template_path = 'company/reports/Fin_paymentsMadePdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'Report_paymentsMade_Details'
                subject = f"Report_paymentsMade_Details"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Report for - payments Made Details. \n{email_message}\n\n--\nRegards,\n{cmp.Company_name}\n{cmp.Address}\n{cmp.State} - {cmp.Country}\n{cmp.Contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Report has been shared via email successfully..!')
                return redirect(Fin_Paymentmade_report)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(Fin_Paymentmade_report)
            
#End