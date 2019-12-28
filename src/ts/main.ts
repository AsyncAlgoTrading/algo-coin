// tslint:disable: no-empty
import perspective from "@finos/perspective";
import { PerspectiveWidget, PerspectiveWorkspace } from "@finos/perspective-phosphor";
import { CommandRegistry } from "@phosphor/commands";
import { DockPanel, SplitPanel, Widget } from "@phosphor/widgets";

import "@finos/perspective-viewer-d3fc";
import "@finos/perspective-viewer-hypergrid";

import { buildMenubar, constructCommands, Header, loggedIn, LoginWidget, LogoutWidget, RegisterWidget, setupSidepanel } from "tkp_utils";

import {LOGIN, LOGOUT, REGISTER} from "./define";

export const commands = new CommandRegistry();

export
    async function main() {
    // connect to perspective
    const websocket = perspective.websocket("ws:0.0.0.0:8080/api/v1/ws");
    const accountsTable = websocket.open_table("accounts");

    // perspective workspace
    const workspace = new PerspectiveWorkspace();
    workspace.addClass("workspace");
    workspace.title.label = "Workspace";

    const accountsWidget = new PerspectiveWidget("Accounts");

    // main container
    const mainPage = new SplitPanel({ orientation: "horizontal" });
    const centerPage = new DockPanel();
    mainPage.addWidget(centerPage);
    centerPage.addWidget(workspace);

    // top bar
    const header = new Header();

    // Login helpers
    const login = new LoginWidget(LOGIN);
    const logout = new LogoutWidget(LOGOUT);
    const register = new RegisterWidget(REGISTER);

    // helper to clear sidebar
    const setSidePanel = setupSidepanel(mainPage, false);

    // setup commands
    constructCommands(commands, [
        {
            execute: () => { },
            iconClass: "fa fa-question",
            isEnabled: () => true,
            label: "About",
            name: "About",
        },
        {
            execute: () => { setSidePanel(register); },
            iconClass: "fa fa-pencil-square-o",
            isEnabled: () => !loggedIn(),
            label: "Register",
            name: "register",
        },
        {
            execute: () => { setSidePanel(login); },
            iconClass: "fa fa-sign-in",
            isEnabled: () => !loggedIn(),
            label: "Login",
            name: "login",
        },
        {
            execute: () => { setSidePanel(logout); },
            iconClass: "fa fa-sign-out",
            isEnabled: loggedIn,
            label: "Logout",
            name: "logout",
        },
    ]);

    // Construct top menu
    const menubar = buildMenubar(commands, 'Settings', 'settings', [
      {
        class: 'settings',
        commands: ['about'],
      },
      {
        class: 'settings',
        commands: ['register', 'login', 'logout'],
        name: 'Login/Register',
      },
    ]);
    menubar.addClass("topmenu");

    // Add tables to workspace
    workspace.addViewer(accountsWidget, {});

    // Attach parts to dom
    Widget.attach(header, document.body);
    Widget.attach(menubar, document.body);
    Widget.attach(mainPage, document.body);

    // Load perspective tables
    accountsWidget.load(accountsTable);

    window.onresize = () => {
        mainPage.update();
    };
    (window as any).workspace = workspace;
}
