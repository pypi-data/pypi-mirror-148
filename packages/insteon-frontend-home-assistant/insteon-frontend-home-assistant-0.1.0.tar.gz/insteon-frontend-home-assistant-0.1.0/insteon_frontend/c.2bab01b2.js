import{_ as e,s as i,e as s,t as d,$ as t,a5 as n,r as o,n as a}from"./entrypoint-4b72043f.js";import"./c.121c8686.js";import{c}from"./c.d5834b7e.js";import{q as l}from"./c.813ffe65.js";import"./c.ba88c3a2.js";import"./c.a557ab18.js";e([a("dialog-insteon-adding-device")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[s({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[s({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[d()],key:"_title",value:void 0},{kind:"field",decorators:[d()],key:"_opened",value:()=>!1},{kind:"field",decorators:[d()],key:"_devicesAddedText",value:()=>""},{kind:"field",decorators:[d()],key:"_subscribed",value:void 0},{kind:"field",key:"_devicesAdded",value:void 0},{kind:"field",key:"_address",value:()=>""},{kind:"field",key:"_multiple",value:()=>!1},{kind:"field",key:"_refreshLinkingTimeoutHandle",value:void 0},{kind:"method",key:"showDialog",value:async function(e){this.hass=e.hass,this.insteon=e.insteon,this._address=e.address,this._multiple=e.multiple,this._title=e.title,this._opened=!0,this._subscribe(),this._devicesAddedText="",this._devicesAdded=void 0}},{kind:"method",key:"render",value:function(){return this._opened?t`
      <ha-dialog
        open
        @closed="${this._close}"
        .heading=${c(this.hass,this._title)}
      >
        <div class="instructions">${this._showInstructions()}</div>
        <br />
        <div class="devices">${this._devicesAddedText}</div>
        <div class="buttons">
          <mwc-button @click=${this._checkCancel} slot="primaryAction">
            ${this._buttonText(this._subscribed)}
          </mwc-button>
        </div>
      </ha-dialog>
    `:t``}},{kind:"method",key:"_showInstructions",value:function(){return this.insteon&&!this._subscribed?this.insteon.localize("device.add.complete"):this._address?this._addressText(this._address):this._multiple?this.insteon.localize("device.add.multiple"):this.insteon.localize("device.add.single")}},{kind:"method",key:"_buttonText",value:function(e){return e?this.insteon.localize("device.actions.stop"):this.hass.localize("ui.dialogs.generic.ok")}},{kind:"method",key:"_showAddedDevices",value:function(){if(!this._devicesAdded)return"";let e="";return this._devicesAdded.forEach(i=>{var s,d;let n=null===(s=this.insteon)||void 0===s?void 0:s.localize("device.add.added");n=null===(d=n)||void 0===d?void 0:d.replace("--address--",i),e=t`${e}<br />${n}`}),e}},{kind:"method",key:"_addressText",value:function(e){let i=this.insteon.localize("device.add.address");return i=i.replace("--address--",e.toUpperCase()),i}},{kind:"method",key:"_handleMessage",value:function(e){"device_added"===e.type&&(console.info("Added device: "+e.address),this._devicesAdded?this._devicesAdded.push(e.address):this._devicesAdded=[e.address],this._devicesAddedText=this._showAddedDevices()),"linking_stopped"===e.type&&this._unsubscribe()}},{kind:"method",key:"_unsubscribe",value:function(){this._refreshLinkingTimeoutHandle&&clearTimeout(this._refreshLinkingTimeoutHandle),this._subscribed&&(this._subscribed.then(e=>e()),this._subscribed=void 0)}},{kind:"method",key:"_subscribe",value:function(){this.hass&&(this._subscribed=this.hass.connection.subscribeMessage(e=>this._handleMessage(e),{type:"insteon/device/add",multiple:this._multiple,address:this._address}),this._refreshLinkingTimeoutHandle=window.setTimeout(()=>this._unsubscribe(),195e3))}},{kind:"method",key:"_checkCancel",value:function(){this._subscribed&&(l(this.hass),this._unsubscribe()),this._close()}},{kind:"method",key:"_close",value:function(){this._opened=!1}},{kind:"get",static:!0,key:"styles",value:function(){return[n,o`
        table {
          width: 100%;
        }
        ha-combo-box {
          width: 20px;
        }
        .title {
          width: 200px;
        }
      `]}}]}}),i);
