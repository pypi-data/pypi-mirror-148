from win32com.client import Dispatch


def MyOpenExcel(excel,Visible=True,Quit =True):
    xlApp = Dispatch("Excel.Application")
    if Visible:
        xlApp.Visible = Visible
        xlApp.Workbooks.Open(excel)

    else:
        xlApp.Visible = Visible
        xlApp.DisplayAlerts = False
        xlBook = xlApp.Workbooks.Open(excel)
        xlBook.Save()
        xlBook.Close()
        if Quit:
            xlApp.Quit()