# 这个app用个的本程序原始数据，而不是作为pip安装的第三方webform package

from prportal.i5562 import F5562
from prportal.i5406 import F5406
from prportal.i5669 import F5669
from prportal.i0008 import F0008
from prportal.login import Login
from models.definition import Role,Action
from models.pr.prmodel import PrModel
from prportal.application import Application
import json,dotenv


def main():
    # actions container
    actions=[]
    # get pa, sp, and dps object
    pa=PrModel(['/Users/jacky/desktop/doc/pr/pa.xlsx'])
    # print(pa.personal.age)
    sp=PrModel(['/Users/jacky/desktop/doc/pr/sp.xlsx'])
    dps=[]
    for excel in ['/Users/jacky/desktop/doc/pr/dp1.xlsx','/Users/jacky/desktop/doc/pr/dp2.xlsx']:
        dps.append(PrModel([excel]))
    
    # login config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
    config=dotenv.dotenv_values("webform/.env")
    rcic='jacky'
    rcic_account={
        "account":config[rcic+"_prportal_account"],
        "password":config[rcic+"_prportal_password"]
    }
    rcic=Login(rcic_account)
    actions+=rcic.login()
    # get application
    app=Application(pa)
    actions+=app.pick()
    
    # handle 5562
    f5562=F5562(pa,sp,dps)
    actions+=f5562.fill()
    # handle 5604
    f5406=F5406(pa,sp,dps)
    actions+=f5406.fill()
    # handle 5669
    f5669=F5669(pa,sp,dps)
    actions+=f5669.fill()
    # handle 0008
    f0008=F0008(pa,sp,dps)
    actions+=f0008.fill()
    
    print(json.dumps(actions,indent=3,default=str))
    
if __name__=='__main__':
    main()