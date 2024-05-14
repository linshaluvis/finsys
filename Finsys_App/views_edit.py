
def sale_summary_byHSN(request):
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
        items = Fin_Items.objects.filter(Company = cmp)


        reportData = []
        totitem=0

        invoice_items = Fin_Invoice_Items.objects.filter(Invoice__Company=cmp).values('hsn').annotate(
            total_sales=Sum('total'),
            total_igst=Sum('Invoice__igst'),
            total_sgst=Sum('Invoice__sgst'),
            
            total_cgst=Sum('Invoice__cgst'),
            total_subtotal=Sum('Invoice__subtotal'),
            
        )
        print(invoice_items)
        
        recurring_invoice_items = Fin_Recurring_Invoice_Items.objects.filter(RecInvoice__Company=cmp).values('hsn').annotate(
            total_sales=Sum('total'),
            total_igst=Sum('RecInvoice__igst'),
            total_sgst=Sum('RecInvoice__sgst'),
            total_cgst=Sum('RecInvoice__cgst'),
            total_subtotal=Sum('RecInvoice__subtotal'),
        )
        print(recurring_invoice_items)


        merged_data = {}

        for item in invoice_items:
            hsn = item['hsn'] 
            if hsn not in merged_data:
                merged_data[hsn] = {
                    'total_sales': item.get('total_sales', 0),
                    'total_igst': item.get('total_igst', 0),
                    'total_sgst': item.get('total_sgst', 0),
                    'total_cgst': item.get('total_cgst', 0),
                    'total_subtotal': item.get('total_subtotal', 0),
                }
            else:
                merged_data[hsn]['total_sales'] += item.get('total_sales', 0)
                merged_data[hsn]['total_igst'] += item.get('total_igst', 0)
                merged_data[hsn]['total_sgst'] += item.get('total_sgst', 0)
                merged_data[hsn]['total_cgst'] += item.get('total_cgst', 0)
                merged_data[hsn]['total_subtotal'] += item.get('total_subtotal', 0)
       
        for item in recurring_invoice_items:
            hsn = item['hsn']
            if hsn not in merged_data:
                merged_data[hsn] = {
                    'total_sales': item.get('total_sales', 0),
                    'total_igst': item.get('total_igst', 0),
                    'total_sgst': item.get('total_sgst', 0),
                    'total_cgst': item.get('total_cgst', 0),
                    'total_subtotal': item.get('total_subtotal', 0),
                }
            else:
                merged_data[hsn]['total_sales'] += item.get('total_sales', 0)
                merged_data[hsn]['total_igst'] += item.get('total_igst', 0)
                merged_data[hsn]['total_sgst'] += item.get('total_sgst', 0)
                merged_data[hsn]['total_cgst'] += item.get('total_cgst', 0)
                merged_data[hsn]['total_subtotal'] += item.get('total_subtotal', 0)


       

        # Construct the aggregated report data
        for hsn, item in merged_data.items():
            total = item.get('total_sales', 0)
            igst = item.get('total_igst', 0)
            sgst = item.get('total_sgst', 0)
            cgst = item.get('total_cgst', 0)
            subtotal = item.get('total_subtotal', 0)

            details = {
                'type': hsn,
                'total': total,
                'igst': igst,
                'sgst': sgst,
                'cgst': cgst,
                'subtotal': subtotal,
            }
            reportData.append(details)

        tototal = sum(item['total_sales'] for item in merged_data.values())  # Calculate total sales
        totitem=len(items)


        context = {
            'allmodules': allmodules,
            'com': com,
            'cmp': cmp,
            'data': data,
            'reportData': reportData,
            'tototal': tototal,
            'totitem':totitem,
        }
        return render(request, 'company/reports/sale_summary_byHSN.html', context)
    

