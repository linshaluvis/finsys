def Fin_AlltransactionsCustomized(request):
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
            status = request.GET['status']
            search_key = request.GET['searchkey']
            type = request.GET['types']
            print(startDate)
            print(endDate)
            print(status)
            print(search_key)
            print(type)



            if startDate == "":
                startDate = None
            if endDate == "":
                endDate = None


            reportData = []
            totMoneyIn = 0
            totMoneyOut = 0
            bill = Fin_Purchase_Bill.objects.filter(company=cmp,bill_date__range = [startDate, endDate])
            if status and status != 'all':
                if status == 'Party Name':
                    bill = bill.filter(vendor__first_name__icontains=search_key) | \
                            bill.filter(vendor__last_name__icontains=search_key)
                
                elif status == 'Total':
                    bill = bill.filter(grandtotal__icontains=search_key)
                elif status == 'Received':
                    bill = bill.filter(paid__icontains=search_key)
                    pass
                elif status == 'Balance':
                    bill = bill.filter(balance__icontains=search_key)
                    pass
            if type == 'Bill':

                if bill:
                    for s in bill:
                        partyName = s.vendor.first_name +" "+s.vendor.last_name
                        date = s.bill_date
                        ref = s.bill_no
                        type = 'Bill'
                        total = s.grandtotal
                        balance = s.balance
                        paid = s.paid
                        totMoneyOut += float(s.grandtotal)

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance
                        }
                    reportData.append(details)
            po = Fin_Purchase_Order.objects.filter(Company=cmp,purchase_order_date__range = [startDate, endDate])
            if status and status != 'all':
                if status == 'Party Name':
                    po = po.filter(Vendor__first_name__icontains=search_key) | \
                            po.filter(Vendor__last_name__icontains=search_key)
                elif status == 'Total':
                    po = po.filter(grandtotal__icontains=search_key)
                elif status == 'Received':
                    po = po.filter(paid_off__icontains=search_key)
                    pass
                elif status == 'Balance':
                    po = po.filter(balance__icontains=search_key)
                    pass
            if type == 'Purchase':
                if po:
                    for s in po:
                        partyName = s.Vendor.first_name +" "+s.Vendor.last_name
                        date = s.purchase_order_date
                        ref = s.purchase_order_no
                        type = 'Purchase Order'
                        total = s.grandtotal
                        balance = s.balance
                        paid = s.paid_off
                        totMoneyOut += float(s.grandtotal)
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance
                        }
                        reportData.append(details)
            recbill = Fin_Recurring_Bills.objects.filter(company=cmp,date__range = [startDate, endDate])
            if status and status != 'all':
                if status == 'Party Name':
                    recbill = recbill.filter(vendor__first_name__icontains=search_key) | \
                            recbill.filter(vendor__last_name__icontains=search_key)
                elif status == 'Total':
                    recbill = recbill.filter(grand_total__icontains=search_key)
                elif status == 'Received':
                    recbill = recbill.filter(paid_off__icontains=search_key)
                    pass
                elif status == 'Balance':
                    recbill = recbill.filter(balance__icontains=search_key)
                    pass
            if type == 'Recurring Bill':
                if recbill:
                    for s in recbill:
                        partyName = s.vendor.first_name +" "+s.vendor.last_name
                        date = s.date
                        ref = s.recurring_bill_number
                        type = 'Recurring Bills'
                        total = s.grand_total
                        balance = s.balance
                        paid = s.advanceAmount_paid
                        totMoneyOut += float(s.grand_total)

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance
                        }
                        reportData.append(details)
            dbNote = Fin_Debit_Note.objects.filter(Company = cmp,debit_note_date__range = [startDate, endDate])
            if status and status != 'all':
                if status == 'Party Name':
                    dbNote = dbNote.filter(Vendor__first_name__icontains=search_key) | \
                            dbNote.filter(Vendor__last_name__icontains=search_key)
                elif status == 'Total':
                    dbNote = dbNote.filter(grandtotal__icontains=search_key)
                elif status == 'Received':
                    dbNote = dbNote.filter(paid__icontains=search_key)
                    pass
                elif status == 'Balance':
                    dbNote = dbNote.filter(balance__icontains=search_key)
                    pass
            if type == 'Debit Note':
                if dbNote:
                    for d in dbNote:
                        partyName = d.Vendor.first_name +" "+d.Vendor.last_name
                        date = d.debit_note_date
                        ref = d.debit_note_number
                        type = 'Debit Note'
                        total = d.grandtotal
                        paid =d.paid
                        balance=d.balance
                        totMoneyIn += float(d.grandtotal)


                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance
                        }
                        reportData.append(details)
            inv = Fin_Invoice.objects.filter(Company = cmp,invoice_date__range = [startDate, endDate])
            if status and status != 'all':
                if status == 'Party Name':
                    inv = inv.filter(Customer__first_name__icontains=search_key) | \
                            inv.filter(Customer__last_name__icontains=search_key)
                elif status == 'Total':
                    inv = inv.filter(grandtotal__icontains=search_key)
                elif status == 'Received':
                    inv = inv.filter(paid_off__icontains=search_key)
                    pass
                elif status == 'Balance':
                    inv = inv.filter(balance__icontains=search_key)
                    pass
            if type == 'Invoice':
                if inv:
                    for i in inv:
                        partyName = i.Customer.first_name +" "+i.Customer.last_name
                        date = i.invoice_date
                        ref = i.invoice_no
                        type = 'Invoice'
                        total = i.grandtotal
                        paid =i.paid_off
                        balance=i.balance
                        totMoneyIn += float(i.grandtotal)

                        
                        

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance
                        }
                        reportData.append(details)

            recInv = Fin_Recurring_Invoice.objects.filter(Company = cmp,start_date__range = [startDate, endDate])
            if status and status != 'all':
                    if status == 'Party Name':
                        recInv = recInv.filter(Customer__first_name__icontains=search_key) | \
                                recInv.filter(Customer__last_name__icontains=search_key)
                    elif status == 'Total':
                        recInv = recInv.filter(grandtotal__icontains=search_key)
                    elif status == 'Received':
                        recInv = recInv.filter(paid_off__icontains=search_key)
                        pass
                    elif status == 'Balance':
                        recInv = recInv.filter(balance__icontains=search_key)
                        pass
            if type == 'Recurring Invoices':
                if recInv:
                    for r in recInv:
                        partyName = r.Customer.first_name +" "+r.Customer.last_name
                        date = r.start_date
                        ref = r.rec_invoice_no
                        type = 'Recurring Invoice'
                        total = r.grandtotal
                        paid =r.paid_off
                        balance=r.balance
                        totMoneyIn += float(r.grandtotal)


                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance
                        }
                        reportData.append(details)

            rtInv = Fin_Retainer_Invoice.objects.filter(Company = cmp,Retainer_Invoice_date__range = [startDate, endDate])
            if status and status != 'all':
                    if status == 'Party Name':
                        rtInv = rtInv.filter(Customer__first_name__icontains=search_key) | \
                                rtInv.filter(Customer__last_name__icontains=search_key)
                    elif status == 'Total':
                        rtInv = rtInv.filter(grandtotal__icontains=search_key)
                    elif status == 'Received':
                        rtInv = rtInv.filter(paid_off__icontains=search_key)
                        pass
                    elif status == 'Balance':
                        rtInv = rtInv.filter(balance__icontains=search_key)
                        pass
            if type == 'Retainer Invoices':
                if rtInv:
                    for rt in rtInv:
                        partyName = rt.Customer.first_name +" "+rt.Customer.last_name
                        date = rt.Retainer_Invoice_date
                        ref = rt.Retainer_Invoice_number
                        type = 'Retainer Invoice'
                        total = rt.grandtotal
                        paid =rt.paid_off
                        balance=rt.balance
                        totMoneyIn += float(rt.grandtotal)


                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance
                        }
                        reportData.append(details)

            est = Fin_Estimate.objects.filter(Company=cmp,estimate_date__range = [startDate, endDate])
            if status and status != 'all':
                    if status == 'Party Name':
                        est = est.filter(Customer__first_name__icontains=search_key) | \
                                est.filter(Customer__last_name__icontains=search_key)
                    elif status == 'Total':
                        est = est.filter(grandtotal__icontains=search_key)
                    elif status == 'Received':
                        est = est.filter(paid_off__icontains=search_key)
                        pass
                    elif status == 'Balance':
                        est = est.filter(balance__icontains=search_key)
                        pass
            if type == 'Estimate':

                if est:
                    for s in est:
                        partyName = s.Customer.first_name +" "+s.Customer.last_name
                        date = s.estimate_date
                        ref = s.estimate_no
                        type = 'Estimate'
                        total = s.grandtotal
                        balance = s.balance
                        paid = 0

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance
                        }
                        reportData.append(details)
            cNote = Fin_CreditNote.objects.filter(Company = cmp,creditnote_date__range = [startDate, endDate])
            if status and status != 'all':
                    if status == 'Party Name':
                        cNote = cNote.filter(Customer__first_name__icontains=search_key) | \
                                cNote.filter(Customer__last_name__icontains=search_key)
                    elif status == 'Total':
                        cNote = cNote.filter(grandtotal__icontains=search_key)
                    
            if type == 'Credit Note':
                if cNote:
                    for note in cNote:
                        partyName = note.Customer.first_name +" "+note.Customer.last_name
                        date = note.creditnote_date
                        ref = note.creditnote_number
                        type = 'Credit Note'
                        total = note.grandtotal
                        mOut = note.grandtotal
                        mIn = 0
                        totMoneyOut += float(note.grandtotal)

                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'moneyIn':mIn,
                            'moneyOut':mOut
                        }
                        reportData.append(details)
            sOrder = Fin_Sales_Order.objects.filter(Company=cmp,sales_order_date__range = [startDate, endDate])
            if status and status != 'all':
                    if status == 'Party Name':
                        est = est.filter(Customer__first_name__icontains=search_key) | \
                                est.filter(Customer__last_name__icontains=search_key)
                    elif status == 'Total':
                        est = est.filter(grandtotal__icontains=search_key)
                    elif status == 'Received':
                        est = est.filter(paid_off__icontains=search_key)
                        pass
                    elif status == 'Balance':
                        est = est.filter(balance__icontains=search_key)
                        pass
            if type == 'Sales Order':

                if sOrder:
                    for s in sOrder:
                        partyName = s.Customer.first_name +" "+s.Customer.last_name
                        date = s.sales_order_date
                        ref = s.sales_order_no
                        type = 'Sales Order'
                        total = s.grandtotal
                        paid =s.paid_off
                        balance=s.balance
                        totMoneyIn += float(s.grandtotal)
                        
                        details = {
                            'date': date,
                            'partyName': partyName,
                            'ref':ref,
                            'type':type,
                            'total':total,
                            'paid':paid,
                            'balance':balance
                        }
                        reportData.append(details)
        pmade = Fin_PaymentMade.objects.filter(Company=cmp)
        if pmade:
            for s in pmade:
                partyName = s.vendor.first_name +" "+s.vendor.last_name
                date = s.payment_date
                ref = s.payment_number
                type = 'Payment Made'
                total = 0
                paid =s.total_payment
                balance=s.total_balance
                totMoneyOut += float(s.total_payment)
                details = {
                    'date': date,
                    'partyName': partyName,
                    'ref':ref,
                    'type':type,
                    'total':total,
                    'paid':paid,
                    'balance':balance
                }
                reportData.append(details)
        prec = Fin_Payment_Received.objects.filter(company=cmp)
        if prec:
            for s in prec:
                partyName = s.customer.first_name +" "+s.customer.last_name
                date = s.payment_date
                ref = s.payment_no
                type = 'Payment Received'
                total = s.total_amount
                paid =s.total_payment
                balance=s.total_balance
                totMoneyIn += float(s.total_amount)
                details = {
                    'date': date,
                    'partyName': partyName,
                    'ref':ref,
                    'type':type,
                    'total':total,
                    'paid':paid,
                    'balance':balance
                }
                reportData.append(details)
        exp = Fin_Expense.objects.filter(Company=cmp)
        if exp:
            for s in exp:
                partyName = s.Vendor.first_name +" "+s.Vendor.last_name
                date = s.expense_date
                ref = s.expense_no
                type = 'Expense'
                total = s.amount
                balance = 0
                paid = 0

                details = {
                    'date': date,
                    'partyName': partyName,
                    'ref':ref,
                    'type':type,
                    'total':total,
                    'paid':paid,
                    'balance':balance
                }
                reportData.append(details)
        dcn = Fin_Delivery_Challan.objects.filter(Company=cmp)
        if dcn:
            for s in dcn:
                partyName = s.Customer.first_name +" "+s.Customer.last_name
                date = s.challan_date
                ref = s.challan_no
                type = 'Delivery Challan'
                total = s.grandtotal
                balance = s.balance
                paid = 0

                details = {
                    'date': date,
                    'partyName': partyName,
                    'ref':ref,
                    'type':type,
                    'total':total,
                    'paid':paid,
                    'balance':balance
                }
                reportData.append(details)
        

            


            context = {
                'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data, 'reportData':reportData, 'totalMoneyIn':totMoneyIn, 'totalMoneyOut':totMoneyOut,
                'startDate':startDate, 'endDate':endDate, 'currentDate':None
            }
            return render(request,'company/reports/Fin_alltransactions.html', context)
    else:
        return redirect('/')
