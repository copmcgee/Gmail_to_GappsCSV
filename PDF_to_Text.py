import pdftotext

def Get_Paysheet_info(file):
    with open(f'/home/ryan/Downloads/{file}', 'rb') as file:
        pdf = pdftotext.PDF(file)

    paysheet_pdf = pdf[0].split()

    # for num,thing in enumerate(paysheet_pdf):
    #     print(num, thing)

    Legend ={ "Date": 21, "PeriodStart": 28, "PeriodFinish": 30, "Gross": 33, "Tax":  60, "Net": 43,
    "Hours": 53,"Rate": 24,  "SuperAdd": 65, "SuperTotal": 66, "TotalTax": 61, "YTD": 56}
    
    pay_info_list =[paysheet_pdf[item] for item in Legend.values()]
    
    return pay_info_list