def Fin_saleshsnCustomized(request):
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
       
        items = Fin_Items.objects.filter(Company = cmp)


        reportData = []
        totitem=0
        
        if status == 'all':

            invoice_items = Fin_Invoice_Items.objects.filter(Invoice__Company=cmp,Invoice__invoice_date__range=[startDate, endDate]).values('hsn').annotate(
                total_sales=Sum('total'),
                total_igst=Sum('Invoice__igst'),
                total_sgst=Sum('Invoice__sgst'),
                
                total_cgst=Sum('Invoice__cgst'),
                total_subtotal=Sum('Invoice__subtotal'),
                
            )
            
            recurring_invoice_items = Fin_Recurring_Invoice_Items.objects.filter(RecInvoice__Company=cmp,RecInvoice__start_date__range=[startDate, endDate]).values('hsn').annotate(
                total_sales=Sum('total'),
                total_igst=Sum('RecInvoice__igst'),
                total_sgst=Sum('RecInvoice__sgst'),
                total_cgst=Sum('RecInvoice__cgst'),
                total_subtotal=Sum('RecInvoice__subtotal'),
            )

            merged_data = {}

            for item in invoice_items:
                hsn = item['hsn'] 
                if hsn not in merged_data:
                    merged_data[hsn] = {
                        'total_sales': item.get('total_sales', 0),
                        'total_igst': item.get('total_igst', 0),
                        'total_sgst': item.get('total_sgst', 0),
                        'total_cgst': item.get('total_cgst', 0),
                        'total_subtotal': item.get('total_subtotal', 0),
                    }
                else:
                    merged_data[hsn]['total_sales'] += item.get('total_sales', 0)
                    merged_data[hsn]['total_igst'] += item.get('total_igst', 0)
                    merged_data[hsn]['total_sgst'] += item.get('total_sgst', 0)
                    merged_data[hsn]['total_cgst'] += item.get('total_cgst', 0)
                    merged_data[hsn]['total_subtotal'] += item.get('total_subtotal', 0)
        
            for item in recurring_invoice_items:
                hsn = item['hsn']
                if hsn not in merged_data:
                    merged_data[hsn] = {
                        'total_sales': item.get('total_sales', 0),
                        'total_igst': item.get('total_igst', 0),
                        'total_sgst': item.get('total_sgst', 0),
                        'total_cgst': item.get('total_cgst', 0),
                        'total_subtotal': item.get('total_subtotal', 0),
                    }
                else:
                    merged_data[hsn]['total_sales'] += item.get('total_sales', 0)
                    merged_data[hsn]['total_igst'] += item.get('total_igst', 0)
                    merged_data[hsn]['total_sgst'] += item.get('total_sgst', 0)
                    merged_data[hsn]['total_cgst'] += item.get('total_cgst', 0)
                    merged_data[hsn]['total_subtotal'] += item.get('total_subtotal', 0)


        

            # Construct the aggregated report data
            for hsn, item in merged_data.items():
                total = item.get('total_sales', 0)
                igst = item.get('total_igst', 0)
                sgst = item.get('total_sgst', 0)
                cgst = item.get('total_cgst', 0)
                subtotal = item.get('total_subtotal', 0)

                details = {
                    'type': hsn,
                    'total': total,
                    'igst': igst,
                    'sgst': sgst,
                    'cgst': cgst,
                    'subtotal': subtotal,
                }
                reportData.append(details)

            tototal = sum(item['total_sales'] for item in merged_data.values())  # Calculate total sales
            totitem=len(items)
        if status == 'Invoice':

            invoice_items = Fin_Invoice_Items.objects.filter(Invoice__Company=cmp,Invoice__invoice_date__range=[startDate, endDate]).values('hsn').annotate(
                total_sales=Sum('total'),
                total_igst=Sum('Invoice__igst'),
                total_sgst=Sum('Invoice__sgst'),
                
                total_cgst=Sum('Invoice__cgst'),
                total_subtotal=Sum('Invoice__subtotal'),
                
            )
            merged_data = {}

            for item in invoice_items:
                hsn = item['hsn'] 
                if hsn not in merged_data:
                    merged_data[hsn] = {
                        'total_sales': item.get('total_sales', 0),
                        'total_igst': item.get('total_igst', 0),
                        'total_sgst': item.get('total_sgst', 0),
                        'total_cgst': item.get('total_cgst', 0),
                        'total_subtotal': item.get('total_subtotal', 0),
                    }
                else:
                    merged_data[hsn]['total_sales'] += item.get('total_sales', 0)
                    merged_data[hsn]['total_igst'] += item.get('total_igst', 0)
                    merged_data[hsn]['total_sgst'] += item.get('total_sgst', 0)
                    merged_data[hsn]['total_cgst'] += item.get('total_cgst', 0)
                    merged_data[hsn]['total_subtotal'] += item.get('total_subtotal', 0)
        

            # Construct the aggregated report data
            for hsn, item in merged_data.items():
                total = item.get('total_sales', 0)
                igst = item.get('total_igst', 0)
                sgst = item.get('total_sgst', 0)
                cgst = item.get('total_cgst', 0)
                subtotal = item.get('total_subtotal', 0)

                details = {
                    'type': hsn,
                    'total': total,
                    'igst': igst,
                    'sgst': sgst,
                    'cgst': cgst,
                    'subtotal': subtotal,
                }
                reportData.append(details)

            tototal = sum(item['total_sales'] for item in merged_data.values())  # Calculate total sales
            totitem=len(items)
        if status == 'Recurring':

            
            
            recurring_invoice_items = Fin_Recurring_Invoice_Items.objects.filter(RecInvoice__Company=cmp,RecInvoice__start_date__range=[startDate, endDate]).values('hsn').annotate(
                total_sales=Sum('total'),
                total_igst=Sum('RecInvoice__igst'),
                total_sgst=Sum('RecInvoice__sgst'),
                total_cgst=Sum('RecInvoice__cgst'),
                total_subtotal=Sum('RecInvoice__subtotal'),
            )
            merged_data = {}
        
            for item in recurring_invoice_items:
                hsn = item['hsn']
                if hsn not in merged_data:
                    merged_data[hsn] = {
                        'total_sales': item.get('total_sales', 0),
                        'total_igst': item.get('total_igst', 0),
                        'total_sgst': item.get('total_sgst', 0),
                        'total_cgst': item.get('total_cgst', 0),
                        'total_subtotal': item.get('total_subtotal', 0),
                    }
                else:
                    merged_data[hsn]['total_sales'] += item.get('total_sales', 0)
                    merged_data[hsn]['total_igst'] += item.get('total_igst', 0)
                    merged_data[hsn]['total_sgst'] += item.get('total_sgst', 0)
                    merged_data[hsn]['total_cgst'] += item.get('total_cgst', 0)
                    merged_data[hsn]['total_subtotal'] += item.get('total_subtotal', 0)


        

            # Construct the aggregated report data
            for hsn, item in merged_data.items():
                total = item.get('total_sales', 0)
                igst = item.get('total_igst', 0)
                sgst = item.get('total_sgst', 0)
                cgst = item.get('total_cgst', 0)
                subtotal = item.get('total_subtotal', 0)

                details = {
                    'type': hsn,
                    'total': total,
                    'igst': igst,
                    'sgst': sgst,
                    'cgst': cgst,
                    'subtotal': subtotal,
                }
                reportData.append(details)

            tototal = sum(item['total_sales'] for item in merged_data.values())  # Calculate total sales
            totitem=len(items)



        

        context = {
            'allmodules': allmodules, 'com': com, 'cmp': cmp, 'data': data, 'reportData': reportData, 'tototal': tototal,
            'totitem':totitem, 'startDate': startDate, 'endDate': endDate, 'status': status
        }
        return render(request, 'company/reports/sale_summary_byHSN.html', context)
    else:
        return redirect('/')


