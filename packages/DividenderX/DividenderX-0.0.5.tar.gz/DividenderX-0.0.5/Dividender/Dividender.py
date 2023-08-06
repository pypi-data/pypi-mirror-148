import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def getDividendQuarter(Price, DivdendPerShare, Quarters, Ticker="UnderlyingAsset"):
    equityHistory = []
    #newerReturn = []
    normalDiviReturn = DivdendPerShare/ Price
    equity = Price
    for i in range(Quarters):
        temp = equity * normalDiviReturn
        # print(temp)
        equity += temp
        # print(equity)
        #print(str(i+1),"equity ---> ", equity, "and", "temp ---->", temp)
        equityHistory.append(equity)
        #newerReturn.append(temp)
        #print(equityHistory)
    df = pd.DataFrame(equityHistory, columns=["EquityHistory"])
    df['EquityHistory'].plot(title=str(Ticker))
    plt.xlabel("Quarters")
    plt.ylabel("USD Growth")
    plt.show()

    return equityHistory[-1]
def getDividendMonthly(Price, DivdendPerShare, Month, Ticker="UnderlyingAsset"):
    equityHistory = []
    #newerReturn = []
    normalDiviReturn = DivdendPerShare/ Price
    equity = Price
    for i in range(Month):
        temp = equity * normalDiviReturn
        # print(temp)cls
        equity += temp
        # print(equity)
        #print(str(i+1),"equity ---> ", equity, "and", "temp ---->", temp)
        equityHistory.append(equity)
        #newerReturn.append(temp)
    df = pd.DataFrame(equityHistory, columns=["EquityHistory"])
    df['EquityHistory'].plot(title=str(Ticker))
    plt.xlabel("Months")
    plt.ylabel("USD Growth")
    plt.show()
    return equityHistory[-1]
def getDividendQuarterNoCompound(Price, DivdendPerShare, Quarters, Ticker="UnderlyingAsset"):
    equityHistory = []
    normalDiviReturn = DivdendPerShare
    equity = Price
    for i in range(Quarters):
        equity = equity + normalDiviReturn
        # print(temp)
        #equity += temp
        # print(equity)
        #print(str(i+1),"equity ---> ", equity)
        equityHistory.append(equity)
    df = pd.DataFrame(equityHistory, columns=["EquityHistory"])
    df['EquityHistory'].plot(title=str(Ticker))
    plt.xlabel("Quarters")
    plt.ylabel("USD Growth")
    plt.show()
    return equityHistory[-1]

getDividendQuarterNoCompound(52,2,20,"IEP")
#getDividendQuarter(52,2,80,"IEP")

#getDividendMonthly(12,0.1,8,"PFLT")

#getDividendQuarter(52,2,80,"IEP")
