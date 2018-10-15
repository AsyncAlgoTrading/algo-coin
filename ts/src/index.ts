import 'es6-promise/auto';  // polyfill Promise on IE

import {
  CommandRegistry
} from '@phosphor/commands';

import {
  TabPanel, BoxPanel, DockPanel, MenuBar, Widget, Menu
} from '@phosphor/widgets';

import '../ts/style/index.css';
import "@jpmorganchase/perspective-viewer";
import "@jpmorganchase/perspective-viewer-hypergrid";
import "@jpmorganchase/perspective-viewer-highcharts";

import {PSPWidget, PerspectiveHelper, ViewOption, DataOption, TypeNames} from './perspective-widget';
import {Header} from './header';


const commands = new CommandRegistry();

function main(): void {
  // window.addEventListener('WebComponentsReady', () => {

    /* File Menu */
    let menu = new Menu({ commands });
    menu.title.label = 'About';
    menu.title.mnemonic = 0;

    let loader = document.createElement('div');
    loader.classList.add('loader');
    let loader_icon = document.createElement('div');
    loader_icon.classList.add('loader_icon');
    loader.appendChild(loader_icon);
    document.body.appendChild(loader);

    /* Title bar */
    let header = new Header();

    /* Top bar */
    let bar = new MenuBar();
    bar.addMenu(menu);
    bar.id = 'menuBar';

    /* perspectives */
    let psp = new PSPWidget('BTC-perf-chart');  // chart
    let psp2 = new PSPWidget('ETH-perf-chart');  // chart
    let psp3 = new PSPWidget('LTC-perf-chart');  // chart
    let psp4 = new PSPWidget('BCH-perf-chart');  // chart
    let psp5 = new PSPWidget('Perf-grid');  // grid
    let psp6 = new PSPWidget('Quotes');  // quote

    let psps1 = {'btc-performance-chart':psp}
    let psps2 = {'eth-performance-chart':psp2}
    let psps3 = {'ltc-performance-chart':psp3}
    let psps4 = {'bch-performance-chart':psp4}
    let psps5 = {'performance-grid':psp5,
                 'quote':psp6}

    let psps_view_options = {
      'btc-performance-chart': {
        [ViewOption.VIEW]: 'xy_line',
        [ViewOption.INDEX]: 'sequence',
        [ViewOption.COLUMNS]: '["time", "price"]',
        [ViewOption.ROW_PIVOTS]: '["time"]',
        [ViewOption.AGGREGATES]: '{"time":"last", "price":"last"}',
        [ViewOption.SORT]: '["time"]',
        [ViewOption.LIMIT]: '100'
      },
      'eth-performance-chart': {
        [ViewOption.VIEW]: 'xy_line',
        [ViewOption.INDEX]: 'sequence',
        [ViewOption.COLUMNS]: '["time", "price"]',
        [ViewOption.ROW_PIVOTS]: '["time"]',
        [ViewOption.AGGREGATES]: '{"time":"last", "price":"last"}',
        [ViewOption.SORT]: '["time"]',
        [ViewOption.LIMIT]: '100'
      },
      'ltc-performance-chart': {
        [ViewOption.VIEW]: 'xy_line',
        [ViewOption.INDEX]: 'sequence',
        [ViewOption.COLUMNS]: '["time", "price"]',
        [ViewOption.ROW_PIVOTS]: '["time"]',
        [ViewOption.AGGREGATES]: '{"time":"last", "price":"last"}',
        [ViewOption.SORT]: '["time"]',
        [ViewOption.LIMIT]: '100'
      },
      'bch-performance-chart': {
        [ViewOption.VIEW]: 'xy_line',
        [ViewOption.INDEX]: 'sequence',
        [ViewOption.COLUMNS]: '["time", "price"]',
        [ViewOption.ROW_PIVOTS]: '["time"]',
        [ViewOption.AGGREGATES]: '{"time":"last", "price":"last"}',
        [ViewOption.SORT]: '["time"]',
        [ViewOption.LIMIT]: '100'
      },
      'performance-grid': {
        [ViewOption.VIEW]: 'hypergrid',
        [ViewOption.INDEX]: 'sequence',
        [ViewOption.COLUMNS]: '["time", "price", "volume", "underlying", "side"]',
        [ViewOption.SORT]: '["time"]',
        [ViewOption.LIMIT]: '100'
      },
      'quote': {
        [ViewOption.VIEW]: 'hypergrid',
        [ViewOption.INDEX]: 'sequence',
        [ViewOption.COLUMNS]: '["time", "price", "volume", "underlying", "side"]',
        [ViewOption.SORT]: '["time"]',
        [ViewOption.LIMIT]: '100'
      }
    };

    let psps_data_options = {
     'btc-performance-chart': {
       [DataOption.DELETE]: false,
       [DataOption.WRAP]: false
      },
     'eth-performance-chart': {
       [DataOption.DELETE]: false,
       [DataOption.WRAP]: false
      },
     'ltc-performance-chart': {
       [DataOption.DELETE]: false,
       [DataOption.WRAP]: false
      },
     'bch-performance-chart': {
       [DataOption.DELETE]: false,
       [DataOption.WRAP]: false
      },
      'performance-grid': {
       [DataOption.DELETE]: false,
       [DataOption.WRAP]: false
      },
      'quote': {
       [DataOption.DELETE]: false,
       [DataOption.WRAP]: false
      } 
    };

    let psps_schemas = {
      'btc-performance-chart': {
        'time': TypeNames.DATETIME,
        'price': TypeNames.FLOAT
      },
      'eth-performance-chart': {
        'time': TypeNames.DATETIME,
        'price': TypeNames.FLOAT
      },
      'ltc-performance-chart': {
        'time': TypeNames.DATETIME,
        'price': TypeNames.FLOAT
      },
      'bch-performance-chart': {
        'time': TypeNames.DATETIME,
        'price': TypeNames.FLOAT
      },
      'performance-grid': {
        'time': TypeNames.DATETIME,
        'price': TypeNames.FLOAT,
        'volume': TypeNames.FLOAT,
        'sequence': TypeNames.INTEGER,
        'underlying': TypeNames.STRING,
        'side': TypeNames.STRING,
        'order_type': TypeNames.STRING
      },
      'quote': {
        'time': TypeNames.DATETIME,
        'price': TypeNames.FLOAT,
        'volume': TypeNames.FLOAT,
        'sequence': TypeNames.INTEGER,
        'underlying': TypeNames.STRING,
        'side': TypeNames.STRING,
        'order_type': TypeNames.STRING
      }
    };

    let psps_helper1 = new PerspectiveHelper('/api/json/v1/messages?type=TRADE&pair=BTCUSD',
                                             psps1,
                                             psps_view_options,
                                             psps_data_options,
                                             psps_schemas,
                                             '/api/json/v1/messages?type=TRADE&page=-1&pair=BTCUSD',
                                             500);

    let psps_helper2 = new PerspectiveHelper('/api/json/v1/messages?type=TRADE&pair=ETHUSD',
                                             psps2,
                                             psps_view_options,
                                             psps_data_options,
                                             psps_schemas,
                                             '/api/json/v1/messages?type=TRADE&page=-1&pair=ETHUSD',
                                             500);

    let psps_helper3 = new PerspectiveHelper('/api/json/v1/messages?type=TRADE&pair=LTCUSD',
                                             psps3,
                                             psps_view_options,
                                             psps_data_options,
                                             psps_schemas,
                                             '/api/json/v1/messages?type=TRADE&page=-1&pair=LTCUSD',
                                             500);

    let psps_helper4 = new PerspectiveHelper('/api/json/v1/messages?type=TRADE&pair=BCHUSD',
                                             psps4,
                                             psps_view_options,
                                             psps_data_options,
                                             psps_schemas,
                                             '/api/json/v1/messages?type=TRADE&page=-1&pair=BCHUSD',
                                             500);

    let psps_helper5 = new PerspectiveHelper('/api/json/v1/messages?type=TRADE',
                                             psps5,
                                             psps_view_options,
                                             psps_data_options,
                                             psps_schemas,
                                             '/api/json/v1/messages?type=TRADE&page=-1',
                                             500);


    /* main dock */
    let dock = new DockPanel();
    dock.title.label = 'Trades';
    dock.addWidget(psps1['btc-performance-chart']);
    dock.addWidget(psps2['eth-performance-chart'], {mode: 'split-right', ref: psp});
    dock.addWidget(psps3['ltc-performance-chart'], {mode: 'split-bottom', ref: psp});
    dock.addWidget(psps4['bch-performance-chart'], {mode: 'split-bottom', ref: psp2});
    dock.id = 'dock';

    /* main area setup */
    BoxPanel.setStretch(dock, 1);

    let main = new TabPanel();
    main.id = 'main';
    main.addWidget(dock);
    main.addWidget(psps5['performance-grid']);
    main.addWidget(psps5['quote']);

    window.onresize = () => { main.update(); };

    Widget.attach(header, document.body);
    Widget.attach(bar, document.body);
    Widget.attach(main, document.body);

    loader.style.display = 'flex';

    setTimeout(()=>{
      psps_helper1.start();
      psps_helper2.start();
      psps_helper3.start();
      psps_helper4.start();
      psps_helper5.start();
      loader.style.display = 'none';
    }, 2000);
}


window.onload = main;
