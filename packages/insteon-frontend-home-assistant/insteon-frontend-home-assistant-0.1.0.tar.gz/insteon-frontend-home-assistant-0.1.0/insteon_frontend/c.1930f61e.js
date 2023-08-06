import{J as e,h as t,_ as a,s as i,e as o,y as r,t as s,$ as n,O as l,R as d,f as h,r as c,n as p,l as u,j as v,k as b,z as f,i as k}from"./entrypoint-4b72043f.js";import{r as m}from"./c.ba88c3a2.js";import{i as g}from"./c.813ffe65.js";customElements.define("ha-service-description",class extends e{static get template(){return t` [[_getDescription(hass, domain, service)]] `}static get properties(){return{hass:Object,domain:String,service:String}}_getDescription(e,t,a){const i=e.services[t];if(!i)return"";const o=i[a];return o?o.description:""}});a([p("ha-tab")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[o({type:Boolean,reflect:!0})],key:"active",value:()=>!1},{kind:"field",decorators:[o({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[o()],key:"name",value:void 0},{kind:"field",decorators:[r("mwc-ripple")],key:"_ripple",value:void 0},{kind:"field",decorators:[s()],key:"_shouldRenderRipple",value:()=>!1},{kind:"method",key:"render",value:function(){return n`
      <div
        tabindex="0"
        role="tab"
        aria-selected=${this.active}
        aria-label=${l(this.name)}
        @focus=${this.handleRippleFocus}
        @blur=${this.handleRippleBlur}
        @mousedown=${this.handleRippleActivate}
        @mouseup=${this.handleRippleDeactivate}
        @mouseenter=${this.handleRippleMouseEnter}
        @mouseleave=${this.handleRippleMouseLeave}
        @touchstart=${this.handleRippleActivate}
        @touchend=${this.handleRippleDeactivate}
        @touchcancel=${this.handleRippleDeactivate}
        @keydown=${this._handleKeyDown}
      >
        ${this.narrow?n`<slot name="icon"></slot>`:""}
        ${!this.narrow||this.active?n`<span class="name">${this.name}</span>`:""}
        ${this._shouldRenderRipple?n`<mwc-ripple></mwc-ripple>`:""}
      </div>
    `}},{kind:"field",key:"_rippleHandlers",value(){return new d(()=>(this._shouldRenderRipple=!0,this._ripple))}},{kind:"method",key:"_handleKeyDown",value:function(e){13===e.keyCode&&e.target.click()}},{kind:"method",decorators:[h({passive:!0})],key:"handleRippleActivate",value:function(e){this._rippleHandlers.startPress(e)}},{kind:"method",key:"handleRippleDeactivate",value:function(){this._rippleHandlers.endPress()}},{kind:"method",key:"handleRippleMouseEnter",value:function(){this._rippleHandlers.startHover()}},{kind:"method",key:"handleRippleMouseLeave",value:function(){this._rippleHandlers.endHover()}},{kind:"method",key:"handleRippleFocus",value:function(){this._rippleHandlers.startFocus()}},{kind:"method",key:"handleRippleBlur",value:function(){this._rippleHandlers.endFocus()}},{kind:"get",static:!0,key:"styles",value:function(){return c`
      div {
        padding: 0 32px;
        display: flex;
        flex-direction: column;
        text-align: center;
        box-sizing: border-box;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: var(--header-height);
        cursor: pointer;
        position: relative;
        outline: none;
      }

      .name {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
      }

      :host([active]) {
        color: var(--primary-color);
      }

      :host(:not([narrow])[active]) div {
        border-bottom: 2px solid var(--primary-color);
      }

      :host([narrow]) {
        min-width: 0;
        display: flex;
        justify-content: center;
        overflow: hidden;
      }

      :host([narrow]) div {
        padding: 0 4px;
      }
    `}}]}}),i),a([p("hass-tabs-subpage")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[o({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[o({type:Boolean})],key:"supervisor",value:()=>!1},{kind:"field",decorators:[o({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[o({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[o()],key:"backCallback",value:void 0},{kind:"field",decorators:[o({type:Boolean,attribute:"main-page"})],key:"mainPage",value:()=>!1},{kind:"field",decorators:[o({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[o({attribute:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[o({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[o({type:Boolean,reflect:!0,attribute:"is-wide"})],key:"isWide",value:()=>!1},{kind:"field",decorators:[o({type:Boolean,reflect:!0})],key:"rtl",value:()=>!1},{kind:"field",decorators:[s()],key:"_activeTab",value:void 0},{kind:"field",decorators:[m(".content")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_getTabs",value(){return u((e,t,a,i,o,r,s)=>e.filter(e=>{return(!e.component||e.core||(t=this.hass,i=e.component,t&&t.config.components.includes(i)))&&(!e.advancedOnly||a);var t,i}).map(e=>n`
            <a href=${e.path}>
              <ha-tab
                .hass=${this.hass}
                .active=${e.path===(null==t?void 0:t.path)}
                .narrow=${this.narrow}
                .name=${e.translationKey?s(e.translationKey):e.name}
              >
                ${e.iconPath?n`<ha-svg-icon
                      slot="icon"
                      .path=${e.iconPath}
                    ></ha-svg-icon>`:""}
              </ha-tab>
            </a>
          `))}},{kind:"method",key:"willUpdate",value:function(e){if(e.has("route")&&(this._activeTab=this.tabs.find(e=>`${this.route.prefix}${this.route.path}`.includes(e.path))),e.has("hass")){const t=e.get("hass");t&&t.language===this.hass.language||(this.rtl=g(this.hass))}v(b(a.prototype),"willUpdate",this).call(this,e)}},{kind:"method",key:"render",value:function(){var e,t;const a=this._getTabs(this.tabs,this._activeTab,null===(e=this.hass.userData)||void 0===e?void 0:e.showAdvanced,this.hass.config.components,this.hass.language,this.narrow,this.localizeFunc||this.hass.localize),i=a.length>1||!this.narrow;return n`
      <div class="toolbar">
        ${this.mainPage||!this.backPath&&null!==(t=history.state)&&void 0!==t&&t.root?n`
              <ha-menu-button
                .hassio=${this.supervisor}
                .hass=${this.hass}
                .narrow=${this.narrow}
              ></ha-menu-button>
            `:this.backPath?n`
              <a href=${this.backPath}>
                <ha-icon-button-arrow-prev
                  .hass=${this.hass}
                ></ha-icon-button-arrow-prev>
              </a>
            `:n`
              <ha-icon-button-arrow-prev
                .hass=${this.hass}
                @click=${this._backTapped}
              ></ha-icon-button-arrow-prev>
            `}
        ${this.narrow?n`<div class="main-title"><slot name="header"></slot></div>`:""}
        ${i?n`
              <div id="tabbar" class=${f({"bottom-bar":this.narrow})}>
                ${a}
              </div>
            `:""}
        <div id="toolbar-icon">
          <slot name="toolbar-icon"></slot>
        </div>
      </div>
      <div
        class="content ${f({tabs:i})}"
        @scroll=${this._saveScrollPos}
      >
        <slot></slot>
      </div>
      <div id="fab" class=${f({tabs:i})}>
        <slot name="fab"></slot>
      </div>
    `}},{kind:"method",decorators:[h({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return c`
      :host {
        display: block;
        height: 100%;
        background-color: var(--primary-background-color);
      }

      :host([narrow]) {
        width: 100%;
        position: fixed;
      }

      ha-menu-button {
        margin-right: 24px;
      }

      .toolbar {
        display: flex;
        align-items: center;
        font-size: 20px;
        height: var(--header-height);
        background-color: var(--sidebar-background-color);
        font-weight: 400;
        border-bottom: 1px solid var(--divider-color);
        padding: 0 16px;
        box-sizing: border-box;
      }
      .toolbar a {
        color: var(--sidebar-text-color);
        text-decoration: none;
      }
      .bottom-bar a {
        width: 25%;
      }

      #tabbar {
        display: flex;
        font-size: 14px;
        overflow: hidden;
      }

      #tabbar > a {
        overflow: hidden;
        max-width: 45%;
      }

      #tabbar.bottom-bar {
        position: absolute;
        bottom: 0;
        left: 0;
        padding: 0 16px;
        box-sizing: border-box;
        background-color: var(--sidebar-background-color);
        border-top: 1px solid var(--divider-color);
        justify-content: space-around;
        z-index: 2;
        font-size: 12px;
        width: 100%;
        padding-bottom: env(safe-area-inset-bottom);
      }

      #tabbar:not(.bottom-bar) {
        flex: 1;
        justify-content: center;
      }

      :host(:not([narrow])) #toolbar-icon {
        min-width: 40px;
      }

      ha-menu-button,
      ha-icon-button-arrow-prev,
      ::slotted([slot="toolbar-icon"]) {
        flex-shrink: 0;
        pointer-events: auto;
        color: var(--sidebar-icon-color);
      }

      .main-title {
        flex: 1;
        max-height: var(--header-height);
        line-height: 20px;
        color: var(--sidebar-text-color);
      }

      .content {
        position: relative;
        width: calc(
          100% - env(safe-area-inset-left) - env(safe-area-inset-right)
        );
        margin-left: env(safe-area-inset-left);
        margin-right: env(safe-area-inset-right);
        height: calc(100% - 1px - var(--header-height));
        height: calc(
          100% - 1px - var(--header-height) - env(safe-area-inset-bottom)
        );
        overflow: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([narrow]) .content.tabs {
        height: calc(100% - 2 * var(--header-height));
        height: calc(
          100% - 2 * var(--header-height) - env(safe-area-inset-bottom)
        );
      }

      #fab {
        position: fixed;
        right: calc(16px + env(safe-area-inset-right));
        bottom: calc(16px + env(safe-area-inset-bottom));
        z-index: 1;
      }
      :host([narrow]) #fab.tabs {
        bottom: calc(84px + env(safe-area-inset-bottom));
      }
      #fab[is-wide] {
        bottom: 24px;
        right: 24px;
      }
      :host([rtl]) #fab {
        right: auto;
        left: calc(16px + env(safe-area-inset-left));
      }
      :host([rtl][is-wide]) #fab {
        bottom: 24px;
        left: 24px;
        right: auto;
      }
    `}}]}}),i);const y=()=>import("./c.f9f08903.js"),w=(e,t,a)=>new Promise(i=>{const o=t.cancel,r=t.confirm;k(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:y,dialogParams:{...t,...a,cancel:()=>{i(!(null==a||!a.prompt)&&null),o&&o()},confirm:e=>{i(null==a||!a.prompt||e),r&&r(e)}}})}),x=(e,t)=>w(e,t),$=(e,t)=>w(e,t,{confirmation:!0});export{x as a,$ as s};
