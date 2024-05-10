    
def gstr1(request):
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
        cNotedata = []


        inv = Fin_Invoice.objects.filter(Company = cmp)
        if inv:
            for i in inv:
                partyName = i.Customer.first_name +" "+i.Customer.last_name
                date = i.invoice_date
                ref = i.invoice_no
                type = 'Invoice'
                total = i.grandtotal
                paid =i.paid_off
                balance=i.balance
                gstin=i.gstin
                invoice_no=i.invoice_no
                igst=i.igst
                sgst=i.sgst
                cgst=i.cgst
                place_of_supply=i.place_of_supply
                subtotal=i.subtotal
                tax_amount=i.tax_amount

                
                
                

                details = {
                    'date': date,
                    'partyName': partyName,
                    'ref':ref,
                    'type':type,
                    'total':total,
                    'paid':paid,
                    'balance':balance,
                    'gstin':gstin,
                    'invoice_no':invoice_no,
                    'igst':igst,
                    'sgst':sgst,
                    'cgst':cgst,
                    'place_of_supply':place_of_supply,
                    'subtotal':subtotal,
                    'tax_amount':tax_amount,
                    
                }
                reportData.append(details)

        recInv = Fin_Recurring_Invoice.objects.filter(Company = cmp)
        if recInv:
            for r in recInv:
                partyName = r.Customer.first_name +" "+r.Customer.last_name
                date = r.start_date
                ref = r.rec_invoice_no
                type = 'Recurring Invoice'
                total = r.grandtotal
                paid =r.paid_off
                balance=r.balance
                gstin=r.gstin
                igst=r.igst
                sgst=r.sgst
                cgst=r.cgst
                place_of_supply=r.place_of_supply
                subtotal=r.subtotal
                tax_amount=r.tax_amount

                
                
                

                details = {
                    'date': date,
                    'partyName': partyName,
                    'ref':ref,
                    'type':type,
                    'total':total,
                    'paid':paid,
                    'balance':balance,
                    'gstin':gstin,
                    'igst':igst,
                    'sgst':sgst,
                    'cgst':cgst,
                    'place_of_supply':place_of_supply,
                    'subtotal':subtotal,
                    'tax_amount':tax_amount,
                    
                }
                reportData.append(details)
        rtInv = Fin_Retainer_Invoice.objects.filter(Company = cmp)
        if rtInv:
            for rt in rtInv:
                partyName = rt.Customer.first_name +" "+rt.Customer.last_name
                date = rt.Retainer_Invoice_date
                ref = rt.Retainer_Invoice_number
                type = 'Retainer Invoice'
                total = rt.Grand_total
                paid =rt.Paid_amount
                balance=rt.Balance
                gstin=rt.Customer_gstin
                igst=0
                sgst=0
                cgst=0
                place_of_supply=rt.Customer_place_of_supply
                subtotal=rt.Sub_total
                tax_amount=0

                
                
                

                details = {
                    'date': date,
                    'partyName': partyName,
                    'ref':ref,
                    'type':type,
                    'total':total,
                    'paid':paid,
                    'balance':balance,
                    'gstin':gstin,
                    'igst':igst,
                    'sgst':sgst,
                    'cgst':cgst,
                    'place_of_supply':place_of_supply,
                    'subtotal':subtotal,
                    'tax_amount':tax_amount
                    
                }
                reportData.append(details)
        cNote = Fin_CreditNote.objects.filter(Company = cmp)
        if cNote:
            for note in cNote:
                partyName = note.Customer.first_name +" "+note.Customer.last_name
                date = note.creditnote_date
                ref = note.creditnote_number
                type = 'Credit Note'
                total = note.grandtotal
                balance = note.balance
                paid = note.paid
                gstin=note.gstin
                igst=note.igst
                sgst=note.sgst
                cgst=note.cgst
                place_of_supply=note.place_of_supply
                subtotal=note.subtotal
                tax_amount=note.tax_amount
                invoice_number=note.invoice_number
                invoice_type=note.invoice_type
                details = {
                    'date': date,
                    'partyName': partyName,
                    'ref':ref,
                    'type':type,
                    'total':total,
                    'paid':paid,
                    'balance':balance,
                    'gstin':gstin,
                    'igst':igst,
                    'sgst':sgst,
                    'cgst':cgst,
                    'place_of_supply':place_of_supply,
                    'subtotal':subtotal,
                    'tax_amount':tax_amount,
                    'invoice_number':invoice_number,
                    'invoice_type':invoice_type
                    
                }
                cNotedata.append(details)
                        
                        
        context = {
            'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data,'reportData':reportData,'cNotedata':cNotedata}
        return render(request,'company/reports/Fin_gstr1.html', context)
    else:
        return redirect('/')



def Fin_gstr1Customized(request):
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

        if request.method == 'GET':
            startDate = request.GET['from_date']
            endDate = request.GET['to_date']
            type = request.GET['status']
            if startDate == "":
                startDate = None
            if endDate == "":
                endDate = None
            reportData = []
            cNotedata = []

            
            if type == 'all':


                inv = Fin_Invoice.objects.filter(Company = cmp,invoice_date__range = [startDate, endDate])
                if inv:
                    for i in inv:
                        partyName = i.Customer.first_name +" "+i.Customer.last_name
                        date = i.invoice_date
                        ref = i.invoice_no
                        type = 'Invoice'
                        total = i.grandtotal
                        paid =i.paid_off
                        balance=i.balance
                        gstin=i.gstin
                        invoice_no=i.invoice_no
                        igst=i.igst
                        sgst=i.sgst
                        cgst=i.cgst
                        place_of_supply=i.place_of_supply
                        subtotal=i.subtotal
                        tax_amount=i.tax_amount

                        
                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'invoice_no':invoice_no,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount,
                            
                        }
                        reportData.append(details)

                recInv = Fin_Recurring_Invoice.objects.filter(Company = cmp,start_date__range = [startDate, endDate])
                if recInv:
                    for r in recInv:
                        partyName = r.Customer.first_name +" "+r.Customer.last_name
                        date = r.start_date
                        ref = r.rec_invoice_no
                        type = 'Recurring Invoice'
                        total = r.grandtotal
                        paid =r.paid_off
                        balance=r.balance
                        gstin=r.gstin
                        igst=r.igst
                        sgst=r.sgst
                        cgst=r.cgst
                        place_of_supply=r.place_of_supply
                        subtotal=r.subtotal
                        tax_amount=r.tax_amount

                        
                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount,
                            
                        }
                        reportData.append(details)
                rtInv = Fin_Retainer_Invoice.objects.filter(Company = cmp,Retainer_Invoice_date__range = [startDate, endDate])
                if rtInv:
                    for rt in rtInv:
                        partyName = rt.Customer.first_name +" "+rt.Customer.last_name
                        date = rt.Retainer_Invoice_date
                        ref = rt.Retainer_Invoice_number
                        type = 'Retainer Invoice'
                        total = rt.Grand_total
                        paid =rt.Paid_amount
                        balance=rt.Balance
                        gstin=rt.Customer_gstin
                        igst=0
                        sgst=0
                        cgst=0
                        place_of_supply=rt.Customer_place_of_supply
                        subtotal=rt.Sub_total
                        tax_amount=0

                        
                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount
                            
                        }
                        reportData.append(details)
                cNote = Fin_CreditNote.objects.filter(Company = cmp,creditnote_date__range = [startDate, endDate])
                if cNote:
                    for note in cNote:
                        partyName = note.Customer.first_name +" "+note.Customer.last_name
                        date = note.creditnote_date
                        ref = note.creditnote_number
                        type = 'Credit Note'
                        total = note.grandtotal
                        balance = note.balance
                        paid = note.paid
                        gstin=note.gstin
                        igst=note.igst
                        sgst=note.sgst
                        cgst=note.cgst
                        place_of_supply=note.place_of_supply
                        subtotal=note.subtotal
                        tax_amount=note.tax_amount
                        invoice_number=note.invoice_number
                        invoice_type=note.invoice_type
                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount,
                            'invoice_number':invoice_number,
                            'invoice_type':invoice_type
                            
                        }
                        cNotedata.append(details)
                        
            if type == 'with GSTIN':


                inv = Fin_Invoice.objects.filter(Company = cmp,invoice_date__range = [startDate, endDate]).exclude(gstin='')
                

                if inv:
                    for i in inv:
                        partyName = i.Customer.first_name +" "+i.Customer.last_name
                        date = i.invoice_date
                        ref = i.invoice_no
                        type = 'Invoice'
                        total = i.grandtotal
                        paid =i.paid_off
                        balance=i.balance
                        gstin=i.gstin
                        invoice_no=i.invoice_no
                        igst=i.igst
                        sgst=i.sgst
                        cgst=i.cgst
                        place_of_supply=i.place_of_supply
                        subtotal=i.subtotal
                        tax_amount=i.tax_amount

                        
                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'invoice_no':invoice_no,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount,
                            
                        }
                        reportData.append(details)

                recInv = Fin_Recurring_Invoice.objects.filter(Company = cmp,start_date__range = [startDate, endDate]).exclude(gstin='')

                if recInv:
                    for r in recInv:
                        partyName = r.Customer.first_name +" "+r.Customer.last_name
                        date = r.start_date
                        ref = r.rec_invoice_no
                        type = 'Recurring Invoice'
                        total = r.grandtotal
                        paid =r.paid_off
                        balance=r.balance
                        gstin=r.gstin
                        igst=r.igst
                        sgst=r.sgst
                        cgst=r.cgst
                        place_of_supply=r.place_of_supply
                        subtotal=r.subtotal
                        tax_amount=r.tax_amount

                        
                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount,
                            
                        }
                        reportData.append(details)
                rtInv = Fin_Retainer_Invoice.objects.filter(Company = cmp,Retainer_Invoice_date__range = [startDate, endDate]).exclude(Customer_gstin='')

                if rtInv:
                    for rt in rtInv:
                        partyName = rt.Customer.first_name +" "+rt.Customer.last_name
                        date = rt.Retainer_Invoice_date
                        ref = rt.Retainer_Invoice_number
                        type = 'Retainer Invoice'
                        total = rt.Grand_total
                        paid =rt.Paid_amount
                        balance=rt.Balance
                        gstin=rt.Customer_gstin
                        igst=0
                        sgst=0
                        cgst=0
                        place_of_supply=rt.Customer_place_of_supply
                        subtotal=rt.Sub_total
                        tax_amount=0

                        
                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount
                            
                        }
                        reportData.append(details)
                cNote = Fin_CreditNote.objects.filter(Company=cmp, creditnote_date__range=[startDate, endDate]).exclude(gstin='')
                if cNote:
                    for note in cNote:
                        partyName = note.Customer.first_name +" "+note.Customer.last_name
                        date = note.creditnote_date
                        ref = note.creditnote_number
                        type = 'Credit Note'
                        total = note.grandtotal
                        balance = note.balance
                        paid = note.paid
                        gstin=note.gstin
                        igst=note.igst
                        sgst=note.sgst
                        cgst=note.cgst
                        place_of_supply=note.place_of_supply
                        subtotal=note.subtotal
                        tax_amount=note.tax_amount
                        invoice_number=note.invoice_number
                        invoice_type=note.invoice_type
                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount,
                            'invoice_number':invoice_number,
                            'invoice_type':invoice_type
                            
                        }
                        cNotedata.append(details)
            if type == 'without GSTIN':
                inv = Fin_Invoice.objects.filter(Company=cmp, invoice_date__range=[startDate, endDate], gstin__exact='')
                print(inv)
                print("ok")

                if inv:
                    for i in inv:
                        partyName = i.Customer.first_name +" "+i.Customer.last_name
                        date = i.invoice_date
                        ref = i.invoice_no
                        type = 'Invoice'
                        total = i.grandtotal
                        paid =i.paid_off
                        balance=i.balance
                        gstin=i.gstin
                        invoice_no=i.invoice_no
                        igst=i.igst
                        sgst=i.sgst
                        cgst=i.cgst
                        place_of_supply=i.place_of_supply
                        subtotal=i.subtotal
                        tax_amount=i.tax_amount

                        
                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'invoice_no':invoice_no,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount,
                            
                        }
                        reportData.append(details)

                recInv = Fin_Recurring_Invoice.objects.filter(Company = cmp,start_date__range = [startDate, endDate], gstin__exact='')
                for r in recInv:
                        partyName = r.Customer.first_name +" "+r.Customer.last_name
                        date = r.start_date
                        ref = r.rec_invoice_no
                        type = 'Recurring Invoice'
                        total = r.grandtotal
                        paid =r.paid_off
                        balance=r.balance
                        gstin=r.gstin
                        igst=r.igst
                        sgst=r.sgst
                        cgst=r.cgst
                        place_of_supply=r.place_of_supply
                        subtotal=r.subtotal
                        tax_amount=r.tax_amount

                        
                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount,
                            
                        }
                        reportData.append(details)
                rtInv = Fin_Retainer_Invoice.objects.filter(Company = cmp,Retainer_Invoice_date__range = [startDate, endDate], Customer_gstin__exact='')

                if rtInv:
                    for rt in rtInv:
                        partyName = rt.Customer.first_name +" "+rt.Customer.last_name
                        date = rt.Retainer_Invoice_date
                        ref = rt.Retainer_Invoice_number
                        type = 'Retainer Invoice'
                        total = rt.Grand_total
                        paid =rt.Paid_amount
                        balance=rt.Balance
                        gstin=rt.Customer_gstin
                        igst=0
                        sgst=0
                        cgst=0
                        place_of_supply=rt.Customer_place_of_supply
                        subtotal=rt.Sub_total
                        tax_amount=0

                        
                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount
                            
                        }
                        reportData.append(details)
                cNote = Fin_CreditNote.objects.filter(Company=cmp, creditnote_date__range=[startDate, endDate], gstin__exact='')


                if cNote:
                    for note in cNote:
                        partyName = note.Customer.first_name +" "+note.Customer.last_name
                        date = note.creditnote_date
                        ref = note.creditnote_number
                        type = 'Credit Note'
                        total = note.grandtotal
                        balance = note.balance
                        paid = note.paid
                        gstin=note.gstin
                        igst=note.igst
                        sgst=note.sgst
                        cgst=note.cgst
                        place_of_supply=note.place_of_supply
                        subtotal=note.subtotal
                        tax_amount=note.tax_amount
                        invoice_number=note.invoice_number
                        invoice_type=note.invoice_type
                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount,
                            'invoice_number':invoice_number,
                            'invoice_type':invoice_type
                            
                        }
                        cNotedata.append(details)
                
            
            

            


            context = {
                'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data, 'reportData':reportData,'cNotedata':cNotedata ,
                'startDate':startDate, 'endDate':endDate, 'currentDate':None,'status':type
            }
            return render(request,'company/reports/Fin_gstr1.html', context)
    else:
        return redirect('/')
     
