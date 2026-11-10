/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { OdooCommunityAssistantDrawer } from "./ai_assistant_drawer";

export class OdooCommunityAssistantSystray extends Component {
    static template = "odoo_community_ai.SystrayIcon";
    static components = { OdooCommunityAssistantDrawer };

    setup() {
        this.state = useState({ isOpen: false });
    }

    toggleDrawer() {
        this.state.isOpen = !this.state.isOpen;
    }
}

registry.category("systray").add(
    "OdooCommunityAssistantSystray",
    { Component: OdooCommunityAssistantSystray },
    { sequence: 95 }
);
