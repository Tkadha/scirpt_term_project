import requests
import xml.etree.ElementTree as ET

url='https://openapi.gg.go.kr/PublicTennis'
service_key="35e95396d48a4df5a63e464e54e6b457"
Params={'Key': service_key,'Type': 'xml','pSize':214 }
response = requests.get(url,params=Params)
root = ET.fromstring(response.text)

header = ["Name","sigun","Area","Material","x","y"]

class Tennis():
    tennis_lists=list()
    for item in root.iter("row"):
        name=item.findtext("FACLT_NM")
        area=item.findtext("AR")
        material=item.findtext("BOTM_MATRL_NM")
        x=item.findtext("REFINE_WGS84_LAT")
        y=item.findtext("REFINE_WGS84_LOGT")
        sigun=item.findtext("SIGUN_NM")
        tennis_lists.append([name,sigun,area,material,x,y])
