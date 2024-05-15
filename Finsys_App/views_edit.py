
def Fin_sales_item_DiscountReportcutomized(request):
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

        items = Fin_Items.objects.filter(Company = cmp)

        reportData = []
        totamt=0
        totdiscount=0

        for i in items:
            qIn = 0
            qOut = 0
            discount=0
            amt =0

            name = i.name
            bQty = int(i.opening_stock)
            pAmt = i.purchase_price
            sAmt = i.selling_price
            minstock=i.min_stock
            stock_unit_rate=i.stock_unit_rate

            invItems = Fin_Invoice_Items.objects.filter(Item = i,Invoice__invoice_date__range=[startDate, endDate])
            recInvItems = Fin_Recurring_Invoice_Items.objects.filter(Item = i,RecInvoice__start_date__range=[startDate, endDate])
            retInvItems = Fin_Retainer_Invoice_Items.objects.filter(Item = i,Ret_Inv__Retainer_Invoice_date__range=[startDate, endDate])
            print(invItems)

            if invItems:
                for itm in invItems:
                    qOut += int(itm.quantity)
                    discount +=itm.discount
                    amt +=itm.total

            print(recInvItems)

            if recInvItems:
                for itm in recInvItems:
                    qOut += int(itm.quantity)
                    discount +=itm.discount
                    amt +=itm.total
            print(retInvItems)

            if retInvItems:
                for itm in retInvItems:
                    qOut += int(itm.Quantity)
                    discount +=itm.discount
                    amt +=itm.Total
            totamt+=qOut
            totdiscount+=discount
           

            det = {
                'name':name,
                'minstock':minstock,
                'stock_unit_rate':stock_unit_rate,
                'bQty':bQty,
                'qtyIn':qIn,
                'qtyOut':qOut,
                'discount':discount,
                'sAmount':sAmt,
                'amt':amt,


            }
            reportData.append(det)

        context = {
            'allmodules':allmodules, 'com':com, 'cmp':cmp, 'data':data, 'reportData':reportData,
            'startDate':startDate, 'endDate':endDate,'totamt':totamt,'totdiscount':totdiscount,
        }
        return render(request,'company/reports/Fin_sales_item_Discount.html', context)
    else:
        return redirect('/')
        