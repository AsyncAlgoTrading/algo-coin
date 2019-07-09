import {CommandRegistry} from "@phosphor/commands";
import {DockPanel, Menu, MenuBar, Panel} from "@phosphor/widgets";
import {DataLoader, PerspectiveDataLoader} from "phosphor-perspective-utils/data";
import {APIS, COMMAND_ICONS, COMMANDS, INTERVAL} from "./define";
import {build_menu_commands, exchanges_and_instruments, ITab} from "./utils";

export
function buildMarketDataTab(commands: CommandRegistry): ITab {
  /** outer panel to contain menubar and sub widget */
  const marketDataContainer = new Panel();
  marketDataContainer.title.label = "Data";
  marketDataContainer.addClass("marketdata-container");

  const bar = new MenuBar();
  const marketData = new DockPanel();

  /** menu for live data */
  const liveMenu = new Menu({commands});
  liveMenu.title.label = "Live";

  /** Live */
  const trades = new PerspectiveDataLoader("Trades");
  trades.title.closable = true;

  const lastPrice = new PerspectiveDataLoader("Last Price");
  lastPrice.title.closable = true;

  const tradesDataLoader = new DataLoader([trades], APIS.TRADES, {}, INTERVAL.TEN_SECONDS);
  const lastPriceDataLoader = new DataLoader([lastPrice], APIS.LAST_PRICE, {}, INTERVAL.TEN_SECONDS);

  /** trades monitored by backend */
  commands.addCommand(COMMANDS.LIVEDATA_TRADES, {
    execute: () => {
      marketData.addWidget(trades);
      // marketData.activateWidget(trades);
    },
    iconClass: COMMAND_ICONS.LIVEDATA_TRADES,
    label: "Trades",
    mnemonic: 2,
  });
  liveMenu.addItem({ command: COMMANDS.LIVEDATA_TRADES});

  /** Last trades processed by system */
  commands.addCommand(COMMANDS.LIVEDATA_LAST_PRICE, {
    execute: () => {
      marketData.addWidget(lastPrice);
      // marketData.activateWidget(lastTrades);
    },
    iconClass: COMMAND_ICONS.LIVEDATA_TRADES,
    label: "Last Price",
    mnemonic: 2,
  });
  liveMenu.addItem({ command: COMMANDS.LIVEDATA_LAST_PRICE});

  const tradesMenu = new Menu({commands});
  tradesMenu.title.label = "Trades - Exchange";

  /** Trades by exchange/asset */
  exchanges_and_instruments().then((res: {[key: string]: string[]}) => {
    build_menu_commands(res, commands, tradesMenu, COMMANDS.LIVEDATA_TRADES_BY_EXCH_ASSET);
  });
  liveMenu.addItem({type: "submenu", submenu: tradesMenu});

  /** menu for historical data */
  const historicalMenu = new Menu({commands});
  historicalMenu.title.label = "Historical";

  const priceData = new Menu({commands});
  priceData.title.label = "OHLCV";
  historicalMenu.addItem({type: "submenu", submenu: priceData});

  exchanges_and_instruments().then((res: {[key: string]: string[]}) => {
    build_menu_commands(res, commands, priceData, COMMANDS.HISTORICALDATA_OHLCV);
  });

  /** Assemble bar */
  bar.addMenu(liveMenu);
  bar.addMenu(historicalMenu);
  marketDataContainer.addWidget(bar);
  marketDataContainer.addWidget(marketData);

  return {loaders: [tradesDataLoader, lastPriceDataLoader],
          menus: [],
          perspectives: [trades, lastPrice],
          tab: marketDataContainer};
}
