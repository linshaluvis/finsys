# ------------------------------------ Payment Received Report ------------------------------------
        path('Fin_PaymentReceived_report',views.Fin_PaymentReceived_report, name='Fin_PaymentReceived_report'),
        path('Fin_payments_receivedCustomized',views.Fin_payments_receivedCustomized, name='Fin_payments_receivedCustomized'),
        path('Fin_sharePaymentsReceivedReportToEmail',views.Fin_sharePaymentsReceivedReportToEmail, name='Fin_sharePaymentsReceivedReportToEmail'),
# ------------------------------------ Payment made Report ------------------------------------
        path('Fin_Paymentmade_report',views.Fin_Paymentmade_report, name='Fin_Paymentmade_report'),
        path('Fin_payments_madeCustomized',views.Fin_payments_madeCustomized, name='Fin_payments_madeCustomized'),
        path('Fin_sharePaymentsmadeReportToEmail',views.Fin_sharePaymentsmadeReportToEmail, name='Fin_sharePaymentsmadeReportToEmail'),


