import json
from PIL import Image, ImageDraw
import pprint as p
import xlsxwriter




class Table:
    def __init__(self,Block):
        self.id = Block['Id']
        self.children = Block['Relationships'][0]['Ids']
        self.cells = []
        self.title = ""
        Table.workbook = xlsxwriter.Workbook('Table.xlsx')
    def getChildren(self):
        return self.children
    def addCellToTable(self,CellBlock):
        self.cells.append(CellBlock)
    def addTitleToTable(self,TitleBlock):
        self.title = TitleBlock
    def makeTable(self,Hash):
        self.worksheet = Table.workbook.add_worksheet(f"Table {1}") 
        if self.title and self.title['Confidence'] >= 90:
            self.worksheet.write(0,0,self.title)
        for cell in self.cells:
            self.worksheet.write(cell['RowIndex'],cell['ColumnIndex'],Hash[cell['Relationships'][0]['Ids'][0]])
        Table.workbook.close()
def TableExtraction(blocks):
    List_of_tables = []
    Index_t = -1
    Line_Hash_Map = {}
    for index,block in enumerate(blocks):
        if block['BlockType'] == "TABLE":
            List_of_tables.append(Table(block))
            Index_t += 1
        if block['BlockType'] == "CELL":
            List_of_tables[Index_t].addCellToTable(block)
        if block['BlockType'] == "TABLE_TITLE":
            List_of_tables[Index_t].addTitleToTable(block)
        if block['BlockType'] == "LINE":
            Line_Hash_Map[block['Relationships'][0]['Ids'][0]] = block['Text']
        
    return List_of_tables,Line_Hash_Map




def main():
    with open('.vscode\Blocks.json') as f:
        response = json.load(f)
        Tables,Lines = TableExtraction(response['Blocks'])
        p.pprint(Lines["6691c3e1-07fa-44db-a850-9b9c76c3d142"])
        for i in Tables:
            i.makeTable(Lines)


        
        #p.pprint(Tables,Lines)

 



if __name__ == "__main__":
    main()
    


            

        
        





