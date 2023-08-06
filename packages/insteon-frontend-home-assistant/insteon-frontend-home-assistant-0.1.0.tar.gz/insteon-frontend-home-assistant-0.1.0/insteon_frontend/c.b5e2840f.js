import{P as e,h as t,d as i,_ as a,s,e as o,x as n,l,$ as r,n as d,i as h,t as c,j as u,k as m,a4 as p,o as b,p as v,r as _}from"./entrypoint-4b72043f.js";import"./c.8d5e8972.js";import{s as f,a as g}from"./c.1930f61e.js";import{I as y,a as k,P as w,b as $}from"./c.ba88c3a2.js";import{c as x,f as z,a as L,b as C,l as B,w as R,r as T,d as D,e as S,g as A,h as U}from"./c.813ffe65.js";import{insteonDeviceTabs as E}from"./c.58e096b2.js";e({_template:t`
    <style>
      :host {
        display: inline-block;
        position: relative;
        width: 400px;
        border: 1px solid;
        padding: 2px;
        -moz-appearance: textarea;
        -webkit-appearance: textarea;
        overflow: hidden;
      }

      .mirror-text {
        visibility: hidden;
        word-wrap: break-word;
        @apply --iron-autogrow-textarea;
      }

      .fit {
        @apply --layout-fit;
      }

      textarea {
        position: relative;
        outline: none;
        border: none;
        resize: none;
        background: inherit;
        color: inherit;
        /* see comments in template */
        width: 100%;
        height: 100%;
        font-size: inherit;
        font-family: inherit;
        line-height: inherit;
        text-align: inherit;
        @apply --iron-autogrow-textarea;
      }

      textarea::-webkit-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea::-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-ms-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }
    </style>

    <!-- the mirror sizes the input/textarea so it grows with typing -->
    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->
    <div id="mirror" class="mirror-text" aria-hidden="true">&nbsp;</div>

    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->
    <div class="textarea-container fit">
      <textarea id="textarea" name$="[[name]]" aria-label$="[[label]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" autocapitalize$="[[autocapitalize]]" inputmode$="[[inputmode]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" disabled$="[[disabled]]" rows$="[[rows]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]"></textarea>
    </div>
`,is:"iron-autogrow-textarea",behaviors:[y,k],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},autocapitalize:{type:String,value:"none"},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(e){this.$.textarea.selectionStart=e},set selectionEnd(e){this.$.textarea.selectionEnd=e},attached:function(){navigator.userAgent.match(/iP(?:[oa]d|hone)/)&&!navigator.userAgent.match(/OS 1[3456789]/)&&(this.$.textarea.style.marginLeft="-3px")},validate:function(){var e=this.$.textarea.validity.valid;return e&&(this.required&&""===this.value?e=!1:this.hasValidator()&&(e=y.validate.call(this,this.value))),this.invalid=!e,this.fire("iron-input-validate"),e},_bindValueChanged:function(e){this.value=e},_valueChanged:function(e){var t=this.textarea;t&&(t.value!==e&&(t.value=e||0===e?e:""),this.bindValue=e,this.$.mirror.innerHTML=this._valueForMirror(),this.fire("bind-value-changed",{value:this.bindValue}))},_onInput:function(e){var t=i(e).path;this.value=t?t[0].value:e.target.value},_constrain:function(e){var t;for(e=e||[""],t=this.maxRows>0&&e.length>this.maxRows?e.slice(0,this.maxRows):e.slice(0);this.rows>0&&t.length<this.rows;)t.push("");return t.join("<br/>")+"&#160;"},_valueForMirror:function(){var e=this.textarea;if(e)return this.tokens=e&&e.value?e.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""],this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}}),e({_template:t`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
        display: none !important;
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container no-label-float$="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <iron-autogrow-textarea class="paper-input-input" slot="input" id$="[[_inputId]]" aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" bind-value="{{value}}" invalid="{{invalid}}" validator$="[[validator]]" disabled$="[[disabled]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" autocapitalize$="[[autocapitalize]]" rows$="[[rows]]" max-rows$="[[maxRows]]" on-change="_onChange"></iron-autogrow-textarea>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
`,is:"paper-textarea",behaviors:[w,$],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(e){this.$.input.textarea.selectionStart=e},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(e){this.$.input.textarea.selectionEnd=e},_ariaLabelledByChanged:function(e){this._focusableElement.setAttribute("aria-labelledby",e)},_ariaDescribedByChanged:function(e){this._focusableElement.setAttribute("aria-describedby",e)},get _focusableElement(){return this.inputElement.textarea}}),a([d("insteon-aldb-data-table")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[o({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[o({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[o({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[o()],key:"records",value:()=>[]},{kind:"field",decorators:[o({type:Boolean})],key:"isLoading",value:()=>!1},{kind:"field",decorators:[o({type:Boolean})],key:"showWait",value:()=>!1},{kind:"field",decorators:[n("insteon-data-table")],key:"_dataTable",value:void 0},{kind:"field",key:"_records",value:()=>l(e=>{if(!e)return[];return e.map(e=>({...e}))})},{kind:"field",key:"_columns",value(){return l(e=>e?{in_use:{title:this.insteon.localize("aldb.fields.in_use"),template:e=>e?r`${this.hass.localize("ui.common.yes")}`:r`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"15%"},dirty:{title:this.insteon.localize("aldb.fields.modified"),template:e=>e?r`${this.hass.localize("ui.common.yes")}`:r`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"15%"},target:{title:this.insteon.localize("aldb.fields.target"),sortable:!0,grows:!0},group:{title:this.insteon.localize("aldb.fields.group"),sortable:!0,width:"15%"},is_controller:{title:this.insteon.localize("aldb.fields.mode"),template:e=>e?r`${this.insteon.localize("aldb.mode.controller")}`:r`${this.insteon.localize("aldb.mode.responder")}`,sortable:!0,width:"25%"}}:{mem_addr:{title:this.insteon.localize("aldb.fields.id"),template:e=>e<0?r`New`:r`${e}`,sortable:!0,direction:"desc",width:"10%"},in_use:{title:this.insteon.localize("aldb.fields.in_use"),template:e=>e?r`${this.hass.localize("ui.common.yes")}`:r`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"10%"},dirty:{title:this.insteon.localize("aldb.fields.modified"),template:e=>e?r`${this.hass.localize("ui.common.yes")}`:r`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"10%"},target:{title:this.insteon.localize("aldb.fields.target"),sortable:!0,width:"15%"},target_name:{title:this.insteon.localize("aldb.fields.target_device"),sortable:!0,grows:!0},group:{title:this.insteon.localize("aldb.fields.group"),sortable:!0,width:"10%"},is_controller:{title:this.insteon.localize("aldb.fields.mode"),template:e=>e?r`${this.insteon.localize("aldb.mode.controller")}`:r`${this.insteon.localize("aldb.mode.responder")}`,sortable:!0,width:"12%"}})}},{kind:"method",key:"_noDataText",value:function(e){return e?"":this.insteon.localize("aldb.no_data")}},{kind:"method",key:"clearSelection",value:function(){this._dataTable.clearSelection()}},{kind:"method",key:"render",value:function(){return this.showWait?r` <ha-circular-progress active alt="Loading"></ha-circular-progress> `:r`
      <insteon-data-table
        .columns=${this._columns(this.narrow)}
        .data=${this._records(this.records)}
        .id=${"mem_addr"}
        .dir=${x(this.hass)}
        .searchLabel=${this.hass.localize("ui.components.data-table.search")}
        .noDataText="${this._noDataText(this.isLoading)}"
      >
        <ha-circular-progress active alt="Loading"></ha-circular-progress>
      </insteon-data-table>
    `}}]}}),s);const I=()=>import("./c.a018ccdb.js"),M=(e,t)=>{h(e,"show-dialog",{dialogTag:"dialog-insteon-aldb-record",dialogImport:I,dialogParams:t})};a([d("insteon-device-aldb-page")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[o({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[o({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[o({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[o({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[o({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[o()],key:"deviceId",value:void 0},{kind:"field",decorators:[c()],key:"_device",value:void 0},{kind:"field",decorators:[c()],key:"_records",value:void 0},{kind:"field",decorators:[c()],key:"_allRecords",value:void 0},{kind:"field",decorators:[c()],key:"_showHideUnused",value:()=>"show"},{kind:"field",decorators:[c()],key:"_showUnused",value:()=>!1},{kind:"field",decorators:[c()],key:"_isLoading",value:()=>!1},{kind:"field",key:"_subscribed",value:void 0},{kind:"field",key:"_refreshDevicesTimeoutHandle",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){console.info("Device GUID: "+this.deviceId+" in aldb"),u(m(i.prototype),"firstUpdated",this).call(this,e),this.deviceId&&this.hass&&z(this.hass,this.deviceId).then(e=>{this._device=e,this._getRecords()},()=>{this._noDeviceError()})}},{kind:"method",key:"disconnectedCallback",value:function(){u(m(i.prototype),"disconnectedCallback",this).call(this),this._unsubscribe()}},{kind:"method",key:"_dirty",value:function(){var e;return null===(e=this._records)||void 0===e?void 0:e.reduce((e,t)=>e||t.dirty,!1)}},{kind:"method",key:"_filterRecords",value:function(e,t){return e.filter(e=>e.in_use||t)}},{kind:"method",key:"render",value:function(){var e,t,i;return r`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${E}
        .localizeFunc=${this.insteon.localize}
        .backCallback=${()=>this._handleBackTapped()}
      >
        ${this.narrow?r`
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
                      ${this.insteon.localize("aldb.actions."+this._showHideUnused)}
                    </mwc-list-item>
                    <mwc-list-item>
                      ${this.insteon.localize("aldb.actions.add_default_links")}
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
          ${this.narrow?"":r`
                <div class="page-header fullwidth">
                  <div class="device-name">
                    <h1>${null===(t=this._device)||void 0===t?void 0:t.name}</h1>
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
                  <div class="aldb-status">
                    ALDB Status:
                    ${this._device?this.insteon.localize("aldb.status."+(null===(i=this._device)||void 0===i?void 0:i.aldb_status)):""}
                  </div>
                  <div class="actions header-right">
                    <mwc-button @click=${this._onLoadALDBClick}>
                      ${this.insteon.localize("common.actions.load")}
                    </mwc-button>
                    <mwc-button @click=${this._onAddDefaultLinksClicked}>
                      ${this.insteon.localize("aldb.actions.add_default_links")}
                    </mwc-button>
                    <mwc-button .disabled=${!this._dirty()} @click=${this._onWriteALDBClick}>
                      ${this.insteon.localize("common.actions.write")}
                    </mwc-button>
                    <mwc-button .disabled=${!this._dirty()} @click=${this._onResetALDBClick}>
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
                        ${this.insteon.localize("aldb.actions."+this._showHideUnused)}
                      </mwc-list-item>
                    </ha-button-menu>
                  </div>
                </div>
              `}
          <insteon-aldb-data-table
            .insteon=${this.insteon}
            .hass=${this.hass}
            .narrow=${this.narrow}
            .records=${this._records}
            @row-click=${this._handleRowClicked}
            .isLoading=${this._isLoading}
          ></insteon-aldb-data-table>
        </div>
        <mwc-fab
          slot="fab"
          title="${this.insteon.localize("aldb.actions.create")}"
          @click=${this._createRecord}
        >
          <ha-svg-icon slot="icon" path=${b}></ha-svg-icon>
        </mwc-fab>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_getRecords",value:function(){var e;this._device?L(this.hass,null===(e=this._device)||void 0===e?void 0:e.address).then(e=>{this._allRecords=e,this._records=this._filterRecords(this._allRecords,this._showUnused)}):this._records=[]}},{kind:"method",key:"_createRecord",value:function(){M(this,{hass:this.hass,insteon:this.insteon,schema:C(this.insteon),record:{mem_addr:0,in_use:!0,is_controller:!0,highwater:!1,group:0,target:"",target_name:"",data1:0,data2:0,data3:0,dirty:!0},title:this.insteon.localize("aldb.actions.new"),callback:async e=>this._handleRecordCreate(e)})}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.display="inline-block"}},{kind:"method",key:"_onImageError",value:function(e){e.target.style.display="none"}},{kind:"method",key:"_onLoadALDBClick",value:async function(){await f(this,{text:this.insteon.localize("common.warn.load"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:()=>this._load()})}},{kind:"method",key:"_load",value:function(){this._subscribe(),B(this.hass,this._device.address),this._isLoading=!0,this._records=[]}},{kind:"method",key:"_onShowHideUnusedClicked",value:async function(){this._showUnused=!this._showUnused,this._showUnused?this._showHideUnused="hide":this._showHideUnused="show",this._records=this._filterRecords(this._allRecords,this._showUnused)}},{kind:"method",key:"_onWriteALDBClick",value:async function(){await f(this,{text:this.insteon.localize("common.warn.write"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:()=>this._write()})}},{kind:"method",key:"_write",value:function(){this._subscribe(),R(this.hass,this._device.address),this._isLoading=!0,this._records=[]}},{kind:"method",key:"_onResetALDBClick",value:async function(){T(this.hass,this._device.address),this._getRecords()}},{kind:"method",key:"_onAddDefaultLinksClicked",value:async function(){await f(this,{text:this.insteon.localize("common.warn.add_default_links"),confirm:()=>this._addDefaultLinks()})}},{kind:"method",key:"_addDefaultLinks",value:async function(){this._subscribe(),D(this.hass,this._device.address),this._records=[]}},{kind:"method",key:"_handleRecordChange",value:async function(e){S(this.hass,this._device.address,e),e.in_use||(this._showUnused=!0),this._getRecords()}},{kind:"method",key:"_handleRecordCreate",value:async function(e){A(this.hass,this._device.address,e),this._getRecords()}},{kind:"method",key:"_handleRowClicked",value:async function(e){const t=e.detail.id,i=this._records.find(e=>e.mem_addr===+t);M(this,{hass:this.hass,insteon:this.insteon,schema:U(this.insteon),record:i,title:this.insteon.localize("aldb.actions.change"),callback:async e=>this._handleRecordChange(e)}),history.back()}},{kind:"method",key:"_handleBackTapped",value:async function(){this._dirty()?await f(this,{text:this.hass.localize("ui.panel.config.common.editor.confirm_unsaved"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:()=>this._goBack()}):v("/insteon/devices")}},{kind:"method",key:"_handleMenuAction",value:async function(e){switch(e.detail.index){case 0:await this._onShowHideUnusedClicked();break;case 1:await this._addDefaultLinks();break;case 2:await this._onLoadALDBClick();break;case 3:await this._onWriteALDBClick();break;case 4:await this._onResetALDBClick()}}},{kind:"method",key:"_goBack",value:function(){T(this.hass,this._device.address),v("/insteon/devices")}},{kind:"method",key:"_handleMessage",value:function(e){"record_loaded"===e.type&&this._getRecords(),"status_changed"===e.type&&(z(this.hass,this.deviceId).then(e=>{this._device=e}),this._isLoading=e.is_loading,e.is_loading||this._unsubscribe())}},{kind:"method",key:"_unsubscribe",value:function(){this._refreshDevicesTimeoutHandle&&clearTimeout(this._refreshDevicesTimeoutHandle),this._subscribed&&(this._subscribed.then(e=>e()),this._subscribed=void 0)}},{kind:"method",key:"_subscribe",value:function(){var e;this.hass&&(this._subscribed=this.hass.connection.subscribeMessage(e=>this._handleMessage(e),{type:"insteon/aldb/notify",device_address:null===(e=this._device)||void 0===e?void 0:e.address}),this._refreshDevicesTimeoutHandle=window.setTimeout(()=>this._unsubscribe(),12e5))}},{kind:"method",key:"_noDeviceError",value:function(){g(this,{text:this.insteon.localize("common.error.device_not_found")}),this._goBack(),this._goBack()}},{kind:"get",static:!0,key:"styles",value:function(){return _`
      :host {
        --app-header-background-color: var(--sidebar-background-color);
        --app-header-text-color: var(--sidebar-text-color);
        --app-header-border-bottom: 1px solid var(--divider-color);
      }

      :host([narrow]) {
        --aldb-table-height: 86vh;
      }

      :host(:not([narrow])) {
        --aldb-table-height: 80vh;
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

      insteon-aldb-data-table {
        width: 100%;
        height: var(--aldb-table-height);
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
    `}}]}}),s);
