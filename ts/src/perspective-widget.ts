import {
  Message
} from '@phosphor/messaging';

import {
  Widget
} from '@phosphor/widgets';


import '../ts/style/index.css';
import "@jpmorganchase/perspective-viewer";
import "@jpmorganchase/perspective-viewer-hypergrid";
import "@jpmorganchase/perspective-viewer-highcharts";

export
class PSPWidget extends Widget {

  static createNode(): HTMLElement {
    let node = document.createElement('div');
    let content = document.createElement('perspective-viewer');
    node.appendChild(content);
    return node;
  }

  constructor(name: string) {
    super({ node: PSPWidget.createNode() });
    this.addClass('pspwidget');
    this.title.label = name;
    // this.title.closable = true;
    this.title.caption = `Long description for: ${name}`;
  }

  get pspNode(): any {
    return this.node.getElementsByTagName('perspective-viewer')[0];
  }

  onAfterAttach(msg: Message) : void {
    this.pspNode.notifyResize();
  }

  onAfterShow(msg: Message): void {
    this.pspNode.notifyResize();
  }

  onResize(msg: Message): void {
    this.pspNode.notifyResize();
  }

  protected onActivateRequest(msg: Message): void {
    this.pspNode.notifyResize();
    if (this.isAttached) {
      this.pspNode.focus();
    }
  }
}

export enum ViewOption {
  VIEW = 'view',
  INDEX = 'index',
  COLUMNS = 'columns',
  ROW_PIVOTS = 'row-pivots',
  COLUMN_PIVOTS = 'column-pivots',
  AGGREGATES = 'aggregates',
  SORT = 'sort',
  SETTINGS = 'settings',
  LIMIT = 'limit'
}

function view_string_to_view_option(option: string): ViewOption {
  switch(option){
    case 'view': {
      return ViewOption.VIEW;
    }
    case 'index': {
      return ViewOption.INDEX;
    }
    case 'columns': {
      return ViewOption.COLUMNS;
    }
    case 'row-pivots': {
      return ViewOption.ROW_PIVOTS;
    }
    case 'column-pivots': {
      return ViewOption.COLUMN_PIVOTS;
    }
    case 'aggregates': {
      return ViewOption.AGGREGATES;
    }
    case 'sort': {
      return ViewOption.SORT;
    }
    case 'settings': {
      return ViewOption.SETTINGS;
    }
    case 'limit': {
      return ViewOption.LIMIT;
    }
    default: {
      throw 'option not recognized';
    }
  }
}

export type ViewSettings = {
  [ key in ViewOption ]?: string;
}

export enum DataOption {
  DELETE = 'delete',
  WRAP = 'wrap',
  KEY = 'key'
}

// function data_string_to_data_option(option: string): DataOption {
//   switch(option){
//     case 'delete': {
//       return DataOption.DELETE;
//     }
//     case 'wrap': {
//       return DataOption.WRAP;
//     }
//     default: {
//       throw 'option not recognized';
//     }
//   }
// }

export type DataSettings = {
  [ key in DataOption ]?: boolean | string;
}


// TODO pull from perspective/types
export enum TypeNames {
  STRING = 'string',
  FLOAT = 'float',
  INTEGER = 'integer',
  BOOLEAN = 'boolean',
  DATE = 'date',
  DATETIME = 'datetime'
}

// TODO pull from perspective/types
export type Schema = {
  [ key: string ]: TypeNames ;
}

export class PerspectiveHelper {
constructor(url: string,  // The url to fetch data from
            psps: {[key:string]:PSPWidget}, // A set of perspective widgets 
            view_options?: {[psp_key: string]: ViewSettings}, // view options to configure the widgets,
                                                              // keyed by the `psps` keys
            data_options?: {[psp_key: string]: DataSettings}, // data load options to configure the widgets,
                                                              // keyed by the `psps` keys
            schema?: {[psp_key: string]: Schema},    // <optional> schemas to preload onto the widgets,
                                                     // keyed by the `psps` keys
            preload_url?: string,  // The url to fetch initial/cached data from
            repeat?: number) // repeat interval, if http or https
  {  
    this._url = url;
    this._preload_url = preload_url;
    this._datatype = Private.data_source(url);
    this._psp_widgets = psps;
    this._data_options = data_options;
    this._view_options = view_options;

    if (repeat){this._repeat = repeat}
    for (let psp of Object.keys(this._psp_widgets)){
      // preload schema
      if(schema && Object.keys(schema).includes(psp)){
        this._psp_widgets[psp].pspNode.load(schema[psp]);
      }

      // preset view options
      if(view_options && Object.keys(view_options).includes(psp)){
        for (let attr of Object.keys(view_options[psp])){
          let view_option = view_string_to_view_option(attr);
          this._psp_widgets[psp].pspNode.setAttribute(attr, view_options[psp][view_option]);
        }
      }
    }
  }

