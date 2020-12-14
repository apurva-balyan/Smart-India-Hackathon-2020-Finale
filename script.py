from flask import Flask, Response, request
from flask import render_template, make_response, redirect
from flask_restful import Resource, Api
import numpy as np
import flask
import pickle     
import json
import jsonify
from collections import OrderedDict
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "u484skTfr7ZfUNcLw9lRxAhsm1IIqNmtOYyqCf_JTtBulXIC53Qv_HE4q_9H_hG3x_DZMXokvcmjkaZ0iVglGg=="
org = "org"
bucket = "sih"
client = InfluxDBClient(url="http://localhost:8086", token=token)


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

api = Api(app)
# api2 = Api(app)


def writedb(maintest):
    try:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        bucket = 'sih'
        tables=['model1','model2','model3','model4','model5','model6','model7','model8']
        for i in range(len(maintest)):
            tname = tables[i]
            wr = tname + ',host=host1 '
            pp = maintest[i]
            for l,m in pp.items():
                s = wr + l+ '=' + str(m)
#                 print(s)
                write_api.write('sih', org,s)
    except Exception as E:
        print(E)
            
def mdl1(txt1):
    ret = OrderedDict()
    org = txt1.split('$')
    hdr = ['room_id','no_of_occupants','indoor_temp','outdoor_temp','rel_hght_of_floor','ceiling_height','room_area','roof_material','humidity']
    ret['model_id'] = 1
    for i in range(len(hdr)):
        ret[hdr[i]] = org[i]
    ls = txt1.split('$')[1:]
    roomid = ls[1]
    floorid = ls[4]
    to_predict = np.array(ls).reshape(1,len(ls))
#     print(to_predict)
    loaded_model = pickle.load(open("model1.pkl","rb"))
    result = loaded_model.predict(to_predict)
    ret['hvac_load'] = result[0]
    return ret

def hvach(txt1):
    ret = OrderedDict()
    org = txt1.split('$')
    hdr = ['compactness', 'surface_area', 'wall_area', 'roof_area', 'height', 'orientation', 'glazing_area', 'glazing_area_distribution']
    ret['model_id'] = 2
    for i in range(len(hdr)):
        ret[hdr[i]] = org[i]
    ls = txt1.split('$')
    to_predict = np.array(ls).reshape(1,len(ls))
#     print(to_predict)
    loaded_model = pickle.load(open("heating_load.pkl","rb"))
    result = loaded_model.predict(to_predict)
    ret['fixed_heating_load'] = result[0]
    return ret

def hvacc(txt1):
    ret = OrderedDict()
    org = txt1.split('$')
    hdr = ['compactness', 'surface_area', 'wall_area', 'roof_area', 'height', 'orientation', 'glazing_area', 'glazing_area_distribution']
    ret['model_id'] = 3
    for i in range(len(hdr)):
        ret[hdr[i]] = org[i]
    ls = txt1.split('$')
    to_predict = np.array(ls).reshape(1,len(ls))
#     print(to_predict)
    loaded_model = pickle.load(open("cooling_load.pkl","rb"))
    result = loaded_model.predict(to_predict)
    ret['fixed_cooling_load'] = result[0]
    return ret

def hec(txt1):
    ret = OrderedDict()
    org = txt1.split('$')
    hdr = ['interval1','interval2','interval3','interval4','interval5']
    ret['model_id'] = 4
    for i in range(len(hdr)):
        ret[hdr[i]] = org[i]
    ls = txt1.split('$')
#     print(ls)
#     print(ls)
    to_predict = np.array(ls).reshape(1,len(ls))
    x = np.asarray(to_predict, dtype='float64')
    loaded_model = pickle.load(open("d2_lr.pkl","rb"))
    result = loaded_model.predict(x)
    ret['hourly_energy_consumption'] = str(result[0])
    return ret
    
def ef(txt1):
    ret = OrderedDict()
    org = txt1.split('$') # kwh kwh kwh
    hdr = ['active_power','reactive_power','voltage','ktch','ldr']
    ret['model_id'] = 5
    for i in range(len(hdr)):
        ret[hdr[i]] = org[i]
    ls = txt1.split('$')
#     print(ls)
    to_predict = np.array(ls).reshape(1,len(ls))
