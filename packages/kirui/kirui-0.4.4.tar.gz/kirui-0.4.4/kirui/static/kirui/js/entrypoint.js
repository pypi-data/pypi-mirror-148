import * as sideBar from "./components/layout/sidebar.js";
import * as Form from "./components/forms/index.js";
import * as Modal from "./components/modal.js";
import * as Table from "./components/tables/index.js";
import * as Chart from "./components/charts/index.js";
import * as Button from "./components/button.js";
import { html, render } from "./core/component.js";

const entrypoint = (content) => {
    render(content, document.body);
}

export { entrypoint, html };
