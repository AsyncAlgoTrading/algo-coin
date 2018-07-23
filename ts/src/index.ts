/*-----------------------------------------------------------------------------
| Copyright (c) 2014-2017, PhosphorJS Contributors
|
| Distributed under the terms of the BSD 3-Clause License.
|
| The full license is in the file LICENSE, distributed with this software.
|----------------------------------------------------------------------------*/
import 'es6-promise/auto';  // polyfill Promise on IE

import {
  CommandRegistry
} from '@phosphor/commands';

import {
  // BoxPanel, CommandPalette, ContextMenu, DockPanel, MenuBar, Widget, DockLayout, Menu
  BoxPanel, CommandPalette, ContextMenu, DockPanel, MenuBar, Widget, Menu
} from '@phosphor/widgets';

import '../ts/style/index.css';
import "@jpmorganchase/perspective-viewer";
import "@jpmorganchase/perspective-viewer-hypergrid";
import "@jpmorganchase/perspective-viewer-highcharts";

import {
  PSPWidget, PerspectiveHelper, ViewOption, DataOption, TypeNames
} from './perspective-widget';

const commands = new CommandRegistry();

function main(): void {
  window.addEventListener('WebComponentsReady', () => {

    /* File Menu */
    let menu = new Menu({ commands });
    menu.title.label = 'File';
    menu.title.mnemonic = 0;

    menu.addItem({ command: 'controls:open' });
    menu.addItem({ type: 'separator'});

    /* Data Menu */
    let menu2 = new Menu({ commands });
    menu2.title.label = 'Data';
    menu2.title.mnemonic = 0;

    menu2.addItem({ command: 'btc-performance-chart:open' });
    menu2.addItem({ command: 'eth-performance-chart:open' });
    menu2.addItem({ command: 'ltc-performance-chart:open' });
    menu2.addItem({ command: 'bch-performance-chart:open' });
    menu2.addItem({ command: 'performance-grid:open' });
    menu2.addItem({ command: 'quotes:open' });
    menu2.addItem({ type: 'separator'});

    /* layouts menu */
    let menu3 = new Menu({ commands });
    menu3.title.label = 'Layout';
    menu3.title.mnemonic = 0;

    menu3.addItem({ command: 'save-dock-layout'});
    menu3.addItem({ type: 'separator'});
    menu3.addItem({ command: 'restore-dock-layout', args: {index: 0}});

    /* Top bar */
    let bar = new MenuBar();
    bar.addMenu(menu);
    bar.addMenu(menu2);
    bar.addMenu(menu3);
    bar.id = 'menuBar';

    /* context menu */
    let contextMenu = new ContextMenu({ commands });

    document.addEventListener('contextmenu', (event: MouseEvent) => {
      if (contextMenu.open(event)) {
        event.preventDefault();
      }
    });

    contextMenu.addItem({ command: 'controls:open', selector: '.content' });
    contextMenu.addItem({ type: 'separator', selector: '.p-CommandPalette-input' });
    contextMenu.addItem({ command: 'save-dock-layout', selector: '.content' });
    contextMenu.addItem({ command: 'restore-dock-layout', selector: '.content' });

    document.addEventListener('keydown', (event: KeyboardEvent) => {
      commands.processKeydownEvent(event);
    });


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
      },
      'eth-performance-chart': {
        [ViewOption.VIEW]: 'xy_line',
        [ViewOption.INDEX]: 'sequence',
        [ViewOption.COLUMNS]: '["time", "price"]',
      },
      'ltc-performance-chart': {
        [ViewOption.VIEW]: 'xy_line',
        [ViewOption.INDEX]: 'sequence',
        [ViewOption.COLUMNS]: '["time", "price"]',
      },
      'bch-performance-chart': {
        [ViewOption.VIEW]: 'xy_line',
        [ViewOption.INDEX]: 'sequence',
        [ViewOption.COLUMNS]: '["time", "price"]',
      },
      'performance-grid': {
        [ViewOption.VIEW]: 'hypergrid',
        [ViewOption.INDEX]: 'sequence',
        [ViewOption.COLUMNS]: '["time", "price", "volume", "currency_pair", "side"]',
      },
      'quote': {
        [ViewOption.VIEW]: 'hypergrid',
        [ViewOption.INDEX]: 'sequence',
        [ViewOption.COLUMNS]: '["time", "price", "volume", "currency_pair", "side"]',
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
        'time': TypeNames.DATE,
        'price': TypeNames.FLOAT
      },
      'eth-performance-chart': {
        'time': TypeNames.DATE,
        'price': TypeNames.FLOAT
      },
      'ltc-performance-chart': {
        'time': TypeNames.DATE,
        'price': TypeNames.FLOAT
      },
      'bch-performance-chart': {
        'time': TypeNames.DATE,
        'price': TypeNames.FLOAT
      },
      'performance-grid': {
        'time': TypeNames.DATE,
        'price': TypeNames.FLOAT,
        'volume': TypeNames.FLOAT,
        'sequence': TypeNames.INTEGER,
        'currency_pair': TypeNames.STRING,
        'side': TypeNames.STRING,
        'order_type': TypeNames.STRING
      },
      'quote': {
        'time': TypeNames.DATE,
        'price': TypeNames.FLOAT,
        'volume': TypeNames.FLOAT,
        'sequence': TypeNames.INTEGER,
        'currency_pair': TypeNames.STRING,
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
    dock.addWidget(psps1['btc-performance-chart']);
    dock.addWidget(psps5['performance-grid'], { mode: 'split-right', ref: psp });
    dock.addWidget(psps5['quote'], { mode: 'split-bottom', ref: psp });
    dock.addWidget(psps2['eth-performance-chart'], {mode: 'split-right', ref: psp});
    dock.addWidget(psps3['ltc-performance-chart'], {mode: 'split-bottom', ref: psp});
    dock.addWidget(psps4['bch-performance-chart'], {mode: 'split-bottom', ref: psp2});

    dock.id = 'dock';

    /* save/restore layouts */
    let savedLayouts: DockPanel.ILayoutConfig[] = [];

    /* command palette */
    let palette = new CommandPalette({ commands });
    palette.id = 'palette';

    palette.addItem({
      command: 'save-dock-layout',
      category: 'Dock Layout',
      rank: 0
    });

    palette.addItem({
      command: 'controls:open',
      category: 'Dock Layout',
      rank: 0
    });

    palette.addItem({
      command: 'btc-performance-chart:open',
      category: 'Dock Layout',
      rank: 0
    });

    palette.addItem({
      command: 'eth-performance-chart:open',
      category: 'Dock Layout',
      rank: 0
    });

    palette.addItem({
      command: 'ltc-performance-chart:open',
      category: 'Dock Layout',
      rank: 0
    });

    palette.addItem({
      command: 'bch-performance-chart:open',
      category: 'Dock Layout',
      rank: 0
    });

    palette.addItem({
      command: 'performance-grid:open',
      category: 'Dock Layout',
      rank: 0
    });

    palette.addItem({
      command: 'quotes:open',
      category: 'Dock Layout',
      rank: 0
    });

    /* command registry */
    commands.addCommand('save-dock-layout', {
      label: 'Save Layout',
      caption: 'Save the current dock layout',
      execute: () => {
        savedLayouts.push(dock.saveLayout());
        palette.addItem({
          command: 'restore-dock-layout',
          category: 'Dock Layout',
          args: { index: savedLayouts.length - 1 }
        });
        menu3.addItem({ command: 'restore-dock-layout', args: {index: savedLayouts.length - 1}});
      }
    });

    commands.addCommand('restore-dock-layout', {
      label: args => {
        return `Restore Layout ${args.index as number}`;
      },
      execute: args => {
        dock.restoreLayout(savedLayouts[args.index as number]);
      }
    });

    commands.addCommand('controls:open', {
      label: 'Controls',
      mnemonic: 1,
      iconClass: 'fa fa-plus',
      execute: () => {
        dock.restoreLayout(savedLayouts[0]);
      }
    });

    commands.addCommand('btc-performance-chart:open', {
      label: 'Open Performance',
      mnemonic: 2,
      iconClass: 'fa fa-plus',
      execute: () => {
        dock.addWidget(psps1['btc-performance-chart']);
      }
    });

    commands.addCommand('eth-performance-chart:open', {
      label: 'Open Performance',
      mnemonic: 2,
      iconClass: 'fa fa-plus',
      execute: () => {
        dock.addWidget(psps2['eth-performance-chart']);
      }
    });

    commands.addCommand('ltc-performance-chart:open', {
      label: 'Open Performance',
      mnemonic: 2,
      iconClass: 'fa fa-plus',
      execute: () => {
        dock.addWidget(psps3['ltc-performance-chart']);
      }
    });

    commands.addCommand('bch-performance-chart:open', {
      label: 'Open Performance',
      mnemonic: 2,
      iconClass: 'fa fa-plus',
      execute: () => {
        dock.addWidget(psps4['bch-performance-chart']);
      }
    });
    commands.addCommand('performance-grid:open', {
      label: 'Open Performance',
      mnemonic: 2,
      iconClass: 'fa fa-plus',
      execute: () => {
        dock.addWidget(psps5['performance-grid']);
      }
    });

    commands.addCommand('quotes:open', {
      label: 'Open Quotes',
      mnemonic: 2,
      iconClass: 'fa fa-plus',
      execute: () => {
        dock.addWidget(psps5['quote']);
      }
    });

    /* hack for custom sizing */
    var layout = dock.saveLayout();
    // var sizes: number[] = (layout.main as DockLayout.ISplitAreaConfig).sizes;
    // sizes[0] = 0.6;
    // sizes[1] = 0.4;
    dock.restoreLayout(layout);
    savedLayouts.push(dock.saveLayout());
    palette.addItem({
      command: 'restore-dock-layout',
      category: 'Dock Layout',
      args: { index: 0}
    });

    /* main area setup */
    BoxPanel.setStretch(dock, 1);

    let main = new BoxPanel({ direction: 'left-to-right', spacing: 0 });
    main.id = 'main';
    main.addWidget(dock);

    window.onresize = () => { main.update(); };

    Widget.attach(bar, document.body);
    Widget.attach(main, document.body);

    psps_helper1.start();
    psps_helper2.start();
    psps_helper3.start();
    psps_helper4.start();
    psps_helper5.start();
  });
}


window.onload = main;
