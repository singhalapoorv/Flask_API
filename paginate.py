import flask
import flask_restful
from flask import Flask, request, jsonify, abort, json
from flask_restful import Resource, Api 
with open('testJson.json') as json_file:
    testJson = json.load(json_file)

app = Flask(__name__)

# This GET call would expect table name, startRow and rowLimit.
# testjson.json is the file it will operate on.
#http://localhost:4000/api/v1/getDataRowsForTable?table=AP_TEST2&startRow=1&rowLimit=10
@app.route('/api/v1/getDataRowsForTable',methods=['GET'])
def GetDataRowsForTable():
     startRow=1
     rowLimit=5
     tableToGet=''
     if 'startRow' in request.args:
        startRow=int(request.args['startRow'])
     if 'rowLimit' in request.args:
        rowLimit=int(request.args['rowLimit'])
     if 'table' in request.args:
        tableToGet= request.args['table']
    
     if tableToGet == '' or startRow < 0 or rowLimit < 0:
        abort(404)
     dataRows={}
     for table in testJson:
        if table['Table'] == tableToGet:
            dataRows = table['DataRow']
            break
     
     rowCount = len(dataRows)
     if rowCount==0 or startRow > rowCount:
        abort(404)
     
     return jsonify(dataRows[(startRow - 1):(startRow - 1 + rowLimit)])
     

# testjson.json is the file it will operate on.
#http://localhost:4000/api/v1/getTablesAndDataRowsCount
@app.route('/api/v1/getTablesAndDataRowsCount',methods=['GET'])
def GetTablesAndDataRowsCount():
    
    # make response
    objList={}
    for table in testJson:
        obj = {}
        obj['Table'] = table['Table']
        obj['SortColumns'] = table['SortColumns']
        obj['Rows'] = table['Rows']
        objList[table['Table']] = obj 
    return jsonify(objList) 
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000, debug=True)