#     print(to_predict)
    loaded_model = pickle.load(open("d3_xgb1.pkl","rb"))
    result = loaded_model.predict(to_predict)
    ret['hvac_load'] = str(result[0])
    return ret
    
def efp(txt1):
    ret = OrderedDict()
    org = txt1.split('$')
    hdr = ['region_cluster','maintenance_vendor','manufacturer','equipment_type','S15','S17','S13','S5','S16','S19','S18','S8','equipment_age']
    ret['model_id'] = 6
    for i in range(len(hdr)):
        ret[hdr[i]] = org[i]
    ls = txt1.split('$')
#     print(ls)
    to_predict = np.array(ls).reshape(1,len(ls))
#     print(to_predict)
    loaded_model = pickle.load(open("dataset5.pkl","rb"))
    result = loaded_model.predict(to_predict)
    ret['equipment_health_status(faliure)'] = str(result[0])
    return ret

def epc(txt1):
    ret = OrderedDict()
    org = txt1.split('$')
    hdr = ['voltage', 'global_intensity','sub_meter_1', 'sub_meter_2','sub_meter_3']
    ret['model_id'] = 7
    for i in range(len(hdr)):
        ret[hdr[i]] = org[i]
    ls = txt1.split('$')
#     print(ls)
    to_predict = np.array(ls).reshape(1,len(ls))
#     print(to_predict)
    loaded_model = pickle.load(open("dataset6_dtr.pkl","rb"))
    result = loaded_model.predict(to_predict)
    ret['predicted_energy_use'] = result[0]
    return ret

def aep(txt1):
    ret = OrderedDict()
    org = txt1.split('$')
    hdr = ['temp_ktcharea','humidity_ktcharea','temp_livroom','humidity_livroom','temp_ldroom','humidity_ldroom','temp_ofroom','humidity_ofroom','temp_bthroom','humidity_bthroom','temp_outdoor','humidity_outdoor','temp_irnroom','humidity_irnroom','temp_tnroom','humidity_tnroom','temp_prroom','humidity_prroom','temp_outdoor2','pressure_outdoor2','humidity_outdoor2','wnd_speed_outdoor2','vis_outdoo2','rv1','rv2']
    ret['model_id'] = 8
#     print('rcv ln',len(org))
    for i in range(len(hdr)):
        ret[hdr[i]] = org[i]
    ls = txt1.split('$')
#     print(ls)
    to_predict = np.array(ls).reshape(1,len(ls))
#     print(to_predict)
    loaded_model = pickle.load(open("d7_lightgbm1.pkl","rb"))
    result = loaded_model.predict(to_predict)
    ret['global_power'] = str(result[0])
    return ret

def invalid(txt):
    return 'Bad Request'

class Dash(Resource):
    pass
res = []
class Display(Resource):

    def get(self, string1):
        global res
        res = []
        txt = string1
        tx = txt.split('_')
        res.append(mdl1(tx[0]))
        res.append(hvach(tx[1]))
        res.append(hvacc(tx[1]))
        res.append(hec(tx[2]))
#         res.append('EF MODEL ERROR XGB')
        res.append(ef(tx[3]))        
        res.append(efp(tx[4]))
        res.append(epc(tx[5]))
#         res.append('AEP MODEL ERROR LGBM')
        res.append(aep(tx[6]))
        maintest = res
        writedb(maintest)
        return flask.jsonify(results = res)
        # return invalid(txt)
        # headers = {'Content-Type': 'text/html'}
        # return{'text':'test'}
        # return make_response(render_template("result.html",result= "{}".format(string1)))

# class Dash(Resource):
#     def get(self):
#         return redirect("https://www.google.com", code=302)
    
api.add_resource(Display, '/search/v1/<string:string1>')
# api.add_resource(Dash, '/dashboard/<string:s1>')
@app.route('/dash')
def hello():
#     webbrowser.open_new_tab("https://curly-stingray-27.loca.lt/dashboard/snapshot/l63YI2RT888zDKHXWd9jFC1ifT6iZrQO?orgId=1&kiosk")
#     return render_template('res.html')
    return redirect('http://139.59.57.119:3000/d/LmTA89zmk/sih-building-management-monitoring-and-control-unit?orgId=1&refresh=5s&kiosk', code = '302')
#     return 'You have been redirected!'


if __name__ == '__main__':
    app.run(threaded=False)
