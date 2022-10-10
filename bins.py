import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
# disable warnings from using verify=False in get/post requests
disable_warnings(InsecureRequestWarning)
import notifications

class Bin:
    def __init__(self, color, description):
        self.color = color
        self.description = description

    def set_date(self, date):
        ignore = "Next Collection: "
        date_string = date[len(ignore):]
        date_time = datetime.strptime(date_string, '%A %d %B %Y')
        self.collection_date = date_time

class Bins:
    def __init__(self):
        self.bins : dict[str, Bin]= {}
    
    def AddBin(self, bin : Bin):
        self.bins[bin.color] = bin

    def PopulateBins(self, data):
        for item in data:
            for key in self.bins:
                if key in item[0]:
                    self.bins[key].set_date(item[1])

    def PrintBins(self):
        for key in self.bins:
            pretty_date = self.bins[key].collection_date.strftime('%A %d %b')
            print(f"The {self.bins[key].color} bin will be collected on {pretty_date}.")

    def SendMessage(self):
        today = datetime.today()
        colors = []
        for key in self.bins:
            if self.bins[key].collection_date.date() - timedelta(days=1) == today.date():
                colors.append(key.lower())
        bin_string = ""
        if len(colors) > 0:
            if len(colors) == 1:
                bin_string = colors[0]
            else:
                bin_string = colors[0]
                for i in range(1, len(colors) - 1):
                    bin_string += ", " + colors[i]
                bin_string += " and " + colors[-1]

            title = "Bins tomorrow"
            if len(colors) == 1:
                message = "The " + bin_string + " bin needs to go out tomorrow."
            else:
                message = "The " + bin_string + " bins need to go out tomorrow."
            
            notifications.SendNotification(title, message)
            # notifications.SendFakeNotification(title, message)
            

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

my_bins = Bins()
my_bins.AddBin(Bin("Green", "General waste"))
my_bins.AddBin(Bin("Blue", "Recycling"))
my_bins.AddBin(Bin("Food", "Food waste"))

bins = [item.text for item in soup3.find_all("th")]
dates = [item.text for item in soup3.find_all("td")]
result = list(zip(bins, dates))
# print(*result, sep='\n')

my_bins.PopulateBins(result)
my_bins.PrintBins()
my_bins.SendMessage()
