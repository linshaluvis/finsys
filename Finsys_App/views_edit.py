    

def alltransactions(request):
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
        totMoneybal = 0
        totMoney = 0
        bill = Fin_Purchase_Bill.objects.filter(company=cmp)
        if bill:
            for s in bill:
                partyName = s.vendor.first_name +" "+s.vendor.last_name
                date = s.bill_date
                ref = s.bill_no
                type = 'Bill'
                total = s.grandtotal
                balance = s.balance
                paid = s.paid
                totMoney += float(s.grandtotal)
                totMoneybal+=float(s.balance)

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
        po = Fin_Purchase_Order.objects.filter(Company=cmp)
        if po:
            for s in po:
                partyName = s.Vendor.first_name +" "+s.Vendor.last_name
                date = s.purchase_order_date
                ref = s.purchase_order_no
                type = 'Purchase Order'
                total = s.grandtotal
                balance = s.balance
                paid = s.paid_off
                totMoney += float(s.grandtotal)
                totMoneybal+=float(s.balance)                

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
        recbill = Fin_Recurring_Bills.objects.filter(company=cmp)
        if recbill:
            for s in recbill:
                partyName = s.vendor.first_name +" "+s.vendor.last_name
                date = s.date
                ref = s.recurring_bill_number
                type = 'Recurring Bills'
                total = s.grand_total
                balance = s.balance
                paid = s.advanceAmount_paid
                totMoney += float(s.grand_total)
                totMoneybal+=float(s.balance)

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
        dbNote = Fin_Debit_Note.objects.filter(Company = cmp)
        if dbNote:
            for d in dbNote:
                partyName = d.Vendor.first_name +" "+d.Vendor.last_name
                date = d.debit_note_date
                ref = d.debit_note_number
                type = 'Debit Note'
                total = d.grandtotal
                paid =d.paid
                balance=d.balance
                totMoney += float(d.grandtotal)
                totMoneybal+=float(d.balance)

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
                totMoney += float(i.grandtotal)
                totMoneybal+=float(i.balance)
                
                

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
                totMoney += float(r.grandtotal)
                totMoneybal+=float(r.balance)


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
                totMoney += float(rt.Grand_total)
                totMoneybal+=float(rt.Balance)
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

        est = Fin_Estimate.objects.filter(Company=cmp)
        if est:
            for s in est:
                partyName = s.Customer.first_name +" "+s.Customer.last_name
                date = s.estimate_date
                ref = s.estimate_no
                type = 'Estimate'
                total = s.grandtotal
                balance = s.balance
                paid = 0
                totMoney += float(s.grandtotal)
                totMoneybal+=float(s.balance)

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
                totMoney += float(note.grandtotal)
                totMoneybal+=float(note.balance)
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
        sOrder = Fin_Sales_Order.objects.filter(Company=cmp)
        if sOrder:
            for s in sOrder:
                partyName = s.Customer.first_name +" "+s.Customer.last_name
                date = s.sales_order_date
                ref = s.sales_order_no
                type = 'Sales Order'
                total = s.grandtotal
                paid =s.paid_off
                balance=s.balance
                totMoney += float(s.grandtotal)
                totMoneybal+=float(s.balance)
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
                totMoney += float(s.amount)

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
                totMoney += float(s.grandtotal)
                totMoneybal+=float(s.balance)

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
            'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data, 'reportData':reportData,'startDate':None, 'endDate':None, 'totMoney':totMoney, 'totMoneybal':totMoneybal,}
        return render(request,'company/reports/Fin_alltransactions.html', context)
    else:
        return redirect('/')

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
            type = request.GET['status']
            if startDate == "":
                startDate = None
            if endDate == "":
                endDate = None
            reportData = []
            totMoneybal = 0
            totMoney = 0
            if type == 'all':
                bill = Fin_Purchase_Bill.objects.filter(company=cmp,bill_date__range = [startDate, endDate])
                if bill:
                    for s in bill:
                        partyName = s.vendor.first_name +" "+s.vendor.last_name
                        date = s.bill_date
                        ref = s.bill_no
                        type = 'Bill'
                        total = s.grandtotal
                        balance = s.balance
                        paid = s.paid
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)

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
                if po:
                    for s in po:
                        partyName = s.Vendor.first_name +" "+s.Vendor.last_name
                        date = s.purchase_order_date
                        ref = s.purchase_order_no
                        type = 'Purchase Order'
                        total = s.grandtotal
                        balance = s.balance
                        paid = s.paid_off
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)                

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
                if recbill:
                    for s in recbill:
                        partyName = s.vendor.first_name +" "+s.vendor.last_name
                        date = s.date
                        ref = s.recurring_bill_number
                        type = 'Recurring Bills'
                        total = s.grand_total
                        balance = s.balance
                        paid = s.advanceAmount_paid
                        totMoney += float(s.grand_total)
                        totMoneybal+=float(s.balance)

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
                if dbNote:
                    for d in dbNote:
                        partyName = d.Vendor.first_name +" "+d.Vendor.last_name
                        date = d.debit_note_date
                        ref = d.debit_note_number
                        type = 'Debit Note'
                        total = d.grandtotal
                        paid =d.paid
                        balance=d.balance
                        totMoney += float(d.grandtotal)
                        totMoneybal+=float(d.balance)

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
                if inv:
                    for i in inv:
                        partyName = i.Customer.first_name +" "+i.Customer.last_name
                        date = i.invoice_date
                        ref = i.invoice_no
                        type = 'Invoice'
                        total = i.grandtotal
                        paid =i.paid_off
                        balance=i.balance
                        totMoney += float(i.grandtotal)
                        totMoneybal+=float(i.balance)
                        
                        

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
                if recInv:
                    for r in recInv:
                        partyName = r.Customer.first_name +" "+r.Customer.last_name
                        date = r.start_date
                        ref = r.rec_invoice_no
                        type = 'Recurring Invoice'
                        total = r.grandtotal
                        paid =r.paid_off
                        balance=r.balance
                        totMoney += float(r.grandtotal)
                        totMoneybal+=float(r.balance)


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
                if rtInv:
                    for rt in rtInv:
                        partyName = rt.Customer.first_name +" "+rt.Customer.last_name
                        date = rt.Retainer_Invoice_date
                        ref = rt.Retainer_Invoice_number
                        type = 'Retainer Invoice'
                        total = rt.Grand_total
                        paid =rt.Paid_amount
                        balance=rt.Balance
                        totMoney += float(rt.Grand_total)
                        totMoneybal+=float(rt.Balance)
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
                if est:
                    for s in est:
                        partyName = s.Customer.first_name +" "+s.Customer.last_name
                        date = s.estimate_date
                        ref = s.estimate_no
                        type = 'Estimate'
                        total = s.grandtotal
                        balance = s.balance
                        paid = 0
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)

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
                if cNote:
                    for note in cNote:
                        partyName = note.Customer.first_name +" "+note.Customer.last_name
                        date = note.creditnote_date
                        ref = note.creditnote_number
                        type = 'Credit Note'
                        total = note.grandtotal
                        balance = note.balance
                        paid = note.paid
                        totMoney += float(note.grandtotal)
                        totMoneybal+=float(note.balance)
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
                sOrder = Fin_Sales_Order.objects.filter(Company=cmp,sales_order_date__range = [startDate, endDate])
                if sOrder:
                    for s in sOrder:
                        partyName = s.Customer.first_name +" "+s.Customer.last_name
                        date = s.sales_order_date
                        ref = s.sales_order_no
                        type = 'Sales Order'
                        total = s.grandtotal
                        paid =s.paid_off
                        balance=s.balance
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)
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
                pmade = Fin_PaymentMade.objects.filter(Company=cmp,payment_date__range = [startDate, endDate])
                if pmade:
                    for s in pmade:
                        partyName = s.vendor.first_name +" "+s.vendor.last_name
                        date = s.payment_date
                        ref = s.payment_number
                        type = 'Payment Made'
                        total = 0
                        paid =s.total_payment
                        balance=s.total_balance
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
                prec = Fin_Payment_Received.objects.filter(company=cmp,payment_date__range = [startDate, endDate])
                if prec:
                    for s in prec:
                        partyName = s.customer.first_name +" "+s.customer.last_name
                        date = s.payment_date
                        ref = s.payment_no
                        type = 'Payment Received'
                        total = s.total_amount
                        paid =s.total_payment
                        balance=s.total_balance
                    
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
                exp = Fin_Expense.objects.filter(Company=cmp,expense_date__range = [startDate, endDate])
                if exp:
                    for s in exp:
                        partyName = s.Vendor.first_name +" "+s.Vendor.last_name
                        date = s.expense_date
                        ref = s.expense_no
                        type = 'Expense'
                        total = s.amount
                        balance = 0
                        paid = 0
                        totMoney += float(s.amount)

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
                dcn = Fin_Delivery_Challan.objects.filter(Company=cmp,challan_date__range = [startDate, endDate])
                if dcn:
                    for s in dcn:
                        partyName = s.Customer.first_name +" "+s.Customer.last_name
                        date = s.challan_date
                        ref = s.challan_no
                        type = 'Delivery Challan'
                        total = s.grandtotal
                        balance = s.balance



                        paid = 0
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)

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
            
            bill = Fin_Purchase_Bill.objects.filter(company=cmp,bill_date__range = [startDate, endDate])
            
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
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)

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
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)
                        

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
                        totMoney += float(s.grand_total)
                        totMoneybal+=float(s.balance)

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
                        totMoney += float(d.grandtotal)
                        totMoneybal+=float(d.balance)


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
                        totMoney += float(i.grandtotal)
                        totMoneybal+=float(i.balance)

                        
                        

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
                        totMoney += float(r.grandtotal)
                        totMoneybal+=float(r.balance)



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
           
            if type == 'Retainer Invoices':
                if rtInv:
                    for rt in rtInv:
                        partyName = rt.Customer.first_name +" "+rt.Customer.last_name
                        date = rt.Retainer_Invoice_date
                        ref = rt.Retainer_Invoice_number
                        type = 'Retainer Invoice'
                        total = rt.Grand_total
                        paid =rt.Paid_amount
                        balance=rt.Balance
                        totMoney += float(rt.Grand_total)
                        totMoneybal+=float(rt.Balance)


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
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)

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
            
            if type == 'Credit Note':
                if cNote:
                    for note in cNote:
                        partyName = note.Customer.first_name +" "+note.Customer.last_name
                        date = note.creditnote_date
                        ref = note.creditnote_number
                        type = 'Credit Note'
                        total = note.grandtotal
                        balance = note.balance
                        paid = note.paid
                        totMoney += float(note.grandtotal)
                        totMoneybal+=float(note.balance)

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
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)
                        
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
            pmade = Fin_PaymentMade.objects.filter(Company=cmp,payment_date__range = [startDate, endDate])
            if type == 'Payment Made':
                if pmade:
                    for s in pmade:
                        partyName = s.vendor.first_name +" "+s.vendor.last_name
                        date = s.payment_date
                        ref = s.payment_number
                        type = 'Payment Made'
                        total = 0
                        paid =s.total_payment
                        balance=s.total_balance
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
            prec = Fin_Payment_Received.objects.filter(company=cmp,payment_date__range = [startDate, endDate])
            if type == 'Payment Received':
                if prec:
                    for s in prec:
                        partyName = s.customer.first_name +" "+s.customer.last_name
                        date = s.payment_date
                        ref = s.payment_no
                        type = 'Payment Received'
                        total = s.total_amount
                        paid =s.total_payment
                        balance=s.total_balance
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
            exp = Fin_Expense.objects.filter(Company=cmp,expense_date__range = [startDate, endDate])
            if type == 'Expense':

                if exp:
                    for s in exp:
                        partyName = s.Vendor.first_name +" "+s.Vendor.last_name
                        date = s.expense_date
                        ref = s.expense_no
                        type = 'Expense'
                        total = s.amount
                        balance = 0
                        paid = 0
                        totMoney += float(s.amount)

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
            dcn = Fin_Delivery_Challan.objects.filter(Company=cmp,challan_date__range = [startDate, endDate])
            if type == 'Delivery Challan':
                if dcn:
                    for s in dcn:
                        partyName = s.Customer.first_name +" "+s.Customer.last_name
                        date = s.challan_date
                        ref = s.challan_no
                        type = 'Delivery Challan'
                        total = s.grandtotal
                        balance = s.balance

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
                'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data, 'reportData':reportData, 'totMoney':totMoney, 'totMoneybal':totMoneybal,
                'startDate':startDate, 'endDate':endDate, 'currentDate':None,'status':type
            }
            return render(request,'company/reports/Fin_alltransactions.html', context)
    else:
        return redirect('/')