def Fin_sharesalesHSNDetailsReportToEmail(request):
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

                items = Fin_Items.objects.filter(Company = cmp)


                reportData = []
                totitem=0

                invoice_items = Fin_Invoice_Items.objects.filter(Invoice__Company=cmp).values('hsn').annotate(
                    total_sales=Sum('total'),
                    total_igst=Sum('Invoice__igst'),
                    total_sgst=Sum('Invoice__sgst'),
                    
                    total_cgst=Sum('Invoice__cgst'),
                    total_subtotal=Sum('Invoice__subtotal'),
                    
                )
                print(invoice_items)
                
                recurring_invoice_items = Fin_Recurring_Invoice_Items.objects.filter(RecInvoice__Company=cmp).values('hsn').annotate(
                    total_sales=Sum('total'),
                    total_igst=Sum('RecInvoice__igst'),
                    total_sgst=Sum('RecInvoice__sgst'),
                    total_cgst=Sum('RecInvoice__cgst'),
                    total_subtotal=Sum('RecInvoice__subtotal'),
                )
                print(recurring_invoice_items)


                merged_data = {}

                for item in invoice_items:
                    hsn = item['hsn'] 
                    if hsn not in merged_data:
                        merged_data[hsn] = {
                            'total_sales': item.get('total_sales', 0),
                            'total_igst': item.get('total_igst', 0),
                            'total_sgst': item.get('total_sgst', 0),
                            'total_cgst': item.get('total_cgst', 0),
                            'total_subtotal': item.get('total_subtotal', 0),
                        }
                    else:
                        merged_data[hsn]['total_sales'] += item.get('total_sales', 0)
                        merged_data[hsn]['total_igst'] += item.get('total_igst', 0)
                        merged_data[hsn]['total_sgst'] += item.get('total_sgst', 0)
                        merged_data[hsn]['total_cgst'] += item.get('total_cgst', 0)
                        merged_data[hsn]['total_subtotal'] += item.get('total_subtotal', 0)
            
                for item in recurring_invoice_items:
                    hsn = item['hsn']
                    if hsn not in merged_data:
                        merged_data[hsn] = {
                            'total_sales': item.get('total_sales', 0),
                            'total_igst': item.get('total_igst', 0),
                            'total_sgst': item.get('total_sgst', 0),
                            'total_cgst': item.get('total_cgst', 0),
                            'total_subtotal': item.get('total_subtotal', 0),
                        }
                    else:
                        merged_data[hsn]['total_sales'] += item.get('total_sales', 0)
                        merged_data[hsn]['total_igst'] += item.get('total_igst', 0)
                        merged_data[hsn]['total_sgst'] += item.get('total_sgst', 0)
                        merged_data[hsn]['total_cgst'] += item.get('total_cgst', 0)
                        merged_data[hsn]['total_subtotal'] += item.get('total_subtotal', 0)


            

                # Construct the aggregated report data
                for hsn, item in merged_data.items():
                    total = item.get('total_sales', 0)
                    igst = item.get('total_igst', 0)
                    sgst = item.get('total_sgst', 0)
                    cgst = item.get('total_cgst', 0)
                    subtotal = item.get('total_subtotal', 0)

                    details = {
                        'type': hsn,
                        'total': total,
                        'igst': igst,
                        'sgst': sgst,
                        'cgst': cgst,
                        'subtotal': subtotal,
                    }
                    reportData.append(details)

                tototal = sum(item['total_sales'] for item in merged_data.values())  # Calculate total sales
                totitem=len(items)


    

                   
                
                context = {'cmp':cmp, 'reportData':reportData, 'tototal': tototal,'totitem':totitem,  'startDate':startDate,'endDate':endDate}
                template_path = 'company/reports/sales_summarypdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'Report_sales_summary_by_HSN'
                subject = f"Report_sales_summary_by_HSN"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Report for - sales_summary_by_HSN. \n{email_message}\n\n--\nRegards,\n{cmp.Company_name}\n{cmp.Address}\n{cmp.State} - {cmp.Country}\n{cmp.Contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Report has been shared via email successfully..!')
                return redirect(sale_summary_byHSN)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(sale_summary_byHSN)
