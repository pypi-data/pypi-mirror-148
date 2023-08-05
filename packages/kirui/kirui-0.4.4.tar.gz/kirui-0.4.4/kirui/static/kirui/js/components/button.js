import * as m from "../core/component.js";
import * as Popper from "https://unpkg.com/@popperjs/core@2";


class EditButtonGroup extends m.Component {
    constructor() {
        super();
    }

    open(ev) {
        ev.stopPropagation();
        ev.preventDefault();

        let event = new Event('click');
        window.dispatchEvent(event);

        // this.querySelector('.dropdown-menu').classList.add('show');
        let parent_rect = this.querySelector('.parent').getBoundingClientRect();
        for (let el of this.getElementsByClassName('dropdown-menu')) {
            if (el.classList.contains('show')) {
                el.classList.remove('show');
            } else {
                el.classList.add('show');
                let rect = el.getBoundingClientRect();
                if (rect.right > window.innerWidth) {
                    let left = rect.width - this.querySelector('button').getBoundingClientRect().width;
                    el.style['left'] = `-${left}px`;
                }

                if (rect.bottom > window.innerHeight) {
                    el.style['top'] = `-${rect.height}px`;
                }
            }
        }
    }

    render() {
        return m.html`
          <div class="parent" style="position: relative;">
            <div class="btn-group">
              <button type="button" class="btn btn-outline-secondary dropdown-toggle" @click="${this.open}"></button>
            </div>
            <div class="dropdown-menu">${this.$children}</div>
          </div>
        `
    }
}
customElements.define("kr-button-group", EditButtonGroup)
