import xml.etree.ElementTree as ET

# Load the XML file
xml_file = 'Billing Report.xml'
tree = ET.parse(xml_file)
root = tree.getroot()

# Retrieve all SQL queries
for query in root.findall('query'):
    query_id = query.get('id')
    query_type = query.get('type')
    sql = query.text.strip()
    print(f"Query ID: {query_id}, Type: {query_type}")
    print(f"SQL: {sql}")
