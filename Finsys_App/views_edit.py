
def Fin_recInvoice_report(request):
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
        totalbalance=0

        Recinv = Fin_Recurring_Invoice.objects.filter(Company=cmp)
        cust = Fin_Customers.objects.filter(Company=cmp)
       
        if Recinv:
            for s in Recinv:
                partyName = s.Customer.first_name +" "+s.Customer.last_name
                date = s.start_date
                ship_date = s.end_date
                end_date = datetime.combine(s.end_date, datetime.min.time())

                ref = s.reference_no
                rinv =s.rec_invoice_no
                total = s.grandtotal
                salesno=s.salesOrder_no
                paid=s.paid_off
                balance=s.balance
                sta=s.status
                invoice_no=0
                totalSales += float(s.grandtotal)
                totalbalance += float(s.balance)
                if s.status == 'Draft':
                    st = 'Draft'
                elif s.paid_off == 0 :
                    st = 'Not paid'
                    
                elif s.paid_off == s.grandtotal:
                    st = 'fully paid'
                
                elif s.paid_off > 0 and s.paid_off<s.grandtotal and end_date>currentDate:
                    st = 'partially paid'
                elif end_date<currentDate and s.paid_off<=s.grandtotal:
                    st = 'overdue'
                
                else:
                    st = s.status

                details = {
                    'date': date,
                    'name': partyName,
                    'sales_no':salesno,
                    'ship_date':ship_date,
                    'rinv':rinv,
                    'invoice_no': invoice_no,
                    'total':total,
                    'status':st,
                    'balance':balance,
                    
                    
                    
                }
                reportData.append(details)
                totcust=len(cust)


        context = {
            'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data, 'reportData':reportData,'totalbalance':totalbalance, 'totalSales':totalSales,'totcust':totcust,
            'startDate':None, 'endDate':None
        }
        return render(request,'company/reports/Fin_rec_invoice_report.html', context)
    else:
        return redirect('/')
from django.db.models import Q

def Fin_recinvCustomized(request):
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

        startDate = request.GET.get('start_date', None)
        endDate = request.GET.get('end_date', None)
        status = request.GET.get('status')
        print(startDate)
        print(endDate)
        print(status)



        currentDate = datetime.today()

        reportData = []
        totalSales = 0
        totcust = len(cust)
        totalbalance = 0

        Recinv = Fin_Recurring_Invoice.objects.filter(Company=cmp)
        
        if startDate and endDate:
            Recinv = Recinv.filter(start_date__range=[startDate, endDate])
            print("1")

        if status:
            if status == 'Draft':
                Recinv = Recinv.filter(status = 'Draft')
                print("2")
            elif status == 'fully paid':
                Recinv = Recinv.filter(paid_off=F('grandtotal'),status='saved')
                print("2")

            elif status == 'overdue':
                Recinv = Recinv.filter(Q(end_date__lt=currentDate) & Q(paid_off__lt=F('grandtotal')),status='saved')
                print("3")

            elif status == 'Not paid':
                Recinv = Recinv.filter(paid_off=0, status='saved')
                print("4")

            elif status == 'partially paid':
                Recinv = Recinv.filter(Q(paid_off__gt=0)  & Q(paid_off__lt=F('grandtotal')),status='saved')
                print(Recinv)
                print("5")

        for s in Recinv:
            partyName = s.Customer.first_name + " " + s.Customer.last_name
            date = s.start_date
            ship_date = s.end_date
            end_date = datetime.combine(s.end_date, datetime.min.time())

            ref = s.reference_no
            rinv = s.rec_invoice_no
            total = s.grandtotal
            salesno = s.salesOrder_no
            paid = s.paid_off
            balance = s.balance
            sta = s.status
            invoice_no = 0
            totalSales += float(s.grandtotal)
            totalbalance += float(s.balance)
            if s.status == 'Draft':
                st = 'Draft'
            elif s.paid_off == 0 and end_date>currentDate:
                st = 'Not paid'
            elif s.paid_off == s.grandtotal:
                st = 'fully paid'
            elif s.paid_off > 0 and s.paid_off < s.grandtotal and end_date>currentDate:
                st = 'partially paid'
            elif end_date < currentDate and s.paid_off <= s.grandtotal:
                st = 'overdue'
            else:
                st = s.status

            details = {
                'date': date,
                'name': partyName,
                'sales_no': salesno,
                'ship_date': ship_date,
                'rinv': rinv,
                'invoice_no': invoice_no,
                'total': total,
                'status': st,
                'balance': balance,
            }
            reportData.append(details)

        context = {
            'allmodules': allmodules, 'com': com, 'cmp': cmp, 'data': data, 'reportData': reportData,'totalbalance':totalbalance,
            'totalSales': totalSales, 'totcust': totcust, 'startDate': startDate, 'endDate': endDate, 'status': status
        }
        return render(request, 'company/reports/Fin_rec_invoice_report.html', context)
    else:
        return redirect('/')


