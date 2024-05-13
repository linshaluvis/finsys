
#sale_summary_byHSN render
def sale_summary_byHSN(request):
    
    cmp1 = company.objects.get(id=request.session["uid"]) 
    
    pickup_records = []
     
    distinct_hsns = recinvoice_item.objects.filter(cid=cmp1.cid).values('hsn').distinct() 
   
    for hsn in distinct_hsns:
       recinvoice_id = recinvoice_item.objects.filter(cid=cmp1.cid,hsn=hsn['hsn'])
        
       for rec in recinvoice_id:
          
          recs = recinvoice.objects.get(cid=cmp1.cid,recinvoiceid=rec.id)
          record = {"hsn":hsn['hsn'],"grandtotal":recs.grandtotal,"subtotal":recs.subtotal, "IGST":recs.IGST,  "CGST":recs.CGST, "SGST":recs.SGST,"startdate":recs.startdate,"enddate":recs.enddate} 
          pickup_records.append(record)

    sale_hsns = invoice_item.objects.filter(cid=cmp1.cid).values('hsn').distinct()  
    for hsn in sale_hsns:
       sale_id = invoice_item.objects.filter(cid=cmp1.cid,hsn=hsn['hsn']) 
       for sale in sale_id:
          
          sales = invoice.objects.get(cid=cmp1.cid,invoiceid=sale.invoice_id)
          sales_record = {"hsn":hsn['hsn'],"grandtotal":sales.grandtotal,"subtotal":sales.subtotal, "IGST":sales.IGST,  "CGST":sales.CGST, "SGST":sales.SGST,"startdate": str(sales.invoicedate),"enddate":sales.duedate} 
          pickup_records.append(sales_record)
         
    context={
        'cmp1':cmp1,
        'recinv':pickup_records,
        
     }
    return render(request,'app1/sale_summary_byHSN.html',context)