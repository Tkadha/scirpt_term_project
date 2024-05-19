import requests
import xml.etree.ElementTree as ET

url='https://openapi.gg.go.kr/PublicTrainingFacilityBasebal'
service_key="147669a9fb7d4cea9b4a472552922dc1"
Params={'Key': service_key,'Type': 'xml','pSize':78 }
response = requests.get(url,params=Params)
root = ET.fromstring(response.text)

header = ["Name","sigun","Area","Material","x","y"]

baseball_dicts=dict()
for item in root.iter("row"):
    name=item.findtext("FACLT_NM")
    area=item.findtext("AR")
    material=item.findtext("INFLD_BOTM_MATRL_NM")
    x=item.findtext("REFINE_WGS84_LAT")
    y=item.findtext("REFINE_WGS84_LOGT")
    sigun=item.findtext("SIGUN_NM")
    baseball_dicts[name]=[sigun,area,material,x,y]



