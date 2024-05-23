
def Fin_trial_balance(request):
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
        totbankbal=0
        totalExpense=0
        totMoneybalLOAN = 0
        totMoneybalEMPLOAN=0
        TOTITEMAMT=0
        venders_data = []
        total_balance1 = 0 
        customers_data = []
        total_balance11 = 0
        Totpurchasediscount=0
        Totsalediscount=0
        
        trans = Fin_BankTransactions.objects.filter(company=cmp)
        exp = Fin_Expense.objects.filter(Company=cmp)
        loan = loan_account.objects.filter(company = cmp)
        EMPloan = Fin_Loan.objects.filter(company_id=cmp)
        items = Fin_Items.objects.filter(Company = cmp)
        vend = Fin_Vendors.objects.filter(Company=cmp)
        cust = Fin_Customers.objects.filter(Company=cmp)
        customer = Fin_Customers.objects.filter(Company=cmp)
        vendor = Fin_Vendors.objects.filter(Company=cmp)
        

        for i in customer:
            fullname = i.first_name + ' ' + i.last_name
            invoice = Fin_Invoice.objects.filter(Company=cmp,Customer=i)
            
            if invoice:
                for inv in invoice:
                    invitems = Fin_Invoice_Items.objects.filter(Invoice=inv)
                    invdiscount = 0
                    for dis in invitems:
                        Totsalediscount += float(dis.discount)
                   
            
            rec_invoice = Fin_Recurring_Invoice.objects.filter(Company=cmp,Customer=i)
            
            if rec_invoice:
                for rec in rec_invoice:
                    recitems = Fin_Recurring_Invoice_Items.objects.filter(RecInvoice=rec)
                    recdiscount = 0
                    for dis in recitems:
                        Totsalediscount +=float(dis.discount)
                    
            ret_invoice = Fin_Retainer_Invoice.objects.filter(Company=cmp,Customer=i)
            
            if ret_invoice:
                for ret in ret_invoice:
                    retitems = Fin_Retainer_Invoice_Items.objects.filter(Ret_Inv=ret)
                    retdiscount = 0
                    for dis in retitems:
                        Totsalediscount += float(dis.discount)
        
            
        
        for i in vendor:
            fullname2 = i.first_name + ' ' + i.last_name
            bill = Fin_Purchase_Bill.objects.filter(company=cmp,vendor=i)
            
            if bill:
                for b in bill:
                    billitems = Fin_Purchase_Bill_Item.objects.filter(pbill=b)
                    billdiscount = 0
                    for dis in billitems:
                        Totpurchasediscount += float(dis.discount)
                        print(Totpurchasediscount)
                    

            recbill = Fin_Recurring_Bills.objects.filter(company=cmp,vendor=i)
            
            if recbill:
                for rb in recbill:
                    recbillitems = Fin_Recurring_Bill_Items.objects.filter(recurring_bill=rb)
                    recbilldiscountf = 0
                    for dis in recbillitems:
                        Totpurchasediscount += float(dis.discount)
                        print(Totpurchasediscount)
                        
            
                   

        

 



            
        for i in trans:
            balance = i.current_balance
            totbankbal += float(i.current_balance)
        if exp:
            for ex in exp:
                totalExpense += float(ex.amount)
        if loan:
            for s in loan:  
                balance = s.balance
                totMoneybalLOAN+=float(s.balance)
        if EMPloan:
            for s in EMPloan:    
                balance = s.balance
                loan_amount=s.loan_amount
                totMoneybalEMPLOAN+=float(s.balance) 
        for i in items:   
            name = i.name
            bQty = int(i.opening_stock)   
            pAmt = i.purchase_price
            totamt=bQty*pAmt
            TOTITEMAMT+=totamt
  

        # Initialize total balance outside the loop
        for vendr in vend:
            vendrName = vendr.first_name +" "+vendr.last_name

            PurchaseBill = Fin_Purchase_Bill.objects.filter(vendor=vendr, status='Save')
            Recurring_Bills = Fin_Recurring_Bills.objects.filter(vendor=vendr, status='Save')
            Debit_Note = Fin_Debit_Note.objects.filter(Vendor=vendr, status='Saved')
            
            bill_balance = sum(float(inv.balance) for inv in PurchaseBill)
            recurring_bill_balance = sum(float(rec_inv.balance) for rec_inv in Recurring_Bills)
            total_bill_balance = bill_balance + recurring_bill_balance
            available_debits = sum(float(credit_note.balance) for credit_note in Debit_Note)
            total_balance = total_bill_balance - available_debits            
            # Update the total balance
            total_balance1 += total_balance
            venders_data.append({
                'name': vendrName,                
                'total_balance': total_balance,
            })
        
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
            total_balance11 += total_balance

            customers_data.append({
                'name': customerName,                
                'total_balance': total_balance,
            })
        inv = Fin_Invoice.objects.filter(Company = cmp)
        crdNt = Fin_CreditNote.objects.filter(Company = cmp)
        recInv = Fin_Recurring_Invoice.objects.filter(Company = cmp)
        sordr= Fin_Sales_Order.objects.filter(Company = cmp)
        rtInv= Fin_Retainer_Invoice.objects.filter(Company = cmp)
        bill= Fin_Purchase_Bill.objects.filter(company = cmp)
        rcrbl= Fin_Recurring_Bills.objects.filter(company = cmp)
        pordr= Fin_Purchase_Order.objects.filter(Company = cmp)
        dbtnt= Fin_Debit_Note.objects.filter(Company = cmp)
        totCashIn=0
        totCashOut=0
        totCashOutpr=0
        totCashIndbt=0
        if inv:
            for i in inv:
                balance=i.balance
                totCashIn += float(i.balance)  

        if crdNt:
            for cr in crdNt:
                balance = cr.balance
                totCashOut += float(cr.balance)


        if recInv:
            for rc in recInv:
                balance = rc.balance                
                totCashIn += float(rc.balance)
        if sordr:
            for so in sordr:
                balance = so.balance      
                totCashIn += float(so.balance)
        if rtInv:
            for rt in rtInv:
                totCashIn += float(rt.Balance)
        if bill:
            for bl in bill:
                balance = bl.balance
                totCashOutpr += float(bl.balance)

        if rcrbl:
            for rb in rcrbl:
                balance = rb.balance
                totCashOutpr += float(rb.balance)

        if pordr:
            for po in pordr:
                balance = po.balance
                totCashOutpr += float(po.balance)

        if dbtnt:
            for db in dbtnt:
                balance = db.balance
                totCashIndbt += float(db.balance)
                print(totCashIndbt)

        context = {
            'cust':cust,
            'totCashOutsale':totCashOut,
            'totCashInsale':totCashIn,
            'totCashOutpr':totCashOutpr,
            'totCashIndbt':totCashIndbt,
            'cust': customers_data,
            'customers': venders_data,
            'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data,'startDate':None, 'endDate':None,
            'loan':totMoneybalLOAN,
            'Itemstock':TOTITEMAMT,
            'emploan':totMoneybalEMPLOAN,
            'total_CUSTbalance':total_balance11,
            'total_VENDORbalance':total_balance1,
            'totalExpense':totalExpense,
            'totbankbal':totbankbal,
            'Totpurchasediscount':Totpurchasediscount,
            'Totsalediscount':Totsalediscount,

        
            }
        return render(request,'company/reports/trialbalance.html', context)
    else:
        return redirect('/')
    
