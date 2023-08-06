import{_ as e,s as i,e as t,t as s,$ as a,a5 as o,r as d,n as r}from"./entrypoint-4b72043f.js";import"./c.121c8686.js";import{c as l}from"./c.d5834b7e.js";import{p as n}from"./c.813ffe65.js";import{c}from"./c.811288a2.js";import"./c.ba88c3a2.js";import"./c.a557ab18.js";e([r("dialog-insteon-add-device")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[s()],key:"_title",value:void 0},{kind:"field",decorators:[s()],key:"_callback",value:void 0},{kind:"field",decorators:[s()],key:"_errors",value:void 0},{kind:"field",decorators:[s()],key:"_formData",value:()=>({multiple:!1,address:""})},{kind:"field",decorators:[s()],key:"_opened",value:()=>!1},{kind:"method",key:"showDialog",value:async function(e){this.hass=e.hass,this.insteon=e.insteon,this._callback=e.callback,this._title=e.title,this._errors={},this._opened=!0,this._formData={multiple:!1,address:""}}},{kind:"method",key:"_schema",value:function(e){return n(e)}},{kind:"method",key:"render",value:function(){var e;return this._opened?a`
      <ha-dialog
        open
        @closed="${this._close}"
        .heading=${l(this.hass,this._title)}
      >
        <div class="form">
          <ha-form
            .data=${this._formData}
            .schema=${this._schema(this._formData.multiple)}
            .error=${this._errors}
            @value-changed=${this._valueChanged}
            .computeLabel=${this._computeLabel(null===(e=this.insteon)||void 0===e?void 0:e.localize)}
          ></ha-form>
        </div>
        <div class="buttons">
          <mwc-button @click=${this._dismiss} slot="secondaryAction">
            ${this.hass.localize("ui.dialogs.generic.cancel")}
          </mwc-button>
          <mwc-button @click=${this._submit} slot="primaryAction">
            ${this.hass.localize("ui.dialogs.generic.ok")}
          </mwc-button>
        </div>
      </ha-dialog>
    `:a``}},{kind:"method",key:"_dismiss",value:function(){this._close()}},{kind:"method",key:"_computeLabel",value:function(e){return i=>e("device.fields."+i.name)||i.name}},{kind:"method",key:"_submit",value:async function(){if(this._checkData()){console.info("Should be calling callback"),this._close();const e=""==this._formData.address?void 0:this._formData.address;await this._callback(e,this._formData.multiple)}else this._errors.base=this.insteon.localize("common.error.base")}},{kind:"method",key:"_close",value:function(){this._opened=!1}},{kind:"method",key:"_valueChanged",value:function(e){this._formData=e.detail.value}},{kind:"method",key:"_checkData",value:function(){return!(""!=this._formData.address&&!c(this._formData.address))||(this._errors={},this._errors.address=this.insteon.localize("common.error.address"),!1)}},{kind:"get",static:!0,key:"styles",value:function(){return[o,d`
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
