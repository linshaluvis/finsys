def Fin_journel_report(request):
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
        totaldebit = 0
        totalcredit=0

        Jrn = Fin_Manual_Journal.objects.filter(Company=cmp)
        JrnAcc = Fin_Manual_Journal_Accounts.objects.filter(Company=cmp)
       
        if JrnAcc:
            for s in JrnAcc:
                date = s.Journal.journal_date 

                accname = s.Account.account_name
                debit = s.Journal.total_debit
                credit = s.Journal.total_credit

                ref = s.Journal.reference_no
                jounal =s.Journal.journal_no
                status=s.Journal.status
                totaldebit += float(s.Journal.total_debit)
                totalcredit += float(s.Journal.total_credit)

                
                    

                details = {
                    'date': date,
                    'name': accname,
                    'sales_no':ref,
                    'jounal':jounal,
                    'debit':debit,
                    'credit': credit,
                    'status': status,

                    
                }
                reportData.append(details)


        context = {
            'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data, 'reportData':reportData, 'totaldebit':totaldebit,'totalcredit':totalcredit,
            'startDate':None, 'endDate':None
        }
        return render(request,'company/reports/Fin_journal_report.html', context)
    else:
        return redirect('/')

def Fin_journalDetailsCustomized(request):
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
        

        if request.method == 'GET':
            startDate = request.GET['from_date']
            endDate = request.GET['to_date']
            status = request.GET['status']

            if startDate == "":
                startDate = None
            if endDate == "":
                endDate = None


            print(startDate)
            print(endDate)
            print(status)

            currentDate = datetime.today()

            reportData = []
            totaldebit = 0
            totalcredit=0

            Jrn = Fin_Manual_Journal.objects.filter(Company=cmp)
            JrnAcc = Fin_Manual_Journal_Accounts.objects.filter(Company=cmp)
        
            
            if startDate and endDate:
                JrnAcc = JrnAcc.filter(Journal__journal_date__range=[startDate, endDate])
                print("1")

            if status:
                if status == 'Draft':
                    JrnAcc = JrnAcc.filter(Journal__status = 'Draft')

                    print("2")
                
                elif status == 'Saved':
                    JrnAcc = JrnAcc.filter(Journal__status = 'Saved')

                    print("5")

            for s in JrnAcc:
                    date = s.Journal.journal_date 

                    accname = s.Account.account_name
                    debit = s.Journal.total_debit
                    credit = s.Journal.total_credit

                    ref = s.Journal.reference_no
                    jounal =s.Journal.journal_no
                    status=s.Journal.status
                    totaldebit += float(s.Journal.total_debit)
                    totalcredit += float(s.Journal.total_credit)

                
                    

                    details = {
                        'date': date,
                        'name': accname,
                        'sales_no':ref,
                        'jounal':jounal,
                        'debit':debit,
                        'credit': credit,
                        'status': status,

                        
                    }
                    reportData.append(details)


        context = {
            'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data, 'reportData':reportData, 'totaldebit':totaldebit,'totalcredit':totalcredit,
            'startDate':startDate, 'endDate':endDate,'status':status
        }
        print(status)
        return render(request,'company/reports/Fin_journal_report.html', context)
    else:
        return redirect('/')
    
def Fin_share_journalDetailsReportToEmail(request):
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


                print(startDate)
                print(endDate)
                print(status)

                currentDate = datetime.today()

                reportData = []
                totaldebit = 0
                totalcredit=0

                Jrn = Fin_Manual_Journal.objects.filter(Company=cmp)
                JrnAcc = Fin_Manual_Journal_Accounts.objects.filter(Company=cmp)
            
                
                if startDate and endDate:
                    JrnAcc = JrnAcc.filter(Journal__journal_date__range=[startDate, endDate])
                    print("1")

                if status:
                    if status == 'Draft':
                        JrnAcc = JrnAcc.filter(Journal__status = 'Draft')

                        print("2")
                    
                    elif status == 'Saved':
                        JrnAcc = JrnAcc.filter(Journal__status = 'Saved')

                        print("5")

                for s in JrnAcc:
                        date = s.Journal.journal_date 

                        accname = s.Account.account_name
                        debit = s.Journal.total_debit
                        credit = s.Journal.total_credit

                        ref = s.Journal.reference_no
                        jounal =s.Journal.journal_no
                        status=s.Journal.status
                        totaldebit += float(s.Journal.total_debit)
                        totalcredit += float(s.Journal.total_credit)

                
                    

                        details = {
                            'date': date,
                            'name': accname,
                            'sales_no':ref,
                            'jounal':jounal,
                            'debit':debit,
                            'credit': credit,
                            'status': status,

                            
                        }
                        reportData.append(details)


                context = { 'cmp':cmp, 'data':data, 'reportData':reportData, 'totaldebit':totaldebit,'totalcredit':totalcredit,
                    'startDate':startDate, 'endDate':endDate,'status':status
                }
                       
                template_path = 'company/reports/Fin_journal_Pdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'Report_journal_Details'
                subject = f"Report_journal_Details"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Report for - journal Details. \n{email_message}\n\n--\nRegards,\n{cmp.Company_name}\n{cmp.Address}\n{cmp.State} - {cmp.Country}\n{cmp.Contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Report has been shared via email successfully..!')
                return redirect(Fin_journel_report)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(Fin_journel_report)
            
#End