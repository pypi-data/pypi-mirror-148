import{_ as e,s as i,e as t,x as o,l as s,$ as a,r as n,n as r,i as d,t as l,j as c,k as h,a4 as p,p as m}from"./entrypoint-4b72043f.js";import{s as u,a as v}from"./c.1930f61e.js";import"./c.ba88c3a2.js";import{c as f,f as k,j as _,k as y,m as w,n as g,o as b}from"./c.813ffe65.js";import{insteonDeviceTabs as z}from"./c.58e096b2.js";e([r("insteon-properties-data-table")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[t({type:Array})],key:"records",value:()=>[]},{kind:"field",decorators:[t()],key:"schema",value:()=>({})},{kind:"field",decorators:[t()],key:"noDataText",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"showWait",value:()=>!1},{kind:"field",decorators:[o("insteon-data-table")],key:"_dataTable",value:void 0},{kind:"field",key:"_records",value(){return s(e=>e.map(e=>({description:this._calcDescription(e.name),display_value:this._translateValue(e.name,e.value),...e})))}},{kind:"method",key:"_calcDescription",value:function(e){return e.startsWith("toggle_")?this.insteon.localize("properties.descriptions.button")+" "+this._calcButtonName(e)+" "+this.insteon.localize("properties.descriptions.toggle"):e.startsWith("radio_button_group_")?this.insteon.localize("properties.descriptions.radio_button_group")+" "+this._calcButtonName(e):this.insteon.localize("properties.descriptions."+e)}},{kind:"method",key:"_calcButtonName",value:function(e){return e.endsWith("main")?this.insteon.localize("properties.descriptions.main"):e.substr(-1,1).toUpperCase()}},{kind:"field",key:"_columns",value(){return s(e=>e?{name:{title:this.insteon.localize("properties.fields.name"),sortable:!0,grows:!0},modified:{title:this.insteon.localize("properties.fields.modified"),template:e=>e?a`${this.hass.localize("ui.common.yes")}`:a`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"20%"},display_value:{title:this.insteon.localize("properties.fields.value"),sortable:!0,width:"20%"}}:{name:{title:this.insteon.localize("properties.fields.name"),sortable:!0,width:"20%"},description:{title:this.insteon.localize("properties.fields.description"),sortable:!0,grows:!0},modified:{title:this.insteon.localize("properties.fields.modified"),template:e=>e?a`${this.hass.localize("ui.common.yes")}`:a`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"20%"},display_value:{title:this.insteon.localize("properties.fields.value"),sortable:!0,width:"20%"}})}},{kind:"method",key:"clearSelection",value:function(){this._dataTable.clearSelection()}},{kind:"method",key:"render",value:function(){return this.showWait?a`
        <ha-circular-progress class="fullwidth" active alt="Loading"></ha-circular-progress>
      `:a`
      <insteon-data-table
        .columns=${this._columns(this.narrow)}
        .data=${this._records(this.records)}
        .id=${"name"}
        .dir=${f(this.hass)}
        noDataText="${this.noDataText}"
      ></insteon-data-table>
    `}},{kind:"method",key:"_translateValue",value:function(e,i){const t=this.schema[e];if("radio_button_groups"==t.name)return i.length+" groups";if("multi_select"===t.type&&Array.isArray(i))return i.map(e=>t.options[e]).join(", ");if("select"===t.type){var o;return(null===(o=t.options)||void 0===o?void 0:o.reduce((e,i)=>({...e,[i[0]]:i[1]}),{}))[i.toString()]}return i}},{kind:"get",static:!0,key:"styles",value:function(){return n`
      ha-circular-progress {
        align-items: center;
        justify-content: center;
        padding: 8px;
        box-sizing: border-box;
        width: 100%;
        flex-grow: 1;
      }
    `}}]}}),i);const $=()=>import("./c.09127afb.js");e([r("insteon-device-properties-page")],(function(e,i){class o extends i{constructor(...i){super(...i),e(this)}}return{F:o,d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[t({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[t({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[t()],key:"deviceId",value:void 0},{kind:"field",decorators:[l()],key:"_device",value:void 0},{kind:"field",decorators:[l()],key:"_properties",value:()=>[]},{kind:"field",decorators:[l()],key:"_schema",value:void 0},{kind:"field",decorators:[l()],key:"_showWait",value:()=>!1},{kind:"field",decorators:[l()],key:"_showAdvanced",value:()=>!1},{kind:"field",key:"_showHideAdvanced",value:()=>"show"},{kind:"method",key:"firstUpdated",value:function(e){c(h(o.prototype),"firstUpdated",this).call(this,e),this.deviceId&&this.hass&&k(this.hass,this.deviceId).then(e=>{this._device=e,this._getProperties()},()=>{this._noDeviceError()})}},{kind:"method",key:"_dirty",value:function(){var e;return null===(e=this._properties)||void 0===e?void 0:e.reduce((e,i)=>e||i.modified,!1)}},{kind:"method",key:"render",value:function(){var e,i;return a`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${z}
        .localizeFunc=${this.insteon.localize}
        .backCallback=${async()=>this._handleBackTapped()}
      >
        ${this.narrow?a`
                <!-- <span slot="header"> -->
                <div slot="header" class="header fullwidth">
                  <div slot="header" class="narrow-header-left">${null===(e=this._device)||void 0===e?void 0:e.name}</div>
                  <div slot="header" class="narrow-header-right">
                    <ha-button-menu
                      corner="BOTTOM_START"
                      @action=${this._handleMenuAction}
                      activatable
                    >
                      <ha-icon-button
                        slot="trigger"
                        .label=${this.hass.localize("ui.common.menu")}
                        .path=${p}
                      ></ha-icon-button>

                      <mwc-list-item>
                        ${this.insteon.localize("properties.actions."+this._showHideAdvanced)}
                      </mwc-list-item>
                      <mwc-list-item>
                        ${this.insteon.localize("common.actions.load")}
                      </mwc-list-item>
                      <mwc-list-item .disabled=${!this._dirty()}>
                        ${this.insteon.localize("common.actions.write")}
                      </mwc-list-item>
                      <mwc-list-item .disabled=${!this._dirty()}>
                        ${this.insteon.localize("common.actions.reset")}
                      </mwc-list-item>
                    </ha-button-menu>
                  </div>
                </div>
                <!-- </span> -->
              `:""}
        <div class="container">
          ${this.narrow?"":a`
                  <div class="page-header fullwidth">
                    <div class="device-name">
                      <h1>${null===(i=this._device)||void 0===i?void 0:i.name}</h1>
                    </div>
                    <div class="logo header-right">
                      <img
                        src="https://brands.home-assistant.io/insteon/logo.png"
                        referrerpolicy="no-referrer"
                        @load=${this._onImageLoad}
                        @error=${this._onImageError}
                      />
                    </div>
                  </div>
                  <div class="page-header fullwidth">
                    <div class="header-right">
                      <div slot="header" class="actions header-right">
                        <mwc-button @click=${this._onLoadPropertiesClick}>
                          ${this.insteon.localize("common.actions.load")}
                        </mwc-button>
                        <mwc-button
                          .disabled=${!this._dirty()}
                          @click=${this._onWritePropertiesClick}
                        >
                          ${this.insteon.localize("common.actions.write")}
                        </mwc-button>
                        <mwc-button
                          .disabled=${!this._dirty()}
                          @click=${this._onResetPropertiesClick}
                        >
                          ${this.insteon.localize("common.actions.reset")}
                        </mwc-button>
                        <ha-button-menu
                          corner="BOTTOM_START"
                          @action=${this._handleMenuAction}
                          activatable
                        >
                          <ha-icon-button
                            slot="trigger"
                            .label=${this.hass.localize("ui.common.menu")}
                            .path=${p}
                          ></ha-icon-button>

                          <mwc-list-item>
                            ${this.insteon.localize("properties.actions."+this._showHideAdvanced)}
                          </mwc-list-item>
                        </ha-button-menu>
                      </div>
                    </div>
                  </div>
                `}
          </div>
          <insteon-properties-data-table
            .hass=${this.hass}
            .insteon=${this.insteon}
            .narrow=${this.narrow}
            .records=${this._properties}
            .schema=${this._schema}
            noDataText=${this.insteon.localize("properties.no_data")}
            @row-click=${this._handleRowClicked}
            .showWait=${this._showWait}
          ></insteon-properties-data-table>
        </div>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.display="inline-block"}},{kind:"method",key:"_onImageError",value:function(e){e.target.style.display="none"}},{kind:"method",key:"_onLoadPropertiesClick",value:async function(){await u(this,{text:this.insteon.localize("common.warn.load"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:async()=>this._load()})}},{kind:"method",key:"_load",value:async function(){this._showWait=!0;try{await _(this.hass,this._device.address)}catch(e){v(this,{text:this.insteon.localize("common.error.load"),confirmText:this.hass.localize("ui.common.ok")})}this._showWait=!1}},{kind:"method",key:"_onWritePropertiesClick",value:async function(){await u(this,{text:this.insteon.localize("common.warn.write"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:async()=>this._write()})}},{kind:"method",key:"_write",value:async function(){this._showWait=!0;try{await y(this.hass,this._device.address)}catch(e){v(this,{text:this.insteon.localize("common.error.write"),confirmText:this.hass.localize("ui.common.ok")})}this._getProperties(),this._showWait=!1}},{kind:"method",key:"_getProperties",value:async function(){const e=await w(this.hass,this._device.address,this._showAdvanced);console.info("Properties: "+e.properties.length),this._properties=e.properties,this._schema=this._translateSchema(e.schema)}},{kind:"method",key:"_onResetPropertiesClick",value:async function(){g(this.hass,this._device.address),this._getProperties()}},{kind:"method",key:"_handleRowClicked",value:async function(e){const i=e.detail.id,t=this._properties.find(e=>e.name===i),o=this._schema[t.name];var s,a;s=this,a={hass:this.hass,insteon:this.insteon,schema:[o],record:t,title:this.insteon.localize("properties.actions.change"),callback:async(e,i)=>this._handlePropertyChange(e,i)},d(s,"show-dialog",{dialogTag:"dialog-insteon-property",dialogImport:$,dialogParams:a}),history.back()}},{kind:"method",key:"_handlePropertyChange",value:async function(e,i){b(this.hass,this._device.address,e,i),this._getProperties()}},{kind:"method",key:"_handleBackTapped",value:async function(){this._dirty()?await u(this,{text:this.hass.localize("ui.panel.config.common.editor.confirm_unsaved"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:()=>this._goBack()}):m("/insteon/devices")}},{kind:"method",key:"_handleMenuAction",value:async function(e){switch(e.detail.index){case 0:await this._onShowHideAdvancedClicked();break;case 1:await this._onLoadPropertiesClick();break;case 2:await this._onWritePropertiesClick();break;case 3:await this._onResetPropertiesClick()}}},{kind:"method",key:"_onShowHideAdvancedClicked",value:async function(){this._showAdvanced=!this._showAdvanced,this._showAdvanced?this._showHideAdvanced="hide":this._showHideAdvanced="show",this._getProperties()}},{kind:"method",key:"_goBack",value:function(){g(this.hass,this._device.address),m("/insteon/devices")}},{kind:"method",key:"_noDeviceError",value:function(){v(this,{text:this.insteon.localize("common.error.device_not_found")}),this._goBack()}},{kind:"method",key:"_translateSchema",value:function(e){const i={...e};return Object.entries(i).forEach(([e,i])=>{i.description||(i.description={}),i.description[e]=this.insteon.localize("properties.descriptions."+e),"multi_select"===i.type&&Object.entries(i.options).forEach(([e,t])=>{isNaN(+t)?i.options[e]=this.insteon.localize("properties.form_options."+t):i.options[e]=t}),"select"===i.type&&Object.entries(i.options).forEach(([e,[t,o]])=>{isNaN(+o)?i.options[e][1]=this.insteon.localize("properties.form_options."+o):i.options[e][1]=o})}),e}},{kind:"get",static:!0,key:"styles",value:function(){return n`
      :host {
        --app-header-background-color: var(--sidebar-background-color);
        --app-header-text-color: var(--sidebar-text-color);
        --app-header-border-bottom: 1px solid var(--divider-color);
      }

      :host([narrow]) {
        --properties-table-height: 86vh;
      }

      :host(:not([narrow])) {
        --properties-table-height: 80vh;
      }

      .header {
        display: flex;
        justify-content: space-between;
      }

      .container {
        display: flex;
        flex-wrap: wrap;
        margin: 0px;
      }

      insteon-properties-data-table {
        width: 100%;
        height: var(--properties-table-height);
        display: block;
        --data-table-border-width: 0;
      }

      h1 {
        margin: 0;
        font-family: var(--paper-font-headline_-_font-family);
        -webkit-font-smoothing: var(--paper-font-headline_-_-webkit-font-smoothing);
        font-size: var(--paper-font-headline_-_font-size);
        font-weight: var(--paper-font-headline_-_font-weight);
        letter-spacing: var(--paper-font-headline_-_letter-spacing);
        line-height: var(--paper-font-headline_-_line-height);
        opacity: var(--dark-primary-opacity);
      }

      .page-header {
        padding: 8px;
        margin-left: 32px;
        margin-right: 32px;
        display: flex;
        justify-content: space-between;
      }

      .fullwidth {
        padding: 8px;
        box-sizing: border-box;
        width: 100%;
        flex-grow: 1;
      }

      .header-right {
        align-self: center;
        display: flex;
      }

      .header-right img {
        height: 30px;
      }

      .header-right:first-child {
        width: 100%;
        justify-content: flex-end;
      }

      .actions mwc-button {
        margin: 8px;
      }

      :host([narrow]) .container {
        margin-top: 0;
      }

      .narrow-header-left {
        padding: 8px;
        width: 90%;
      }
      .narrow-header-right {
        align-self: right;
      }
    `}}]}}),i);
