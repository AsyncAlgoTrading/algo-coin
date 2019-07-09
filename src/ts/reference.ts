import {CommandRegistry} from "@phosphor/commands";
import {DockPanel} from "@phosphor/widgets";
import {DataLoader, PerspectiveDataLoader} from "phosphor-perspective-utils/data";
import {APIS, INTERVAL} from "./define";
import {ITab} from "./utils";

export
function buildReferenceTab(commands: CommandRegistry): ITab {
  const reference = new DockPanel();
  reference.id = "accounts";
  reference.title.label = "Reference";

  const accountsList = new PerspectiveDataLoader("Accounts");
  reference.addWidget(accountsList);
  const accountsLoader = new DataLoader([accountsList], APIS.ACCOUNTS, {}, INTERVAL.FIVE_MINUTES);

  const instrumentList = new PerspectiveDataLoader("Instruments");
  reference.addWidget(instrumentList, {ref: accountsList, mode: "split-right"});
  const instrumentsLoader = new DataLoader([instrumentList], APIS.INSTRUMENTS, {}, INTERVAL.FIVE_MINUTES);

  const exchangeList = new PerspectiveDataLoader("Exchanges");
  reference.addWidget(exchangeList, {ref: instrumentList, mode: "split-bottom"});
  const exchangeLoader = new DataLoader([exchangeList], APIS.EXCHANGES, {}, INTERVAL.FIVE_MINUTES);

  return {loaders: [accountsLoader, instrumentsLoader, exchangeLoader],
          menus: [],
          perspectives: [accountsList, instrumentList, exchangeList],
          tab: reference};
}
