import{_ as e,s as t,e as o,t as i,$ as s,a5 as a,r,n}from"./entrypoint-4b72043f.js";import"./c.121c8686.js";import{c as d}from"./c.d5834b7e.js";import"./c.ba88c3a2.js";import"./c.a557ab18.js";import"./c.813ffe65.js";e([n("dialog-insteon-property")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[o({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[o({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[o({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[o({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[i()],key:"_record",value:void 0},{kind:"field",decorators:[i()],key:"_schema",value:void 0},{kind:"field",decorators:[i()],key:"_title",value:void 0},{kind:"field",decorators:[i()],key:"_callback",value:void 0},{kind:"field",decorators:[i()],key:"_formData",value:()=>({})},{kind:"field",decorators:[i()],key:"_errors",value:()=>({base:""})},{kind:"field",decorators:[i()],key:"_opened",value:()=>!1},{kind:"method",key:"showDialog",value:async function(e){if(this.hass=e.hass,this.insteon=e.insteon,this._record=e.record,"radio_button_groups"==this._record.name){const t=e.schema[0];this._formData=this._radio_button_value(this._record,Math.floor(Object.entries(t.options).length/2)),this._schema=this._radio_button_schema(this._record.value,t)}else this._formData[this._record.name]=this._record.value,this._schema=e.schema;this._callback=e.callback,this._title=e.title,this._errors={base:""},this._opened=!0}},{kind:"method",key:"render",value:function(){return this._opened?s`
      <ha-dialog
        open
        @closed="${this._close}"
        .heading=${d(this.hass,this._title)}
      >
        <div class="form">
          <ha-form
            .data=${this._formData}
            .schema=${this._schema}
            @value-changed=${this._valueChanged}
            .error=${this._errors}
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
    `:s``}},{kind:"method",key:"_dismiss",value:function(){this._close()}},{kind:"method",key:"_submit",value:async function(){if(!this._changeMade())return void this._close();let e=void 0;if("radio_button_groups"==this._record.name){if(!this._validate_radio_buttons(this._formData))return;e=this._radio_button_groups_to_value(this._formData)}else e=this._formData[this._record.name];this._close(),await this._callback(this._record.name,e)}},{kind:"method",key:"_changeMade",value:function(){if("radio_button_groups"==this._record.name){const e=this._radio_button_groups_to_value(this._formData);return this._record.value!==e}return this._record.value!==this._formData[this._record.name]}},{kind:"method",key:"_close",value:function(){this._opened=!1}},{kind:"method",key:"_valueChanged",value:function(e){this._formData=e.detail.value}},{kind:"method",key:"_radio_button_value",value:function(e,t){const o=e.value.length,i=e.value,s={};for(let e=0;e<t;e++){const t="radio_button_group_"+e;if(e<o){const o=[];i[e].forEach(t=>(console.info("Group "+e+" value "+t),o.push(t.toString()))),s[t]=o}else s[t]=[];console.info("New prop value: "+t+" value "+s[t])}return s}},{kind:"method",key:"_radio_button_schema",value:function(e,t){const o=[],i=Object.entries(t.options).length,s=Math.floor(i/2);for(let e=0;e<s;e++){const i="radio_button_group_"+e;o.push({name:i,type:"multi_select",optional:!0,options:t.options,description:{suffix:this.insteon.localize("properties.descriptions."+i)}})}return console.info("RB Schema length: "+o.length),o}},{kind:"method",key:"_radio_button_groups_to_value",value:function(e){const t=[];return Object.entries(e).forEach(([e,o])=>{if(o.length>0){const e=o.map(e=>+e);t.push(e)}}),t}},{kind:"method",key:"_validate_radio_buttons",value:function(e){this._errors={base:""};let t=!0;const o=[];return Object.entries(e).forEach(([e,i])=>{1==i.length&&(this._errors[e]="Must have at least 2 buttons in a group",t=!1),i.length>0&&i.forEach(e=>{console.info("Checking button "+e),o.includes(e)?(console.info("Found buttong "+e),""==this._errors.base&&(this._errors.base="A button can not be selected twice"),t=!1):o.push(e)})}),t}},{kind:"get",static:!0,key:"styles",value:function(){return[a,r`
        table {
          width: 100%;
        }
        ha-combo-box {
          width: 20px;
        }
        .title {
          width: 200px;
        }
      `]}}]}}),t);
