from iqoptionapi.stable_api import IQ_Option
import time
import random



Iq=IQ_Option("scolimoski1995@outlook.com","@Ipdpnm46")
Iq.connect()#connect to iqoption
goal="EURUSD"
Money=20
ACTIVES="EURUSD"
ACTION="put"#"call" or "put"
expirations_mode=1

#while True:
#    remaning_time=Iq.get_remaning(expirations_mode)
#    purchase_time=remaning_time-30
#    print(remaning_time)


print("Escolha a aposta \r\n 1->Acima 2->Abaixo")
option = input()
if(option == "1"):
    ACTION = "call"
else:
    ACTION = "put"

check,id=Iq.buy(Money,ACTIVES,ACTION,expirations_mode)
if check:
    print("!buy!")
else:
    print("buy fail")