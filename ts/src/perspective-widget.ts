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
    this.title.closable = true;
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
  SETTINGS = 'settings'
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
  DATE = 'date'
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

    if (repeat){this._repeat = repeat}
    for (let psp of Object.keys(this._psp_widgets)){
      // preload schema
      if(schema && Object.keys(schema).includes(psp)){
        this._psp_widgets[psp].pspNode.addEventListener('perspective-ready', ()=>{
          this._psp_widgets[psp].pspNode.load(schema[psp]);
        });
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

  start(delay?: number): void {
    if (this._datatype === 'http'){
      if (this._preload_url){
        if(delay){
          setTimeout(() => {this.fetch_and_load(true);}, delay);

        } else {
          this.fetch_and_load(true);
        }
      }

      if (this._repeat > 0){
        setInterval(() => {
          this.fetch_and_load();
        }, this._repeat);
      } else {
        this.fetch_and_load();
      }
    }
  }

  fetch_and_load(use_preload_url = false): void {
    let url = '';
    if(use_preload_url && this._preload_url){
      url = this._preload_url;
    } else {
      url = this._url;
    }

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
      this._fetch_and_load_http(url, psp, data_key, wrap, _delete);
    }
  }

  private _fetch_and_load_http(url: string, psp_key: string, data_key?: string | boolean, wrap?: string | boolean, _delete?: string | boolean): void {
    var xhr1 = new XMLHttpRequest();
    xhr1.open('GET', url, true);
    xhr1.onload = () => { 
      if(xhr1.response){
        var jsn = JSON.parse(xhr1.response);
        if (Object.keys(jsn).length > 0){
          if (wrap){jsn = [jsn];}
          if(_delete){this._psp_widgets[psp_key].pspNode.delete();}
          if(data_key && data_key !== true && data_key !== ''){jsn = jsn[data_key];}
          this._psp_widgets[psp_key].pspNode.update(jsn);
        }
      }
    };
    xhr1.send(null);
  }

  _url: string;
  private _preload_url?: string;
  private _datatype: string;
  private _psp_widgets: {[key:string]:PSPWidget};
  private _data_options?: {[psp_key: string]: DataSettings};
  private _repeat = -1;
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
      return 'http';
    }
  }
}
