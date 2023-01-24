from ParseSQL import ParseSQL
from ParseCSV import ParseCSV
from ParseJSON import ParseJSON
from ExportODS import ExportODS


class Main:
    def __init__(self):
        sqlParser = ParseSQL()
        csvParser = ParseCSV()
        jsonParser = ParseJSON()
        export = ExportODS()

        sqlParser.ParseSQL()
        csvParser.parseCSV()
        jsonParser.parseJSON()
        export.buildTables()
        export.exportODS()


main = Main()
