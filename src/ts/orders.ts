import {CommandRegistry} from "@phosphor/commands";
import {DockPanel} from "@phosphor/widgets";
// import {DataLoader, PerspectiveDataLoader} from "phosphor-perspective-utils/data";
import {PerspectiveDataLoader} from "phosphor-perspective-utils/data";
// import {APIS} from "./define";
import {OrderEntry} from "./order_entry";
import {ITab} from "./utils";

export
function buildOrderEntryTab(commands: CommandRegistry): ITab {
  const oe = new DockPanel();
  oe.title.label = "Manual";

  const myOrdersList = new PerspectiveDataLoader("Orders");
  oe.addWidget(myOrdersList);
  // const myOrdersLoader = new DataLoader([myOrdersList], APIS.MYORDERS, {}, 1000);

  const myTradesList = new PerspectiveDataLoader("Trades");
  oe.addWidget(myTradesList);
  // const myTradesLoader = new DataLoader([myTradesList], APIS.MYTRADES, {}, 1000);

  const manual = new OrderEntry();
  manual.title.label = "Order Entry";
  oe.addWidget(manual);

  // return {tab: oe, loaders: [myOrdersLoader, myTradesLoader], perspectives: [myOrdersList, myTradesList], menus: []};
  return {tab: oe, loaders: [], perspectives: [myOrdersList, myTradesList], menus: []};
}
