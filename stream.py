import flask
import flask_restful
from flask import Flask, request, jsonify, abort, Response,json
from flask_restful import Resource, Api 
from time import sleep
with open('testJson.json') as json_file:
    testJson = json.load(json_file)
app = Flask(__name__)

    
url = '/api/v1/getAllDataRowsForTable'
@app.route(url,methods=['GET'])
def GetAllDataRowsForTable():
    startRow=1
    rowLimit=5
    if 'startRow' in request.args:
        startRow=int(request.args['startRow'])
    if 'rowLimit' in request.args:
        rowLimit=int(request.args['rowLimit'])
    
    if startRow < 0 or rowLimit < 0:
        abort(404)
    
    def streamer():
        
        for table in testJson:
            start=startRow
            count = len(table['DataRow'])
            
            yield '{"Table":' + json.dumps(table['Table']) + ',"SortColumns":' + json.dumps(table['SortColumns']) + ',"Rows":' + json.dumps(table['Rows']) + ',"DataRow":'
            while start<=count:
                yield json.dumps(table['DataRow'][(start - 1):(start - 1 + rowLimit)],indent=4,sort_keys=False)
                start=start+rowLimit
                sleep(1)
            yield '}'
            

    return Response(streamer(),content_type='application/json',headers={'X-Accel-Buffering': 'no'})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000, debug=True)