import { DOMView } from "../../core/dom_view";
import type { ToolbarView } from "./toolbar";
import type { Tool } from "./tool";
export declare abstract class ToolButtonView extends DOMView {
    model: Tool;
    readonly parent: ToolbarView;
    el: HTMLElement;
    private _hammer;
    private _menu?;
    initialize(): void;
    remove(): void;
    styles(): string[];
    css_classes(): string[];
    render(): void;
    protected abstract _clicked(): void;
    protected _pressed(): void;
}
//# sourceMappingURL=tool_button.d.ts.map