def Fin_shareGSTR1ReportToEmail(request):
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
                
                startDate = request.POST['start']
                endDate = request.POST['end']
                if startDate == "":
                    startDate = None
                if endDate == "":
                    endDate = None
            


                reportData = []
                cNotedata=[]
               

                
       
        
             
                

                inv = Fin_Invoice.objects.filter(Company = cmp)
                if inv:
                    for i in inv:
                        partyName = i.Customer.first_name +" "+i.Customer.last_name
                        date = i.invoice_date
                        ref = i.invoice_no
                        type = 'Invoice'
                        total = i.grandtotal
                        paid =i.paid_off
                        balance=i.balance
                        gstin=i.gstin
                        invoice_no=i.invoice_no
                        igst=i.igst
                        sgst=i.sgst
                        cgst=i.cgst
                        place_of_supply=i.place_of_supply
                        subtotal=i.subtotal
                        tax_amount=i.tax_amount

                        
                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'invoice_no':invoice_no,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount,
                            
                        }
                        reportData.append(details)

                recInv = Fin_Recurring_Invoice.objects.filter(Company = cmp)
                if recInv:
                    for r in recInv:
                        partyName = r.Customer.first_name +" "+r.Customer.last_name
                        date = r.start_date
                        ref = r.rec_invoice_no
                        type = 'Recurring Invoice'
                        total = r.grandtotal
                        paid =r.paid_off
                        balance=r.balance
                        gstin=r.gstin
                        igst=r.igst
                        sgst=r.sgst
                        cgst=r.cgst
                        place_of_supply=r.place_of_supply
                        subtotal=r.subtotal
                        tax_amount=r.tax_amount

                        
                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount,
                            
                        }
                        reportData.append(details)
                rtInv = Fin_Retainer_Invoice.objects.filter(Company = cmp)
                if rtInv:
                    for rt in rtInv:
                        partyName = rt.Customer.first_name +" "+rt.Customer.last_name
                        date = rt.Retainer_Invoice_date
                        ref = rt.Retainer_Invoice_number
                        type = 'Retainer Invoice'
                        total = rt.Grand_total
                        paid =rt.Paid_amount
                        balance=rt.Balance
                        gstin=rt.Customer_gstin
                        igst=0
                        sgst=0
                        cgst=0
                        place_of_supply=rt.Customer_place_of_supply
                        subtotal=rt.Sub_total
                        tax_amount=0

                        
                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount
                            
                        }
                        reportData.append(details)
                cNote = Fin_CreditNote.objects.filter(Company = cmp)
                if cNote:
                    for note in cNote:
                        partyName = note.Customer.first_name +" "+note.Customer.last_name
                        date = note.creditnote_date
                        ref = note.creditnote_number
                        type = 'Credit Note'
                        total = note.grandtotal
                        balance = note.balance
                        paid = note.paid
                        gstin=note.gstin
                        igst=note.igst
                        sgst=note.sgst
                        cgst=note.cgst
                        place_of_supply=note.place_of_supply
                        subtotal=note.subtotal
                        tax_amount=note.tax_amount
                        invoice_number=note.invoice_number
                        invoice_type=note.invoice_type
                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance,
                            'gstin':gstin,
                            'igst':igst,
                            'sgst':sgst,
                            'cgst':cgst,
                            'place_of_supply':place_of_supply,
                            'subtotal':subtotal,
                            'tax_amount':tax_amount,
                            'invoice_number':invoice_number,
                            'invoice_type':invoice_type
                            
                        }
                        cNotedata.append(details)
                            
                
                

                


                context = {
                   'cmp':cmp, 'data':data, 'reportData':reportData,'cNotedata':cNotedata , 'startDate':startDate, 'endDate':endDate }

                template_path = 'company/reports/Fin_GSTR1_pdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'Report_GSTR1'
                subject = f"Report_GSTR1"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Report for - GSTR1. \n{email_message}\n\n--\nRegards,\n{cmp.Company_name}\n{cmp.Address}\n{cmp.State} - {cmp.Country}\n{cmp.Contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Report has been shared via email successfully..!')
                return redirect(gstr1)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(gstr1)
            
#End