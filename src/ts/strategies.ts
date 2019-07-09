import {CommandRegistry} from "@phosphor/commands";
import {DockPanel, SplitPanel} from "@phosphor/widgets";
import {DataLoader, PerspectiveDataLoader} from "phosphor-perspective-utils/data";
import {APIS, INTERVAL} from "./define";
import {ITab} from "./utils";

export
function buildStrategiesTab(commands: CommandRegistry): ITab {
  const strategies = new DockPanel();
  strategies.id = "strategies";
  strategies.title.label = "Strategies";

  const stratsList = new PerspectiveDataLoader("Strategies");
  strategies.addWidget(stratsList);
  const stratsLoader = new DataLoader([stratsList], APIS.STRATEGIES);

  const sp = new SplitPanel({orientation: "vertical"});
  sp.title.label = "Trading";

  const stratRequestList = new PerspectiveDataLoader("Trade Reqs");
  sp.addWidget(stratRequestList);
  const stratRequestLoader = new DataLoader([stratRequestList], APIS.STRATEGY_TRADE_REQUESTS, {}, INTERVAL.TEN_SECONDS);

  const stratResponseList = new PerspectiveDataLoader("Trade Resps");
  sp.addWidget(stratResponseList);
// tslint:disable-next-line: max-line-length
  const stratResponseLoader = new DataLoader([stratResponseList], APIS.STRATEGY_TRADE_RESPONSES, {}, INTERVAL.TEN_SECONDS);

  strategies.addWidget(sp, {ref: stratsList, mode: "split-right"});

  const backtest = new DockPanel();
  backtest.title.label = "Backtest";
  strategies.addWidget(backtest, {ref: stratsList, mode: "split-bottom"});

  return {loaders: [stratsLoader, stratRequestLoader, stratResponseLoader],
          menus: [],
          perspectives: [stratsList, stratRequestList, stratResponseList],
          tab: strategies};
}
