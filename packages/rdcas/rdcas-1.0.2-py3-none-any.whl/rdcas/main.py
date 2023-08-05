from requests import  *
from urllib import parse
def casPost(url,data):
    par = {}
    par["params"] = data
    text = parse.urlencode(par)
    r1 = post(url, params=text)
    res = r1.json()
    return(res)
class BankAccount:
    def __init__(self,baseUrl="http://43.226.238.194:6443/",orgCode="CMBS001",secretKey="CpQf35vKCGOHgZtpFgXpB_zKYNTN1t1V"):
        self.baseUrl = baseUrl
        self.orgCode = orgCode
        self.secretKey = secretKey
    def bankCodeQuery(self,bankCode="BOC"):
        self.bankCode = bankCode
        entry = "app/basequery/queryLedgerBankCode.html"
        api = self.baseUrl + entry
        data = {'orgCode': self.orgCode,
        "secretKey": self.secretKey,
        "bankCode": self.bankCode}
        res = casPost(api,data)
        return(res)

