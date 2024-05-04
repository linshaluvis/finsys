def Fin_recbillCustomized(request):
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
        status = request.GET.get('status')
        report = request.GET.get('billdate',None)



        currentDate = datetime.today()
        reportData = []
        totalSales = 0
        totvendr=0
        totalbalance=0

        Recbill = Fin_Recurring_Bills.objects.filter(company=cmp)
        vendr = Fin_Vendors.objects.filter(Company=cmp)
       
        
        if startDate and endDate:
            Recbill = Recbill.filter(date__range=[startDate, endDate])
            
        if report:
            if report=='billdate':
                Recbill = Recbill.filter(date__range=[startDate, endDate])
            if report=='shipdate':
                Recbill = Recbill.filter(expected_shipment_date__range=[startDate, endDate])
              

        if status:
            if status == 'Draft':
                Recbill = Recbill.filter(status = 'Draft')
            elif status == 'fully paid':
                Recbill = Recbill.filter(advanceAmount_paid=F('grand_total'),status='Save')
                

            elif status == 'Not paid':
                Recbill = Recbill.filter(Q(advanceAmount_paid=0)  & Q(expected_shipment_date__gt=currentDate),status='Save')

            elif status == 'partially paid':
                Recbill = Recbill.filter(Q(advanceAmount_paid__gt=0)  & Q(advanceAmount_paid__lt=F('grand_total')) & Q(expected_shipment_date__gt=currentDate),status='Save')
                print(Recbill)
                print("5")
            elif status == 'overdue':
                Recbill = Recbill.filter((Q(expected_shipment_date__lte=currentDate) & Q(advanceAmount_paid__lt=F('grand_total')) ), status='Save')
                print("3")
                print(Recbill)

        for s in Recbill:
            partyName = s.vendor.first_name +" "+s.vendor.last_name
            date = s.date
            ship_date = s.expected_shipment_date
            end_date = datetime.combine(s.expected_shipment_date, datetime.min.time())

            rbill =s.recurring_bill_number
            ordrno =s.purchase_order_number
            total = s.grand_total
            paid=s.advanceAmount_paid
            balance=s.balance
            st=s.status
            totalSales += float(s.grand_total)
            totalbalance += float(s.balance)
            if s.status == 'Draft':
                st = 'Draft'
            elif s.advanceAmount_paid == 0 and end_date>currentDate:
                st = 'Not paid'
                
            elif s.advanceAmount_paid == s.grand_total:
                st = 'fully paid'
            
            elif s.advanceAmount_paid > 0 and s.advanceAmount_paid<s.grand_total and end_date>currentDate:
                st = 'partially paid'
            elif end_date<currentDate and s.advanceAmount_paid<=s.grand_total:
                st = 'overdue'
            
            else:
                st = s.status

            details = {
                'date': date,
                'name': partyName,
                'ship_date':ship_date,
                'rbill':rbill,
                'ordrno': ordrno,
                'total':total,
                'status':st,
                'balance':balance,
                
                
                
            }
            reportData.append(details)
            totvendr=len(vendr)

        context = {
            'allmodules': allmodules, 'com': com, 'cmp': cmp, 'data': data, 'reportData': reportData,'totalbalance':totalbalance,
            'totalSales': totalSales, 'totcust': totvendr, 'startDate': startDate, 'endDate': endDate, 'status': status,'billdate':report
        }
        return render(request, 'company/reports/Fin_rec_bill_report.html', context)
    else:
        return redirect('/')

def Fin_shareREC_billDetailsReportToEmail(request):
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
             
                currentDate = datetime.today()


                reportData = []
                totalSales = 0
                totvendr=0
                totalbalance=0

                Recbill = Fin_Recurring_Bills.objects.filter(company=cmp)
                vendr = Fin_Vendors.objects.filter(Company=cmp)
       
        
                if startDate and endDate:
                    Recbill = Recbill.filter(date__range=[startDate, endDate])
                    print(Recbill)
                    print("1")
                

                if status:
                    if status == 'Draft':
                        Recbill = Recbill.filter(status = 'Draft')
                    elif status == 'fully paid':
                        Recbill = Recbill.filter(advanceAmount_paid=F('grand_total'),status='Save')
                      
                    elif status == 'Not paid':
                        Recbill = Recbill.filter(Q(advanceAmount_paid=0)  & Q(expected_shipment_date__gt=currentDate),status='Save')

                    elif status == 'partially paid':
                        Recbill = Recbill.filter(Q(advanceAmount_paid__gt=0)  & Q(advanceAmount_paid__lt=F('grand_total')) & Q(expected_shipment_date__gt=currentDate),status='Save')
                    
                    elif status == 'overdue':
                        Recbill = Recbill.filter((Q(expected_shipment_date__lte=currentDate) & Q(advanceAmount_paid__lt=F('grand_total')) ), status='Save')
                       

                for s in Recbill:
                    partyName = s.vendor.first_name +" "+s.vendor.last_name
                    date = s.date
                    ship_date = s.expected_shipment_date
                    end_date = datetime.combine(s.expected_shipment_date, datetime.min.time())

                    rbill =s.recurring_bill_number
                    ordrno =s.purchase_order_number
                    total = s.grand_total
                    paid=s.advanceAmount_paid
                    balance=s.balance
                    st=s.status
                    totalSales += float(s.grand_total)
                    totalbalance += float(s.balance)
                    if s.status == 'Draft':
                        st = 'Draft'
                    elif s.advanceAmount_paid == 0 and end_date>currentDate:
                        st = 'Not paid'
                        
                    elif s.advanceAmount_paid == s.grand_total:
                        st = 'fully paid'
                
                    elif s.advanceAmount_paid > 0 and s.advanceAmount_paid<s.grand_total and end_date>currentDate:
                        st = 'partially paid'
                    elif end_date<currentDate and s.advanceAmount_paid<=s.grand_total:
                        st = 'overdue'
                    
                    else:
                        st = s.status

                    details = {
                        'date': date,
                        'name': partyName,
                        'ship_date':ship_date,
                        'rbill':rbill,
                        'ordrno': ordrno,
                        'total':total,
                        'status':st,
                        'balance':balance,
                        
                        
                        
                    }
                    reportData.append(details)
                    totvendr=len(vendr)

                context = {'cmp': cmp, 'reportData': reportData,'totalbalance':totalbalance,'totalSales': totalSales, 'totcust': totvendr, 'startDate': startDate, 'endDate': endDate, 'status': status}
                template_path = 'company/reports/Fin_rec_bill_pdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'Report_rec_bill_Details'
                subject = f"Report_rec_bill_Details"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Report for - recbill Details. \n{email_message}\n\n--\nRegards,\n{cmp.Company_name}\n{cmp.Address}\n{cmp.State} - {cmp.Country}\n{cmp.Contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Report has been shared via email successfully..!')
                return redirect(Fin_recBill_report)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(Fin_recBill_report)
            
#End