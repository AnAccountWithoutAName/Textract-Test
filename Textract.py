import boto3
#from PIL import Image
import json
#Im = Image.open('.vscode\example_table.png')
session = boto3.Session(profile_name= 'Kosu')
Client = session.client("textract",region_name = 'us-east-1')
with open('.vscode\example_table.png','rb') as f:
    f_bytes = f.read()
    response = Client.analyze_document(Document = {'Bytes': f_bytes}, FeatureTypes = ['TABLES'])
    with open('.vscode\Blocks.json','w') as g:
        json.dump(response,g, indent = 4, sort_keys = True)





