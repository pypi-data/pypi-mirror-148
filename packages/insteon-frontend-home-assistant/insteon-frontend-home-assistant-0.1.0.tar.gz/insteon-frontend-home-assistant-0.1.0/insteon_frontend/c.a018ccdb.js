import{_ as t,s as e,e as i,t as a,$ as o,a5 as s,r,n as d}from"./entrypoint-4b72043f.js";import"./c.121c8686.js";import{c}from"./c.d5834b7e.js";import"./c.b5e2840f.js";import{c as n}from"./c.811288a2.js";import"./c.ba88c3a2.js";import"./c.a557ab18.js";import"./c.813ffe65.js";import"./c.8d5e8972.js";import"./c.1930f61e.js";import"./c.58e096b2.js";t([d("dialog-insteon-aldb-record")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[a()],key:"_record",value:void 0},{kind:"field",decorators:[a()],key:"_schema",value:void 0},{kind:"field",decorators:[a()],key:"_title",value:void 0},{kind:"field",decorators:[a()],key:"_callback",value:void 0},{kind:"field",decorators:[a()],key:"_errors",value:void 0},{kind:"field",decorators:[a()],key:"_formData",value:void 0},{kind:"field",decorators:[a()],key:"_opened",value:()=>!1},{kind:"method",key:"showDialog",value:async function(t){this.hass=t.hass,this.insteon=t.insteon,this._record=t.record,this._formData={...t.record},this._formData.mode=this._currentMode(),this._schema=t.schema,this._callback=t.callback,this._title=t.title,this._errors={},this._opened=!0}},{kind:"method",key:"render",value:function(){return this._opened?o`
      <ha-dialog
        open
        @closed="${this._close}"
        .heading=${c(this.hass,this._title)}
      >
        <div class="form">
          <ha-form
            .data=${this._formData}
            .schema=${this._schema}
            .error=${this._errors}
            @value-changed=${this._valueChanged}
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
    `:o``}},{kind:"method",key:"_dismiss",value:function(){this._close()}},{kind:"method",key:"_submit",value:async function(){if(this._changeMade())if(this._checkData()){const t=this._record;t.mem_addr=this._formData.mem_addr,t.in_use=this._formData.in_use,t.target=this._formData.target,t.is_controller=this._updatedMode(),t.group=this._formData.group,t.data1=this._formData.data1,t.data2=this._formData.data2,t.data3=this._formData.data3,t.highwater=!1,t.dirty=!0,this._close(),await this._callback(t)}else this._errors.base=this.insteon.localize("common.error.base");else this._close()}},{kind:"method",key:"_changeMade",value:function(){return this._record.in_use!==this._formData.in_use||this._currentMode()!==this._formData.mode||this._record.target!==this._formData.target||this._record.group!==this._formData.group||this._record.data1!==this._formData.data1||this._record.data2!==this._formData.data2||this._record.data3!==this._formData.data3}},{kind:"method",key:"_close",value:function(){this._opened=!1}},{kind:"method",key:"_currentMode",value:function(){return this._record.is_controller?"c":"r"}},{kind:"method",key:"_updatedMode",value:function(){return"c"===this._formData.mode}},{kind:"method",key:"_valueChanged",value:function(t){this._formData=t.detail.value}},{kind:"method",key:"_checkData",value:function(){let t=!0;return this._errors={},n(this._formData.target)||(this.insteon||console.info("This should NOT show up"),this._errors.target=this.insteon.localize("common.error.address"),t=!1),t}},{kind:"get",static:!0,key:"styles",value:function(){return[s,r`
        table {
          width: 100%;
        }
        ha-combo-box {
          width: 20px;
        }
        .title {
          width: 200px;
        }
      `]}}]}}),e);