  start(delay?: number): Promise<number> {
    return new Promise((resolve) => {
      if (this._datatype === 'http'){
        if (this._preload_url){
          this.fetchAndLoad(true).then((count:number) => {
            resolve(count);
          });
        }

        if (this._repeat > 0){
          setInterval(() => {
            this.fetchAndLoad();
          }, this._repeat);
          resolve(0);
        } else {
          this.fetchAndLoad().then((count: number) => {
            resolve(count);
          });
        }
      }
    });
  }

  setUrl(url: string, refetch = true): Promise<number>{
    return new Promise((resolve) => {
      this._url = url;
      if (refetch){
        this.fetchAndLoad().then((count: number)=>{
          resolve(count);
        });
      } else{
        resolve(0);
      }
    });
  }

  fetchAndLoad(use_preload_url = false): Promise<number> {
    let url = '';
    if(use_preload_url && this._preload_url){
      url = this._preload_url;
    } else {
      url = this._url;
    }

    let count = 0;
    let total:number;
    if (this._psp_widgets){
      total = Object.keys(this._psp_widgets).length;

    } else {
      total = 0;
    }

    return new Promise((resolve) => {
      for(let psp of Object.keys(this._psp_widgets)){
        let _delete;
        let wrap;
        let data_key;

        if(this._data_options && Object.keys(this._data_options).includes(psp)){
          //TODO
          if(Object.keys(this._data_options[psp]).includes(DataOption.DELETE)){
            _delete = this._data_options[psp][DataOption.DELETE] || false;
          }
          if(Object.keys(this._data_options[psp]).includes(DataOption.WRAP)){
            wrap = this._data_options[psp][DataOption.WRAP] || false;
          }
          if(Object.keys(this._data_options[psp]).includes(DataOption.KEY)){
            data_key = this._data_options[psp][DataOption.KEY] || '';
          }
        }
        this._fetchAndLoadHttp(url, psp, data_key, wrap, _delete).then(() => {
          count++;
          if (count >= total){
            return resolve(count);
          }
        });
      }
    });
  }

  private _fetchAndLoadHttp(url: string, psp_key: string, data_key?: string | boolean, wrap?: string | boolean, _delete?: string | boolean): Promise<void> {
    return new Promise((resolve) => {
      var xhr1 = new XMLHttpRequest();
      xhr1.open('GET', url, true);
      xhr1.onload = () => { 
        if(xhr1.response){
          let jsn = JSON.parse(xhr1.response);
          if (Object.keys(jsn).length > 0){
            if (wrap){jsn = [jsn];}
            if(_delete){this._psp_widgets[psp_key].pspNode.delete();}
            if(data_key && data_key !== true && data_key !== ''){
              jsn = jsn[data_key];
            }

            // workaround for heatmap non-refresh issue
            if(this._view_options && Object.keys(this._view_options).includes(psp_key)){
              if(Object.keys(this._view_options[psp_key]).includes('view') && this._view_options[psp_key]['view'] == 'heatmap'){
                if(!Object.keys(this._view_options[psp_key]).includes('columns')) {
                  let columns = Object.keys(jsn[0]);
                  var index = columns.indexOf('index');
                  if (index > -1) {
                    columns.splice(index, 1);
                  }
                  this._psp_widgets[psp_key].pspNode.setAttribute('columns', JSON.stringify(columns));
                  this._psp_widgets[psp_key].pspNode.removeAttribute('aggregates');
                }
              }
            }
            if(jsn && jsn.length){
              this._psp_widgets[psp_key].pspNode.update(jsn);
              setTimeout(() => {
                resolve();
              }, 1000);
            } else {
              resolve();
            }
          }
        }
      };
      xhr1.send(null);
    });
  }

  _url: string;
  private _preload_url?: string;
  private _datatype: string;
  private _psp_widgets: {[key:string]:PSPWidget};
  private _data_options?: {[psp_key: string]: DataSettings};
  private _repeat = -1;
  private _view_options?: {[psp_key: string]: ViewSettings};
  // private _worker: any; // TODO make this a shared perspective worker
}


namespace Private {
  export let _loaded = false;

  export function data_source(url: string): string {
    if(url.indexOf('sio://') !== -1){
      return 'sio';
    } else if(url.indexOf('ws://') !== -1){
      return  'ws';
    } else if(url.indexOf('wss://') !== -1){
      return  'wss';
    } else if(url.indexOf('http://') !== -1){
      return  'http';
    } else if(url.indexOf('https://') !== -1){
      return  'http';
    } else if(url.indexOf('comm://') !== -1){
      return  'comm';
    } else{
      return 'http'
    }
  }
}
