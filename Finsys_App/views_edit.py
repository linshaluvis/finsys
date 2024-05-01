def Fin_estimate_report(request):
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
        totcust=0

        Est = Fin_Estimate.objects.filter(Company=cmp)
        cust = Fin_Customers.objects.filter(Company=cmp)
       
        if Est:
            for s in Est:
                partyName = s.Customer.first_name +" "+s.Customer.last_name
                date = s.estimate_date
                ship_date = s.exp_date
                ref = s.reference_no
                est =s.estimate_no
                total = s.grandtotal
                invoice_no=0
                totalSales += float(s.grandtotal)
                if s.converted_to_invoice != None:
                    st = 'Converted to Invoice'
                    invoice_no = s.converted_to_invoice.invoice_no
                    print(invoice_no)
                elif s.converted_to_rec_invoice != None:
                    st = 'Converted to Rec. Invoice'
                elif s.converted_to_sales_order != None:
                    st = 'Converted to sales order'
                else:
                    st = s.status

                details = {
                    'date': date,
                    'name': partyName,
                    'sales_no':ref,
                    'ship_date':ship_date,
                    'est':est,
                    'invoice_no': invoice_no,
                    'total':total,
                    'status':st,
                    
                    
                }
                reportData.append(details)
                totcust=len(cust)


        context = {
            'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data, 'reportData':reportData, 'totalSales':totalSales,'totcust':totcust,
            'startDate':None, 'endDate':None
        }
        return render(request,'company/reports/Fin_estimate_report.html', context)
    else:
        return redirect('/')
    

def Fin_estimateDetailsCustomized(request):
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

        if request.method == 'GET':
            startDate = request.GET['from_date']
            endDate = request.GET['to_date']
            status = request.GET['status']

            if startDate == "":
                startDate = None
            if endDate == "":
                endDate = None


            reportData = []
            totalSales = 0
            totcust=0

            if startDate is None or endDate is None:
                if status == 'invoice':
                    sOrder = Fin_Estimate.objects.filter(Company=cmp, converted_to_invoice__isnull = False, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = True)
                elif status == 'recurring_invoice':
                    sOrder = Fin_Estimate.objects.filter(Company=cmp, converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = False,converted_to_sales_order__isnull = True)
                elif status == 'sales_order':
                    sOrder = Fin_Estimate.objects.filter(Company=cmp, converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = False)
                elif status == 'saved':
                    sOrder = Fin_Estimate.objects.filter(Company=cmp, converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = True, status = 'Saved')
                elif status == 'draft':
                    sOrder = Fin_Estimate.objects.filter(Company=cmp, converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = True, status = 'Draft')
                else:
                    sOrder = Fin_Estimate.objects.filter(Company=cmp)
            else:
                if status == 'invoice':
                    sOrder = Fin_Estimate.objects.filter(Company=cmp, estimate_date__range = [startDate, endDate], converted_to_invoice__isnull = False, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = True)
                elif status == 'recurring_invoice':
                    sOrder = Fin_Estimate.objects.filter(Company=cmp, estimate_date__range = [startDate, endDate], converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = False,converted_to_sales_order__isnull = True)
                elif status == 'sales_order':
                    sOrder = Fin_Estimate.objects.filter(Company=cmp,estimate_date__range = [startDate, endDate], converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = False)
                elif status == 'saved':
                    sOrder = Fin_Estimate.objects.filter(Company=cmp, estimate_date__range = [startDate, endDate], converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = True, status = 'Saved')
                elif status == 'draft':
                    sOrder = Fin_Estimate.objects.filter(Company=cmp, estimate_date__range = [startDate, endDate], converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = True, status = 'Draft')
                else:
                    sOrder = Fin_Estimate.objects.filter(Company=cmp, estimate_date__range = [startDate, endDate])

            if sOrder:
                for s in sOrder:
                    partyName = s.Customer.first_name +" "+s.Customer.last_name
                    date = s.estimate_date
                    ship_date = s.exp_date
                    ref = s.reference_no
                    est =s.estimate_no
                    total = s.grandtotal
                    invoice_no=0
                    totalSales += float(s.grandtotal)
                    if s.converted_to_invoice != None:
                        st = 'Converted to Invoice'
                        invoice_no = s.converted_to_invoice.invoice_no
                        print(invoice_no)
                    elif s.converted_to_rec_invoice != None:
                        st = 'Converted to Rec. Invoice'
                    elif s.converted_to_sales_order != None:
                        st = 'Converted to sales order'
                    else:
                        st = s.status

                    details = {
                        'date': date,
                        'name': partyName,
                        'est':est,
                        'invoice_no': invoice_no,
                        'sales_no':ref,
                        'ship_date':ship_date,
                        'total':total,
                        'status':st
                    }
                    reportData.append(details)
                    totcust=len(cust)


            context = {
                'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data, 'reportData':reportData, 'totalSales':totalSales,'totcust':totcust,
                'startDate':startDate, 'endDate':endDate, 'status':status
            }
            return render(request,'company/reports/Fin_estimate_report.html', context)
    else:
        return redirect('/')