def Fin_alltransactionReportToEmail(request):
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
                type = request.POST['status']

                if startDate == "":
                    startDate = None
                if endDate == "":
                    endDate = None



                reportData = []
                totMoneybal = 0
                totMoney = 0
                bill = Fin_Purchase_Bill.objects.filter(company=cmp)
                if bill:
                    for s in bill:
                        partyName = s.vendor.first_name +" "+s.vendor.last_name
                        date = s.bill_date
                        ref = s.bill_no
                        type = 'Bill'
                        total = s.grandtotal
                        balance = s.balance
                        paid = s.paid
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)

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
                po = Fin_Purchase_Order.objects.filter(Company=cmp)
                if po:
                    for s in po:
                        partyName = s.Vendor.first_name +" "+s.Vendor.last_name
                        date = s.purchase_order_date
                        ref = s.purchase_order_no
                        type = 'Purchase Order'
                        total = s.grandtotal
                        balance = s.balance
                        paid = s.paid_off
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)                

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
                recbill = Fin_Recurring_Bills.objects.filter(company=cmp)
                if recbill:
                    for s in recbill:
                        partyName = s.vendor.first_name +" "+s.vendor.last_name
                        date = s.date
                        ref = s.recurring_bill_number
                        type = 'Recurring Bills'
                        total = s.grand_total
                        balance = s.balance
                        paid = s.advanceAmount_paid
                        totMoney += float(s.grand_total)
                        totMoneybal+=float(s.balance)

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
                dbNote = Fin_Debit_Note.objects.filter(Company = cmp)
                if dbNote:
                    for d in dbNote:
                        partyName = d.Vendor.first_name +" "+d.Vendor.last_name
                        date = d.debit_note_date
                        ref = d.debit_note_number
                        type = 'Debit Note'
                        total = d.grandtotal
                        paid =d.paid
                        balance=d.balance
                        totMoney += float(d.grandtotal)
                        totMoneybal+=float(d.balance)

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
                        totMoney += float(i.grandtotal)
                        totMoneybal+=float(i.balance)
                        
                        

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
                        totMoney += float(r.grandtotal)
                        totMoneybal+=float(r.balance)


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
                        totMoney += float(rt.Grand_total)
                        totMoneybal+=float(rt.Balance)
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

                est = Fin_Estimate.objects.filter(Company=cmp)
                if est:
                    for s in est:
                        partyName = s.Customer.first_name +" "+s.Customer.last_name
                        date = s.estimate_date
                        ref = s.estimate_no
                        type = 'Estimate'
                        total = s.grandtotal
                        balance = s.balance
                        paid = 0
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)

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
                        totMoney += float(note.grandtotal)
                        totMoneybal+=float(note.balance)
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
                sOrder = Fin_Sales_Order.objects.filter(Company=cmp)
                if sOrder:
                    for s in sOrder:
                        partyName = s.Customer.first_name +" "+s.Customer.last_name
                        date = s.sales_order_date
                        ref = s.sales_order_no
                        type = 'Sales Order'
                        total = s.grandtotal
                        paid =s.paid_off
                        balance=s.balance
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)
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
                        totMoney += float(s.amount)

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
                        totMoney += float(s.grandtotal)
                        totMoneybal+=float(s.balance)

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


           

                
                context = {'cmp':cmp, 'reportData':reportData, 'totMoney':totMoney, 'totMoneybal':totMoneybal}
                template_path = 'company/reports/Fin_alltransactions_pdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'Report_alltransactions'
                subject = f"Report_alltransactions"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Report for - alltransactions. \n{email_message}\n\n--\nRegards,\n{cmp.Company_name}\n{cmp.Address}\n{cmp.State} - {cmp.Country}\n{cmp.Contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Report has been shared via email successfully..!')
                return redirect(alltransactions)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(alltransactions)