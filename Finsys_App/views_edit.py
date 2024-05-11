def Fin_gstr2Customized(request):
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

            vend1 = Fin_Vendors.objects.filter(Company=cmp).filter(Q(gstin__exact='') | Q(gstin=None))
            vend2 = Fin_Vendors.objects.filter(Company=cmp).exclude(Q(gstin__exact='') | Q(gstin=None))



            
            if type == 'all':


                inv = Fin_Purchase_Bill.objects.filter(company = cmp,bill_date__range = [startDate, endDate])
                if inv:
                    for i in inv:
                        partyName = i.vendor.first_name +" "+i.vendor.last_name
                        date = i.bill_date
                        ref = i.bill_no
                        type = 'Purchase Bill'
                        total = i.grandtotal
                        paid =i.paid
                        balance=i.balance
                        gstin=i.vendor.gstin
                        igst=i.igst
                        sgst=i.sgst
                        cgst=i.cgst
                        place_of_supply=i.ven_psupply
                        subtotal=i.subtotal
                        tax_amount=i.taxamount

                        
                        
                        

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
                recInv = Fin_Recurring_Bills.objects.filter(company = cmp,date__range = [startDate, endDate])
                if recInv:
                    for r in recInv:
                        partyName = r.vendor.first_name +" "+r.vendor.last_name
                        date = r.date
                        ref = r.recurring_bill_number
                        type = 'Recurring Bills'
                        total = r.grand_total
                        paid =r.advanceAmount_paid
                        balance=r.balance
                        gstin=r.vendor_gst_number
                        igst=r.taxAmount_igst
                        sgst=r.sgst
                        cgst=r.cgst
                        place_of_supply=r.vendor_place_of_supply
                        subtotal=r.sub_total
                        tax_amount=r.taxAmount_igst

                        
                        
                        

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
                        reportData.append(details)
                cNote = Fin_Debit_Note.objects.filter(Company = cmp,debit_note_date__range = [startDate, endDate])
                if cNote:
                    for note in cNote:
                        partyName = note.Vendor.first_name +" "+note.Vendor.last_name
                        date = note.debit_note_date
                        ref = note.debit_note_number
                        type = 'Debit Note'
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
                        invoice_number=note.bill_number
                        invoice_type=note.bill_type
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


                for vendor in vend2:
    # Apply the filter for the current vendor
                    inv = Fin_Purchase_Bill.objects.filter(company=cmp, bill_date__range=[startDate, endDate], vendor=vendor)
                    for i in inv:
                        partyName = i.vendor.first_name +" "+i.vendor.last_name
                        date = i.bill_date
                        ref = i.bill_no
                        type = 'Purchase Bill'
                        total = i.grandtotal
                        paid =i.paid
                        balance=i.balance
                        gstin=i.vendor.gstin
                        igst=i.igst
                        sgst=i.sgst
                        cgst=i.cgst
                        place_of_supply=i.ven_psupply
                        subtotal=i.subtotal
                        tax_amount=i.taxamount

                        
                        
                        

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
                recInv = Fin_Recurring_Bills.objects.filter(company=cmp, date__range=[startDate, endDate]).exclude(Q(vendor_gst_number__exact='') | Q(vendor_gst_number=None))

                if recInv:
                    for r in recInv:
                        partyName = r.vendor.first_name +" "+r.vendor.last_name
                        date = r.date
                        ref = r.recurring_bill_number
                        type = 'Recurring Bills'
                        total = r.grand_total
                        paid =r.advanceAmount_paid
                        balance=r.balance
                        gstin=r.vendor_gst_number
                        igst=r.taxAmount_igst
                        sgst=r.sgst
                        cgst=r.cgst
                        place_of_supply=r.vendor_place_of_supply
                        subtotal=r.sub_total
                        tax_amount=r.taxAmount_igst

                        
                        
                        

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
                
                cNote = Fin_Debit_Note.objects.filter(Company=cmp, debit_note_date__range=[startDate, endDate]).exclude(Q(gstin__exact='') | Q(gstin=None))
                if cNote:
                    for note in cNote:
                        partyName = note.Vendor.first_name +" "+note.Vendor.last_name
                        date = note.debit_note_date
                        ref = note.debit_note_number
                        type = 'Debit Note'
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
                        invoice_number=note.bill_number
                        invoice_type=note.bill_type
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
                for vendor in vend1:
    # Apply the filter for the current vendor
                    inv = Fin_Purchase_Bill.objects.filter(company=cmp, bill_date__range=[startDate, endDate], vendor=vendor)
                #

                    for i in inv:
                        partyName = i.vendor.first_name +" "+i.vendor.last_name
                        date = i.bill_date
                        ref = i.bill_no
                        type = 'Purchase Bill'
                        total = i.grandtotal
                        paid =i.paid
                        balance=i.balance
                        gstin=i.vendor.gstin
                        igst=i.igst
                        sgst=i.sgst
                        cgst=i.cgst
                        place_of_supply=i.ven_psupply
                        subtotal=i.subtotal
                        tax_amount=i.taxamount

                        
                        
                        

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

                recInv = Fin_Recurring_Bills.objects.filter(company=cmp, date__range=[startDate, endDate]).filter(Q(vendor_gst_number__exact='') | Q(vendor_gst_number=None))
                if recInv:
                    for r in recInv:
                        partyName = r.vendor.first_name +" "+r.vendor.last_name
                        date = r.date
                        ref = r.recurring_bill_number
                        type = 'Recurring Bills'
                        total = r.grand_total
                        paid =r.advanceAmount_paid
                        balance=r.balance
                        gstin=r.vendor_gst_number
                        igst=r.taxAmount_igst
                        sgst=r.sgst
                        cgst=r.cgst
                        place_of_supply=r.vendor_place_of_supply
                        subtotal=r.sub_total
                        tax_amount=r.taxAmount_igst

                        
                        
                        

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
                cNote = Fin_Debit_Note.objects.filter(Company=cmp, debit_note_date__range=[startDate, endDate]).filter(Q(gstin__exact='') | Q(gstin=None))


                if cNote:
                    for note in cNote:
                        partyName = note.Vendor.first_name +" "+note.Vendor.last_name
                        date = note.debit_note_date
                        ref = note.debit_note_number
                        type = 'Debit Note'
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
                        invoice_number=note.bill_number
                        invoice_type=note.bill_type
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
            return render(request,'company/reports/Fin_gstr2.html', context)
    else:
        return redirect('/')
    