def Fin_shareREC_INVOICEDetailsReportToEmail(request):
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

                
                print(startDate)
                print(endDate)
                print(status)



                currentDate = datetime.today()

                reportData = []
                totalSales = 0
                totcust = len(cust)
                totalbalance = 0

                Recinv = Fin_Recurring_Invoice.objects.filter(Company=cmp)
                
                if startDate and endDate:
                    Recinv = Recinv.filter(start_date__range=[startDate, endDate])
                    print("1")

                if status:
                    if status == 'Draft':
                        Recinv = Recinv.filter(status = 'Draft')
                        print("2")
                    elif status == 'fully paid':
                        Recinv = Recinv.filter(paid_off=F('grandtotal'),status='saved')
                        print("2")

                    elif status == 'overdue':
                        Recinv = Recinv.filter(Q(end_date__lt=currentDate) & Q(paid_off__lt=F('grandtotal')),status='saved')
                        print("3")

                    elif status == 'Not paid':
                        Recinv = Recinv.filter(paid_off=0, status='saved')
                        print("4")

                    elif status == 'partially paid':
                        Recinv = Recinv.filter(Q(paid_off__gt=0) & Q(paid_off__lt=F('grandtotal')),status='saved')
                        print("5")

                for s in Recinv:
                    partyName = s.Customer.first_name + " " + s.Customer.last_name
                    date = s.start_date
                    ship_date = s.end_date
                    end_date = datetime.combine(s.end_date, datetime.min.time())

                    ref = s.reference_no
                    rinv = s.rec_invoice_no
                    total = s.grandtotal
                    salesno = s.salesOrder_no
                    paid = s.paid_off
                    balance = s.balance
                    sta = s.status
                    invoice_no = 0
                    totalSales += float(s.grandtotal)
                    totalbalance += float(s.balance)
                    if s.status == 'Draft':
                        st = 'Draft'
                    elif s.paid_off == 0 and end_date>currentDate:
                        st = 'Not paid'
                    elif s.paid_off == s.grandtotal:
                        st = 'fully paid'
                    elif s.paid_off > 0 and s.paid_off < s.grandtotal and end_date>currentDate:
                        st = 'partially paid'
                    elif end_date < currentDate and s.paid_off <= s.grandtotal:
                        st = 'overdue'
                    else:
                        st = s.status

                    details = {
                        'date': date,
                        'name': partyName,
                        'sales_no': salesno,
                        'ship_date': ship_date,
                        'rinv': rinv,
                        'invoice_no': invoice_no,
                        'total': total,
                        'status': st,
                        'balance': balance,
                    }
                    reportData.append(details)

                    totcust=len(cust)
                
                context = {'cmp':cmp, 'reportData':reportData, 'totalSales':totalSales,'totcust':totcust, 'startDate':startDate,'totalbalance':totalbalance, 'endDate':endDate}
                template_path = 'company/reports/Fin_rec_invoice_pdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'Report_rec_invoice_Details'
                subject = f"Report_rec_invoice_Details"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Report for - Sales Order Details. \n{email_message}\n\n--\nRegards,\n{cmp.Company_name}\n{cmp.Address}\n{cmp.State} - {cmp.Country}\n{cmp.Contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Report has been shared via email successfully..!')
                return redirect(Fin_recInvoice_report)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(Fin_recInvoice_report)
            
#End
    