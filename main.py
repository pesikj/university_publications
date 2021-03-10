import xml.etree.ElementTree as ET
import pandas as pd
import re


xml_data = open('publications.xml', 'r', encoding="utf-8").read()
xml_data = xml_data.replace("&", "")
root = ET.fromstring(xml_data)


def process_author_list(author_list):
    return ", ".join([author_list_child.find("prijmeni").text if author_list_child.find("prijmeni").text else "" for
                      author_list_child in author_list])


def process_title(title_list):
    for title in title_list:
        if title.find("nazev").text is not None:
            return title.find("nazev").text


def process_resource(resource):
    resource


data = {}
for child in root:
    literarni_forma = child.find('literarni_forma').text
    row = {}
    for subchild in child:
        if subchild.tag == "autor_list":
            row["autoři"] = process_author_list(subchild)
        elif subchild.tag == "titul_list":
            row["název"] = process_title(subchild)
        else:
            if subchild.text:
                row[subchild.tag] = subchild.text
    if literarni_forma not in data:
        data[literarni_forma] = [row, ]
    else:
        data[literarni_forma].append(row)

with pd.ExcelWriter('publikace.xlsx') as writer:
    for key, value in data.items():
        df = pd.DataFrame(value)
        df.to_excel(writer, sheet_name=key)
