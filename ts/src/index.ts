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
  BoxPanel, CommandPalette, ContextMenu, DockPanel, MenuBar, Widget, DockLayout, Menu
} from '@phosphor/widgets';

import '../ts/style/index.css';
import "@jpmorganchase/perspective-viewer";
import "@jpmorganchase/perspective-viewer-hypergrid";
import "@jpmorganchase/perspective-viewer-highcharts";

import {
  PSPWidget, PerspectiveHelper, ViewOption, DataOption
} from './perspective-widget';

const commands = new CommandRegistry();

function main(): void {
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

  menu2.addItem({ command: 'performance-chart:open' });
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
  let psp = new PSPWidget('Perf-chart');  // chart
  let psp2 = new PSPWidget('Perf-grid');  // grid
  let psp3 = new PSPWidget('Quotes');  // quote

  let psps= {'performance-chart':psp,
             'performance-grid':psp2,
             'quote':psp3}

  let psps_view_options = {
    'performance-chart': {
      [ViewOption.VIEW]: 'xy_line',
      [ViewOption.INDEX]: 'sequence',
      [ViewOption.COLUMN_PIVOTS]: '["currency_pair"]',
      [ViewOption.COLUMNS]: '["time", "price"]'
    },
    'performance-grid': {
      [ViewOption.VIEW]: 'hypergrid',
      [ViewOption.INDEX]: 'sequence'
    },
    'quote': {}
  };

  let psps_data_options = {
   'performance-chart': {
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

  let psps_schemas = {};

  let psps_helper1 = new PerspectiveHelper('/api/json/v1/messages?type=TRADE',
                                           psps,
                                           psps_view_options,
                                           psps_data_options,
                                           psps_schemas,
                                           '/api/json/v1/messages?type=TRADE&page=-1',
                                           500);

  /* main dock */
  let dock = new DockPanel();
  dock.addWidget(psps['performance-chart']);
  dock.addWidget(psps['performance-grid'], { mode: 'split-right', ref: psp });
  dock.addWidget(psps['quote'], { mode: 'split-bottom', ref: psp });

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
    command: 'performance-chart:open',
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

  commands.addCommand('performance-chart:open', {
    label: 'Open Performance',
    mnemonic: 2,
    iconClass: 'fa fa-plus',
    execute: () => {
      dock.addWidget(psps['performance-chart']);
    }
  });

  commands.addCommand('performance-grid:open', {
    label: 'Open Performance',
    mnemonic: 2,
    iconClass: 'fa fa-plus',
    execute: () => {
      dock.addWidget(psps['performance-grid']);
    }
  });

  commands.addCommand('quotes:open', {
    label: 'Open Quotes',
    mnemonic: 2,
    iconClass: 'fa fa-plus',
    execute: () => {
      dock.addWidget(psps['quote']);
    }
  });

  /* hack for custom sizing */
  var layout = dock.saveLayout();
  var sizes: number[] = (layout.main as DockLayout.ISplitAreaConfig).sizes;
  sizes[0] = 0.6;
  sizes[1] = 0.4;
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
}


window.onload = main;
