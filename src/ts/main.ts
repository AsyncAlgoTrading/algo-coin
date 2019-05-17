import {BoxPanel, DockPanel, MenuBar, TabPanel, Widget} from "@phosphor/widgets";
// import {BoxPanel, DockLayout, DockPanel, MenuBar, TabPanel, Widget} from "@phosphor/widgets";

import {DataLoader, PerspectiveDataLoader} from "phosphor-perspective-utils/data";
import {Header} from "phosphor-perspective-utils/header";
import {hideLoader, showLoader} from "phosphor-perspective-utils/loader";

export
function main(): void {
  // tslint:disable-next-line: no-shadowed-variable
  const main = new TabPanel();
  main.id = "main";

  /* File bar */
  const bar = new MenuBar();
  bar.id = "menuBar";

  const dock = new DockPanel();
  dock.id = "dock";
  dock.title.label = "Home";

  showLoader();
  hideLoader(1000);

  const accounts = new PerspectiveDataLoader("Accounts");
  dock.addWidget(accounts);

  const data = new PerspectiveDataLoader("Data");
  dock.addWidget(data);

  const dataLoader = new DataLoader([data], "/api/json/v1/messages", {pair: "BTCUSD", type: "TRADE"});
  dataLoader.start();

  const accountsLoader = new DataLoader([accounts], "/api/json/v1/accounts");
  accountsLoader.start();

  /* save/restore layouts */
  // let savedLayouts: DockPanel.ILayoutConfig[] = [];
  // savedLayouts.push(dock.saveLayout());

  /* hack for custom sizing */
  // const layout = dock.saveLayout();
  // const sizes: number[] = (layout.main as DockLayout.ISplitAreaConfig).sizes;
  // sizes[0] = 0.25;
  // sizes[1] = 0.75;
  // dock.restoreLayout(layout);

  /* main area setup */
  BoxPanel.setStretch(dock, 1);
  main.addWidget(dock);

  /* Title bar */
  const header = new Header([accounts, data]);

  window.onresize = () => { main.update(); };
  Widget.attach(header, document.body);
  Widget.attach(bar, document.body);
  Widget.attach(main, document.body);
}
