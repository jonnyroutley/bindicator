import requests
from bs4 import BeautifulSoup

bin_url = 'https://ecitizen.oxford.gov.uk/citizenportal/form.aspx?form=Bin_Collection_Day'

r1 = requests.get(bin_url, verify=False)
soup1 = BeautifulSoup(r1.content, "html.parser")


payload1 = {
    "Eform$Bin_Collection_Address_Search$AddressField_CustomerAddress$ibtnFindAddress.x" : 1,
    "Eform$Bin_Collection_Address_Search$AddressField_CustomerAddress$ibtnFindAddress.y" : 1,
    "Eform$Bin_Collection_Address_Search$AddressField_CustomerAddress$CustomerAddress" : "OX4 1QL"

}

payload1['__VIEWSTATE'] = soup1.select_one("#__VIEWSTATE")['value']
payload1['__VIEWSTATEGENERATOR'] = soup1.select_one("#__VIEWSTATEGENERATOR")['value']
payload1['__EVENTVALIDATION'] = soup1.select_one("#__EVENTVALIDATION")['value']

r2 = requests.post(bin_url, data=payload1, verify=False, cookies=r1.cookies)
soup2 = BeautifulSoup(r2.text, "html.parser")

payload2 = {

    "Eform$Bin_Collection_Address_Search$AddressField_CustomerAddress$CustomerAddress" : "OX4 1QL",
    "Eform$Bin_Collection_Address_Search$AddressField_CustomerAddress$lstSelectAddress" : "propertyref:101000470834",
    "Eform$Bin_Collection_Address_Search$NavigateNextButton.x" : 62,
    "Eform$Bin_Collection_Address_Search$NavigateNextButton.y" : 17
}

payload2['__VIEWSTATE'] = soup2.select_one("#__VIEWSTATE")['value']
payload2['__VIEWSTATEGENERATOR'] = soup2.select_one("#__VIEWSTATEGENERATOR")['value']
payload2['__EVENTVALIDATION'] = soup2.select_one("#__EVENTVALIDATION")['value']

r3 = requests.post(bin_url, data=payload2, verify=False, cookies=r2.cookies)
soup3 = BeautifulSoup(r3.text, "html.parser")
# print(soup3)

bins = [item.text for item in soup3.find_all("th")]
dates = [item.text for item in soup3.find_all("td")]
result = list(zip(bins, dates))
print(*result, sep='\n')