def Fin_trial_balancecustomized(request):
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
        startDate = request.GET.get('from_date', None)
        endDate = request.GET.get('to_date', None)
        print(startDate)
        print(endDate)
        totbankbal=0
        totalExpense=0
        totMoneybalLOAN = 0
        totMoneybalEMPLOAN=0
        TOTITEMAMT=0
        venders_data = []
        total_balance1 = 0 
        customers_data = []
        total_balance11 = 0
        Totpurchasediscount=0
        Totsalediscount=0

        if startDate is None or endDate is None:
            cash = Fin_CashInHand.objects.filter(Company = cmp)
            trans = Fin_BankTransactions.objects.filter(company=cmp)
            exp = Fin_Expense.objects.filter(Company=cmp)
            loan = loan_account.objects.filter(company = cmp)
            EMPloan = Fin_Loan.objects.filter(company_id=cmp)
            items = Fin_Items.objects.filter(Company = cmp)
            vend = Fin_Vendors.objects.filter(Company=cmp)
            cust = Fin_Customers.objects.filter(Company=cmp)
            customer = Fin_Customers.objects.filter(Company=cmp)
            vendor = Fin_Vendors.objects.filter(Company=cmp)
            

            for i in customer:
                fullname = i.first_name + ' ' + i.last_name
                invoice = Fin_Invoice.objects.filter(Company=cmp,Customer=i)
                
                if invoice:
                    for inv in invoice:
                        invitems = Fin_Invoice_Items.objects.filter(Invoice=inv)
                        for dis in invitems:
                            Totsalediscount += float(dis.discount)
                    
                
                rec_invoice = Fin_Recurring_Invoice.objects.filter(Company=cmp,Customer=i)
                
                if rec_invoice:
                    for rec in rec_invoice:
                        recitems = Fin_Recurring_Invoice_Items.objects.filter(RecInvoice=rec)
                        for dis in recitems:
                            Totsalediscount +=float(dis.discount)
                        
                ret_invoice = Fin_Retainer_Invoice.objects.filter(Company=cmp,Customer=i)
                
                if ret_invoice:
                    for ret in ret_invoice:
                        retitems = Fin_Retainer_Invoice_Items.objects.filter(Ret_Inv=ret)
                        for dis in retitems:
                            Totsalediscount += float(dis.discount)
            
                
            
            for i in vendor:
                fullname2 = i.first_name + ' ' + i.last_name
                bill = Fin_Purchase_Bill.objects.filter(company=cmp,vendor=i)
                
                if bill:
                    for b in bill:
                        billitems = Fin_Purchase_Bill_Item.objects.filter(pbill=b)
                        for dis in billitems:
                            Totpurchasediscount += float(dis.discount)
                            print(Totpurchasediscount)
                        

                recbill = Fin_Recurring_Bills.objects.filter(company=cmp,vendor=i)
                
                if recbill:
                    for rb in recbill:
                        recbillitems = Fin_Recurring_Bill_Items.objects.filter(recurring_bill=rb)
                        for dis in recbillitems:
                            Totpurchasediscount += float(dis.discount)
                            print(Totpurchasediscount)
                            
                


    



                
            for i in trans:
                balance = i.current_balance
                totbankbal += float(i.current_balance)
            if exp:
                for ex in exp:
                    totalExpense += float(ex.amount)
            if loan:
                for s in loan:  
                    balance = s.balance
                    totMoneybalLOAN+=float(s.balance)
            if EMPloan:
                for s in EMPloan:    
                    balance = s.balance
                    loan_amount=s.loan_amount
                    totMoneybalEMPLOAN+=float(s.balance) 
            for i in items:   
                name = i.name
                bQty = int(i.opening_stock)   
                pAmt = i.purchase_price
                totamt=bQty*pAmt
                TOTITEMAMT+=totamt
    

            # Initialize total balance outside the loop
            for vendr in vend:
                vendrName = vendr.first_name +" "+vendr.last_name

                PurchaseBill = Fin_Purchase_Bill.objects.filter(vendor=vendr, status='Save')
                Recurring_Bills = Fin_Recurring_Bills.objects.filter(vendor=vendr, status='Save')
                Debit_Note = Fin_Debit_Note.objects.filter(Vendor=vendr, status='Saved')
                
                bill_balance = sum(float(inv.balance) for inv in PurchaseBill)
                recurring_bill_balance = sum(float(rec_inv.balance) for rec_inv in Recurring_Bills)
                total_bill_balance = bill_balance + recurring_bill_balance
                available_debits = sum(float(credit_note.balance) for credit_note in Debit_Note)
                total_balance = total_bill_balance - available_debits            
                # Update the total balance
                total_balance1 += total_balance
                venders_data.append({
                    'name': vendrName,                
                    'total_balance': total_balance,
                })
            
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
                total_balance11 += total_balance

                customers_data.append({
                    'name': customerName,                
                    'total_balance': total_balance,
                })
            inv = Fin_Invoice.objects.filter(Company = cmp)
            crdNt = Fin_CreditNote.objects.filter(Company = cmp)
            recInv = Fin_Recurring_Invoice.objects.filter(Company = cmp)
            sordr= Fin_Sales_Order.objects.filter(Company = cmp)
            rtInv= Fin_Retainer_Invoice.objects.filter(Company = cmp)
            bill= Fin_Purchase_Bill.objects.filter(company = cmp)
            rcrbl= Fin_Recurring_Bills.objects.filter(company = cmp)
            pordr= Fin_Purchase_Order.objects.filter(Company = cmp)
            dbtnt= Fin_Debit_Note.objects.filter(Company = cmp)
            totCashIn=0
            totCashOut=0
            totCashOutpr=0
            totCashIndbt=0
            if inv:
                for i in inv:
                    balance=i.balance
                    totCashIn += float(i.balance)  

            if crdNt:
                for cr in crdNt:
                    balance = cr.balance
                    totCashOut += float(cr.balance)


            if recInv:
                for rc in recInv:
                    balance = rc.balance                
                    totCashIn += float(rc.balance)
            if sordr:
                for so in sordr:
                    balance = so.balance      
                    totCashIn += float(so.balance)
            if rtInv:
                for rt in rtInv:
                    totCashIn += float(rt.Balance)
            if bill:
                for bl in bill:
                    balance = bl.balance
                    totCashOutpr += float(bl.balance)

            if rcrbl:
                for rb in rcrbl:
                    balance = rb.balance
                    totCashOutpr += float(rb.balance)

            if pordr:
                for po in pordr:
                    balance = po.balance
                    totCashOutpr += float(po.balance)

            if dbtnt:
                for db in dbtnt:
                    balance = db.balance
                    totCashIndbt += float(db.balance)
                    print(totCashIndbt)

        else:
            trans = Fin_BankTransactions.objects.filter(company=cmp,adjustment_date__range = [startDate, endDate])
            exp = Fin_Expense.objects.filter(Company=cmp,expense_date__range = [startDate, endDate])
            loan = loan_account.objects.filter(company = cmp,date__range = [startDate, endDate])
            EMPloan = Fin_Loan.objects.filter(company_id=cmp,loan_date__range = [startDate, endDate])
            items = Fin_Items.objects.filter(Company = cmp,item_created__range = [startDate, endDate])
            vend = Fin_Vendors.objects.filter(Company=cmp)
            cust = Fin_Customers.objects.filter(Company=cmp)
            customer = Fin_Customers.objects.filter(Company=cmp)
            vendor = Fin_Vendors.objects.filter(Company=cmp)
            
            

            for i in customer:
                fullname = i.first_name + ' ' + i.last_name
                invoice = Fin_Invoice.objects.filter(Company=cmp,Customer=i)
                
                if invoice:
                    for inv in invoice:
                        invitems = Fin_Invoice_Items.objects.filter(Invoice=inv,invoice_date__range=[startDate, endDate])
                        for dis in invitems:
                            Totsalediscount += float(dis.discount)
                    
                
                rec_invoice = Fin_Recurring_Invoice.objects.filter(Company=cmp,Customer=i,start_date__range=[startDate, endDate])
                
                if rec_invoice:
                    for rec in rec_invoice:
                        recitems = Fin_Recurring_Invoice_Items.objects.filter(RecInvoice=rec)
                        for dis in recitems:
                            Totsalediscount +=float(dis.discount)
                        
                ret_invoice = Fin_Retainer_Invoice.objects.filter(Company=cmp,Customer=i,Retainer_Invoice_date__range=[startDate, endDate])
                
                if ret_invoice:
                    for ret in ret_invoice:
                        retitems = Fin_Retainer_Invoice_Items.objects.filter(Ret_Inv=ret)
                        for dis in retitems:
                            Totsalediscount += float(dis.discount)
            
                
            
            for i in vendor:
                fullname2 = i.first_name + ' ' + i.last_name
                bill = Fin_Purchase_Bill.objects.filter(company=cmp,vendor=i,bill_date__range=[startDate, endDate])
                
                if bill:
                    for b in bill:
                        billitems = Fin_Purchase_Bill_Item.objects.filter(pbill=b)
                        for dis in billitems:
                            Totpurchasediscount += float(dis.discount)
                        

                recbill = Fin_Recurring_Bills.objects.filter(company=cmp,vendor=i,date__range=[startDate, endDate])
                
                if recbill:
                    for rb in recbill:
                        recbillitems = Fin_Recurring_Bill_Items.objects.filter(recurring_bill=rb)
                        for dis in recbillitems:
                            Totpurchasediscount += float(dis.discount)

                
            for i in trans:
                balance = i.current_balance
                totbankbal += float(i.current_balance)
            if exp:
                for ex in exp:
                    totalExpense += float(ex.amount)
            if loan:
                for s in loan:  
                    balance = s.balance
                    totMoneybalLOAN+=float(s.balance)
            if EMPloan:
                for s in EMPloan:    
                    balance = s.balance
                    loan_amount=s.loan_amount
                    totMoneybalEMPLOAN+=float(s.balance) 
            for i in items:   
                name = i.name
                bQty = int(i.opening_stock)   
                pAmt = i.purchase_price
                totamt=bQty*pAmt
                TOTITEMAMT+=totamt
    

            # Initialize total balance outside the loop
            for vendr in vend:
                vendrName = vendr.first_name +" "+vendr.last_name

                PurchaseBill = Fin_Purchase_Bill.objects.filter(vendor=vendr, status='Save',bill_date__range=[startDate, endDate])
                Recurring_Bills = Fin_Recurring_Bills.objects.filter(vendor=vendr, status='Save',date__range=[startDate, endDate])
                Debit_Note = Fin_Debit_Note.objects.filter(Vendor=vendr, status='Saved',debit_note_date__range=[startDate, endDate])
            
                bill_balance = sum(float(inv.balance) for inv in PurchaseBill)
                recurring_bill_balance = sum(float(rec_inv.balance) for rec_inv in Recurring_Bills)
                total_bill_balance = bill_balance + recurring_bill_balance
                available_debits = sum(float(credit_note.balance) for credit_note in Debit_Note)
                total_balance = total_bill_balance - available_debits            
                # Update the total balance
                total_balance1 += total_balance
                venders_data.append({
                    'name': vendrName,                
                    'total_balance': total_balance,
                })
            
            for customer in cust:
                customerName = customer.first_name +" "+customer.last_name
                invoices = Fin_Invoice.objects.filter(Customer=customer, status='Saved',invoice_date__range=[startDate, endDate])
                recurring_invoices = Fin_Recurring_Invoice.objects.filter(Customer=customer, status='Saved',start_date__range=[startDate, endDate])
                credit_notes = Fin_CreditNote.objects.filter(Customer=customer, status='Saved',creditnote_date__range=[startDate, endDate])
                
                invoice_balance = sum(float(inv.balance) for inv in invoices)
                recurring_invoice_balance = sum(float(rec_inv.balance) for rec_inv in recurring_invoices)
                total_invoice_balance = invoice_balance + recurring_invoice_balance
                
                available_credits = sum(float(credit_note.balance) for credit_note in credit_notes)
                
                total_balance = total_invoice_balance - available_credits
                
                # Update the total balance
                total_balance11 += total_balance

                customers_data.append({
                    'name': customerName,                
                    'total_balance': total_balance,
                })
            inv = Fin_Invoice.objects.filter(Company = cmp,invoice_date__range = [startDate, endDate])
            crdNt = Fin_CreditNote.objects.filter(Company = cmp,creditnote_date__range = [startDate, endDate])
            recInv = Fin_Recurring_Invoice.objects.filter(Company = cmp,start_date__range = [startDate, endDate])
            sordr= Fin_Sales_Order.objects.filter(Company = cmp, sales_order_date__range = [startDate, endDate])
            rtInv= Fin_Retainer_Invoice.objects.filter(Company = cmp, Retainer_Invoice_date__range = [startDate, endDate])
            bill= Fin_Purchase_Bill.objects.filter(company = cmp, bill_date__range = [startDate, endDate])
            rcrbl= Fin_Recurring_Bills.objects.filter(company = cmp,date__range = [startDate, endDate])
            pordr= Fin_Purchase_Order.objects.filter(Company = cmp,purchase_order_date__range = [startDate, endDate])
            dbtnt= Fin_Debit_Note.objects.filter(Company = cmp,debit_note_date__range = [startDate, endDate])
            totCashIn=0
            totCashOut=0
            totCashOutpr=0
            totCashIndbt=0
            if inv:
                for i in inv:
                    balance=i.balance
                    totCashIn += float(i.balance)  

            if crdNt:
                for cr in crdNt:
                    balance = cr.balance
                    totCashOut += float(cr.balance)


            if recInv:
                for rc in recInv:
                    balance = rc.balance                
                    totCashIn += float(rc.balance)
            if sordr:
                for so in sordr:
                    balance = so.balance      
                    totCashIn += float(so.balance)
            if rtInv:
                for rt in rtInv:
                    totCashIn += float(rt.Balance)
            if bill:
                for bl in bill:
                    balance = bl.balance
                    totCashOutpr += float(bl.balance)

            if rcrbl:
                for rb in rcrbl:
                    balance = rb.balance
                    totCashOutpr += float(rb.balance)

            if pordr:
                for po in pordr:
                    balance = po.balance
                    totCashOutpr += float(po.balance)

            if dbtnt:
                for db in dbtnt:
                    balance = db.balance
                    totCashIndbt += float(db.balance)
                    print(totCashIndbt)
            context = {
                'cust':cust,
                'totCashOutsale':totCashOut,
                'totCashInsale':totCashIn,
                'totCashOutpr':totCashOutpr,
                'totCashIndbt':totCashIndbt,
                'cust': customers_data,
                'customers': venders_data,
                'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data,
                'startDate': startDate, 
                'endDate': endDate,
                'loan':totMoneybalLOAN,
                'Itemstock':TOTITEMAMT,
                'emploan':totMoneybalEMPLOAN,
                'total_CUSTbalance':total_balance11,
                'total_VENDORbalance':total_balance1,
                'totalExpense':totalExpense,
                'totbankbal':totbankbal,
                 'Totpurchasediscount':Totpurchasediscount,
            'Totsalediscount':Totsalediscount,
                
                }
            return render(request,'company/reports/trialbalance.html', context)
    else:
        return redirect('/')
    
   

