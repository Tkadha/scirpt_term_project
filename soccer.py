import requests
import xml.etree.ElementTree as ET

url = 'https://openapi.gg.go.kr/PublicTrainingFacilitySoccer'
service_key = "de852e4aa3fa49d09907453c21f5188c"
Params = {'Key': service_key, 'Type': 'xml', 'pSize': 265}
response = requests.get(url, params=Params)
root = ET.fromstring(response.text)

header = ["Name", "sigun", "Area", "Material", "x", "y", "Addr"]


class Soccer():
    soccer_lists = list()
    for item in root.iter("row"):
        name = item.findtext("FACLT_NM")
        area = item.findtext("AR")
        material = item.findtext("BOTM_MATRL_NM")
        x = item.findtext("REFINE_WGS84_LAT")
        y = item.findtext("REFINE_WGS84_LOGT")
        sigun = item.findtext("SIGUN_NM")
        addr = item.findtext("REFINE_ROADNM_ADDR")
        soccer_lists.append([name, sigun, area, material, x, y, addr])
