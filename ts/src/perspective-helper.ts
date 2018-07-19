import "@jpmorganchase/perspective-viewer";
import "@jpmorganchase/perspective-viewer-hypergrid";
import "@jpmorganchase/perspective-viewer-highcharts";

import {
  PSPWidget
} from './perspective-widget';


function fetch_and_load(psps: {[key:string]:PSPWidget;}){
    _fetch_and_load('/api/json/v1/messages?type=TRADE', 'grid', psps['performance-grid'], false, false);
    _fetch_and_load('/api/json/v1/messages?type=TRADE', 'performance-chart', psps['performance-chart'], false, false);
    // _fetch_and_load('/api/json/v1/messages', 'grid', psps['quote']);
}

function _fetch_and_load(path:string, type:string, loadto:PSPWidget, wrap_list=false, _delete=true){
    var xhr1 = new XMLHttpRequest();
    xhr1.open('GET', path, true);
    xhr1.onload = function () { 
        if(xhr1.response){
            var jsn = JSON.parse(xhr1.response);
            if (Object.keys(jsn).length > 0){
              setup_psp_and_load(type, jsn, loadto, wrap_list, _delete);
            }
        }
    };
    xhr1.send(null);
}

function setup_psp_and_load(type: string, data: any, loadto: PSPWidget, wrap_list=false, _delete=true){
    if (wrap_list){data = [data];}
    if(_delete){loadto.pspNode.delete();}
    if (data) {
        switch(type){
            case 'performance-chart': {
                loadto.pspNode.view = 'xy_line';
                loadto.pspNode.setAttribute('index', 'sequence');
                loadto.pspNode.setAttribute('column-pivots', '["currency_pair"]');
                loadto.pspNode.setAttribute('columns', '["time", "price"]');
                loadto.pspNode.update(data);
                break;
              }
            case 'grid': {
                loadto.pspNode.view = 'hypergrid';
                loadto.pspNode.setAttribute('index', 'sequence');
                loadto.pspNode.update(data);
                break;
            }
        }
    }
}


export class PerspectiveHelper {
    constructor(url: string,  // The url to fetch data from
                psps: {[key:string]:PSPWidget;}, // A set of perspective widgets 
                options: {[psp_key: string]: {[option: string]: string}}, // options to configure the widgets,
                                                                          // keyed by the `psps` keys
                schema?: {[psp_key: string]: {[key: string]: string}})    // <optional> schemas to preload onto the widgets,
                                                                          // keyed by the `psps` keys
    {
      if(url.indexOf('sio://') !== -1){
          this._datatype = 'sio';
      } else if(url.indexOf('ws://') !== -1){
          this._datatype = 'ws';
      } else if(url.indexOf('wss://') !== -1){
          this._datatype = 'wss';
      } else if(url.indexOf('http://') !== -1){
          this._datatype = 'http';
      } else if(url.indexOf('https://') !== -1){
          this._datatype = 'http';
      } else if(url.indexOf('comm://') !== -1){
          this._datatype = 'comm';
      } else{
          throw 'can\'t determine datatype';
      }


    }

    private _datatype: string;
    private _psp_widgets: [PSPWidget];
    private _worker: any; // TODO make this a shared perspective worker
}


namespace Private {
    export let _loaded = false;

    export function createNode(): void {
    }
}
