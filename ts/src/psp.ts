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