def Fin_shareFin_trial_balanceToEmail(request):
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
                if startDate == "":
                    startDate = None
                if endDate == "":
                    endDate = None
                
                totbankbal=0
                totalExpense=0
                totMoneybalLOAN = 0
                totMoneybalEMPLOAN=0
                TOTITEMAMT=0
                venders_data = []
                total_balance1 = 0 
                customers_data = []
                total_balance11 = 0
                Totpurchasediscount=0
                Totsalediscount=0
                
                trans = Fin_BankTransactions.objects.filter(company=cmp)
                exp = Fin_Expense.objects.filter(Company=cmp)
                loan = loan_account.objects.filter(company = cmp)
                EMPloan = Fin_Loan.objects.filter(company_id=cmp)
                items = Fin_Items.objects.filter(Company = cmp)
                vend = Fin_Vendors.objects.filter(Company=cmp)
                cust = Fin_Customers.objects.filter(Company=cmp)
                customer = Fin_Customers.objects.filter(Company=cmp)
                vendor = Fin_Vendors.objects.filter(Company=cmp)
                

                for i in customer:
                    fullname = i.first_name + ' ' + i.last_name
                    invoice = Fin_Invoice.objects.filter(Company=cmp,Customer=i)
                    
                    if invoice:
                        for inv in invoice:
                            invitems = Fin_Invoice_Items.objects.filter(Invoice=inv)
                            invdiscount = 0
                            for dis in invitems:
                                Totsalediscount += float(dis.discount)
                        
                    
                    rec_invoice = Fin_Recurring_Invoice.objects.filter(Company=cmp,Customer=i)
                    
                    if rec_invoice:
                        for rec in rec_invoice:
                            recitems = Fin_Recurring_Invoice_Items.objects.filter(RecInvoice=rec)
                            recdiscount = 0
                            for dis in recitems:
                                Totsalediscount +=float(dis.discount)
                            
                    ret_invoice = Fin_Retainer_Invoice.objects.filter(Company=cmp,Customer=i)
                    
                    if ret_invoice:
                        for ret in ret_invoice:
                            retitems = Fin_Retainer_Invoice_Items.objects.filter(Ret_Inv=ret)
                            retdiscount = 0
                            for dis in retitems:
                                Totsalediscount += float(dis.discount)
                
                    
                
                for i in vendor:
                    fullname2 = i.first_name + ' ' + i.last_name
                    bill = Fin_Purchase_Bill.objects.filter(company=cmp,vendor=i)
                    
                    if bill:
                        for b in bill:
                            billitems = Fin_Purchase_Bill_Item.objects.filter(pbill=b)
                            billdiscount = 0
                            for dis in billitems:
                                Totpurchasediscount += float(dis.discount)
                                print(Totpurchasediscount)
                            

                    recbill = Fin_Recurring_Bills.objects.filter(company=cmp,vendor=i)
                    
                    if recbill:
                        for rb in recbill:
                            recbillitems = Fin_Recurring_Bill_Items.objects.filter(recurring_bill=rb)
                            recbilldiscountf = 0
                            for dis in recbillitems:
                                Totpurchasediscount += float(dis.discount)
                                print(Totpurchasediscount)
                                
                    
                        

                

        



                    
                for i in trans:
                    balance = i.current_balance
                    totbankbal += float(i.current_balance)
                if exp:
                    for ex in exp:
                        totalExpense += float(ex.amount)
                if loan:
                    for s in loan:  
                        balance = s.balance
                        totMoneybalLOAN+=float(s.balance)
                if EMPloan:
                    for s in EMPloan:    
                        balance = s.balance
                        loan_amount=s.loan_amount
                        totMoneybalEMPLOAN+=float(s.balance) 
                for i in items:   
                    name = i.name
                    bQty = int(i.opening_stock)   
                    pAmt = i.purchase_price
                    totamt=bQty*pAmt
                    TOTITEMAMT+=totamt
        

                # Initialize total balance outside the loop
                for vendr in vend:
                    vendrName = vendr.first_name +" "+vendr.last_name

                    PurchaseBill = Fin_Purchase_Bill.objects.filter(vendor=vendr, status='Save')
                    Recurring_Bills = Fin_Recurring_Bills.objects.filter(vendor=vendr, status='Save')
                    Debit_Note = Fin_Debit_Note.objects.filter(Vendor=vendr, status='Saved')
                    
                    bill_balance = sum(float(inv.balance) for inv in PurchaseBill)
                    recurring_bill_balance = sum(float(rec_inv.balance) for rec_inv in Recurring_Bills)
                    total_bill_balance = bill_balance + recurring_bill_balance
                    available_debits = sum(float(credit_note.balance) for credit_note in Debit_Note)
                    total_balance = total_bill_balance - available_debits            
                    # Update the total balance
                    total_balance1 += total_balance
                    venders_data.append({
                        'name': vendrName,                
                        'total_balance': total_balance,
                    })
                
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
                    total_balance11 += total_balance

                    customers_data.append({
                        'name': customerName,                
                        'total_balance': total_balance,
                    })
                inv = Fin_Invoice.objects.filter(Company = cmp)
                crdNt = Fin_CreditNote.objects.filter(Company = cmp)
                recInv = Fin_Recurring_Invoice.objects.filter(Company = cmp)
                sordr= Fin_Sales_Order.objects.filter(Company = cmp)
                rtInv= Fin_Retainer_Invoice.objects.filter(Company = cmp)
                bill= Fin_Purchase_Bill.objects.filter(company = cmp)
                rcrbl= Fin_Recurring_Bills.objects.filter(company = cmp)
                pordr= Fin_Purchase_Order.objects.filter(Company = cmp)
                dbtnt= Fin_Debit_Note.objects.filter(Company = cmp)
                totCashIn=0
                totCashOut=0
                totCashOutpr=0
                totCashIndbt=0
                if inv:
                    for i in inv:
                        balance=i.balance
                        totCashIn += float(i.balance)  

                if crdNt:
                    for cr in crdNt:
                        balance = cr.balance
                        totCashOut += float(cr.balance)


                if recInv:
                    for rc in recInv:
                        balance = rc.balance                
                        totCashIn += float(rc.balance)
                if sordr:
                    for so in sordr:
                        balance = so.balance      
                        totCashIn += float(so.balance)
                if rtInv:
                    for rt in rtInv:
                        totCashIn += float(rt.Balance)
                if bill:
                    for bl in bill:
                        balance = bl.balance
                        totCashOutpr += float(bl.balance)

                if rcrbl:
                    for rb in rcrbl:
                        balance = rb.balance
                        totCashOutpr += float(rb.balance)

                if pordr:
                    for po in pordr:
                        balance = po.balance
                        totCashOutpr += float(po.balance)

                if dbtnt:
                    for db in dbtnt:
                        balance = db.balance
                        totCashIndbt += float(db.balance)
                        print(totCashIndbt)

                context = {
                    'cust':cust,
                    'totCashOutsale':totCashOut,
                    'totCashInsale':totCashIn,
                    'totCashOutpr':totCashOutpr,
                    'totCashIndbt':totCashIndbt,
                    'cust': customers_data,
                    'customers': venders_data,
                   
                    'cmp':cmp, 
                    'data':data,
                    'startDate':startDate, 
                    'endDate':endDate,
                    'loan':totMoneybalLOAN,
                    'Itemstock':TOTITEMAMT,
                    'emploan':totMoneybalEMPLOAN,
                    'total_CUSTbalance':total_balance11,
                    'total_VENDORbalance':total_balance1,
                    'totalExpense':totalExpense,
                    'totbankbal':totbankbal,
                    'Totpurchasediscount':Totpurchasediscount,
                    'Totsalediscount':Totsalediscount,

                
                    }

                template_path = 'company/reports/trialbalancepdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'Report_trialbalancepdf_Details'
                subject = f"Report_trialbalancepdf_Details"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Report for - trialbalancepdf Details. \n{email_message}\n\n--\nRegards,\n{cmp.Company_name}\n{cmp.Address}\n{cmp.State} - {cmp.Country}\n{cmp.Contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Report has been shared via email successfully..!')
                return redirect(Fin_trial_balance)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(Fin_trial_balance)
            