def Fin_shareestimateDetailsReportToEmail(request):
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
            
                startDate = request.POST['start']
                endDate = request.POST['end']
                status = request.POST['status']
                if startDate == "":
                    startDate = None
                if endDate == "":
                    endDate = None

                reportData = []
                totalSales = 0
                totcust=0
                if startDate is None or endDate is None:
                    if status == 'invoice':
                        sOrder = Fin_Estimate.objects.filter(Company=cmp, converted_to_invoice__isnull = False, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = True)
                    elif status == 'recurring_invoice':
                        sOrder = Fin_Estimate.objects.filter(Company=cmp, converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = False,converted_to_sales_order__isnull = True)
                    elif status == 'sales_order':
                        sOrder = Fin_Estimate.objects.filter(Company=cmp, converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = False)
                    elif status == 'saved':
                        sOrder = Fin_Estimate.objects.filter(Company=cmp, converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = True, status = 'Saved')
                    elif status == 'draft':
                        sOrder = Fin_Estimate.objects.filter(Company=cmp, converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = True, status = 'Draft')
                    else:
                        sOrder = Fin_Estimate.objects.filter(Company=cmp)
                else:
                    if status == 'invoice':
                        sOrder = Fin_Estimate.objects.filter(Company=cmp, sales_order_date__range = [startDate, endDate], converted_to_invoice__isnull = False, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = True)
                    elif status == 'recurring_invoice':
                        sOrder = Fin_Estimate.objects.filter(Company=cmp, sales_order_date__range = [startDate, endDate], converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = False,converted_to_sales_order__isnull = True)
                    elif status == 'sales_order':
                        sOrder = Fin_Estimate.objects.filter(Company=cmp,estimate_date__range = [startDate, endDate], converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = False)
                    elif status == 'saved':
                        sOrder = Fin_Estimate.objects.filter(Company=cmp, sales_order_date__range = [startDate, endDate], converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = True, status = 'Saved')
                    elif status == 'draft':
                        sOrder = Fin_Estimate.objects.filter(Company=cmp, sales_order_date__range = [startDate, endDate], converted_to_invoice__isnull = True, converted_to_rec_invoice__isnull = True,converted_to_sales_order__isnull = True, status = 'Draft')
                    else:
                        sOrder = Fin_Estimate.objects.filter(Company=cmp, sales_order_date__range = [startDate, endDate])

                if sOrder:
                    for s in sOrder:
                        partyName = s.Customer.first_name +" "+s.Customer.last_name
                        date = s.estimate_date
                        ship_date = s.exp_date
                        ref = s.reference_no
                        est =s.estimate_no
                        invoice_no=0
                        total = s.grandtotal
                        totalSales += float(s.grandtotal)
                        if s.converted_to_invoice != None:
                            st = 'Converted to Invoice'
                            invoice_no = s.converted_to_invoice.invoice_no
                            print(invoice_no)
                        elif s.converted_to_rec_invoice != None:
                            st = 'Converted to Rec. Invoice'
                        elif s.converted_to_sales_order != None:
                            st = 'Converted to sales order'
                        else:
                            st = s.status

                        details = {
                            'date': date,
                            'name': partyName,
                            'invoice_no': invoice_no,
                            'sales_no':ref,
                            'est':est,
                            'ship_date':ship_date,
                            'total':total,
                            'status':st
                        }
                        reportData.append(details)
                        totcust=len(cust)
                
                context = {'cmp':cmp, 'reportData':reportData, 'totalSales':totalSales,'totcust':totcust, 'startDate':startDate, 'endDate':endDate}
                template_path = 'company/reports/Fin_estimate_report_Pdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'Report_estimate_Details'
                subject = f"Report_estimate_Details"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Report for - Sales Order Details. \n{email_message}\n\n--\nRegards,\n{cmp.Company_name}\n{cmp.Address}\n{cmp.State} - {cmp.Country}\n{cmp.Contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Report has been shared via email successfully..!')
                return redirect(Fin_estimate_report)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(Fin_estimate_report)
            
#End