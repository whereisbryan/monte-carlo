import random as rd
import math
import numpy as np
import matplotlib.pyplot as plt

discount_rate=0.1
growth_rate=0.03
repet=1000
price_matrix=[]
for l in range(repet):
    FCFE=[]
    sgaY=3611
    cogsY=5468
    salesY=9743
    taxrate=0.21
    net_inc=[]
    netinc=0
    for i in range(8):      # what is the purpose of that loop? 9 years? yes but i changed for 8 to reach the net income in 2028
        if l==repet-1 and i==4:
            salesY=salesY*(1+rd.gauss(-0.15, 0.01)) #blackswan scenario
        else:
            salesY=salesY*(1+rd.gauss(0.022, 0.01))
        cogsY=cogsY*(1+rd.gauss(-0.02, 0.005))
        grossprof=salesY-cogsY
        sgaY=sgaY*(1+rd.gauss(-0.025, 0.01))
        opeinc=grossprof-sgaY
        taxamount=opeinc*taxrate #I will introduce new scenario if democrats win the election
        netinc=opeinc-taxamount # netinc=opeinc-netinc why? it was a mistake
        net_inc.append(netinc)
        # don't forget that with each loop the values of salesY, cogsY, etc. are the updated values, e.g. smaller and smaller    
    posprec=100000  # what are this numbers? just a trick to make a growth of the working cap related to the net income growth (there is probably a better way to do it...)
    workcap=50      # what are this numbers? this is the initial working cap estimate of 2019
    capex=75        # what are this numbers? this is the initial capex estimate of 2019
    year=2020
    for j in net_inc:
        year=year+1         # what is the purpose? You are not using it at all - I am going to use it for the debt repayment 
        CFO_bforWC=j+300    # what are this numbers? this is the Non-cash item in the CF statement that we assume constant (historically constant)
        if posprec==100000:
            workcap=workcap
        else:
            workcap=workcap*(j/posprec) # why? we see a correlation between net income growth and working capital growth historically
        CFO_net=CFO_bforWC+workcap
        posprec=j
        capex=capex*1.05
        if year==2022:
            debt=-100
        if year==2023:
            debt=-250
        if year>2023:
            debt=-40
        if year<2022:
            debt=-33.75         # what is this number?  this is the coupon payments of the current debt 
        fcfe=CFO_net-capex+debt
        T=year-2019
        if T<10:
            pv=fcfe/((1+discount_rate)**T)
        else:
            pv=(fcfe*(1+growth_rate))/(discount_rate-growth_rate)
            pv=pv/((1+discount_rate)**T)
        FCFE.append(pv)
        # don't forget that with each loop the values of capex are the updated values, e.g. bigger and bigger
        # do you intend it? why did not increase other numbers in that case? yes, I intend it but I simulate only  the numbers used in that are used to calculate free cash flows  
    price=np.sum(FCFE)/69.6
    if price<0:
        price=1
    price_matrix.append(price)

    
target_price=np.mean(price_matrix) # easier to use np.mean()- thanks for the tip
print('our target price is: ',target_price)
print(len(price_matrix))
plt.grid()
plt.hist(price_matrix, bins=50, density=True)
plt.show()
#print(price_matrix)
