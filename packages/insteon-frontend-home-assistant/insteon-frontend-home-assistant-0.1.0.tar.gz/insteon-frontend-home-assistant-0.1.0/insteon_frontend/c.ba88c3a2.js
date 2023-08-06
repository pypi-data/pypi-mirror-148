import{u as t,v as e,w as i,x as n,y as o,e as s,t as a,s as r,R as c,$ as l,z as d,r as h,n as u,A as p,B as m,C as _,E as b,F as f,G as g,P as v,h as y,d as x,I as k,J as w,_ as E,K as I,L as C,i as T,M as S,N as A,f as R,O,j as F,k as z,Q as L,S as D,T as B,l as M,U as $,V as P,W as N,X as H,Y as V,Z as U,a0 as K,a1 as G,a2 as W}from"./entrypoint-4b72043f.js";function j(i,n,o){let s,a=i;return"object"==typeof i?(a=i.slot,s=i):s={flatten:n},o?t({slot:a,flatten:n,selector:o}):e({descriptor:t=>({get(){var t,e;const i="slot"+(a?`[name=${a}]`:":not([name])"),n=null===(t=this.renderRoot)||void 0===t?void 0:t.querySelector(i);return null!==(e=null==n?void 0:n.assignedNodes(s))&&void 0!==e?e:[]},enumerable:!0,configurable:!0})})}const q=t=>(e,i)=>{if(e.constructor._observers){if(!e.constructor.hasOwnProperty("_observers")){const t=e.constructor._observers;e.constructor._observers=new Map,t.forEach((t,i)=>e.constructor._observers.set(i,t))}}else{e.constructor._observers=new Map;const t=e.updated;e.updated=function(e){t.call(this,e),e.forEach((t,e)=>{const i=this.constructor._observers.get(e);void 0!==i&&i.call(this,this[e],t)})}}e.constructor._observers.set(i,t)};class X extends r{constructor(){super(...arguments),this.value="",this.group=null,this.tabindex=-1,this.disabled=!1,this.twoline=!1,this.activated=!1,this.graphic=null,this.multipleGraphics=!1,this.hasMeta=!1,this.noninteractive=!1,this.selected=!1,this.shouldRenderRipple=!1,this._managingList=null,this.boundOnClick=this.onClick.bind(this),this._firstChanged=!0,this._skipPropRequest=!1,this.rippleHandlers=new c(()=>(this.shouldRenderRipple=!0,this.ripple)),this.listeners=[{target:this,eventNames:["click"],cb:()=>{this.onClick()}},{target:this,eventNames:["mouseenter"],cb:this.rippleHandlers.startHover},{target:this,eventNames:["mouseleave"],cb:this.rippleHandlers.endHover},{target:this,eventNames:["focus"],cb:this.rippleHandlers.startFocus},{target:this,eventNames:["blur"],cb:this.rippleHandlers.endFocus},{target:this,eventNames:["mousedown","touchstart"],cb:t=>{const e=t.type;this.onDown("mousedown"===e?"mouseup":"touchend",t)}}]}get text(){const t=this.textContent;return t?t.trim():""}render(){const t=this.renderText(),e=this.graphic?this.renderGraphic():l``,i=this.hasMeta?this.renderMeta():l``;return l`
      ${this.renderRipple()}
      ${e}
      ${t}
      ${i}`}renderRipple(){return this.shouldRenderRipple?l`
      <mwc-ripple
        .activated=${this.activated}>
      </mwc-ripple>`:this.activated?l`<div class="fake-activated-ripple"></div>`:""}renderGraphic(){const t={multi:this.multipleGraphics};return l`
      <span class="mdc-deprecated-list-item__graphic material-icons ${d(t)}">
        <slot name="graphic"></slot>
      </span>`}renderMeta(){return l`
      <span class="mdc-deprecated-list-item__meta material-icons">
        <slot name="meta"></slot>
      </span>`}renderText(){const t=this.twoline?this.renderTwoline():this.renderSingleLine();return l`
      <span class="mdc-deprecated-list-item__text">
        ${t}
      </span>`}renderSingleLine(){return l`<slot></slot>`}renderTwoline(){return l`
      <span class="mdc-deprecated-list-item__primary-text">
        <slot></slot>
      </span>
      <span class="mdc-deprecated-list-item__secondary-text">
        <slot name="secondary"></slot>
      </span>
    `}onClick(){this.fireRequestSelected(!this.selected,"interaction")}onDown(t,e){const i=()=>{window.removeEventListener(t,i),this.rippleHandlers.endPress()};window.addEventListener(t,i),this.rippleHandlers.startPress(e)}fireRequestSelected(t,e){if(this.noninteractive)return;const i=new CustomEvent("request-selected",{bubbles:!0,composed:!0,detail:{source:e,selected:t}});this.dispatchEvent(i)}connectedCallback(){super.connectedCallback(),this.noninteractive||this.setAttribute("mwc-list-item","");for(const t of this.listeners)for(const e of t.eventNames)t.target.addEventListener(e,t.cb,{passive:!0})}disconnectedCallback(){super.disconnectedCallback();for(const t of this.listeners)for(const e of t.eventNames)t.target.removeEventListener(e,t.cb);this._managingList&&(this._managingList.debouncedLayout?this._managingList.debouncedLayout(!0):this._managingList.layout(!0))}firstUpdated(){const t=new Event("list-item-rendered",{bubbles:!0,composed:!0});this.dispatchEvent(t)}}i([n("slot")],X.prototype,"slotElement",void 0),i([o("mwc-ripple")],X.prototype,"ripple",void 0),i([s({type:String})],X.prototype,"value",void 0),i([s({type:String,reflect:!0})],X.prototype,"group",void 0),i([s({type:Number,reflect:!0})],X.prototype,"tabindex",void 0),i([s({type:Boolean,reflect:!0}),q((function(t){t?this.setAttribute("aria-disabled","true"):this.setAttribute("aria-disabled","false")}))],X.prototype,"disabled",void 0),i([s({type:Boolean,reflect:!0})],X.prototype,"twoline",void 0),i([s({type:Boolean,reflect:!0})],X.prototype,"activated",void 0),i([s({type:String,reflect:!0})],X.prototype,"graphic",void 0),i([s({type:Boolean})],X.prototype,"multipleGraphics",void 0),i([s({type:Boolean})],X.prototype,"hasMeta",void 0),i([s({type:Boolean,reflect:!0}),q((function(t){t?(this.removeAttribute("aria-checked"),this.removeAttribute("mwc-list-item"),this.selected=!1,this.activated=!1,this.tabIndex=-1):this.setAttribute("mwc-list-item","")}))],X.prototype,"noninteractive",void 0),i([s({type:Boolean,reflect:!0}),q((function(t){const e=this.getAttribute("role"),i="gridcell"===e||"option"===e||"row"===e||"tab"===e;i&&t?this.setAttribute("aria-selected","true"):i&&this.setAttribute("aria-selected","false"),this._firstChanged?this._firstChanged=!1:this._skipPropRequest||this.fireRequestSelected(t,"property")}))],X.prototype,"selected",void 0),i([a()],X.prototype,"shouldRenderRipple",void 0),i([a()],X.prototype,"_managingList",void 0);const Q=h`:host{cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent;height:48px;display:flex;position:relative;align-items:center;justify-content:flex-start;overflow:hidden;padding:0;padding-left:var(--mdc-list-side-padding, 16px);padding-right:var(--mdc-list-side-padding, 16px);outline:none;height:48px;color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host:focus{outline:none}:host([activated]){color:#6200ee;color:var(--mdc-theme-primary, #6200ee);--mdc-ripple-color: var( --mdc-theme-primary, #6200ee )}:host([activated]) .mdc-deprecated-list-item__graphic{color:#6200ee;color:var(--mdc-theme-primary, #6200ee)}:host([activated]) .fake-activated-ripple::before{position:absolute;display:block;top:0;bottom:0;left:0;right:0;width:100%;height:100%;pointer-events:none;z-index:1;content:"";opacity:0.12;opacity:var(--mdc-ripple-activated-opacity, 0.12);background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-deprecated-list-item__graphic{flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;display:inline-flex}.mdc-deprecated-list-item__graphic ::slotted(*){flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;width:100%;height:100%;text-align:center}.mdc-deprecated-list-item__meta{width:var(--mdc-list-item-meta-size, 24px);height:var(--mdc-list-item-meta-size, 24px);margin-left:auto;margin-right:0;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-item__meta.multi{width:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:var(--mdc-list-item-meta-size, 24px);line-height:var(--mdc-list-item-meta-size, 24px)}.mdc-deprecated-list-item__meta ::slotted(.material-icons),.mdc-deprecated-list-item__meta ::slotted(mwc-icon){line-height:var(--mdc-list-item-meta-size, 24px) !important}.mdc-deprecated-list-item__meta ::slotted(:not(.material-icons):not(mwc-icon)){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-caption-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.75rem;font-size:var(--mdc-typography-caption-font-size, 0.75rem);line-height:1.25rem;line-height:var(--mdc-typography-caption-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-caption-font-weight, 400);letter-spacing:0.0333333333em;letter-spacing:var(--mdc-typography-caption-letter-spacing, 0.0333333333em);text-decoration:inherit;text-decoration:var(--mdc-typography-caption-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-caption-text-transform, inherit)}[dir=rtl] .mdc-deprecated-list-item__meta,.mdc-deprecated-list-item__meta[dir=rtl]{margin-left:0;margin-right:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:100%;height:100%}.mdc-deprecated-list-item__text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden}.mdc-deprecated-list-item__text ::slotted([for]),.mdc-deprecated-list-item__text[for]{pointer-events:none}.mdc-deprecated-list-item__primary-text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;margin-bottom:-20px;display:block}.mdc-deprecated-list-item__primary-text::before{display:inline-block;width:0;height:32px;content:"";vertical-align:0}.mdc-deprecated-list-item__primary-text::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}.mdc-deprecated-list-item__secondary-text{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;display:block}.mdc-deprecated-list-item__secondary-text::before{display:inline-block;width:0;height:20px;content:"";vertical-align:0}.mdc-deprecated-list--dense .mdc-deprecated-list-item__secondary-text{font-size:inherit}* ::slotted(a),a{color:inherit;text-decoration:none}:host([twoline]){height:72px}:host([twoline]) .mdc-deprecated-list-item__text{align-self:flex-start}:host([disabled]),:host([noninteractive]){cursor:default;pointer-events:none}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*){opacity:.38}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__primary-text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__secondary-text ::slotted(*){color:#000;color:var(--mdc-theme-on-surface, #000)}.mdc-deprecated-list-item__secondary-text ::slotted(*){color:rgba(0, 0, 0, 0.54);color:var(--mdc-theme-text-secondary-on-background, rgba(0, 0, 0, 0.54))}.mdc-deprecated-list-item__graphic ::slotted(*){background-color:transparent;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-icon-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-group__subheader ::slotted(*){color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 40px);height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 40px);line-height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 40px) !important}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){border-radius:50%}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic{margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 16px)}[dir=rtl] :host([graphic=avatar]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=medium]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=large]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=control]) .mdc-deprecated-list-item__graphic,:host([graphic=avatar]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=medium]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=large]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=control]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 16px);margin-right:0}:host([graphic=icon]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 24px);height:var(--mdc-list-item-graphic-size, 24px);margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 32px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 24px);line-height:var(--mdc-list-item-graphic-size, 24px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 24px) !important}[dir=rtl] :host([graphic=icon]) .mdc-deprecated-list-item__graphic,:host([graphic=icon]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 32px);margin-right:0}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:56px}:host([graphic=medium]:not([twoLine])),:host([graphic=large]:not([twoLine])){height:72px}:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 56px);height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic.multi,:host([graphic=large]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(*),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 56px);line-height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 56px) !important}:host([graphic=large]){padding-left:0px}`;let Y=class extends X{};Y.styles=[Q],Y=i([u("mwc-list-item")],Y);const{H:Z}=p,J=t=>void 0===t.strings,tt=()=>document.createComment(""),et=(t,e,i)=>{var n;const o=t._$AA.parentNode,s=void 0===e?t._$AB:e._$AA;if(void 0===i){const e=o.insertBefore(tt(),s),n=o.insertBefore(tt(),s);i=new Z(e,n,t,t.options)}else{const e=i._$AB.nextSibling,a=i._$AM,r=a!==t;if(r){let e;null===(n=i._$AQ)||void 0===n||n.call(i,t),i._$AM=t,void 0!==i._$AP&&(e=t._$AU)!==a._$AU&&i._$AP(e)}if(e!==s||r){let t=i._$AA;for(;t!==e;){const e=t.nextSibling;o.insertBefore(t,s),t=e}}}return i},it=(t,e,i=t)=>(t._$AI(e,i),t),nt={},ot=(t,e=nt)=>t._$AH=e,st=t=>{var e;null===(e=t._$AP)||void 0===e||e.call(t,!1,!0);let i=t._$AA;const n=t._$AB.nextSibling;for(;i!==n;){const t=i.nextSibling;i.remove(),i=t}},at=(t,e)=>{var i,n;const o=t._$AN;if(void 0===o)return!1;for(const t of o)null===(n=(i=t)._$AO)||void 0===n||n.call(i,e,!1),at(t,e);return!0},rt=t=>{let e,i;do{if(void 0===(e=t._$AM))break;i=e._$AN,i.delete(t),t=e}while(0===(null==i?void 0:i.size))},ct=t=>{for(let e;e=t._$AM;t=e){let i=e._$AN;if(void 0===i)e._$AN=i=new Set;else if(i.has(t))break;i.add(t),ht(e)}};function lt(t){void 0!==this._$AN?(rt(this),this._$AM=t,ct(this)):this._$AM=t}function dt(t,e=!1,i=0){const n=this._$AH,o=this._$AN;if(void 0!==o&&0!==o.size)if(e)if(Array.isArray(n))for(let t=i;t<n.length;t++)at(n[t],!1),rt(n[t]);else null!=n&&(at(n,!1),rt(n));else at(this,t)}const ht=t=>{var e,i,n,o;t.type==_.CHILD&&(null!==(e=(n=t)._$AP)&&void 0!==e||(n._$AP=dt),null!==(i=(o=t)._$AQ)&&void 0!==i||(o._$AQ=lt))};class ut extends m{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,e,i){super._$AT(t,e,i),ct(this),this.isConnected=t._$AU}_$AO(t,e=!0){var i,n;t!==this.isConnected&&(this.isConnected=t,t?null===(i=this.reconnected)||void 0===i||i.call(this):null===(n=this.disconnected)||void 0===n||n.call(this)),e&&(at(this,t),rt(this))}setValue(t){if(J(this._$Ct))this._$Ct._$AI(t,this);else{const e=[...this._$Ct._$AH];e[this._$Ci]=t,this._$Ct._$AI(e,this,0)}}disconnected(){}reconnected(){}}const pt=(t,e,i)=>{const n=new Map;for(let o=e;o<=i;o++)n.set(t[o],o);return n},mt=b(class extends m{constructor(t){if(super(t),t.type!==_.CHILD)throw Error("repeat() can only be used in text expressions")}dt(t,e,i){let n;void 0===i?i=e:void 0!==e&&(n=e);const o=[],s=[];let a=0;for(const e of t)o[a]=n?n(e,a):a,s[a]=i(e,a),a++;return{values:s,keys:o}}render(t,e,i){return this.dt(t,e,i).values}update(t,[e,i,n]){var o;const s=(t=>t._$AH)(t),{values:a,keys:r}=this.dt(e,i,n);if(!Array.isArray(s))return this.at=r,a;const c=null!==(o=this.at)&&void 0!==o?o:this.at=[],l=[];let d,h,u=0,p=s.length-1,m=0,_=a.length-1;for(;u<=p&&m<=_;)if(null===s[u])u++;else if(null===s[p])p--;else if(c[u]===r[m])l[m]=it(s[u],a[m]),u++,m++;else if(c[p]===r[_])l[_]=it(s[p],a[_]),p--,_--;else if(c[u]===r[_])l[_]=it(s[u],a[_]),et(t,l[_+1],s[u]),u++,_--;else if(c[p]===r[m])l[m]=it(s[p],a[m]),et(t,s[u],s[p]),p--,m++;else if(void 0===d&&(d=pt(r,m,_),h=pt(c,u,p)),d.has(c[u]))if(d.has(c[p])){const e=h.get(r[m]),i=void 0!==e?s[e]:null;if(null===i){const e=et(t,s[u]);it(e,a[m]),l[m]=e}else l[m]=it(i,a[m]),et(t,s[u],i),s[e]=null;m++}else st(s[p]),p--;else st(s[u]),u++;for(;m<=_;){const e=et(t,l[_+1]);it(e,a[m]),l[m++]=e}for(;u<=p;){const t=s[u++];null!==t&&st(t)}return this.at=r,ot(t,l),f}});let _t,bt;async function ft(){return bt||async function(){if(_t)return(await _t).default;_t=window.ResizeObserver;try{new _t((function(){}))}catch(t){_t=import("./c.fe385c94.js"),_t=(await _t).default}return bt=_t}()}const gt=Symbol("scrollerRef");let vt="attachShadow"in Element.prototype&&(!("ShadyDOM"in window)||!window.ShadyDOM.inUse);let yt=null;function xt(t,e){return`\n    ${t} {\n      display: block;\n      position: relative;\n      contain: strict;\n      height: 150px;\n      overflow: auto;\n    }\n    ${e} {\n      box-sizing: border-box;\n    }`}class kt{constructor(t){this._benchmarkStart=null,this._layout=null,this._scrollTarget=null,this._sizer=null,this._scrollSize=null,this._scrollErr=null,this._childrenPos=null,this._childMeasurements=null,this._toBeMeasured=new Map,this._rangeChanged=!0,this._itemsChanged=!0,this._visibilityChanged=!0,this._container=null,this._containerElement=null,this._containerInlineStyle=null,this._containerStylesheet=null,this._containerSize=null,this._containerRO=null,this._childrenRO=null,this._mutationObserver=null,this._mutationPromise=null,this._mutationPromiseResolver=null,this._mutationsObserved=!1,this._loadListener=this._childLoaded.bind(this),this._scrollToIndex=null,this._items=[],this._totalItems=null,this._first=0,this._last=0,this._scheduled=new WeakSet,this._measureCallback=null,this._measureChildOverride=null,this._first=-1,this._last=-1,t&&Object.assign(this,t)}set items(t){t!==this._items&&(this._itemsChanged=!0,this._items=t,this._schedule(this._updateLayout))}get totalItems(){return null===this._totalItems?this._items.length:this._totalItems}set totalItems(t){if("number"!=typeof t&&null!==t)throw new Error("New value must be a number.");t!==this._totalItems&&(this._totalItems=t,this._schedule(this._updateLayout))}get container(){return this._container}set container(t){t!==this._container&&(this._container&&this._children.forEach(t=>t.parentNode.removeChild(t)),this._container=t,this._schedule(this._updateLayout),this._initResizeObservers().then(()=>{const e=this._containerElement,i=t&&t.nodeType===Node.DOCUMENT_FRAGMENT_NODE?t.host:t;e!==i&&(this._containerRO.disconnect(),this._containerSize=null,e?(this._containerInlineStyle?e.setAttribute("style",this._containerInlineStyle):e.removeAttribute("style"),this._containerInlineStyle=null,e===this._scrollTarget&&(e.removeEventListener("scroll",this,{passive:!0}),this._sizer&&this._sizer.remove()),e.removeEventListener("load",this._loadListener,!0),this._mutationObserver.disconnect()):addEventListener("scroll",this,{passive:!0}),this._containerElement=i,i&&(this._containerInlineStyle=i.getAttribute("style")||null,this._applyContainerStyles(),i===this._scrollTarget&&(this._sizer=this._sizer||this._createContainerSizer(),this._container.insertBefore(this._sizer,this._container.firstChild)),this._schedule(this._updateLayout),this._containerRO.observe(i),this._mutationObserver.observe(i,{childList:!0}),this._mutationPromise=new Promise(t=>this._mutationPromiseResolver=t),this._layout&&this._layout.listenForChildLoadEvents&&i.addEventListener("load",this._loadListener,!0)))}))}get layout(){return this._layout}set layout(t){if(this._layout===t)return;let e,i;if("object"==typeof t?(void 0!==t.type&&(e=t.type,delete t.type),i=t):e=t,"function"==typeof e){if(this._layout instanceof e)return void(i&&(this._layout.config=i));e=new e(i)}this._layout&&(this._measureCallback=null,this._measureChildOverride=null,this._layout.removeEventListener("scrollsizechange",this),this._layout.removeEventListener("scrollerrorchange",this),this._layout.removeEventListener("itempositionchange",this),this._layout.removeEventListener("rangechange",this),delete this.container[gt],this.container.removeEventListener("load",this._loadListener,!0),this._containerElement&&this._sizeContainer(void 0)),this._layout=e,this._layout&&(this._layout.measureChildren&&"function"==typeof this._layout.updateItemSizes&&("function"==typeof this._layout.measureChildren&&(this._measureChildOverride=this._layout.measureChildren),this._measureCallback=this._layout.updateItemSizes.bind(this._layout)),this._layout.addEventListener("scrollsizechange",this),this._layout.addEventListener("scrollerrorchange",this),this._layout.addEventListener("itempositionchange",this),this._layout.addEventListener("rangechange",this),this._container[gt]=this,this._layout.listenForChildLoadEvents&&this._container.addEventListener("load",this._loadListener,!0),this._schedule(this._updateLayout))}startBenchmarking(){null===this._benchmarkStart&&(this._benchmarkStart=window.performance.now())}stopBenchmarking(){if(null!==this._benchmarkStart){const t=window.performance.now(),e=t-this._benchmarkStart,i=performance.getEntriesByName("uv-virtualizing","measure").filter(e=>e.startTime>=this._benchmarkStart&&e.startTime<t).reduce((t,e)=>t+e.duration,0);return this._benchmarkStart=null,{timeElapsed:e,virtualizationTime:i}}return null}_measureChildren(){const t={},e=this._children,i=this._measureChildOverride||this._measureChild;for(let n=0;n<e.length;n++){const o=e[n],s=this._first+n;(this._itemsChanged||this._toBeMeasured.has(o))&&(t[s]=i.call(this,o,this._items[s]))}this._childMeasurements=t,this._schedule(this._updateLayout),this._toBeMeasured.clear()}_measureChild(t){const{width:e,height:i}=t.getBoundingClientRect();return Object.assign({width:e,height:i},function(t){const e=window.getComputedStyle(t);return{marginTop:wt(e.marginTop),marginRight:wt(e.marginRight),marginBottom:wt(e.marginBottom),marginLeft:wt(e.marginLeft)}}(t))}get scrollTarget(){return this._scrollTarget}set scrollTarget(t){t===window&&(t=null),this._scrollTarget!==t&&(this._sizeContainer(void 0),this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this,{passive:!0}),this._sizer&&this._scrollTarget===this._containerElement&&this._sizer.remove()),this._scrollTarget=t,t&&(t.addEventListener("scroll",this,{passive:!0}),t===this._containerElement&&(this._sizer=this._sizer||this._createContainerSizer(),this._container.insertBefore(this._sizer,this._container.firstChild))))}set scrollToIndex(t){this._scrollToIndex=t,this._schedule(this._updateLayout)}async _schedule(t){this._scheduled.has(t)||(this._scheduled.add(t),await Promise.resolve(),this._scheduled.delete(t),t.call(this))}async _updateDOM(){const{_rangeChanged:t,_itemsChanged:e}=this;this._visibilityChanged&&(this._notifyVisibility(),this._visibilityChanged=!1),(t||e)&&(this._notifyRange(),this._rangeChanged=!1,this._itemsChanged=!1,await this._mutationPromise),this._layout.measureChildren&&this._children.forEach(t=>this._childrenRO.observe(t)),this._positionChildren(this._childrenPos),this._sizeContainer(this._scrollSize),this._scrollErr&&(this._correctScrollError(this._scrollErr),this._scrollErr=null),this._benchmarkStart&&"mark"in window.performance&&window.performance.mark("uv-end")}_updateLayout(){this._layout.totalItems=this._totalItems,null!==this._scrollToIndex&&(this._layout.scrollToIndex(this._scrollToIndex.index,this._scrollToIndex.position),this._scrollToIndex=null),this._updateView(),null!==this._childMeasurements&&(this._measureCallback&&this._measureCallback(this._childMeasurements),this._childMeasurements=null),this._layout.reflowIfNeeded(this._itemsChanged),this._benchmarkStart&&"mark"in window.performance&&window.performance.mark("uv-end")}_handleScrollEvent(){if(this._benchmarkStart&&"mark"in window.performance){try{window.performance.measure("uv-virtualizing","uv-start","uv-end")}catch(t){}window.performance.mark("uv-start")}this._schedule(this._updateLayout)}handleEvent(t){switch(t.type){case"scroll":this._scrollTarget&&t.target!==this._scrollTarget||this._handleScrollEvent();break;case"scrollsizechange":this._scrollSize=t.detail,this._schedule(this._updateDOM);break;case"scrollerrorchange":this._scrollErr=t.detail,this._schedule(this._updateDOM);break;case"itempositionchange":this._childrenPos=t.detail,this._schedule(this._updateDOM);break;case"rangechange":this._adjustRange(t.detail),this._schedule(this._updateDOM);break;default:console.warn("event not handled",t)}}async _initResizeObservers(){if(null===this._containerRO){const t=await ft();this._containerRO=new t(t=>this._containerSizeChanged(t[0].contentRect)),this._childrenRO=new t(this._childrenSizeChanged.bind(this)),this._mutationObserver=new MutationObserver(this._observeMutations.bind(this))}}_applyContainerStyles(){if(vt){if(null===this._containerStylesheet){(this._containerStylesheet=document.createElement("style")).textContent=xt(":host","::slotted(*)")}const t=this._containerElement.shadowRoot||this._containerElement.attachShadow({mode:"open"}),e=t.querySelector("slot:not([name])");t.appendChild(this._containerStylesheet),e||t.appendChild(document.createElement("slot"))}else yt||(yt=document.createElement("style"),yt.textContent=xt(".uni-virtualizer-host",".uni-virtualizer-host > *"),document.head.appendChild(yt)),this._containerElement&&this._containerElement.classList.add("uni-virtualizer-host")}_createContainerSizer(){const t=document.createElement("div");return Object.assign(t.style,{position:"absolute",margin:"-2px 0 0 0",padding:0,visibility:"hidden",fontSize:"2px"}),t.innerHTML="&nbsp;",t.id="uni-virtualizer-spacer",t}get _children(){const t=[];let e=this.container.firstElementChild;for(;e;)"uni-virtualizer-spacer"!==e.id&&t.push(e),e=e.nextElementSibling;return t}_updateView(){if(!this.container||!this._containerElement||!this._layout)return;let t,e,i,n;if(this._scrollTarget===this._containerElement&&null!==this._containerSize)t=this._containerSize.width,e=this._containerSize.height,n=this._containerElement.scrollLeft,i=this._containerElement.scrollTop;else{const o=this._containerElement.getBoundingClientRect(),s=this._scrollTarget?this._scrollTarget.getBoundingClientRect():{top:o.top+window.pageYOffset,left:o.left+window.pageXOffset,width:innerWidth,height:innerHeight},a=s.width,r=s.height,c=Math.max(0,Math.min(a,o.left-s.left)),l=Math.max(0,Math.min(r,o.top-s.top));t=("vertical"===this._layout.direction?Math.max(0,Math.min(a,o.right-s.left)):a)-c,e=("vertical"===this._layout.direction?r:Math.max(0,Math.min(r,o.bottom-s.top)))-l,n=Math.max(0,-(o.left-s.left)),i=Math.max(0,-(o.top-s.top))}this._layout.viewportSize={width:t,height:e},this._layout.viewportScroll={top:i,left:n}}_sizeContainer(t){if(this._scrollTarget===this._containerElement){const e=t&&t.width?t.width-1:0,i=t&&t.height?t.height-1:0;this._sizer&&(this._sizer.style.transform=`translate(${e}px, ${i}px)`)}else if(this._containerElement){const e=this._containerElement.style;e.minWidth=t&&t.width?t.width+"px":null,e.minHeight=t&&t.height?t.height+"px":null}}_positionChildren(t){if(t){const e=this._children;Object.keys(t).forEach(i=>{const n=i-this._first,o=e[n];if(o){const{top:e,left:n,width:s,height:a}=t[i];o.style.position="absolute",o.style.transform=`translate(${n}px, ${e}px)`,void 0!==s&&(o.style.width=s+"px"),void 0!==a&&(o.style.height=a+"px")}})}}async _adjustRange(t){const{_first:e,_last:i,_firstVisible:n,_lastVisible:o}=this;this._first=t.first,this._last=t.last,this._firstVisible=t.firstVisible,this._lastVisible=t.lastVisible,this._rangeChanged=this._rangeChanged||this._first!==e||this._last!==i,this._visibilityChanged=this._visibilityChanged||this._firstVisible!==n||this._lastVisible!==o}_correctScrollError(t){this._scrollTarget?(this._scrollTarget.scrollTop-=t.top,this._scrollTarget.scrollLeft-=t.left):window.scroll(window.pageXOffset-t.left,window.pageYOffset-t.top)}_notifyRange(){this._container.dispatchEvent(new CustomEvent("rangeChanged",{detail:{first:this._first,last:this._last,firstVisible:this._firstVisible,lastVisible:this._lastVisible}}))}_notifyVisibility(){this._container.dispatchEvent(new CustomEvent("visibilityChanged",{detail:{first:this._first,last:this._last,firstVisible:this._firstVisible,lastVisible:this._lastVisible}}))}_containerSizeChanged(t){const{width:e,height:i}=t;this._containerSize={width:e,height:i},this._schedule(this._updateLayout)}async _observeMutations(){this._mutationsObserved||(this._mutationsObserved=!0,this._mutationPromiseResolver(),this._mutationPromise=new Promise(t=>this._mutationPromiseResolver=t),this._mutationsObserved=!1)}_childLoaded(){}_childrenSizeChanged(t){for(let e of t)this._toBeMeasured.set(e.target,e.contentRect);this._measureChildren(),this._schedule(this._updateLayout)}}function wt(t){const e=t?parseFloat(t):NaN;return Number.isNaN(e)?0:e}const Et=t=>t;const It=b(class extends ut{constructor(t){if(super(t),this.first=0,this.last=-1,t.type!==_.CHILD)throw new Error("The scroll directive can only be used in child expressions")}render(t){t&&(this.renderItem=t.renderItem,this.keyFunction=t.keyFunction);const e=[];if(this.first>=0&&this.last>=this.first)for(let t=this.first;t<this.last+1;t++)e.push(this.items[t]);return mt(e,this.keyFunction||Et,this.renderItem)}update(t,[e]){var i;if(this.scroller||this._initialize(t,e)){const{scroller:t}=this;return this.items=t.items=e.items,t.totalItems=e.totalItems||(null===(i=e.items)||void 0===i?void 0:i.length)||0,t.layout=e.layout,t.scrollTarget=e.scrollTarget||this.container,e.scrollToIndex&&(t.scrollToIndex=e.scrollToIndex),this.render(e)}return g}_initialize(t,e){const i=this.container=t.parentNode;return i&&1===i.nodeType?(this.scroller=new kt({container:i}),i.addEventListener("rangeChanged",t=>{this.first=t.detail.first,this.last=t.detail.last,this.setValue(this.render())}),!0):(Promise.resolve().then(()=>this.update(t,[e])),!1)}});let Ct,Tt;async function St(){return Tt||async function(){Ct=window.EventTarget;try{new Ct}catch(t){Ct=(await import("./c.e4ba960c.js")).EventTarget}return Tt=Ct}()}class At{constructor(t){this._latestCoords={left:0,top:0},this._direction="vertical",this._viewportSize={width:0,height:0},this._pendingReflow=!1,this._pendingLayoutUpdate=!1,this._scrollToIndex=-1,this._scrollToAnchor=0,this._eventTargetPromise=St().then(t=>{this._eventTarget=new t}),this._physicalMin=0,this._physicalMax=0,this._first=-1,this._last=-1,this._itemSize={width:100,height:100},this._spacing=0,this._sizeDim="height",this._secondarySizeDim="width",this._positionDim="top",this._secondaryPositionDim="left",this._scrollPosition=0,this._scrollError=0,this._totalItems=0,this._scrollSize=1,this._overhang=1e3,t&&(this.config=t)}set config(t){Object.assign(this,Object.assign({},this.constructor._defaultConfig,t))}get config(){const t={};for(let e in this.constructor._defaultConfig)t[e]=this[e];return t}get totalItems(){return this._totalItems}set totalItems(t){const e=Number(t);e!==this._totalItems&&(this._totalItems=e,this._scheduleReflow())}get direction(){return this._direction}set direction(t){(t="horizontal"===t?t:"vertical")!==this._direction&&(this._direction=t,this._sizeDim="horizontal"===t?"width":"height",this._secondarySizeDim="horizontal"===t?"height":"width",this._positionDim="horizontal"===t?"left":"top",this._secondaryPositionDim="horizontal"===t?"top":"left",this._scheduleLayoutUpdate())}get itemSize(){return this._itemSize}set itemSize(t){const{_itemDim1:e,_itemDim2:i}=this;Object.assign(this._itemSize,t),e===this._itemDim1&&i===this._itemDim2||(i!==this._itemDim2?this._itemDim2Changed():this._scheduleLayoutUpdate())}get spacing(){return this._spacing}set spacing(t){const e=Number(t);e!==this._spacing&&(this._spacing=e,this._scheduleLayoutUpdate())}get viewportSize(){return this._viewportSize}set viewportSize(t){const{_viewDim1:e,_viewDim2:i}=this;Object.assign(this._viewportSize,t),i!==this._viewDim2?this._viewDim2Changed():e!==this._viewDim1&&this._checkThresholds()}get viewportScroll(){return this._latestCoords}set viewportScroll(t){Object.assign(this._latestCoords,t);const e=this._scrollPosition;this._scrollPosition=this._latestCoords[this._positionDim],e!==this._scrollPosition&&(this._scrollPositionChanged(e,this._scrollPosition),this._updateVisibleIndices({emit:!0})),this._checkThresholds()}reflowIfNeeded(t){(t||this._pendingReflow)&&(this._pendingReflow=!1,this._reflow())}scrollToIndex(t,e="start"){if(Number.isFinite(t)){switch(t=Math.min(this.totalItems,Math.max(0,t)),this._scrollToIndex=t,"nearest"===e&&(e=t>this._first+this._num/2?"end":"start"),e){case"start":this._scrollToAnchor=0;break;case"center":this._scrollToAnchor=.5;break;case"end":this._scrollToAnchor=1;break;default:throw new TypeError("position must be one of: start, center, end, nearest")}this._scheduleReflow()}}async dispatchEvent(...t){await this._eventTargetPromise,this._eventTarget.dispatchEvent(...t)}async addEventListener(...t){await this._eventTargetPromise,this._eventTarget.addEventListener(...t)}async removeEventListener(...t){await this._eventTargetPromise,this._eventTarget.removeEventListener(...t)}_itemDim2Changed(){}_viewDim2Changed(){}_updateLayout(){}_getItemSize(t){return{[this._sizeDim]:this._itemDim1,[this._secondarySizeDim]:this._itemDim2}}get _delta(){return this._itemDim1+this._spacing}get _itemDim1(){return this._itemSize[this._sizeDim]}get _itemDim2(){return this._itemSize[this._secondarySizeDim]}get _viewDim1(){return this._viewportSize[this._sizeDim]}get _viewDim2(){return this._viewportSize[this._secondarySizeDim]}_scheduleReflow(){this._pendingReflow=!0}_scheduleLayoutUpdate(){this._pendingLayoutUpdate=!0,this._scheduleReflow()}_reflow(){const{_first:t,_last:e,_scrollSize:i}=this;this._pendingLayoutUpdate&&(this._updateLayout(),this._pendingLayoutUpdate=!1),this._updateScrollSize(),this._getActiveItems(),this._scrollIfNeeded(),this._updateVisibleIndices(),this._scrollSize!==i&&this._emitScrollSize(),-1===this._first&&-1===this._last?this._emitRange():(this._first!==t||this._last!==e||this._spacingChanged)&&(this._emitRange(),this._emitChildPositions()),this._emitScrollError()}_updateScrollSize(){this._scrollSize=Math.max(1,this._totalItems*this._delta)}_scrollIfNeeded(){if(-1===this._scrollToIndex)return;const t=this._scrollToIndex,e=this._scrollToAnchor,i=this._getItemPosition(t)[this._positionDim],n=this._getItemSize(t)[this._sizeDim],o=this._scrollPosition+this._viewDim1*e,s=i+n*e,a=Math.floor(Math.min(this._scrollSize-this._viewDim1,Math.max(0,this._scrollPosition-o+s)));this._scrollError+=this._scrollPosition-a,this._scrollPosition=a}_emitRange(t){const e=Object.assign({first:this._first,last:this._last,num:this._num,stable:!0,firstVisible:this._firstVisible,lastVisible:this._lastVisible},t);this.dispatchEvent(new CustomEvent("rangechange",{detail:e}))}_emitScrollSize(){const t={[this._sizeDim]:this._scrollSize};this.dispatchEvent(new CustomEvent("scrollsizechange",{detail:t}))}_emitScrollError(){if(this._scrollError){const t={[this._positionDim]:this._scrollError,[this._secondaryPositionDim]:0};this.dispatchEvent(new CustomEvent("scrollerrorchange",{detail:t})),this._scrollError=0}}_emitChildPositions(){const t={};for(let e=this._first;e<=this._last;e++)t[e]=this._getItemPosition(e);this.dispatchEvent(new CustomEvent("itempositionchange",{detail:t}))}get _num(){return-1===this._first||-1===this._last?0:this._last-this._first+1}_checkThresholds(){if(0===this._viewDim1&&this._num>0)this._scheduleReflow();else{const t=Math.max(0,this._scrollPosition-this._overhang),e=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang);(this._physicalMin>t||this._physicalMax<e)&&this._scheduleReflow()}}_updateVisibleIndices(t){if(-1===this._first||-1===this._last)return;let e=this._first;for(;Math.round(this._getItemPosition(e)[this._positionDim]+this._getItemSize(e)[this._sizeDim])<=Math.round(this._scrollPosition);)e++;let i=this._last;for(;Math.round(this._getItemPosition(i)[this._positionDim])>=Math.round(this._scrollPosition+this._viewDim1);)i--;e===this._firstVisible&&i===this._lastVisible||(this._firstVisible=e,this._lastVisible=i,t&&t.emit&&this._emitRange())}_scrollPositionChanged(t,e){const i=this._scrollSize-this._viewDim1;(t<i||e<i)&&(this._scrollToIndex=-1)}}At._defaultConfig={};class Rt extends At{constructor(t){super(t),this._physicalItems=new Map,this._newPhysicalItems=new Map,this._metrics=new Map,this._anchorIdx=null,this._anchorPos=null,this._stable=!0,this._needsRemeasure=!1,this._nMeasured=0,this._tMeasured=0,this._measureChildren=!0,this._estimate=!0}get measureChildren(){return this._measureChildren}updateItemSizes(t){Object.keys(t).forEach(e=>{const i=t[e],n=this._getMetrics(Number(e)),o=n[this._sizeDim];n.width=i.width+(i.marginLeft||0)+(i.marginRight||0),n.height=i.height+(i.marginTop||0)+(i.marginBottom||0);const s=n[this._sizeDim],a=this._getPhysicalItem(Number(e));if(a){let t;void 0!==s&&(a.size=s,void 0===o?(t=s,this._nMeasured++):t=s-o),this._tMeasured=this._tMeasured+t}}),this._nMeasured&&(this._updateItemSize(),this._scheduleReflow())}_updateItemSize(){this._itemSize[this._sizeDim]=Math.round(this._tMeasured/this._nMeasured)}_getMetrics(t){return this._metrics[t]=this._metrics[t]||{}}_getPhysicalItem(t){return this._newPhysicalItems.get(t)||this._physicalItems.get(t)}_getSize(t){const e=this._getPhysicalItem(t);return e&&e.size}_getPosition(t){const e=this._getPhysicalItem(t);return e?e.pos:t*this._delta+this._spacing}_calculateAnchor(t,e){return 0===t?0:e>this._scrollSize-this._viewDim1?this._totalItems-1:Math.max(0,Math.min(this._totalItems-1,Math.floor((t+e)/2/this._delta)))}_getAnchor(t,e){if(0===this._physicalItems.size)return this._calculateAnchor(t,e);if(this._first<0)return console.error("_getAnchor: negative _first"),this._calculateAnchor(t,e);if(this._last<0)return console.error("_getAnchor: negative _last"),this._calculateAnchor(t,e);const i=this._getPhysicalItem(this._first),n=this._getPhysicalItem(this._last),o=i.pos,s=o+i.size,a=n.pos,r=a+n.size;if(r<t)return this._calculateAnchor(t,e);if(o>e)return this._calculateAnchor(t,e);if(o>=t||s>=t)return this._first;if(r<=e||a<=e)return this._last;let c=this._last,l=this._first;for(;;){const i=Math.round((c+l)/2),n=this._physicalItems.get(i),o=n.pos,s=o+n.size;if(o>=t&&o<=e||s>=t&&s<=e)return i;s<t?l=i+1:o>e&&(c=i-1)}}_getActiveItems(){0===this._viewDim1||0===this._totalItems?this._clearItems():this._getItems()}_clearItems(){this._first=-1,this._last=-1,this._physicalMin=0,this._physicalMax=0;const t=this._newPhysicalItems;this._newPhysicalItems=this._physicalItems,this._newPhysicalItems.clear(),this._physicalItems=t,this._stable=!0}_getItems(){const t=this._newPhysicalItems;let e,i;this._scrollToIndex>=0?(this._anchorIdx=this._scrollToIndex,this._anchorPos=this._getPosition(this._anchorIdx),this._scrollIfNeeded(),e=Math.max(0,this._scrollPosition-this._overhang),i=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang)):(i=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang),e=Math.max(0,i-this._viewDim1-2*this._overhang),null!==this._anchorIdx&&null!==this._anchorPos||(this._anchorIdx=this._getAnchor(e,i),this._anchorPos=this._getPosition(this._anchorIdx)));let n=this._getSize(this._anchorIdx);void 0===n&&(n=this._itemDim1);let o=0;for(this._anchorPos+n+this._spacing<e&&(o=e-(this._anchorPos+n+this._spacing)),this._anchorPos>i&&(o=i-this._anchorPos),o&&(this._scrollPosition-=o,e-=o,i-=o,this._scrollError+=o),t.set(this._anchorIdx,{pos:this._anchorPos,size:n}),this._first=this._last=this._anchorIdx,this._physicalMin=this._physicalMax=this._anchorPos,this._stable=!0;this._physicalMin>e&&this._first>0;){let e=this._getSize(--this._first);void 0===e&&(this._stable=!1,e=this._itemDim1);const i=this._physicalMin-=e+this._spacing;if(t.set(this._first,{pos:i,size:e}),!1===this._stable&&!1===this._estimate)break}for(;this._physicalMax<i&&this._last<this._totalItems;){let e=this._getSize(this._last);if(void 0===e&&(this._stable=!1,e=this._itemDim1),t.set(this._last++,{pos:this._physicalMax,size:e}),!1===this._stable&&!1===this._estimate)break;this._physicalMax+=e+this._spacing}this._last--;const s=this._calculateError();s&&(this._physicalMin-=s,this._physicalMax-=s,this._anchorPos-=s,this._scrollPosition-=s,t.forEach(t=>t.pos-=s),this._scrollError+=s),this._stable&&(this._newPhysicalItems=this._physicalItems,this._newPhysicalItems.clear(),this._physicalItems=t)}_calculateError(){return 0===this._first?this._physicalMin:this._physicalMin<=0?this._physicalMin-this._first*this._delta:this._last===this._totalItems-1?this._physicalMax-this._scrollSize:this._physicalMax>=this._scrollSize?this._physicalMax-this._scrollSize+(this._totalItems-1-this._last)*this._delta:0}_updateScrollSize(){super._updateScrollSize(),this._scrollSize=Math.max(this._physicalMax,this._scrollSize)}_reflow(){const{_first:t,_last:e,_scrollSize:i}=this;this._updateScrollSize(),this._getActiveItems(),this._scrollSize!==i&&this._emitScrollSize(),this._updateVisibleIndices(),this._emitRange(),-1===this._first&&-1===this._last?this._resetReflowState():this._first!==t||this._last!==e||this._needsRemeasure?(this._emitChildPositions(),this._emitScrollError()):(this._emitChildPositions(),this._emitScrollError(),this._resetReflowState())}_resetReflowState(){this._anchorIdx=null,this._anchorPos=null,this._stable=!0}_getItemPosition(t){return{[this._positionDim]:this._getPosition(t),[this._secondaryPositionDim]:0}}_getItemSize(t){return{[this._sizeDim]:this._getSize(t)||this._itemDim1,[this._secondarySizeDim]:this._itemDim2}}_viewDim2Changed(){this._needsRemeasure=!0,this._scheduleReflow()}_emitRange(){const t=this._needsRemeasure,e=this._stable;this._needsRemeasure=!1,super._emitRange({remeasure:t,stable:e})}}function Ot(t,e,i,n){var o,s=arguments.length,a=s<3?e:null===n?n=Object.getOwnPropertyDescriptor(e,i):n;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)a=Reflect.decorate(t,e,i,n);else for(var r=t.length-1;r>=0;r--)(o=t[r])&&(a=(s<3?o(a):s>3?o(e,i,a):o(e,i))||a);return s>3&&a&&Object.defineProperty(e,i,a),a}let Ft=class extends r{constructor(){super(...arguments),this.scrollTarget=this}createRenderRoot(){return this}set layout(t){this._layout=t,this.requestUpdate()}get layout(){return this[gt].layout}async scrollToIndex(t,e="start"){this._scrollToIndex={index:t,position:e},this.requestUpdate(),await this.updateComplete,this._scrollToIndex=null}render(){const{items:t,renderItem:e,keyFunction:i,scrollTarget:n}=this,o=this._layout;return l`
            ${It({items:t,renderItem:e,layout:o,keyFunction:i,scrollTarget:n,scrollToIndex:this._scrollToIndex})}
        `}};function zt(t){if(!t||"object"!=typeof t)return t;if("[object Date]"==Object.prototype.toString.call(t))return new Date(t.getTime());if(Array.isArray(t))return t.map(zt);var e={};return Object.keys(t).forEach((function(i){e[i]=zt(t[i])})),e}Ot([s()],Ft.prototype,"renderItem",void 0),Ot([s({attribute:!1})],Ft.prototype,"items",void 0),Ot([s({attribute:!1})],Ft.prototype,"scrollTarget",void 0),Ot([s()],Ft.prototype,"keyFunction",void 0),Ot([s({attribute:!1})],Ft.prototype,"layout",null),Ft=Ot([u("lit-virtualizer")],Ft);const Lt=t=>e=>({kind:"method",placement:"prototype",key:e.key,descriptor:{set(t){this["__"+String(e.key)]=t},get(){return this["__"+String(e.key)]},enumerable:!0,configurable:!0},finisher(i){const n=i.prototype.connectedCallback;i.prototype.connectedCallback=function(){if(n.call(this),this[e.key]){const i=this.renderRoot.querySelector(t);if(!i)return;i.scrollTop=this[e.key]}}}}),Dt=v({_template:y`
    <style>
      :host {
        display: inline-block;
        position: fixed;
        clip: rect(0px,0px,0px,0px);
      }
    </style>
    <div aria-live$="[[mode]]">[[_text]]</div>
`,is:"iron-a11y-announcer",properties:{mode:{type:String,value:"polite"},timeout:{type:Number,value:150},_text:{type:String,value:""}},created:function(){Dt.instance||(Dt.instance=this),document.addEventListener("iron-announce",this._onIronAnnounce.bind(this))},announce:function(t){this._text="",this.async((function(){this._text=t}),this.timeout)},_onIronAnnounce:function(t){t.detail&&t.detail.text&&this.announce(t.detail.text)}});Dt.instance=null,Dt.requestAvailability=function(){Dt.instance||(Dt.instance=document.createElement("iron-a11y-announcer")),document.body?document.body.appendChild(Dt.instance):document.addEventListener("load",(function(){document.body.appendChild(Dt.instance)}))};class Bt{constructor(t){Bt[" "](t),this.type=t&&t.type||"default",this.key=t&&t.key,t&&"value"in t&&(this.value=t.value)}get value(){var t=this.type,e=this.key;if(t&&e)return Bt.types[t]&&Bt.types[t][e]}set value(t){var e=this.type,i=this.key;e&&i&&(e=Bt.types[e]=Bt.types[e]||{},null==t?delete e[i]:e[i]=t)}get list(){if(this.type){var t=Bt.types[this.type];return t?Object.keys(t).map((function(t){return Mt[this.type][t]}),this):[]}}byKey(t){return this.key=t,this.value}}Bt[" "]=function(){},Bt.types={};var Mt=Bt.types;v({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(t,e,i){var n=new Bt({type:t,key:e});return void 0!==i&&i!==n.value?n.value=i:this.value!==n.value&&(this.value=n.value),n},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(t){t&&(this.value=this)},byKey:function(t){return new Bt({type:this.type,key:t}).value}});let $t=null;const Pt={properties:{validator:{type:String},invalid:{notify:!0,reflectToAttribute:!0,type:Boolean,value:!1,observer:"_invalidChanged"}},registered:function(){$t=new Bt({type:"validator"})},_invalidChanged:function(){this.invalid?this.setAttribute("aria-invalid","true"):this.removeAttribute("aria-invalid")},get _validator(){return $t&&$t.byKey(this.validator)},hasValidator:function(){return null!=this._validator},validate:function(t){return void 0===t&&void 0!==this.value?this.invalid=!this._getValidity(this.value):this.invalid=!this._getValidity(t),!this.invalid},_getValidity:function(t){return!this.hasValidator()||this._validator.validate(t)}};v({_template:y`
    <style>
      :host {
        display: inline-block;
      }
    </style>
    <slot id="content"></slot>
`,is:"iron-input",behaviors:[Pt],properties:{bindValue:{type:String,value:""},value:{type:String,computed:"_computeValue(bindValue)"},allowedPattern:{type:String},autoValidate:{type:Boolean,value:!1},_inputElement:Object},observers:["_bindValueChanged(bindValue, _inputElement)"],listeners:{input:"_onInput",keypress:"_onKeypress"},created:function(){Dt.requestAvailability(),this._previousValidInput="",this._patternAlreadyChecked=!1},attached:function(){this._observer=x(this).observeNodes(function(t){this._initSlottedInput()}.bind(this))},detached:function(){this._observer&&(x(this).unobserveNodes(this._observer),this._observer=null)},get inputElement(){return this._inputElement},_initSlottedInput:function(){this._inputElement=this.getEffectiveChildren()[0],this.inputElement&&this.inputElement.value&&(this.bindValue=this.inputElement.value),this.fire("iron-input-ready")},get _patternRegExp(){var t;if(this.allowedPattern)t=new RegExp(this.allowedPattern);else switch(this.inputElement.type){case"number":t=/[0-9.,e-]/}return t},_bindValueChanged:function(t,e){e&&(void 0===t?e.value=null:t!==e.value&&(this.inputElement.value=t),this.autoValidate&&this.validate(),this.fire("bind-value-changed",{value:t}))},_onInput:function(){this.allowedPattern&&!this._patternAlreadyChecked&&(this._checkPatternValidity()||(this._announceInvalidCharacter("Invalid string of characters not entered."),this.inputElement.value=this._previousValidInput));this.bindValue=this._previousValidInput=this.inputElement.value,this._patternAlreadyChecked=!1},_isPrintable:function(t){var e=8==t.keyCode||9==t.keyCode||13==t.keyCode||27==t.keyCode,i=19==t.keyCode||20==t.keyCode||45==t.keyCode||46==t.keyCode||144==t.keyCode||145==t.keyCode||t.keyCode>32&&t.keyCode<41||t.keyCode>111&&t.keyCode<124;return!(e||0==t.charCode&&i)},_onKeypress:function(t){if(this.allowedPattern||"number"===this.inputElement.type){var e=this._patternRegExp;if(e&&!(t.metaKey||t.ctrlKey||t.altKey)){this._patternAlreadyChecked=!0;var i=String.fromCharCode(t.charCode);this._isPrintable(t)&&!e.test(i)&&(t.preventDefault(),this._announceInvalidCharacter("Invalid character "+i+" not entered."))}}},_checkPatternValidity:function(){var t=this._patternRegExp;if(!t)return!0;for(var e=0;e<this.inputElement.value.length;e++)if(!t.test(this.inputElement.value[e]))return!1;return!0},validate:function(){if(!this.inputElement)return this.invalid=!1,!0;var t=this.inputElement.checkValidity();return t&&(this.required&&""===this.bindValue?t=!1:this.hasValidator()&&(t=Pt.validate.call(this,this.bindValue))),this.invalid=!t,this.fire("iron-input-validate"),t},_announceInvalidCharacter:function(t){this.fire("iron-announce",{text:t})},_computeValue:function(t){return t}});const Nt={attached:function(){this.fire("addon-attached")},update:function(t){}};v({_template:y`
    <style>
      :host {
        display: inline-block;
        float: right;

        @apply --paper-font-caption;
        @apply --paper-input-char-counter;
      }

      :host([hidden]) {
        display: none !important;
      }

      :host(:dir(rtl)) {
        float: left;
      }
    </style>

    <span>[[_charCounterStr]]</span>
`,is:"paper-input-char-counter",behaviors:[Nt],properties:{_charCounterStr:{type:String,value:"0"}},update:function(t){if(t.inputElement){t.value=t.value||"";var e=t.value.toString().length.toString();t.inputElement.hasAttribute("maxlength")&&(e+="/"+t.inputElement.getAttribute("maxlength")),this._charCounterStr=e}}});const Ht=y`
<custom-style>
  <style is="custom-style">
    html {
      --paper-input-container-shared-input-style: {
        position: relative; /* to make a stacking context */
        outline: none;
        box-shadow: none;
        padding: 0;
        margin: 0;
        width: 100%;
        max-width: 100%;
        background: transparent;
        border: none;
        color: var(--paper-input-container-input-color, var(--primary-text-color));
        -webkit-appearance: none;
        text-align: inherit;
        vertical-align: var(--paper-input-container-input-align, bottom);

        @apply --paper-font-subhead;
      };
    }
  </style>
</custom-style>
`;Ht.setAttribute("style","display: none;"),document.head.appendChild(Ht.content),v({_template:y`
    <style>
      :host {
        display: block;
        padding: 8px 0;
        @apply --paper-input-container;
      }

      :host([inline]) {
        display: inline-block;
      }

      :host([disabled]) {
        pointer-events: none;
        opacity: 0.33;

        @apply --paper-input-container-disabled;
      }

      :host([hidden]) {
        display: none !important;
      }

      [hidden] {
        display: none !important;
      }

      .floated-label-placeholder {
        @apply --paper-font-caption;
      }

      .underline {
        height: 2px;
        position: relative;
      }

      .focused-line {
        @apply --layout-fit;
        border-bottom: 2px solid var(--paper-input-container-focus-color, var(--primary-color));

        -webkit-transform-origin: center center;
        transform-origin: center center;
        -webkit-transform: scale3d(0,1,1);
        transform: scale3d(0,1,1);

        @apply --paper-input-container-underline-focus;
      }

      .underline.is-highlighted .focused-line {
        -webkit-transform: none;
        transform: none;
        -webkit-transition: -webkit-transform 0.25s;
        transition: transform 0.25s;

        @apply --paper-transition-easing;
      }

      .underline.is-invalid .focused-line {
        border-color: var(--paper-input-container-invalid-color, var(--error-color));
        -webkit-transform: none;
        transform: none;
        -webkit-transition: -webkit-transform 0.25s;
        transition: transform 0.25s;

        @apply --paper-transition-easing;
      }

      .unfocused-line {
        @apply --layout-fit;
        border-bottom: 1px solid var(--paper-input-container-color, var(--secondary-text-color));
        @apply --paper-input-container-underline;
      }

      :host([disabled]) .unfocused-line {
        border-bottom: 1px dashed;
        border-color: var(--paper-input-container-color, var(--secondary-text-color));
        @apply --paper-input-container-underline-disabled;
      }

      .input-wrapper {
        @apply --layout-horizontal;
        @apply --layout-center;
        position: relative;
      }

      .input-content {
        @apply --layout-flex-auto;
        @apply --layout-relative;
        max-width: 100%;
      }

      .input-content ::slotted(label),
      .input-content ::slotted(.paper-input-label) {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        font: inherit;
        color: var(--paper-input-container-color, var(--secondary-text-color));
        -webkit-transition: -webkit-transform 0.25s, width 0.25s;
        transition: transform 0.25s, width 0.25s;
        -webkit-transform-origin: left top;
        transform-origin: left top;
        /* Fix for safari not focusing 0-height date/time inputs with -webkit-apperance: none; */
        min-height: 1px;

        @apply --paper-font-common-nowrap;
        @apply --paper-font-subhead;
        @apply --paper-input-container-label;
        @apply --paper-transition-easing;
      }


      .input-content ::slotted(label):before,
      .input-content ::slotted(.paper-input-label):before {
        @apply --paper-input-container-label-before;
      }

      .input-content ::slotted(label):after,
      .input-content ::slotted(.paper-input-label):after {
        @apply --paper-input-container-label-after;
      }

      .input-content.label-is-floating ::slotted(label),
      .input-content.label-is-floating ::slotted(.paper-input-label) {
        -webkit-transform: translateY(-75%) scale(0.75);
        transform: translateY(-75%) scale(0.75);

        /* Since we scale to 75/100 of the size, we actually have 100/75 of the
        original space now available */
        width: 133%;

        @apply --paper-input-container-label-floating;
      }

      :host(:dir(rtl)) .input-content.label-is-floating ::slotted(label),
      :host(:dir(rtl)) .input-content.label-is-floating ::slotted(.paper-input-label) {
        right: 0;
        left: auto;
        -webkit-transform-origin: right top;
        transform-origin: right top;
      }

      .input-content.label-is-highlighted ::slotted(label),
      .input-content.label-is-highlighted ::slotted(.paper-input-label) {
        color: var(--paper-input-container-focus-color, var(--primary-color));

        @apply --paper-input-container-label-focus;
      }

      .input-content.is-invalid ::slotted(label),
      .input-content.is-invalid ::slotted(.paper-input-label) {
        color: var(--paper-input-container-invalid-color, var(--error-color));
      }

      .input-content.label-is-hidden ::slotted(label),
      .input-content.label-is-hidden ::slotted(.paper-input-label) {
        visibility: hidden;
      }

      .input-content ::slotted(input),
      .input-content ::slotted(iron-input),
      .input-content ::slotted(textarea),
      .input-content ::slotted(iron-autogrow-textarea),
      .input-content ::slotted(.paper-input-input) {
        @apply --paper-input-container-shared-input-style;
        /* The apply shim doesn't apply the nested color custom property,
          so we have to re-apply it here. */
        color: var(--paper-input-container-input-color, var(--primary-text-color));
        @apply --paper-input-container-input;
      }

      .input-content ::slotted(input)::-webkit-outer-spin-button,
      .input-content ::slotted(input)::-webkit-inner-spin-button {
        @apply --paper-input-container-input-webkit-spinner;
      }

      .input-content.focused ::slotted(input),
      .input-content.focused ::slotted(iron-input),
      .input-content.focused ::slotted(textarea),
      .input-content.focused ::slotted(iron-autogrow-textarea),
      .input-content.focused ::slotted(.paper-input-input) {
        @apply --paper-input-container-input-focus;
      }

      .input-content.is-invalid ::slotted(input),
      .input-content.is-invalid ::slotted(iron-input),
      .input-content.is-invalid ::slotted(textarea),
      .input-content.is-invalid ::slotted(iron-autogrow-textarea),
      .input-content.is-invalid ::slotted(.paper-input-input) {
        @apply --paper-input-container-input-invalid;
      }

      .prefix ::slotted(*) {
        display: inline-block;
        @apply --paper-font-subhead;
        @apply --layout-flex-none;
        @apply --paper-input-prefix;
      }

      .suffix ::slotted(*) {
        display: inline-block;
        @apply --paper-font-subhead;
        @apply --layout-flex-none;

        @apply --paper-input-suffix;
      }

      /* Firefox sets a min-width on the input, which can cause layout issues */
      .input-content ::slotted(input) {
        min-width: 0;
      }

      .input-content ::slotted(textarea) {
        resize: none;
      }

      .add-on-content {
        position: relative;
      }

      .add-on-content.is-invalid ::slotted(*) {
        color: var(--paper-input-container-invalid-color, var(--error-color));
      }

      .add-on-content.is-highlighted ::slotted(*) {
        color: var(--paper-input-container-focus-color, var(--primary-color));
      }
    </style>

    <div class="floated-label-placeholder" aria-hidden="true" hidden="[[noLabelFloat]]">&nbsp;</div>

    <div class="input-wrapper">
      <span class="prefix"><slot name="prefix"></slot></span>

      <div class$="[[_computeInputContentClass(noLabelFloat,alwaysFloatLabel,focused,invalid,_inputHasContent)]]" id="labelAndInputContainer">
        <slot name="label"></slot>
        <slot name="input"></slot>
      </div>

      <span class="suffix"><slot name="suffix"></slot></span>
    </div>

    <div class$="[[_computeUnderlineClass(focused,invalid)]]">
      <div class="unfocused-line"></div>
      <div class="focused-line"></div>
    </div>

    <div class$="[[_computeAddOnContentClass(focused,invalid)]]">
      <slot name="add-on"></slot>
    </div>
`,is:"paper-input-container",properties:{noLabelFloat:{type:Boolean,value:!1},alwaysFloatLabel:{type:Boolean,value:!1},attrForValue:{type:String,value:"bind-value"},autoValidate:{type:Boolean,value:!1},invalid:{observer:"_invalidChanged",type:Boolean,value:!1},focused:{readOnly:!0,type:Boolean,value:!1,notify:!0},_addons:{type:Array},_inputHasContent:{type:Boolean,value:!1},_inputSelector:{type:String,value:"input,iron-input,textarea,.paper-input-input"},_boundOnFocus:{type:Function,value:function(){return this._onFocus.bind(this)}},_boundOnBlur:{type:Function,value:function(){return this._onBlur.bind(this)}},_boundOnInput:{type:Function,value:function(){return this._onInput.bind(this)}},_boundValueChanged:{type:Function,value:function(){return this._onValueChanged.bind(this)}}},listeners:{"addon-attached":"_onAddonAttached","iron-input-validate":"_onIronInputValidate"},get _valueChangedEvent(){return this.attrForValue+"-changed"},get _propertyForValue(){return k(this.attrForValue)},get _inputElement(){return x(this).querySelector(this._inputSelector)},get _inputElementValue(){return this._inputElement[this._propertyForValue]||this._inputElement.value},ready:function(){this.__isFirstValueUpdate=!0,this._addons||(this._addons=[]),this.addEventListener("focus",this._boundOnFocus,!0),this.addEventListener("blur",this._boundOnBlur,!0)},attached:function(){this.attrForValue?this._inputElement.addEventListener(this._valueChangedEvent,this._boundValueChanged):this.addEventListener("input",this._onInput),this._inputElementValue&&""!=this._inputElementValue?this._handleValueAndAutoValidate(this._inputElement):this._handleValue(this._inputElement)},_onAddonAttached:function(t){this._addons||(this._addons=[]);var e=t.target;-1===this._addons.indexOf(e)&&(this._addons.push(e),this.isAttached&&this._handleValue(this._inputElement))},_onFocus:function(){this._setFocused(!0)},_onBlur:function(){this._setFocused(!1),this._handleValueAndAutoValidate(this._inputElement)},_onInput:function(t){this._handleValueAndAutoValidate(t.target)},_onValueChanged:function(t){var e=t.target;this.__isFirstValueUpdate&&(this.__isFirstValueUpdate=!1,void 0===e.value||""===e.value)||this._handleValueAndAutoValidate(t.target)},_handleValue:function(t){var e=this._inputElementValue;e||0===e||"number"===t.type&&!t.checkValidity()?this._inputHasContent=!0:this._inputHasContent=!1,this.updateAddons({inputElement:t,value:e,invalid:this.invalid})},_handleValueAndAutoValidate:function(t){var e;this.autoValidate&&t&&(e=t.validate?t.validate(this._inputElementValue):t.checkValidity(),this.invalid=!e);this._handleValue(t)},_onIronInputValidate:function(t){this.invalid=this._inputElement.invalid},_invalidChanged:function(){this._addons&&this.updateAddons({invalid:this.invalid})},updateAddons:function(t){for(var e,i=0;e=this._addons[i];i++)e.update(t)},_computeInputContentClass:function(t,e,i,n,o){var s="input-content";if(t)o&&(s+=" label-is-hidden"),n&&(s+=" is-invalid");else{var a=this.querySelector("label");e||o?(s+=" label-is-floating",this.$.labelAndInputContainer.style.position="static",n?s+=" is-invalid":i&&(s+=" label-is-highlighted")):(a&&(this.$.labelAndInputContainer.style.position="relative"),n&&(s+=" is-invalid"))}return i&&(s+=" focused"),s},_computeUnderlineClass:function(t,e){var i="underline";return e?i+=" is-invalid":t&&(i+=" is-highlighted"),i},_computeAddOnContentClass:function(t,e){var i="add-on-content";return e?i+=" is-invalid":t&&(i+=" is-highlighted"),i}}),v({_template:y`
    <style>
      :host {
        display: inline-block;
        visibility: hidden;

        color: var(--paper-input-container-invalid-color, var(--error-color));

        @apply --paper-font-caption;
        @apply --paper-input-error;
        position: absolute;
        left:0;
        right:0;
      }

      :host([invalid]) {
        visibility: visible;
      }

      #a11yWrapper {
        visibility: hidden;
      }

      :host([invalid]) #a11yWrapper {
        visibility: visible;
      }
    </style>

    <!--
    If the paper-input-error element is directly referenced by an
    \`aria-describedby\` attribute, such as when used as a paper-input add-on,
    then applying \`visibility: hidden;\` to the paper-input-error element itself
    does not hide the error.

    For more information, see:
    https://www.w3.org/TR/accname-1.1/#mapping_additional_nd_description
    -->
    <div id="a11yWrapper">
      <slot></slot>
    </div>
`,is:"paper-input-error",behaviors:[Nt],properties:{invalid:{readOnly:!0,reflectToAttribute:!0,type:Boolean}},update:function(t){this._setInvalid(t.invalid)}});const Vt={properties:{name:{type:String},value:{notify:!0,type:String},required:{type:Boolean,value:!1}},attached:function(){},detached:function(){}};var Ut={"U+0008":"backspace","U+0009":"tab","U+001B":"esc","U+0020":"space","U+007F":"del"},Kt={8:"backspace",9:"tab",13:"enter",27:"esc",33:"pageup",34:"pagedown",35:"end",36:"home",32:"space",37:"left",38:"up",39:"right",40:"down",46:"del",106:"*"},Gt={shift:"shiftKey",ctrl:"ctrlKey",alt:"altKey",meta:"metaKey"},Wt=/[a-z0-9*]/,jt=/U\+/,qt=/^arrow/,Xt=/^space(bar)?/,Qt=/^escape$/;function Yt(t,e){var i="";if(t){var n=t.toLowerCase();" "===n||Xt.test(n)?i="space":Qt.test(n)?i="esc":1==n.length?e&&!Wt.test(n)||(i=n):i=qt.test(n)?n.replace("arrow",""):"multiply"==n?"*":n}return i}function Zt(t,e){return t.key?Yt(t.key,e):t.detail&&t.detail.key?Yt(t.detail.key,e):(i=t.keyIdentifier,n="",i&&(i in Ut?n=Ut[i]:jt.test(i)?(i=parseInt(i.replace("U+","0x"),16),n=String.fromCharCode(i).toLowerCase()):n=i.toLowerCase()),n||function(t){var e="";return Number(t)&&(e=t>=65&&t<=90?String.fromCharCode(32+t):t>=112&&t<=123?"f"+(t-112+1):t>=48&&t<=57?String(t-48):t>=96&&t<=105?String(t-96):Kt[t]),e}(t.keyCode)||"");var i,n}function Jt(t,e){return Zt(e,t.hasModifiers)===t.key&&(!t.hasModifiers||!!e.shiftKey==!!t.shiftKey&&!!e.ctrlKey==!!t.ctrlKey&&!!e.altKey==!!t.altKey&&!!e.metaKey==!!t.metaKey)}function te(t){return t.trim().split(" ").map((function(t){return function(t){return 1===t.length?{combo:t,key:t,event:"keydown"}:t.split("+").reduce((function(t,e){var i=e.split(":"),n=i[0],o=i[1];return n in Gt?(t[Gt[n]]=!0,t.hasModifiers=!0):(t.key=n,t.event=o||"keydown"),t}),{combo:t.split(":").shift()})}(t)}))}const ee={properties:{keyEventTarget:{type:Object,value:function(){return this}},stopKeyboardEventPropagation:{type:Boolean,value:!1},_boundKeyHandlers:{type:Array,value:function(){return[]}},_imperativeKeyBindings:{type:Object,value:function(){return{}}}},observers:["_resetKeyEventListeners(keyEventTarget, _boundKeyHandlers)"],keyBindings:{},registered:function(){this._prepKeyBindings()},attached:function(){this._listenKeyEventListeners()},detached:function(){this._unlistenKeyEventListeners()},addOwnKeyBinding:function(t,e){this._imperativeKeyBindings[t]=e,this._prepKeyBindings(),this._resetKeyEventListeners()},removeOwnKeyBindings:function(){this._imperativeKeyBindings={},this._prepKeyBindings(),this._resetKeyEventListeners()},keyboardEventMatchesKeys:function(t,e){for(var i=te(e),n=0;n<i.length;++n)if(Jt(i[n],t))return!0;return!1},_collectKeyBindings:function(){var t=this.behaviors.map((function(t){return t.keyBindings}));return-1===t.indexOf(this.keyBindings)&&t.push(this.keyBindings),t},_prepKeyBindings:function(){for(var t in this._keyBindings={},this._collectKeyBindings().forEach((function(t){for(var e in t)this._addKeyBinding(e,t[e])}),this),this._imperativeKeyBindings)this._addKeyBinding(t,this._imperativeKeyBindings[t]);for(var e in this._keyBindings)this._keyBindings[e].sort((function(t,e){var i=t[0].hasModifiers;return i===e[0].hasModifiers?0:i?-1:1}))},_addKeyBinding:function(t,e){te(t).forEach((function(t){this._keyBindings[t.event]=this._keyBindings[t.event]||[],this._keyBindings[t.event].push([t,e])}),this)},_resetKeyEventListeners:function(){this._unlistenKeyEventListeners(),this.isAttached&&this._listenKeyEventListeners()},_listenKeyEventListeners:function(){this.keyEventTarget&&Object.keys(this._keyBindings).forEach((function(t){var e=this._keyBindings[t],i=this._onKeyBindingEvent.bind(this,e);this._boundKeyHandlers.push([this.keyEventTarget,t,i]),this.keyEventTarget.addEventListener(t,i)}),this)},_unlistenKeyEventListeners:function(){for(var t,e,i,n;this._boundKeyHandlers.length;)e=(t=this._boundKeyHandlers.pop())[0],i=t[1],n=t[2],e.removeEventListener(i,n)},_onKeyBindingEvent:function(t,e){if(this.stopKeyboardEventPropagation&&e.stopPropagation(),!e.defaultPrevented)for(var i=0;i<t.length;i++){var n=t[i][0],o=t[i][1];if(Jt(n,e)&&(this._triggerKeyHandler(n,o,e),e.defaultPrevented))return}},_triggerKeyHandler:function(t,e,i){var n=Object.create(t);n.keyboardEvent=i;var o=new CustomEvent(t.event,{detail:n,cancelable:!0});this[e].call(this,o),o.defaultPrevented&&i.preventDefault()}},ie={properties:{focused:{type:Boolean,value:!1,notify:!0,readOnly:!0,reflectToAttribute:!0},disabled:{type:Boolean,value:!1,notify:!0,observer:"_disabledChanged",reflectToAttribute:!0},_oldTabIndex:{type:String},_boundFocusBlurHandler:{type:Function,value:function(){return this._focusBlurHandler.bind(this)}}},observers:["_changedControlState(focused, disabled)"],ready:function(){this.addEventListener("focus",this._boundFocusBlurHandler,!0),this.addEventListener("blur",this._boundFocusBlurHandler,!0)},_focusBlurHandler:function(t){this._setFocused("focus"===t.type)},_disabledChanged:function(t,e){this.setAttribute("aria-disabled",t?"true":"false"),this.style.pointerEvents=t?"none":"",t?(this._oldTabIndex=this.getAttribute("tabindex"),this._setFocused(!1),this.tabIndex=-1,this.blur()):void 0!==this._oldTabIndex&&(null===this._oldTabIndex?this.removeAttribute("tabindex"):this.setAttribute("tabindex",this._oldTabIndex))},_changedControlState:function(){this._controlStateChanged&&this._controlStateChanged()}},ne={NextLabelID:1,NextAddonID:1,NextInputID:1},oe={properties:{label:{type:String},value:{notify:!0,type:String},disabled:{type:Boolean,value:!1},invalid:{type:Boolean,value:!1,notify:!0},allowedPattern:{type:String},type:{type:String},list:{type:String},pattern:{type:String},required:{type:Boolean,value:!1},errorMessage:{type:String},charCounter:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1},alwaysFloatLabel:{type:Boolean,value:!1},autoValidate:{type:Boolean,value:!1},validator:{type:String},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,observer:"_autofocusChanged"},inputmode:{type:String},minlength:{type:Number},maxlength:{type:Number},min:{type:String},max:{type:String},step:{type:String},name:{type:String},placeholder:{type:String,value:""},readonly:{type:Boolean,value:!1},size:{type:Number},autocapitalize:{type:String,value:"none"},autocorrect:{type:String,value:"off"},autosave:{type:String},results:{type:Number},accept:{type:String},multiple:{type:Boolean},_ariaDescribedBy:{type:String,value:""},_ariaLabelledBy:{type:String,value:""},_inputId:{type:String,value:""}},listeners:{"addon-attached":"_onAddonAttached"},keyBindings:{"shift+tab:keydown":"_onShiftTabDown"},hostAttributes:{tabindex:0},get inputElement(){return this.$||(this.$={}),this.$.input||(this._generateInputId(),this.$.input=this.$$("#"+this._inputId)),this.$.input},get _focusableElement(){return this.inputElement},created:function(){this._typesThatHaveText=["date","datetime","datetime-local","month","time","week","file"]},attached:function(){this._updateAriaLabelledBy(),!w&&this.inputElement&&-1!==this._typesThatHaveText.indexOf(this.inputElement.type)&&(this.alwaysFloatLabel=!0)},_appendStringWithSpace:function(t,e){return t=t?t+" "+e:e},_onAddonAttached:function(t){var e=x(t).rootTarget;if(e.id)this._ariaDescribedBy=this._appendStringWithSpace(this._ariaDescribedBy,e.id);else{var i="paper-input-add-on-"+ne.NextAddonID++;e.id=i,this._ariaDescribedBy=this._appendStringWithSpace(this._ariaDescribedBy,i)}},validate:function(){return this.inputElement.validate()},_focusBlurHandler:function(t){ie._focusBlurHandler.call(this,t),this.focused&&!this._shiftTabPressed&&this._focusableElement&&this._focusableElement.focus()},_onShiftTabDown:function(t){var e=this.getAttribute("tabindex");this._shiftTabPressed=!0,this.setAttribute("tabindex","-1"),this.async((function(){this.setAttribute("tabindex",e),this._shiftTabPressed=!1}),1)},_handleAutoValidate:function(){this.autoValidate&&this.validate()},updateValueAndPreserveCaret:function(t){try{var e=this.inputElement.selectionStart;this.value=t,this.inputElement.selectionStart=e,this.inputElement.selectionEnd=e}catch(e){this.value=t}},_computeAlwaysFloatLabel:function(t,e){return e||t},_updateAriaLabelledBy:function(){var t,e=x(this.root).querySelector("label");e?(e.id?t=e.id:(t="paper-input-label-"+ne.NextLabelID++,e.id=t),this._ariaLabelledBy=t):this._ariaLabelledBy=""},_generateInputId:function(){this._inputId&&""!==this._inputId||(this._inputId="input-"+ne.NextInputID++)},_onChange:function(t){this.shadowRoot&&this.fire(t.type,{sourceEvent:t},{node:this,bubbles:t.bubbles,cancelable:t.cancelable})},_autofocusChanged:function(){if(this.autofocus&&this._focusableElement){var t=document.activeElement;t instanceof HTMLElement&&t!==document.body&&t!==document.documentElement||this._focusableElement.focus()}}},se=[ie,ee,oe];v({is:"paper-input",_template:y`
    <style>
      :host {
        display: block;
      }

      :host([focused]) {
        outline: none;
      }

      :host([hidden]) {
        display: none !important;
      }

      input {
        /* Firefox sets a min-width on the input, which can cause layout issues */
        min-width: 0;
      }

      /* In 1.x, the <input> is distributed to paper-input-container, which styles it.
      In 2.x the <iron-input> is distributed to paper-input-container, which styles
      it, but in order for this to work correctly, we need to reset some
      of the native input's properties to inherit (from the iron-input) */
      iron-input > input {
        @apply --paper-input-container-shared-input-style;
        font-family: inherit;
        font-weight: inherit;
        font-size: inherit;
        letter-spacing: inherit;
        word-spacing: inherit;
        line-height: inherit;
        text-shadow: inherit;
        color: inherit;
        cursor: inherit;
      }

      input:disabled {
        @apply --paper-input-container-input-disabled;
      }

      input::-webkit-outer-spin-button,
      input::-webkit-inner-spin-button {
        @apply --paper-input-container-input-webkit-spinner;
      }

      input::-webkit-clear-button {
        @apply --paper-input-container-input-webkit-clear;
      }

      input::-webkit-calendar-picker-indicator {
        @apply --paper-input-container-input-webkit-calendar-picker-indicator;
      }

      input::-webkit-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input:-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-moz-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      input::-ms-clear {
        @apply --paper-input-container-ms-clear;
      }

      input::-ms-reveal {
        @apply --paper-input-container-ms-reveal;
      }

      input:-ms-input-placeholder {
        color: var(--paper-input-container-color, var(--secondary-text-color));
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container id="container" no-label-float="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <slot name="prefix" slot="prefix"></slot>

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <!-- Need to bind maxlength so that the paper-input-char-counter works correctly -->
      <iron-input bind-value="{{value}}" slot="input" class="input-element" id$="[[_inputId]]" maxlength$="[[maxlength]]" allowed-pattern="[[allowedPattern]]" invalid="{{invalid}}" validator="[[validator]]">
        <input aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" disabled$="[[disabled]]" title$="[[title]]" type$="[[type]]" pattern$="[[pattern]]" required$="[[required]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" min$="[[min]]" max$="[[max]]" step$="[[step]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" list$="[[list]]" size$="[[size]]" autocapitalize$="[[autocapitalize]]" autocorrect$="[[autocorrect]]" on-change="_onChange" tabindex$="[[tabIndex]]" autosave$="[[autosave]]" results$="[[results]]" accept$="[[accept]]" multiple$="[[multiple]]" role$="[[inputRole]]" aria-haspopup$="[[inputAriaHaspopup]]">
      </iron-input>

      <slot name="suffix" slot="suffix"></slot>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
  `,behaviors:[se,Vt],properties:{value:{type:String},inputRole:{type:String,value:void 0},inputAriaHaspopup:{type:String,value:void 0}},get _focusableElement(){return this.inputElement._inputElement},listeners:{"iron-input-ready":"_onIronInputReady"},_onIronInputReady:function(){this.$.nativeInput||(this.$.nativeInput=this.$$("input")),this.inputElement&&-1!==this._typesThatHaveText.indexOf(this.$.nativeInput.type)&&(this.alwaysFloatLabel=!0),this.inputElement.bindValue&&this.$.container._handleValueAndAutoValidate(this.inputElement)}}),E([u("search-input")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"filter",value:void 0},{kind:"field",decorators:[s({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value:()=>!1},{kind:"field",decorators:[s({type:Boolean,attribute:"no-underline"})],key:"noUnderline",value:()=>!1},{kind:"field",decorators:[s({type:Boolean})],key:"autofocus",value:()=>!1},{kind:"field",decorators:[s({type:String})],key:"label",value:void 0},{kind:"method",key:"focus",value:function(){this.shadowRoot.querySelector("paper-input").focus()}},{kind:"field",decorators:[n("paper-input",!0)],key:"_input",value:void 0},{kind:"method",key:"render",value:function(){return l`
      <paper-input
        .autofocus=${this.autofocus}
        .label=${this.label||"Search"}
        .value=${this.filter}
        @value-changed=${this._filterInputChanged}
        .noLabelFloat=${this.noLabelFloat}
      >
        <slot name="prefix" slot="prefix">
          <ha-svg-icon class="prefix" .path=${I}></ha-svg-icon>
        </slot>
        ${this.filter&&l`
          <ha-icon-button
            slot="suffix"
            @click=${this._clearSearch}
            .label=${this.hass.localize("ui.common.clear")}
            .path=${C}
          ></ha-icon-button>
        `}
      </paper-input>
    `}},{kind:"method",key:"updated",value:function(t){t.has("noUnderline")&&(this.noUnderline||void 0!==t.get("noUnderline"))&&(this._input.inputElement.parentElement.shadowRoot.querySelector("div.unfocused-line").style.display=this.noUnderline?"none":"block")}},{kind:"method",key:"_filterChanged",value:async function(t){T(this,"value-changed",{value:String(t)})}},{kind:"method",key:"_filterInputChanged",value:async function(t){this._filterChanged(t.target.value)}},{kind:"method",key:"_clearSearch",value:async function(){this._filterChanged("")}},{kind:"get",static:!0,key:"styles",value:function(){return h`
      ha-svg-icon,
      ha-icon-button {
        color: var(--primary-text-color);
      }
      ha-icon-button {
        --mdc-icon-button-size: 24px;
      }
      ha-svg-icon.prefix {
        margin: 8px;
      }
    `}}]}}),r);const ae=(t,e,i=!1)=>{let n;return(...o)=>{const s=i&&!n;clearTimeout(n),n=window.setTimeout(()=>{n=void 0,i||t(...o)},e),s&&t(...o)}},re=()=>new Promise(t=>{var e;e=t,requestAnimationFrame(()=>setTimeout(e,0))});var ce,le;const de=null!==(le=null===(ce=window.ShadyDOM)||void 0===ce?void 0:ce.inUse)&&void 0!==le&&le;class he extends S{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=t=>{this.disabled||this.setFormData(t.formData)}}findFormElement(){if(!this.shadowRoot||de)return null;const t=this.getRootNode().querySelectorAll("form");for(const e of Array.from(t))if(e.contains(this))return e;return null}connectedCallback(){var t;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(t=this.containingForm)||void 0===t||t.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this.containingForm)||void 0===t||t.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",t=>{this.dispatchEvent(new Event("change",t))})}}he.shadowRootOptions={mode:"open",delegatesFocus:!0},i([s({type:Boolean})],he.prototype,"disabled",void 0);class ue extends he{constructor(){super(...arguments),this.checked=!1,this.indeterminate=!1,this.disabled=!1,this.name="",this.value="on",this.reducedTouchTarget=!1,this.animationClass="",this.shouldRenderRipple=!1,this.focused=!1,this.mdcFoundationClass=void 0,this.mdcFoundation=void 0,this.rippleElement=null,this.rippleHandlers=new c(()=>(this.shouldRenderRipple=!0,this.ripple.then(t=>this.rippleElement=t),this.ripple))}createAdapter(){return{}}update(t){const e=t.get("indeterminate"),i=t.get("checked"),n=t.get("disabled");if(void 0!==e||void 0!==i||void 0!==n){const t=this.calculateAnimationStateName(!!i,!!e,!!n),o=this.calculateAnimationStateName(this.checked,this.indeterminate,this.disabled);this.animationClass=`${t}-${o}`}super.update(t)}calculateAnimationStateName(t,e,i){return i?"disabled":e?"indeterminate":t?"checked":"unchecked"}renderRipple(){return this.shouldRenderRipple?this.renderRippleTemplate():""}renderRippleTemplate(){return l`<mwc-ripple
        .disabled="${this.disabled}"
        unbounded></mwc-ripple>`}render(){const t=this.indeterminate||this.checked,e={"mdc-checkbox--disabled":this.disabled,"mdc-checkbox--selected":t,"mdc-checkbox--touch":!this.reducedTouchTarget,"mdc-ripple-upgraded--background-focused":this.focused,"mdc-checkbox--anim-checked-indeterminate":"checked-indeterminate"==this.animationClass,"mdc-checkbox--anim-checked-unchecked":"checked-unchecked"==this.animationClass,"mdc-checkbox--anim-indeterminate-checked":"indeterminate-checked"==this.animationClass,"mdc-checkbox--anim-indeterminate-unchecked":"indeterminate-unchecked"==this.animationClass,"mdc-checkbox--anim-unchecked-checked":"unchecked-checked"==this.animationClass,"mdc-checkbox--anim-unchecked-indeterminate":"unchecked-indeterminate"==this.animationClass},i=this.indeterminate?"mixed":void 0;return l`
      <div class="mdc-checkbox mdc-checkbox--upgraded ${d(e)}">
        <input type="checkbox"
              class="mdc-checkbox__native-control"
              name="${O(this.name)}"
              aria-checked="${O(i)}"
              aria-label="${O(this.ariaLabel)}"
              aria-labelledby="${O(this.ariaLabelledBy)}"
              aria-describedby="${O(this.ariaDescribedBy)}"
              data-indeterminate="${this.indeterminate?"true":"false"}"
              ?disabled="${this.disabled}"
              .indeterminate="${this.indeterminate}"
              .checked="${this.checked}"
              .value="${this.value}"
              @change="${this.handleChange}"
              @focus="${this.handleFocus}"
              @blur="${this.handleBlur}"
              @mousedown="${this.handleRippleMouseDown}"
              @mouseenter="${this.handleRippleMouseEnter}"
              @mouseleave="${this.handleRippleMouseLeave}"
              @touchstart="${this.handleRippleTouchStart}"
              @touchend="${this.handleRippleDeactivate}"
              @touchcancel="${this.handleRippleDeactivate}">
        <div class="mdc-checkbox__background"
          @animationend="${this.resetAnimationClass}">
          <svg class="mdc-checkbox__checkmark"
              viewBox="0 0 24 24">
            <path class="mdc-checkbox__checkmark-path"
                  fill="none"
                  d="M1.73,12.91 8.1,19.28 22.79,4.59"></path>
          </svg>
          <div class="mdc-checkbox__mixedmark"></div>
        </div>
        ${this.renderRipple()}
      </div>`}setFormData(t){this.name&&this.checked&&t.append(this.name,this.value)}handleFocus(){this.focused=!0,this.handleRippleFocus()}handleBlur(){this.focused=!1,this.handleRippleBlur()}handleRippleMouseDown(t){const e=()=>{window.removeEventListener("mouseup",e),this.handleRippleDeactivate()};window.addEventListener("mouseup",e),this.rippleHandlers.startPress(t)}handleRippleTouchStart(t){this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}handleChange(){this.checked=this.formElement.checked,this.indeterminate=this.formElement.indeterminate}resetAnimationClass(){this.animationClass=""}get isRippleActive(){var t;return(null===(t=this.rippleElement)||void 0===t?void 0:t.isActive)||!1}}i([n(".mdc-checkbox")],ue.prototype,"mdcRoot",void 0),i([n("input")],ue.prototype,"formElement",void 0),i([s({type:Boolean,reflect:!0})],ue.prototype,"checked",void 0),i([s({type:Boolean})],ue.prototype,"indeterminate",void 0),i([s({type:Boolean,reflect:!0})],ue.prototype,"disabled",void 0),i([s({type:String,reflect:!0})],ue.prototype,"name",void 0),i([s({type:String})],ue.prototype,"value",void 0),i([A,s({type:String,attribute:"aria-label"})],ue.prototype,"ariaLabel",void 0),i([A,s({type:String,attribute:"aria-labelledby"})],ue.prototype,"ariaLabelledBy",void 0),i([A,s({type:String,attribute:"aria-describedby"})],ue.prototype,"ariaDescribedBy",void 0),i([s({type:Boolean})],ue.prototype,"reducedTouchTarget",void 0),i([a()],ue.prototype,"animationClass",void 0),i([a()],ue.prototype,"shouldRenderRipple",void 0),i([a()],ue.prototype,"focused",void 0),i([o("mwc-ripple")],ue.prototype,"ripple",void 0),i([R({passive:!0})],ue.prototype,"handleRippleTouchStart",null);const pe=h`.mdc-checkbox{padding:calc((40px - 18px) / 2);padding:calc((var(--mdc-checkbox-ripple-size, 40px) - 18px) / 2);margin:calc((40px - 40px) / 2);margin:calc((var(--mdc-checkbox-touch-target-size, 40px) - 40px) / 2)}.mdc-checkbox .mdc-checkbox__ripple::before,.mdc-checkbox .mdc-checkbox__ripple::after{background-color:#000;background-color:var(--mdc-ripple-color, #000)}.mdc-checkbox:hover .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-ripple-surface--hover .mdc-checkbox__ripple::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-checkbox.mdc-ripple-upgraded--background-focused .mdc-checkbox__ripple::before,.mdc-checkbox:not(.mdc-ripple-upgraded):focus .mdc-checkbox__ripple::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-checkbox:not(.mdc-ripple-upgraded) .mdc-checkbox__ripple::after{transition:opacity 150ms linear}.mdc-checkbox:not(.mdc-ripple-upgraded):active .mdc-checkbox__ripple::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-checkbox.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-checkbox.mdc-checkbox--selected .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-checkbox--selected .mdc-checkbox__ripple::after{background-color:#018786;background-color:var(--mdc-ripple-color, var(--mdc-theme-secondary, #018786))}.mdc-checkbox.mdc-checkbox--selected:hover .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-checkbox--selected.mdc-ripple-surface--hover .mdc-checkbox__ripple::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-checkbox.mdc-checkbox--selected.mdc-ripple-upgraded--background-focused .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded):focus .mdc-checkbox__ripple::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded) .mdc-checkbox__ripple::after{transition:opacity 150ms linear}.mdc-checkbox.mdc-checkbox--selected:not(.mdc-ripple-upgraded):active .mdc-checkbox__ripple::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-checkbox.mdc-checkbox--selected.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-checkbox.mdc-ripple-upgraded--background-focused.mdc-checkbox--selected .mdc-checkbox__ripple::before,.mdc-checkbox.mdc-ripple-upgraded--background-focused.mdc-checkbox--selected .mdc-checkbox__ripple::after{background-color:#018786;background-color:var(--mdc-ripple-color, var(--mdc-theme-secondary, #018786))}.mdc-checkbox .mdc-checkbox__background{top:calc((40px - 18px) / 2);top:calc((var(--mdc-checkbox-ripple-size, 40px) - 18px) / 2);left:calc((40px - 18px) / 2);left:calc((var(--mdc-checkbox-ripple-size, 40px) - 18px) / 2)}.mdc-checkbox .mdc-checkbox__native-control{top:calc((40px - 40px) / 2);top:calc((40px - var(--mdc-checkbox-touch-target-size, 40px)) / 2);right:calc((40px - 40px) / 2);right:calc((40px - var(--mdc-checkbox-touch-target-size, 40px)) / 2);left:calc((40px - 40px) / 2);left:calc((40px - var(--mdc-checkbox-touch-target-size, 40px)) / 2);width:40px;width:var(--mdc-checkbox-touch-target-size, 40px);height:40px;height:var(--mdc-checkbox-touch-target-size, 40px)}.mdc-checkbox .mdc-checkbox__native-control:enabled:not(:checked):not(:indeterminate):not([data-indeterminate=true])~.mdc-checkbox__background{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}.mdc-checkbox .mdc-checkbox__native-control:enabled:checked~.mdc-checkbox__background,.mdc-checkbox .mdc-checkbox__native-control:enabled:indeterminate~.mdc-checkbox__background,.mdc-checkbox .mdc-checkbox__native-control[data-indeterminate=true]:enabled~.mdc-checkbox__background{border-color:#018786;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786));background-color:#018786;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786))}@keyframes mdc-checkbox-fade-in-background-8A000000FF01878600000000FF018786{0%{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}50%{border-color:#018786;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786));background-color:#018786;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786))}}@keyframes mdc-checkbox-fade-out-background-8A000000FF01878600000000FF018786{0%,80%{border-color:#018786;border-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786));background-color:#018786;background-color:var(--mdc-checkbox-checked-color, var(--mdc-theme-secondary, #018786))}100%{border-color:rgba(0, 0, 0, 0.54);border-color:var(--mdc-checkbox-unchecked-color, rgba(0, 0, 0, 0.54));background-color:transparent}}.mdc-checkbox.mdc-checkbox--anim-unchecked-checked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background,.mdc-checkbox.mdc-checkbox--anim-unchecked-indeterminate .mdc-checkbox__native-control:enabled~.mdc-checkbox__background{animation-name:mdc-checkbox-fade-in-background-8A000000FF01878600000000FF018786}.mdc-checkbox.mdc-checkbox--anim-checked-unchecked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background,.mdc-checkbox.mdc-checkbox--anim-indeterminate-unchecked .mdc-checkbox__native-control:enabled~.mdc-checkbox__background{animation-name:mdc-checkbox-fade-out-background-8A000000FF01878600000000FF018786}.mdc-checkbox .mdc-checkbox__native-control[disabled]:not(:checked):not(:indeterminate):not([data-indeterminate=true])~.mdc-checkbox__background{border-color:rgba(0, 0, 0, 0.38);border-color:var(--mdc-checkbox-disabled-color, rgba(0, 0, 0, 0.38));background-color:transparent}.mdc-checkbox .mdc-checkbox__native-control[disabled]:checked~.mdc-checkbox__background,.mdc-checkbox .mdc-checkbox__native-control[disabled]:indeterminate~.mdc-checkbox__background,.mdc-checkbox .mdc-checkbox__native-control[data-indeterminate=true][disabled]~.mdc-checkbox__background{border-color:transparent;background-color:rgba(0, 0, 0, 0.38);background-color:var(--mdc-checkbox-disabled-color, rgba(0, 0, 0, 0.38))}.mdc-checkbox .mdc-checkbox__native-control:enabled~.mdc-checkbox__background .mdc-checkbox__checkmark{color:#fff;color:var(--mdc-checkbox-ink-color, #fff)}.mdc-checkbox .mdc-checkbox__native-control:enabled~.mdc-checkbox__background .mdc-checkbox__mixedmark{border-color:#fff;border-color:var(--mdc-checkbox-ink-color, #fff)}.mdc-checkbox .mdc-checkbox__native-control:disabled~.mdc-checkbox__background .mdc-checkbox__checkmark{color:#fff;color:var(--mdc-checkbox-ink-color, #fff)}.mdc-checkbox .mdc-checkbox__native-control:disabled~.mdc-checkbox__background .mdc-checkbox__mixedmark{border-color:#fff;border-color:var(--mdc-checkbox-ink-color, #fff)}.mdc-touch-target-wrapper{display:inline}@keyframes mdc-checkbox-unchecked-checked-checkmark-path{0%,50%{stroke-dashoffset:29.7833385}50%{animation-timing-function:cubic-bezier(0, 0, 0.2, 1)}100%{stroke-dashoffset:0}}@keyframes mdc-checkbox-unchecked-indeterminate-mixedmark{0%,68.2%{transform:scaleX(0)}68.2%{animation-timing-function:cubic-bezier(0, 0, 0, 1)}100%{transform:scaleX(1)}}@keyframes mdc-checkbox-checked-unchecked-checkmark-path{from{animation-timing-function:cubic-bezier(0.4, 0, 1, 1);opacity:1;stroke-dashoffset:0}to{opacity:0;stroke-dashoffset:-29.7833385}}@keyframes mdc-checkbox-checked-indeterminate-checkmark{from{animation-timing-function:cubic-bezier(0, 0, 0.2, 1);transform:rotate(0deg);opacity:1}to{transform:rotate(45deg);opacity:0}}@keyframes mdc-checkbox-indeterminate-checked-checkmark{from{animation-timing-function:cubic-bezier(0.14, 0, 0, 1);transform:rotate(45deg);opacity:0}to{transform:rotate(360deg);opacity:1}}@keyframes mdc-checkbox-checked-indeterminate-mixedmark{from{animation-timing-function:mdc-animation-deceleration-curve-timing-function;transform:rotate(-45deg);opacity:0}to{transform:rotate(0deg);opacity:1}}@keyframes mdc-checkbox-indeterminate-checked-mixedmark{from{animation-timing-function:cubic-bezier(0.14, 0, 0, 1);transform:rotate(0deg);opacity:1}to{transform:rotate(315deg);opacity:0}}@keyframes mdc-checkbox-indeterminate-unchecked-mixedmark{0%{animation-timing-function:linear;transform:scaleX(1);opacity:1}32.8%,100%{transform:scaleX(0);opacity:0}}.mdc-checkbox{display:inline-block;position:relative;flex:0 0 18px;box-sizing:content-box;width:18px;height:18px;line-height:0;white-space:nowrap;cursor:pointer;vertical-align:bottom}@media screen and (forced-colors: active),(-ms-high-contrast: active){.mdc-checkbox__native-control[disabled]:not(:checked):not(:indeterminate):not([data-indeterminate=true])~.mdc-checkbox__background{border-color:GrayText;border-color:var(--mdc-checkbox-disabled-color, GrayText);background-color:transparent}.mdc-checkbox__native-control[disabled]:checked~.mdc-checkbox__background,.mdc-checkbox__native-control[disabled]:indeterminate~.mdc-checkbox__background,.mdc-checkbox__native-control[data-indeterminate=true][disabled]~.mdc-checkbox__background{border-color:GrayText;background-color:transparent;background-color:var(--mdc-checkbox-disabled-color, transparent)}.mdc-checkbox__native-control:disabled~.mdc-checkbox__background .mdc-checkbox__checkmark{color:GrayText;color:var(--mdc-checkbox-ink-color, GrayText)}.mdc-checkbox__native-control:disabled~.mdc-checkbox__background .mdc-checkbox__mixedmark{border-color:GrayText;border-color:var(--mdc-checkbox-ink-color, GrayText)}.mdc-checkbox__mixedmark{margin:0 1px}}.mdc-checkbox--disabled{cursor:default;pointer-events:none}.mdc-checkbox__background{display:inline-flex;position:absolute;align-items:center;justify-content:center;box-sizing:border-box;width:18px;height:18px;border:2px solid currentColor;border-radius:2px;background-color:transparent;pointer-events:none;will-change:background-color,border-color;transition:background-color 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1),border-color 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-checkbox__checkmark{position:absolute;top:0;right:0;bottom:0;left:0;width:100%;opacity:0;transition:opacity 180ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-checkbox--upgraded .mdc-checkbox__checkmark{opacity:1}.mdc-checkbox__checkmark-path{transition:stroke-dashoffset 180ms 0ms cubic-bezier(0.4, 0, 0.6, 1);stroke:currentColor;stroke-width:3.12px;stroke-dashoffset:29.7833385;stroke-dasharray:29.7833385}.mdc-checkbox__mixedmark{width:100%;height:0;transform:scaleX(0) rotate(0deg);border-width:1px;border-style:solid;opacity:0;transition:opacity 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1),transform 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-checkbox--anim-unchecked-checked .mdc-checkbox__background,.mdc-checkbox--anim-unchecked-indeterminate .mdc-checkbox__background,.mdc-checkbox--anim-checked-unchecked .mdc-checkbox__background,.mdc-checkbox--anim-indeterminate-unchecked .mdc-checkbox__background{animation-duration:180ms;animation-timing-function:linear}.mdc-checkbox--anim-unchecked-checked .mdc-checkbox__checkmark-path{animation:mdc-checkbox-unchecked-checked-checkmark-path 180ms linear 0s;transition:none}.mdc-checkbox--anim-unchecked-indeterminate .mdc-checkbox__mixedmark{animation:mdc-checkbox-unchecked-indeterminate-mixedmark 90ms linear 0s;transition:none}.mdc-checkbox--anim-checked-unchecked .mdc-checkbox__checkmark-path{animation:mdc-checkbox-checked-unchecked-checkmark-path 90ms linear 0s;transition:none}.mdc-checkbox--anim-checked-indeterminate .mdc-checkbox__checkmark{animation:mdc-checkbox-checked-indeterminate-checkmark 90ms linear 0s;transition:none}.mdc-checkbox--anim-checked-indeterminate .mdc-checkbox__mixedmark{animation:mdc-checkbox-checked-indeterminate-mixedmark 90ms linear 0s;transition:none}.mdc-checkbox--anim-indeterminate-checked .mdc-checkbox__checkmark{animation:mdc-checkbox-indeterminate-checked-checkmark 500ms linear 0s;transition:none}.mdc-checkbox--anim-indeterminate-checked .mdc-checkbox__mixedmark{animation:mdc-checkbox-indeterminate-checked-mixedmark 500ms linear 0s;transition:none}.mdc-checkbox--anim-indeterminate-unchecked .mdc-checkbox__mixedmark{animation:mdc-checkbox-indeterminate-unchecked-mixedmark 300ms linear 0s;transition:none}.mdc-checkbox__native-control:checked~.mdc-checkbox__background,.mdc-checkbox__native-control:indeterminate~.mdc-checkbox__background,.mdc-checkbox__native-control[data-indeterminate=true]~.mdc-checkbox__background{transition:border-color 90ms 0ms cubic-bezier(0, 0, 0.2, 1),background-color 90ms 0ms cubic-bezier(0, 0, 0.2, 1)}.mdc-checkbox__native-control:checked~.mdc-checkbox__background .mdc-checkbox__checkmark-path,.mdc-checkbox__native-control:indeterminate~.mdc-checkbox__background .mdc-checkbox__checkmark-path,.mdc-checkbox__native-control[data-indeterminate=true]~.mdc-checkbox__background .mdc-checkbox__checkmark-path{stroke-dashoffset:0}.mdc-checkbox__native-control{position:absolute;margin:0;padding:0;opacity:0;cursor:inherit}.mdc-checkbox__native-control:disabled{cursor:default;pointer-events:none}.mdc-checkbox--touch{margin:calc((48px - 40px) / 2);margin:calc((var(--mdc-checkbox-state-layer-size, 48px) - var(--mdc-checkbox-state-layer-size, 40px)) / 2)}.mdc-checkbox--touch .mdc-checkbox__native-control{top:calc((40px - 48px) / 2);top:calc((var(--mdc-checkbox-state-layer-size, 40px) - var(--mdc-checkbox-state-layer-size, 48px)) / 2);right:calc((40px - 48px) / 2);right:calc((var(--mdc-checkbox-state-layer-size, 40px) - var(--mdc-checkbox-state-layer-size, 48px)) / 2);left:calc((40px - 48px) / 2);left:calc((var(--mdc-checkbox-state-layer-size, 40px) - var(--mdc-checkbox-state-layer-size, 48px)) / 2);width:48px;width:var(--mdc-checkbox-state-layer-size, 48px);height:48px;height:var(--mdc-checkbox-state-layer-size, 48px)}.mdc-checkbox__native-control:checked~.mdc-checkbox__background .mdc-checkbox__checkmark{transition:opacity 180ms 0ms cubic-bezier(0, 0, 0.2, 1),transform 180ms 0ms cubic-bezier(0, 0, 0.2, 1);opacity:1}.mdc-checkbox__native-control:checked~.mdc-checkbox__background .mdc-checkbox__mixedmark{transform:scaleX(1) rotate(-45deg)}.mdc-checkbox__native-control:indeterminate~.mdc-checkbox__background .mdc-checkbox__checkmark,.mdc-checkbox__native-control[data-indeterminate=true]~.mdc-checkbox__background .mdc-checkbox__checkmark{transform:rotate(45deg);opacity:0;transition:opacity 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1),transform 90ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-checkbox__native-control:indeterminate~.mdc-checkbox__background .mdc-checkbox__mixedmark,.mdc-checkbox__native-control[data-indeterminate=true]~.mdc-checkbox__background .mdc-checkbox__mixedmark{transform:scaleX(1) rotate(0deg);opacity:1}.mdc-checkbox.mdc-checkbox--upgraded .mdc-checkbox__background,.mdc-checkbox.mdc-checkbox--upgraded .mdc-checkbox__checkmark,.mdc-checkbox.mdc-checkbox--upgraded .mdc-checkbox__checkmark-path,.mdc-checkbox.mdc-checkbox--upgraded .mdc-checkbox__mixedmark{transition:none}:host{outline:none;display:inline-flex;-webkit-tap-highlight-color:transparent}:host([checked]),:host([indeterminate]){--mdc-ripple-color:var(--mdc-theme-secondary, #018786)}.mdc-checkbox .mdc-checkbox__background::before{content:none}`;let me=class extends ue{};me.styles=[pe],me=i([u("mwc-checkbox")],me),E([u("ha-checkbox")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"method",key:"firstUpdated",value:function(){F(z(i.prototype),"firstUpdated",this).call(this),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}}]}}),me);E([u("insteon-data-table")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s({type:Object})],key:"columns",value:()=>({})},{kind:"field",decorators:[s({type:Array})],key:"data",value:()=>[]},{kind:"field",decorators:[s({type:Boolean})],key:"selectable",value:()=>!1},{kind:"field",decorators:[s({type:Boolean})],key:"clickable",value:()=>!1},{kind:"field",decorators:[s({type:Boolean})],key:"hasFab",value:()=>!1},{kind:"field",decorators:[s({attribute:!1})],key:"appendRow",value:void 0},{kind:"field",decorators:[s({type:Boolean,attribute:"auto-height"})],key:"autoHeight",value:()=>!1},{kind:"field",decorators:[s({type:String})],key:"id",value:()=>"id"},{kind:"field",decorators:[s({type:String})],key:"noDataText",value:void 0},{kind:"field",decorators:[s({type:String})],key:"searchLabel",value:void 0},{kind:"field",decorators:[s({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value:()=>!1},{kind:"field",decorators:[s({type:String})],key:"filter",value:()=>""},{kind:"field",decorators:[a()],key:"_filterable",value:()=>!1},{kind:"field",decorators:[a()],key:"_filter",value:()=>""},{kind:"field",decorators:[a()],key:"_sortColumn",value:void 0},{kind:"field",decorators:[a()],key:"_sortDirection",value:()=>null},{kind:"field",decorators:[a()],key:"_filteredData",value:()=>[]},{kind:"field",decorators:[a()],key:"_headerHeight",value:()=>0},{kind:"field",decorators:[n("slot[name='header']")],key:"_header",value:void 0},{kind:"field",decorators:[a()],key:"_items",value:()=>[]},{kind:"field",key:"_checkableRowsCount",value:void 0},{kind:"field",key:"_checkedRows",value:()=>[]},{kind:"field",key:"_sortColumns",value:()=>({})},{kind:"field",key:"curRequest",value:()=>0},{kind:"field",decorators:[Lt(".scroller")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_debounceSearch",value(){return ae(t=>{this._filter=t},100,!1)}},{kind:"method",key:"clearSelection",value:function(){this._checkedRows=[],this._checkedRowsChanged()}},{kind:"method",key:"connectedCallback",value:function(){F(z(i.prototype),"connectedCallback",this).call(this),this._items.length&&(this._items=[...this._items])}},{kind:"method",key:"firstUpdated",value:function(){this.updateComplete.then(()=>this._calcTableHeight())}},{kind:"method",key:"willUpdate",value:function(t){if(F(z(i.prototype),"willUpdate",this).call(this,t),t.has("columns")){this._filterable=Object.values(this.columns).some(t=>t.filterable);for(const t in this.columns)if(this.columns[t].direction){this._sortDirection=this.columns[t].direction,this._sortColumn=t;break}const t=zt(this.columns);Object.values(t).forEach(t=>{delete t.title,delete t.type,delete t.template}),this._sortColumns=t}t.has("filter")&&this._debounceSearch(this.filter),t.has("data")&&(this._checkableRowsCount=this.data.filter(t=>!1!==t.selectable).length),(t.has("data")||t.has("columns")||t.has("_filter")||t.has("_sortColumn")||t.has("_sortDirection"))&&this._sortFilterData()}},{kind:"method",key:"render",value:function(){return l`
      <div class="mdc-data-table">
        <slot name="header" @slotchange=${this._calcTableHeight}>
          ${this._filterable?l`
                <div class="table-header">
                  <search-input
                    .hass=${this.hass}
                    @value-changed=${this._handleSearchChange}
                    .label=${this.searchLabel}
                    .noLabelFloat=${this.noLabelFloat}
                  ></search-input>
                </div>
              `:""}
        </slot>
        <div
          class="mdc-data-table__table ${d({"auto-height":this.autoHeight})}"
          role="table"
          aria-rowcount=${this._filteredData.length-1}
          style=${L({height:this.autoHeight?53*(this._filteredData.length||1)+53+"px":`calc(100% - ${this._headerHeight}px)`})}
        >
          <div class="mdc-data-table__header-row" role="row" aria-rowindex="1">
            ${this.selectable?l`
                  <div
                    class="mdc-data-table__header-cell mdc-data-table__header-cell--checkbox"
                    role="columnheader"
                  >
                    <ha-checkbox
                      class="mdc-data-table__row-checkbox"
                      @change=${this._handleHeaderRowCheckboxClick}
                      .indeterminate=${this._checkedRows.length&&this._checkedRows.length!==this._checkableRowsCount}
                      .checked=${this._checkedRows.length===this._checkableRowsCount}
                    >
                    </ha-checkbox>
                  </div>
                `:""}
            ${Object.entries(this.columns).map(([t,e])=>{if(e.hidden)return"";const i=t===this._sortColumn,n={"mdc-data-table__header-cell--numeric":"numeric"===e.type,"mdc-data-table__header-cell--icon":"icon"===e.type,"mdc-data-table__header-cell--icon-button":"icon-button"===e.type,"mdc-data-table__header-cell--overflow-menu":"overflow-menu"===e.type,sortable:Boolean(e.sortable),"not-sorted":Boolean(e.sortable&&!i),grows:Boolean(e.grows)};return l`
                <div
                  class="mdc-data-table__header-cell ${d(n)}"
                  style=${e.width?L({[e.grows?"minWidth":"width"]:e.width,maxWidth:e.maxWidth||""}):""}
                  role="columnheader"
                  aria-sort=${O(i?"desc"===this._sortDirection?"descending":"ascending":void 0)}
                  @click=${this._handleHeaderClick}
                  .columnId=${t}
                >
                  ${e.sortable?l`
                        <ha-svg-icon
                          .path=${i&&"desc"===this._sortDirection?D:B}
                        ></ha-svg-icon>
                      `:""}
                  <span>${e.title}</span>
                </div>
              `})}
          </div>
          ${this._filteredData.length?l`
                <div
                  class="mdc-data-table__content scroller ha-scrollbar"
                  @scroll=${this._saveScrollPos}
                >
                  ${It({items:this._items,layout:Rt,renderItem:(t,e)=>t?t.append?l` <div class="mdc-data-table__row">${t.content}</div> `:t.empty?l` <div class="mdc-data-table__row"></div> `:l`
                        <div
                          aria-rowindex=${e+2}
                          role="row"
                          .rowId=${t[this.id]}
                          @click=${this._handleRowClick}
                          class="mdc-data-table__row ${d({"mdc-data-table__row--selected":this._checkedRows.includes(String(t[this.id])),clickable:this.clickable})}"
                          aria-selected=${O(!!this._checkedRows.includes(String(t[this.id]))||void 0)}
                          .selectable=${!1!==t.selectable}
                        >
                          ${this.selectable?l`
                                <div
                                  class="mdc-data-table__cell mdc-data-table__cell--checkbox"
                                  role="cell"
                                >
                                  <ha-checkbox
                                    class="mdc-data-table__row-checkbox"
                                    @change=${this._handleRowCheckboxClick}
                                    .rowId=${t[this.id]}
                                    .disabled=${!1===t.selectable}
                                    .checked=${this._checkedRows.includes(String(t[this.id]))}
                                  >
                                  </ha-checkbox>
                                </div>
                              `:""}
                          ${Object.entries(this.columns).map(([e,i])=>i.hidden?"":l`
                              <div
                                role="cell"
                                class="mdc-data-table__cell ${d({"mdc-data-table__cell--numeric":"numeric"===i.type,"mdc-data-table__cell--icon":"icon"===i.type,"mdc-data-table__cell--icon-button":"icon-button"===i.type,"mdc-data-table__cell--overflow-menu":"overflow-menu"===i.type,grows:Boolean(i.grows),forceLTR:Boolean(i.forceLTR)})}"
                                style=${i.width?L({[i.grows?"minWidth":"width"]:i.width,maxWidth:i.maxWidth?i.maxWidth:""}):""}
                              >
                                ${i.template?i.template(t[e],t):t[e]}
                              </div>
                            `)}
                        </div>
                      `:l``})}
                </div>
              `:l`
                <div class="mdc-data-table__content">
                  <div class="mdc-data-table__row" role="row">
                    <div class="mdc-data-table__cell grows center" role="cell">
                      ${this.noDataText||"No data"}
                    </div>
                  </div>
                </div>
              `}
        </div>
      </div>
    `}},{kind:"method",key:"_sortFilterData",value:async function(){const t=(new Date).getTime();this.curRequest++;const e=this.curRequest;let i=this.data;this._filter&&(i=await this._memFilterData(this.data,this._sortColumns,this._filter));const n=this._sortColumn?((t,e,i,n)=>t.sort((t,o)=>{let s=1;"desc"===i&&(s=-1);let a=e.filterKey?t[e.valueColumn||n][e.filterKey]:t[e.valueColumn||n],r=e.filterKey?o[e.valueColumn||n][e.filterKey]:o[e.valueColumn||n];return"string"==typeof a&&(a=a.toUpperCase()),"string"==typeof r&&(r=r.toUpperCase()),void 0===a&&void 0!==r?1:void 0===r&&void 0!==a?-1:a<r?-1*s:a>r?1*s:0}))(i,this._sortColumns[this._sortColumn],this._sortDirection,this._sortColumn):i,[o]=await Promise.all([n,re]),s=(new Date).getTime()-t;if(s<100&&await new Promise(t=>setTimeout(t,100-s)),this.curRequest===e){if(this.appendRow||this.hasFab){const t=[...o];this.appendRow&&t.push({append:!0,content:this.appendRow}),this.hasFab&&t.push({empty:!0}),this._items=t}else this._items=o;this._filteredData=o}}},{kind:"field",key:"_memFilterData",value:()=>M(async(t,e,i)=>((t,e,i)=>(i=i.toUpperCase(),t.filter(t=>Object.entries(e).some(e=>{const[n,o]=e;return!(!o.filterable||!String(o.filterKey?t[o.valueColumn||n][o.filterKey]:t[o.valueColumn||n]).toUpperCase().includes(i))}))))(t,e,i))},{kind:"method",key:"_handleHeaderClick",value:function(t){const e=t.currentTarget.columnId;this.columns[e].sortable&&(this._sortDirection&&this._sortColumn===e?"asc"===this._sortDirection?this._sortDirection="desc":"desc"===this._sortDirection?this._sortDirection="asc":this._sortDirection=null:this._sortDirection="asc",this._sortColumn=null===this._sortDirection?void 0:e,T(this,"sorting-changed",{column:e,direction:this._sortDirection}))}},{kind:"method",key:"_handleHeaderRowCheckboxClick",value:function(t){t.target.checked?(this._checkedRows=this._filteredData.filter(t=>!1!==t.selectable).map(t=>t[this.id]),this._checkedRowsChanged()):(this._checkedRows=[],this._checkedRowsChanged())}},{kind:"method",key:"_handleRowCheckboxClick",value:function(t){const e=t.currentTarget,i=e.rowId;if(e.checked){if(this._checkedRows.includes(i))return;this._checkedRows=[...this._checkedRows,i]}else this._checkedRows=this._checkedRows.filter(t=>t!==i);this._checkedRowsChanged()}},{kind:"method",key:"_handleRowClick",value:function(t){const e=t.target;if(["HA-CHECKBOX","MWC-BUTTON"].includes(e.tagName))return;const i=t.currentTarget.rowId;T(this,"row-click",{id:i},{bubbles:!1})}},{kind:"method",key:"_checkedRowsChanged",value:function(){this._items.length&&(this._items=[...this._items]),T(this,"selection-changed",{value:this._checkedRows})}},{kind:"method",key:"_handleSearchChange",value:function(t){this._debounceSearch(t.detail.value)}},{kind:"method",key:"_calcTableHeight",value:async function(){this.autoHeight||(await this.updateComplete,this._headerHeight=this._header.clientHeight)}},{kind:"method",decorators:[R({passive:!0})],key:"_saveScrollPos",value:function(t){this._savedScrollPos=t.target.scrollTop}},{kind:"get",static:!0,key:"styles",value:function(){return[$,h`
        /* default mdc styles, colors changed, without checkbox styles */
        :host {
          height: 100%;
        }
        .mdc-data-table__content {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.25rem;
          font-weight: 400;
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
        }

        .mdc-data-table {
          background-color: var(--data-table-background-color);
          border-radius: 4px;
          border-width: 1px;
          border-style: solid;
          border-color: var(--divider-color);
          display: inline-flex;
          flex-direction: column;
          box-sizing: border-box;
          overflow: hidden;
        }

        .mdc-data-table__row--selected {
          background-color: rgba(var(--rgb-primary-color), 0.04);
        }

        .mdc-data-table__row {
          display: flex;
          width: 100%;
          height: 52px;
        }

        .mdc-data-table__row ~ .mdc-data-table__row {
          border-top: 1px solid var(--divider-color);
        }

        .mdc-data-table__row:not(.mdc-data-table__row--selected):hover {
          background-color: rgba(var(--rgb-primary-text-color), 0.04);
        }

        .mdc-data-table__header-cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__header-row {
          height: 56px;
          display: flex;
          width: 100%;
          border-bottom: 1px solid var(--divider-color);
          overflow-x: auto;
        }

        .mdc-data-table__header-row::-webkit-scrollbar {
          display: none;
        }

        .mdc-data-table__cell,
        .mdc-data-table__header-cell {
          padding-right: 16px;
          padding-left: 16px;
          align-self: center;
          overflow: hidden;
          text-overflow: ellipsis;
          flex-shrink: 0;
          box-sizing: border-box;
        }

        .mdc-data-table__cell.mdc-data-table__cell--icon {
          overflow: initial;
        }

        .mdc-data-table__header-cell--checkbox,
        .mdc-data-table__cell--checkbox {
          /* @noflip */
          padding-left: 16px;
          /* @noflip */
          padding-right: 0;
          width: 56px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--checkbox,
        :host([dir="rtl"]) .mdc-data-table__cell--checkbox {
          /* @noflip */
          padding-left: 0;
          /* @noflip */
          padding-right: 16px;
        }

        .mdc-data-table__table {
          height: 100%;
          width: 100%;
          border: 0;
          white-space: nowrap;
        }

        .mdc-data-table__cell {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.25rem;
          font-weight: 400;
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
        }

        .mdc-data-table__cell a {
          color: inherit;
          text-decoration: none;
        }

        .mdc-data-table__cell--numeric {
          text-align: right;
        }
        :host([dir="rtl"]) .mdc-data-table__cell--numeric {
          /* @noflip */
          text-align: left;
        }

        .mdc-data-table__cell--icon {
          color: var(--secondary-text-color);
          text-align: center;
        }

        .mdc-data-table__header-cell--icon,
        .mdc-data-table__cell--icon {
          width: 54px;
        }

        .mdc-data-table__header-cell.mdc-data-table__header-cell--icon {
          text-align: center;
        }

        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:hover,
        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:not(.not-sorted) {
          text-align: left;
        }
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:hover,
        :host([dir="rtl"])
          .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:not(.not-sorted) {
          text-align: right;
        }

        .mdc-data-table__cell--icon:first-child ha-icon,
        .mdc-data-table__cell--icon:first-child ha-state-icon,
        .mdc-data-table__cell--icon:first-child ha-svg-icon {
          margin-left: 8px;
        }
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child ha-icon,
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child ha-state-icon,
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child ha-svg-icon {
          margin-left: auto;
          margin-right: 8px;
        }

        .mdc-data-table__cell--icon:first-child state-badge {
          margin-right: -8px;
        }
        :host([dir="rtl"]) .mdc-data-table__cell--icon:first-child state-badge {
          margin-right: auto;
          margin-left: -8px;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__header-cell--overflow-menu,
        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          padding: 8px;
        }

        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          width: 56px;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__cell--icon-button {
          color: var(--secondary-text-color);
          text-overflow: clip;
        }

        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          width: 64px;
        }

        .mdc-data-table__cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child {
          padding-left: 16px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--overflow-menu:first-child,
        :host([dir="rtl"]) .mdc-data-table__cell--overflow-menu:first-child,
        :host([dir="rtl"]) .mdc-data-table__header-cell--overflow-menu:first-child,
        :host([dir="rtl"]) .mdc-data-table__cell--overflow-menu:first-child {
          padding-left: 8px;
          padding-right: 16px;
        }

        .mdc-data-table__cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          padding-right: 16px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--overflow-menu:last-child,
        :host([dir="rtl"]) .mdc-data-table__cell--overflow-menu:last-child,
        :host([dir="rtl"]) .mdc-data-table__header-cell--icon-button:last-child,
        :host([dir="rtl"]) .mdc-data-table__cell--icon-button:last-child {
          padding-right: 8px;
          padding-left: 16px;
        }
        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__header-cell--overflow-menu {
          overflow: initial;
        }
        .mdc-data-table__cell--icon-button a {
          color: var(--secondary-text-color);
        }

        .mdc-data-table__header-cell {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.375rem;
          font-weight: 500;
          letter-spacing: 0.0071428571em;
          text-decoration: inherit;
          text-transform: inherit;
          text-align: left;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell {
          /* @noflip */
          text-align: right;
        }

        .mdc-data-table__header-cell--numeric {
          text-align: right;
        }
        .mdc-data-table__header-cell--numeric.sortable:hover,
        .mdc-data-table__header-cell--numeric.sortable:not(.not-sorted) {
          text-align: left;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--numeric {
          /* @noflip */
          text-align: left;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell--numeric.sortable:hover,
        :host([dir="rtl"]) .mdc-data-table__header-cell--numeric.sortable:not(.not-sorted) {
          text-align: right;
        }

        /* custom from here */

        :host {
          display: block;
        }

        .mdc-data-table {
          display: block;
          border-width: var(--data-table-border-width, 1px);
          height: 100%;
        }
        .mdc-data-table__header-cell {
          overflow: hidden;
          position: relative;
        }
        .mdc-data-table__header-cell span {
          position: relative;
          left: 0px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell span {
          left: auto;
          right: 0px;
        }

        .mdc-data-table__header-cell.sortable {
          cursor: pointer;
        }
        .mdc-data-table__header-cell > * {
          transition: left 0.2s ease;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell > * {
          transition: right 0.2s ease;
        }
        .mdc-data-table__header-cell ha-svg-icon {
          top: -3px;
          position: absolute;
        }
        .mdc-data-table__header-cell.not-sorted ha-svg-icon {
          left: -20px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell.not-sorted ha-svg-icon {
          right: -20px;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) span,
        .mdc-data-table__header-cell.sortable.not-sorted:hover span {
          left: 24px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell.sortable:not(.not-sorted) span,
        :host([dir="rtl"]) .mdc-data-table__header-cell.sortable.not-sorted:hover span {
          left: auto;
          right: 24px;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) ha-svg-icon,
        .mdc-data-table__header-cell.sortable:hover.not-sorted ha-svg-icon {
          left: 12px;
        }
        :host([dir="rtl"]) .mdc-data-table__header-cell.sortable:not(.not-sorted) ha-svg-icon,
        :host([dir="rtl"]) .mdc-data-table__header-cell.sortable:hover.not-sorted ha-svg-icon {
          left: auto;
          right: 12px;
        }
        .table-header {
          border-bottom: 1px solid var(--divider-color);
          padding: 0 16px;
        }
        search-input {
          position: relative;
          top: 2px;
        }
        slot[name="header"] {
          display: block;
        }
        .center {
          text-align: center;
        }
        .secondary {
          color: var(--secondary-text-color);
        }
        .scroller {
          height: calc(100% - 57px);
        }

        .mdc-data-table__table.auto-height .scroller {
          overflow-y: hidden !important;
        }
        .grows {
          flex-grow: 1;
          flex-shrink: 1;
        }
        .forceLTR {
          direction: ltr;
        }
        .clickable {
          cursor: pointer;
        }
      `]}}]}}),r);var _e={UNKNOWN:"Unknown",BACKSPACE:"Backspace",ENTER:"Enter",SPACEBAR:"Spacebar",PAGE_UP:"PageUp",PAGE_DOWN:"PageDown",END:"End",HOME:"Home",ARROW_LEFT:"ArrowLeft",ARROW_UP:"ArrowUp",ARROW_RIGHT:"ArrowRight",ARROW_DOWN:"ArrowDown",DELETE:"Delete",ESCAPE:"Escape",TAB:"Tab"},be=new Set;be.add(_e.BACKSPACE),be.add(_e.ENTER),be.add(_e.SPACEBAR),be.add(_e.PAGE_UP),be.add(_e.PAGE_DOWN),be.add(_e.END),be.add(_e.HOME),be.add(_e.ARROW_LEFT),be.add(_e.ARROW_UP),be.add(_e.ARROW_RIGHT),be.add(_e.ARROW_DOWN),be.add(_e.DELETE),be.add(_e.ESCAPE),be.add(_e.TAB);var fe=8,ge=13,ve=32,ye=33,xe=34,ke=35,we=36,Ee=37,Ie=38,Ce=39,Te=40,Se=46,Ae=27,Re=9,Oe=new Map;Oe.set(fe,_e.BACKSPACE),Oe.set(ge,_e.ENTER),Oe.set(ve,_e.SPACEBAR),Oe.set(ye,_e.PAGE_UP),Oe.set(xe,_e.PAGE_DOWN),Oe.set(ke,_e.END),Oe.set(we,_e.HOME),Oe.set(Ee,_e.ARROW_LEFT),Oe.set(Ie,_e.ARROW_UP),Oe.set(Ce,_e.ARROW_RIGHT),Oe.set(Te,_e.ARROW_DOWN),Oe.set(Se,_e.DELETE),Oe.set(Ae,_e.ESCAPE),Oe.set(Re,_e.TAB);var Fe,ze,Le=new Set;function De(t){var e=t.key;if(be.has(e))return e;var i=Oe.get(t.keyCode);return i||_e.UNKNOWN}Le.add(_e.PAGE_UP),Le.add(_e.PAGE_DOWN),Le.add(_e.END),Le.add(_e.HOME),Le.add(_e.ARROW_LEFT),Le.add(_e.ARROW_UP),Le.add(_e.ARROW_RIGHT),Le.add(_e.ARROW_DOWN);var Be="mdc-list-item--activated",Me="mdc-list-item",$e="mdc-list-item--disabled",Pe="mdc-list-item--selected",Ne="mdc-list-item__text",He="mdc-list-item__primary-text",Ve="mdc-list";(Fe={})[""+Be]="mdc-list-item--activated",Fe[""+Me]="mdc-list-item",Fe[""+$e]="mdc-list-item--disabled",Fe[""+Pe]="mdc-list-item--selected",Fe[""+He]="mdc-list-item__primary-text",Fe[""+Ve]="mdc-list";var Ue=((ze={})[""+Be]="mdc-deprecated-list-item--activated",ze[""+Me]="mdc-deprecated-list-item",ze[""+$e]="mdc-deprecated-list-item--disabled",ze[""+Pe]="mdc-deprecated-list-item--selected",ze[""+Ne]="mdc-deprecated-list-item__text",ze[""+He]="mdc-deprecated-list-item__primary-text",ze[""+Ve]="mdc-deprecated-list",ze),Ke={ACTION_EVENT:"MDCList:action",ARIA_CHECKED:"aria-checked",ARIA_CHECKED_CHECKBOX_SELECTOR:'[role="checkbox"][aria-checked="true"]',ARIA_CHECKED_RADIO_SELECTOR:'[role="radio"][aria-checked="true"]',ARIA_CURRENT:"aria-current",ARIA_DISABLED:"aria-disabled",ARIA_ORIENTATION:"aria-orientation",ARIA_ORIENTATION_HORIZONTAL:"horizontal",ARIA_ROLE_CHECKBOX_SELECTOR:'[role="checkbox"]',ARIA_SELECTED:"aria-selected",ARIA_INTERACTIVE_ROLES_SELECTOR:'[role="listbox"], [role="menu"]',ARIA_MULTI_SELECTABLE_SELECTOR:'[aria-multiselectable="true"]',CHECKBOX_RADIO_SELECTOR:'input[type="checkbox"], input[type="radio"]',CHECKBOX_SELECTOR:'input[type="checkbox"]',CHILD_ELEMENTS_TO_TOGGLE_TABINDEX:"\n    ."+Me+" button:not(:disabled),\n    ."+Me+" a,\n    ."+Ue[Me]+" button:not(:disabled),\n    ."+Ue[Me]+" a\n  ",DEPRECATED_SELECTOR:".mdc-deprecated-list",FOCUSABLE_CHILD_ELEMENTS:"\n    ."+Me+" button:not(:disabled),\n    ."+Me+" a,\n    ."+Me+' input[type="radio"]:not(:disabled),\n    .'+Me+' input[type="checkbox"]:not(:disabled),\n    .'+Ue[Me]+" button:not(:disabled),\n    ."+Ue[Me]+" a,\n    ."+Ue[Me]+' input[type="radio"]:not(:disabled),\n    .'+Ue[Me]+' input[type="checkbox"]:not(:disabled)\n  ',RADIO_SELECTOR:'input[type="radio"]',SELECTED_ITEM_SELECTOR:'[aria-selected="true"], [aria-current="true"]'},Ge={UNSET_INDEX:-1,TYPEAHEAD_BUFFER_CLEAR_TIMEOUT_MS:300};const We=(t,e)=>t-e,je=["input","button","textarea","select"];function qe(t){return t instanceof Set}const Xe=t=>{const e=t===Ge.UNSET_INDEX?new Set:t;return qe(e)?new Set(e):new Set([e])};class Qe extends P{constructor(t){super(Object.assign(Object.assign({},Qe.defaultAdapter),t)),this.isMulti_=!1,this.wrapFocus_=!1,this.isVertical_=!0,this.selectedIndex_=Ge.UNSET_INDEX,this.focusedItemIndex_=Ge.UNSET_INDEX,this.useActivatedClass_=!1,this.ariaCurrentAttrValue_=null}static get strings(){return Ke}static get numbers(){return Ge}static get defaultAdapter(){return{focusItemAtIndex:()=>{},getFocusedElementIndex:()=>0,getListItemCount:()=>0,isFocusInsideList:()=>!1,isRootFocused:()=>!1,notifyAction:()=>{},notifySelected:()=>{},getSelectedStateForElementIndex:()=>!1,setDisabledStateForElementIndex:()=>{},getDisabledStateForElementIndex:()=>!1,setSelectedStateForElementIndex:()=>{},setActivatedStateForElementIndex:()=>{},setTabIndexForElementIndex:()=>{},setAttributeForElementIndex:()=>{},getAttributeForElementIndex:()=>null}}setWrapFocus(t){this.wrapFocus_=t}setMulti(t){this.isMulti_=t;const e=this.selectedIndex_;if(t){if(!qe(e)){const t=e===Ge.UNSET_INDEX;this.selectedIndex_=t?new Set:new Set([e])}}else if(qe(e))if(e.size){const t=Array.from(e).sort(We);this.selectedIndex_=t[0]}else this.selectedIndex_=Ge.UNSET_INDEX}setVerticalOrientation(t){this.isVertical_=t}setUseActivatedClass(t){this.useActivatedClass_=t}getSelectedIndex(){return this.selectedIndex_}setSelectedIndex(t){this.isIndexValid_(t)&&(this.isMulti_?this.setMultiSelectionAtIndex_(Xe(t)):this.setSingleSelectionAtIndex_(t))}handleFocusIn(t,e){e>=0&&this.adapter.setTabIndexForElementIndex(e,0)}handleFocusOut(t,e){e>=0&&this.adapter.setTabIndexForElementIndex(e,-1),setTimeout(()=>{this.adapter.isFocusInsideList()||this.setTabindexToFirstSelectedItem_()},0)}handleKeydown(t,e,i){const n="ArrowLeft"===De(t),o="ArrowUp"===De(t),s="ArrowRight"===De(t),a="ArrowDown"===De(t),r="Home"===De(t),c="End"===De(t),l="Enter"===De(t),d="Spacebar"===De(t);if(this.adapter.isRootFocused())return void(o||c?(t.preventDefault(),this.focusLastElement()):(a||r)&&(t.preventDefault(),this.focusFirstElement()));let h,u=this.adapter.getFocusedElementIndex();if(!(-1===u&&(u=i,u<0))){if(this.isVertical_&&a||!this.isVertical_&&s)this.preventDefaultEvent(t),h=this.focusNextElement(u);else if(this.isVertical_&&o||!this.isVertical_&&n)this.preventDefaultEvent(t),h=this.focusPrevElement(u);else if(r)this.preventDefaultEvent(t),h=this.focusFirstElement();else if(c)this.preventDefaultEvent(t),h=this.focusLastElement();else if((l||d)&&e){const e=t.target;if(e&&"A"===e.tagName&&l)return;this.preventDefaultEvent(t),this.setSelectedIndexOnAction_(u,!0)}this.focusedItemIndex_=u,void 0!==h&&(this.setTabindexAtIndex_(h),this.focusedItemIndex_=h)}}handleSingleSelection(t,e,i){t!==Ge.UNSET_INDEX&&(this.setSelectedIndexOnAction_(t,e,i),this.setTabindexAtIndex_(t),this.focusedItemIndex_=t)}focusNextElement(t){let e=t+1;if(e>=this.adapter.getListItemCount()){if(!this.wrapFocus_)return t;e=0}return this.adapter.focusItemAtIndex(e),e}focusPrevElement(t){let e=t-1;if(e<0){if(!this.wrapFocus_)return t;e=this.adapter.getListItemCount()-1}return this.adapter.focusItemAtIndex(e),e}focusFirstElement(){return this.adapter.focusItemAtIndex(0),0}focusLastElement(){const t=this.adapter.getListItemCount()-1;return this.adapter.focusItemAtIndex(t),t}setEnabled(t,e){this.isIndexValid_(t)&&this.adapter.setDisabledStateForElementIndex(t,!e)}preventDefaultEvent(t){const e=(""+t.target.tagName).toLowerCase();-1===je.indexOf(e)&&t.preventDefault()}setSingleSelectionAtIndex_(t,e=!0){this.selectedIndex_!==t&&(this.selectedIndex_!==Ge.UNSET_INDEX&&(this.adapter.setSelectedStateForElementIndex(this.selectedIndex_,!1),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(this.selectedIndex_,!1)),e&&this.adapter.setSelectedStateForElementIndex(t,!0),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(t,!0),this.setAriaForSingleSelectionAtIndex_(t),this.selectedIndex_=t,this.adapter.notifySelected(t))}setMultiSelectionAtIndex_(t,e=!0){const i=((t,e)=>{const i=Array.from(t),n=Array.from(e),o={added:[],removed:[]},s=i.sort(We),a=n.sort(We);let r=0,c=0;for(;r<s.length||c<a.length;){const t=s[r],e=a[c];t!==e?void 0!==t&&(void 0===e||t<e)?(o.removed.push(t),r++):void 0!==e&&(void 0===t||e<t)&&(o.added.push(e),c++):(r++,c++)}return o})(Xe(this.selectedIndex_),t);if(i.removed.length||i.added.length){for(const t of i.removed)e&&this.adapter.setSelectedStateForElementIndex(t,!1),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(t,!1);for(const t of i.added)e&&this.adapter.setSelectedStateForElementIndex(t,!0),this.useActivatedClass_&&this.adapter.setActivatedStateForElementIndex(t,!0);this.selectedIndex_=t,this.adapter.notifySelected(t,i)}}setAriaForSingleSelectionAtIndex_(t){this.selectedIndex_===Ge.UNSET_INDEX&&(this.ariaCurrentAttrValue_=this.adapter.getAttributeForElementIndex(t,Ke.ARIA_CURRENT));const e=null!==this.ariaCurrentAttrValue_,i=e?Ke.ARIA_CURRENT:Ke.ARIA_SELECTED;this.selectedIndex_!==Ge.UNSET_INDEX&&this.adapter.setAttributeForElementIndex(this.selectedIndex_,i,"false");const n=e?this.ariaCurrentAttrValue_:"true";this.adapter.setAttributeForElementIndex(t,i,n)}setTabindexAtIndex_(t){this.focusedItemIndex_===Ge.UNSET_INDEX&&0!==t?this.adapter.setTabIndexForElementIndex(0,-1):this.focusedItemIndex_>=0&&this.focusedItemIndex_!==t&&this.adapter.setTabIndexForElementIndex(this.focusedItemIndex_,-1),this.adapter.setTabIndexForElementIndex(t,0)}setTabindexToFirstSelectedItem_(){let t=0;"number"==typeof this.selectedIndex_&&this.selectedIndex_!==Ge.UNSET_INDEX?t=this.selectedIndex_:qe(this.selectedIndex_)&&this.selectedIndex_.size>0&&(t=Math.min(...this.selectedIndex_)),this.setTabindexAtIndex_(t)}isIndexValid_(t){if(t instanceof Set){if(!this.isMulti_)throw new Error("MDCListFoundation: Array of index is only supported for checkbox based list");if(0===t.size)return!0;{let e=!1;for(const i of t)if(e=this.isIndexInRange_(i),e)break;return e}}if("number"==typeof t){if(this.isMulti_)throw new Error("MDCListFoundation: Expected array of index for checkbox based list but got number: "+t);return t===Ge.UNSET_INDEX||this.isIndexInRange_(t)}return!1}isIndexInRange_(t){const e=this.adapter.getListItemCount();return t>=0&&t<e}setSelectedIndexOnAction_(t,e,i){if(this.adapter.getDisabledStateForElementIndex(t))return;let n=t;if(this.isMulti_&&(n=new Set([t])),this.isIndexValid_(n)){if(this.isMulti_)this.toggleMultiAtIndex(t,i,e);else if(e||i)this.setSingleSelectionAtIndex_(t,e);else{this.selectedIndex_===t&&this.setSingleSelectionAtIndex_(Ge.UNSET_INDEX)}e&&this.adapter.notifyAction(t)}}toggleMultiAtIndex(t,e,i=!0){let n=!1;n=void 0===e?!this.adapter.getSelectedStateForElementIndex(t):e;const o=Xe(this.selectedIndex_);n?o.add(t):o.delete(t),this.setMultiSelectionAtIndex_(o,i)}}const Ye=t=>t.hasAttribute("mwc-list-item");function Ze(){const t=this.itemsReadyResolver;this.itemsReady=new Promise(t=>this.itemsReadyResolver=t),t()}class Je extends S{constructor(){super(),this.mdcAdapter=null,this.mdcFoundationClass=Qe,this.activatable=!1,this.multi=!1,this.wrapFocus=!1,this.itemRoles=null,this.innerRole=null,this.innerAriaLabel=null,this.rootTabbable=!1,this.previousTabindex=null,this.noninteractive=!1,this.itemsReadyResolver=()=>{},this.itemsReady=Promise.resolve([]),this.items_=[];const t=function(t,e=50){let i;return function(n=!0){clearTimeout(i),i=setTimeout(()=>{t(n)},e)}}(this.layout.bind(this));this.debouncedLayout=(e=!0)=>{Ze.call(this),t(e)}}async getUpdateComplete(){const t=await super.getUpdateComplete();return await this.itemsReady,t}get items(){return this.items_}updateItems(){var t;const e=null!==(t=this.assignedElements)&&void 0!==t?t:[],i=[];for(const t of e)Ye(t)&&(i.push(t),t._managingList=this),t.hasAttribute("divider")&&!t.hasAttribute("role")&&t.setAttribute("role","separator");this.items_=i;const n=new Set;if(this.items_.forEach((t,e)=>{this.itemRoles?t.setAttribute("role",this.itemRoles):t.removeAttribute("role"),t.selected&&n.add(e)}),this.multi)this.select(n);else{const t=n.size?n.entries().next().value[1]:-1;this.select(t)}const o=new Event("items-updated",{bubbles:!0,composed:!0});this.dispatchEvent(o)}get selected(){const t=this.index;if(!qe(t))return-1===t?null:this.items[t];const e=[];for(const i of t)e.push(this.items[i]);return e}get index(){return this.mdcFoundation?this.mdcFoundation.getSelectedIndex():-1}render(){const t=null===this.innerRole?void 0:this.innerRole,e=null===this.innerAriaLabel?void 0:this.innerAriaLabel,i=this.rootTabbable?"0":"-1";return l`
      <!-- @ts-ignore -->
      <ul
          tabindex=${i}
          role="${O(t)}"
          aria-label="${O(e)}"
          class="mdc-deprecated-list"
          @keydown=${this.onKeydown}
          @focusin=${this.onFocusIn}
          @focusout=${this.onFocusOut}
          @request-selected=${this.onRequestSelected}
          @list-item-rendered=${this.onListItemConnected}>
        <slot></slot>
        ${this.renderPlaceholder()}
      </ul>
    `}renderPlaceholder(){var t;const e=null!==(t=this.assignedElements)&&void 0!==t?t:[];return void 0!==this.emptyMessage&&0===e.length?l`
        <mwc-list-item noninteractive>${this.emptyMessage}</mwc-list-item>
      `:null}firstUpdated(){super.firstUpdated(),this.items.length||(this.mdcFoundation.setMulti(this.multi),this.layout())}onFocusIn(t){if(this.mdcFoundation&&this.mdcRoot){const e=this.getIndexOfTarget(t);this.mdcFoundation.handleFocusIn(t,e)}}onFocusOut(t){if(this.mdcFoundation&&this.mdcRoot){const e=this.getIndexOfTarget(t);this.mdcFoundation.handleFocusOut(t,e)}}onKeydown(t){if(this.mdcFoundation&&this.mdcRoot){const e=this.getIndexOfTarget(t),i=t.target,n=Ye(i);this.mdcFoundation.handleKeydown(t,n,e)}}onRequestSelected(t){if(this.mdcFoundation){let e=this.getIndexOfTarget(t);if(-1===e&&(this.layout(),e=this.getIndexOfTarget(t),-1===e))return;if(this.items[e].disabled)return;const i=t.detail.selected,n=t.detail.source;this.mdcFoundation.handleSingleSelection(e,"interaction"===n,i),t.stopPropagation()}}getIndexOfTarget(t){const e=this.items,i=t.composedPath();for(const t of i){let i=-1;if(N(t)&&Ye(t)&&(i=e.indexOf(t)),-1!==i)return i}return-1}createAdapter(){return this.mdcAdapter={getListItemCount:()=>this.mdcRoot?this.items.length:0,getFocusedElementIndex:this.getFocusedItemIndex,getAttributeForElementIndex:(t,e)=>{if(!this.mdcRoot)return"";const i=this.items[t];return i?i.getAttribute(e):""},setAttributeForElementIndex:(t,e,i)=>{if(!this.mdcRoot)return;const n=this.items[t];n&&n.setAttribute(e,i)},focusItemAtIndex:t=>{const e=this.items[t];e&&e.focus()},setTabIndexForElementIndex:(t,e)=>{const i=this.items[t];i&&(i.tabindex=e)},notifyAction:t=>{const e={bubbles:!0,composed:!0};e.detail={index:t};const i=new CustomEvent("action",e);this.dispatchEvent(i)},notifySelected:(t,e)=>{const i={bubbles:!0,composed:!0};i.detail={index:t,diff:e};const n=new CustomEvent("selected",i);this.dispatchEvent(n)},isFocusInsideList:()=>H(this),isRootFocused:()=>{const t=this.mdcRoot;return t.getRootNode().activeElement===t},setDisabledStateForElementIndex:(t,e)=>{const i=this.items[t];i&&(i.disabled=e)},getDisabledStateForElementIndex:t=>{const e=this.items[t];return!!e&&e.disabled},setSelectedStateForElementIndex:(t,e)=>{const i=this.items[t];i&&(i.selected=e)},getSelectedStateForElementIndex:t=>{const e=this.items[t];return!!e&&e.selected},setActivatedStateForElementIndex:(t,e)=>{const i=this.items[t];i&&(i.activated=e)}},this.mdcAdapter}selectUi(t,e=!1){const i=this.items[t];i&&(i.selected=!0,i.activated=e)}deselectUi(t){const e=this.items[t];e&&(e.selected=!1,e.activated=!1)}select(t){this.mdcFoundation&&this.mdcFoundation.setSelectedIndex(t)}toggle(t,e){this.multi&&this.mdcFoundation.toggleMultiAtIndex(t,e)}onListItemConnected(t){const e=t.target;this.layout(-1===this.items.indexOf(e))}layout(t=!0){t&&this.updateItems();const e=this.items[0];for(const t of this.items)t.tabindex=-1;e&&(this.noninteractive?this.previousTabindex||(this.previousTabindex=e):e.tabindex=0),this.itemsReadyResolver()}getFocusedItemIndex(){if(!this.mdcRoot)return-1;if(!this.items.length)return-1;const t=V();if(!t.length)return-1;for(let e=t.length-1;e>=0;e--){const i=t[e];if(Ye(i))return this.items.indexOf(i)}return-1}focusItemAtIndex(t){for(const t of this.items)if(0===t.tabindex){t.tabindex=-1;break}this.items[t].tabindex=0,this.items[t].focus()}focus(){const t=this.mdcRoot;t&&t.focus()}blur(){const t=this.mdcRoot;t&&t.blur()}}i([s({type:String})],Je.prototype,"emptyMessage",void 0),i([n(".mdc-deprecated-list")],Je.prototype,"mdcRoot",void 0),i([j("",!0,"*")],Je.prototype,"assignedElements",void 0),i([j("",!0,'[tabindex="0"]')],Je.prototype,"tabbableElements",void 0),i([s({type:Boolean}),q((function(t){this.mdcFoundation&&this.mdcFoundation.setUseActivatedClass(t)}))],Je.prototype,"activatable",void 0),i([s({type:Boolean}),q((function(t,e){this.mdcFoundation&&this.mdcFoundation.setMulti(t),void 0!==e&&this.layout()}))],Je.prototype,"multi",void 0),i([s({type:Boolean}),q((function(t){this.mdcFoundation&&this.mdcFoundation.setWrapFocus(t)}))],Je.prototype,"wrapFocus",void 0),i([s({type:String}),q((function(t,e){void 0!==e&&this.updateItems()}))],Je.prototype,"itemRoles",void 0),i([s({type:String})],Je.prototype,"innerRole",void 0),i([s({type:String})],Je.prototype,"innerAriaLabel",void 0),i([s({type:Boolean})],Je.prototype,"rootTabbable",void 0),i([s({type:Boolean,reflect:!0}),q((function(t){var e,i;if(t){const t=null!==(i=null===(e=this.tabbableElements)||void 0===e?void 0:e[0])&&void 0!==i?i:null;this.previousTabindex=t,t&&t.setAttribute("tabindex","-1")}else!t&&this.previousTabindex&&(this.previousTabindex.setAttribute("tabindex","0"),this.previousTabindex=null)}))],Je.prototype,"noninteractive",void 0);const ti=h`@keyframes mdc-ripple-fg-radius-in{from{animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transform:translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)}to{transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}}@keyframes mdc-ripple-fg-opacity-in{from{animation-timing-function:linear;opacity:0}to{opacity:var(--mdc-ripple-fg-opacity, 0)}}@keyframes mdc-ripple-fg-opacity-out{from{animation-timing-function:linear;opacity:var(--mdc-ripple-fg-opacity, 0)}to{opacity:0}}:host{display:block}.mdc-deprecated-list{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-subtitle1-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:1rem;font-size:var(--mdc-typography-subtitle1-font-size, 1rem);line-height:1.75rem;line-height:var(--mdc-typography-subtitle1-line-height, 1.75rem);font-weight:400;font-weight:var(--mdc-typography-subtitle1-font-weight, 400);letter-spacing:0.009375em;letter-spacing:var(--mdc-typography-subtitle1-letter-spacing, 0.009375em);text-decoration:inherit;text-decoration:var(--mdc-typography-subtitle1-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-subtitle1-text-transform, inherit);line-height:1.5rem;margin:0;padding:8px 0;list-style-type:none;color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));padding:var(--mdc-list-vertical-padding, 8px) 0}.mdc-deprecated-list:focus{outline:none}.mdc-deprecated-list-item{height:48px}.mdc-deprecated-list--dense{padding-top:4px;padding-bottom:4px;font-size:.812rem}.mdc-deprecated-list ::slotted([divider]){height:0;margin:0;border:none;border-bottom-width:1px;border-bottom-style:solid;border-bottom-color:rgba(0, 0, 0, 0.12)}.mdc-deprecated-list ::slotted([divider][padded]){margin:0 var(--mdc-list-side-padding, 16px)}.mdc-deprecated-list ::slotted([divider][inset]){margin-left:var(--mdc-list-inset-margin, 72px);margin-right:0;width:calc( 100% - var(--mdc-list-inset-margin, 72px) )}[dir=rtl] .mdc-deprecated-list ::slotted([divider][inset]),.mdc-deprecated-list ::slotted([divider][inset][dir=rtl]){margin-left:0;margin-right:var(--mdc-list-inset-margin, 72px)}.mdc-deprecated-list ::slotted([divider][inset][padded]){width:calc( 100% - var(--mdc-list-inset-margin, 72px) - var(--mdc-list-side-padding, 16px) )}.mdc-deprecated-list--dense ::slotted([mwc-list-item]){height:40px}.mdc-deprecated-list--dense ::slotted([mwc-list]){--mdc-list-item-graphic-size: 20px}.mdc-deprecated-list--two-line.mdc-deprecated-list--dense ::slotted([mwc-list-item]),.mdc-deprecated-list--avatar-list.mdc-deprecated-list--dense ::slotted([mwc-list-item]){height:60px}.mdc-deprecated-list--avatar-list.mdc-deprecated-list--dense ::slotted([mwc-list]){--mdc-list-item-graphic-size: 36px}:host([noninteractive]){pointer-events:none;cursor:default}.mdc-deprecated-list--dense ::slotted(.mdc-deprecated-list-item__primary-text){display:block;margin-top:0;line-height:normal;margin-bottom:-20px}.mdc-deprecated-list--dense ::slotted(.mdc-deprecated-list-item__primary-text)::before{display:inline-block;width:0;height:24px;content:"";vertical-align:0}.mdc-deprecated-list--dense ::slotted(.mdc-deprecated-list-item__primary-text)::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}`;let ei=class extends Je{};ei.styles=[ti],ei=i([u("mwc-list")],ei);var ii,ni,oi={ANCHOR:"mdc-menu-surface--anchor",ANIMATING_CLOSED:"mdc-menu-surface--animating-closed",ANIMATING_OPEN:"mdc-menu-surface--animating-open",FIXED:"mdc-menu-surface--fixed",IS_OPEN_BELOW:"mdc-menu-surface--is-open-below",OPEN:"mdc-menu-surface--open",ROOT:"mdc-menu-surface"},si={CLOSED_EVENT:"MDCMenuSurface:closed",CLOSING_EVENT:"MDCMenuSurface:closing",OPENED_EVENT:"MDCMenuSurface:opened",FOCUSABLE_ELEMENTS:["button:not(:disabled)",'[href]:not([aria-disabled="true"])',"input:not(:disabled)","select:not(:disabled)","textarea:not(:disabled)",'[tabindex]:not([tabindex="-1"]):not([aria-disabled="true"])'].join(", ")},ai={TRANSITION_OPEN_DURATION:120,TRANSITION_CLOSE_DURATION:75,MARGIN_TO_EDGE:32,ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO:.67,TOUCH_EVENT_WAIT_MS:30};!function(t){t[t.BOTTOM=1]="BOTTOM",t[t.CENTER=2]="CENTER",t[t.RIGHT=4]="RIGHT",t[t.FLIP_RTL=8]="FLIP_RTL"}(ii||(ii={})),function(t){t[t.TOP_LEFT=0]="TOP_LEFT",t[t.TOP_RIGHT=4]="TOP_RIGHT",t[t.BOTTOM_LEFT=1]="BOTTOM_LEFT",t[t.BOTTOM_RIGHT=5]="BOTTOM_RIGHT",t[t.TOP_START=8]="TOP_START",t[t.TOP_END=12]="TOP_END",t[t.BOTTOM_START=9]="BOTTOM_START",t[t.BOTTOM_END=13]="BOTTOM_END"}(ni||(ni={}));var ri=function(t){function e(i){var n=t.call(this,K(K({},e.defaultAdapter),i))||this;return n.isSurfaceOpen=!1,n.isQuickOpen=!1,n.isHoistedElement=!1,n.isFixedPosition=!1,n.isHorizontallyCenteredOnViewport=!1,n.maxHeight=0,n.openBottomBias=0,n.openAnimationEndTimerId=0,n.closeAnimationEndTimerId=0,n.animationRequestId=0,n.anchorCorner=ni.TOP_START,n.originCorner=ni.TOP_START,n.anchorMargin={top:0,right:0,bottom:0,left:0},n.position={x:0,y:0},n}return U(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return oi},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return si},enumerable:!1,configurable:!0}),Object.defineProperty(e,"numbers",{get:function(){return ai},enumerable:!1,configurable:!0}),Object.defineProperty(e,"Corner",{get:function(){return ni},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},hasClass:function(){return!1},hasAnchor:function(){return!1},isElementInContainer:function(){return!1},isFocused:function(){return!1},isRtl:function(){return!1},getInnerDimensions:function(){return{height:0,width:0}},getAnchorDimensions:function(){return null},getWindowDimensions:function(){return{height:0,width:0}},getBodyDimensions:function(){return{height:0,width:0}},getWindowScroll:function(){return{x:0,y:0}},setPosition:function(){},setMaxHeight:function(){},setTransformOrigin:function(){},saveFocus:function(){},restoreFocus:function(){},notifyClose:function(){},notifyOpen:function(){},notifyClosing:function(){}}},enumerable:!1,configurable:!0}),e.prototype.init=function(){var t=e.cssClasses,i=t.ROOT,n=t.OPEN;if(!this.adapter.hasClass(i))throw new Error(i+" class required in root element.");this.adapter.hasClass(n)&&(this.isSurfaceOpen=!0)},e.prototype.destroy=function(){clearTimeout(this.openAnimationEndTimerId),clearTimeout(this.closeAnimationEndTimerId),cancelAnimationFrame(this.animationRequestId)},e.prototype.setAnchorCorner=function(t){this.anchorCorner=t},e.prototype.flipCornerHorizontally=function(){this.originCorner=this.originCorner^ii.RIGHT},e.prototype.setAnchorMargin=function(t){this.anchorMargin.top=t.top||0,this.anchorMargin.right=t.right||0,this.anchorMargin.bottom=t.bottom||0,this.anchorMargin.left=t.left||0},e.prototype.setIsHoisted=function(t){this.isHoistedElement=t},e.prototype.setFixedPosition=function(t){this.isFixedPosition=t},e.prototype.isFixed=function(){return this.isFixedPosition},e.prototype.setAbsolutePosition=function(t,e){this.position.x=this.isFinite(t)?t:0,this.position.y=this.isFinite(e)?e:0},e.prototype.setIsHorizontallyCenteredOnViewport=function(t){this.isHorizontallyCenteredOnViewport=t},e.prototype.setQuickOpen=function(t){this.isQuickOpen=t},e.prototype.setMaxHeight=function(t){this.maxHeight=t},e.prototype.setOpenBottomBias=function(t){this.openBottomBias=t},e.prototype.isOpen=function(){return this.isSurfaceOpen},e.prototype.open=function(){var t=this;this.isSurfaceOpen||(this.adapter.saveFocus(),this.isQuickOpen?(this.isSurfaceOpen=!0,this.adapter.addClass(e.cssClasses.OPEN),this.dimensions=this.adapter.getInnerDimensions(),this.autoposition(),this.adapter.notifyOpen()):(this.adapter.addClass(e.cssClasses.ANIMATING_OPEN),this.animationRequestId=requestAnimationFrame((function(){t.dimensions=t.adapter.getInnerDimensions(),t.autoposition(),t.adapter.addClass(e.cssClasses.OPEN),t.openAnimationEndTimerId=setTimeout((function(){t.openAnimationEndTimerId=0,t.adapter.removeClass(e.cssClasses.ANIMATING_OPEN),t.adapter.notifyOpen()}),ai.TRANSITION_OPEN_DURATION)})),this.isSurfaceOpen=!0))},e.prototype.close=function(t){var i=this;if(void 0===t&&(t=!1),this.isSurfaceOpen){if(this.adapter.notifyClosing(),this.isQuickOpen)return this.isSurfaceOpen=!1,t||this.maybeRestoreFocus(),this.adapter.removeClass(e.cssClasses.OPEN),this.adapter.removeClass(e.cssClasses.IS_OPEN_BELOW),void this.adapter.notifyClose();this.adapter.addClass(e.cssClasses.ANIMATING_CLOSED),requestAnimationFrame((function(){i.adapter.removeClass(e.cssClasses.OPEN),i.adapter.removeClass(e.cssClasses.IS_OPEN_BELOW),i.closeAnimationEndTimerId=setTimeout((function(){i.closeAnimationEndTimerId=0,i.adapter.removeClass(e.cssClasses.ANIMATING_CLOSED),i.adapter.notifyClose()}),ai.TRANSITION_CLOSE_DURATION)})),this.isSurfaceOpen=!1,t||this.maybeRestoreFocus()}},e.prototype.handleBodyClick=function(t){var e=t.target;this.adapter.isElementInContainer(e)||this.close()},e.prototype.handleKeydown=function(t){var e=t.keyCode;("Escape"===t.key||27===e)&&this.close()},e.prototype.autoposition=function(){var t;this.measurements=this.getAutoLayoutmeasurements();var i=this.getoriginCorner(),n=this.getMenuSurfaceMaxHeight(i),o=this.hasBit(i,ii.BOTTOM)?"bottom":"top",s=this.hasBit(i,ii.RIGHT)?"right":"left",a=this.getHorizontalOriginOffset(i),r=this.getVerticalOriginOffset(i),c=this.measurements,l=c.anchorSize,d=c.surfaceSize,h=((t={})[s]=a,t[o]=r,t);l.width/d.width>ai.ANCHOR_TO_MENU_SURFACE_WIDTH_RATIO&&(s="center"),(this.isHoistedElement||this.isFixedPosition)&&this.adjustPositionForHoistedElement(h),this.adapter.setTransformOrigin(s+" "+o),this.adapter.setPosition(h),this.adapter.setMaxHeight(n?n+"px":""),this.hasBit(i,ii.BOTTOM)||this.adapter.addClass(e.cssClasses.IS_OPEN_BELOW)},e.prototype.getAutoLayoutmeasurements=function(){var t=this.adapter.getAnchorDimensions(),e=this.adapter.getBodyDimensions(),i=this.adapter.getWindowDimensions(),n=this.adapter.getWindowScroll();return t||(t={top:this.position.y,right:this.position.x,bottom:this.position.y,left:this.position.x,width:0,height:0}),{anchorSize:t,bodySize:e,surfaceSize:this.dimensions,viewportDistance:{top:t.top,right:i.width-t.right,bottom:i.height-t.bottom,left:t.left},viewportSize:i,windowScroll:n}},e.prototype.getoriginCorner=function(){var t,i,n=this.originCorner,o=this.measurements,s=o.viewportDistance,a=o.anchorSize,r=o.surfaceSize,c=e.numbers.MARGIN_TO_EDGE;this.hasBit(this.anchorCorner,ii.BOTTOM)?(t=s.top-c+this.anchorMargin.bottom,i=s.bottom-c-this.anchorMargin.bottom):(t=s.top-c+this.anchorMargin.top,i=s.bottom-c+a.height-this.anchorMargin.top),!(i-r.height>0)&&t>i+this.openBottomBias&&(n=this.setBit(n,ii.BOTTOM));var l,d,h=this.adapter.isRtl(),u=this.hasBit(this.anchorCorner,ii.FLIP_RTL),p=this.hasBit(this.anchorCorner,ii.RIGHT)||this.hasBit(n,ii.RIGHT),m=!1;(m=h&&u?!p:p)?(l=s.left+a.width+this.anchorMargin.right,d=s.right-this.anchorMargin.right):(l=s.left+this.anchorMargin.left,d=s.right+a.width-this.anchorMargin.left);var _=l-r.width>0,b=d-r.width>0,f=this.hasBit(n,ii.FLIP_RTL)&&this.hasBit(n,ii.RIGHT);return b&&f&&h||!_&&f?n=this.unsetBit(n,ii.RIGHT):(_&&m&&h||_&&!m&&p||!b&&l>=d)&&(n=this.setBit(n,ii.RIGHT)),n},e.prototype.getMenuSurfaceMaxHeight=function(t){if(this.maxHeight>0)return this.maxHeight;var i=this.measurements.viewportDistance,n=0,o=this.hasBit(t,ii.BOTTOM),s=this.hasBit(this.anchorCorner,ii.BOTTOM),a=e.numbers.MARGIN_TO_EDGE;return o?(n=i.top+this.anchorMargin.top-a,s||(n+=this.measurements.anchorSize.height)):(n=i.bottom-this.anchorMargin.bottom+this.measurements.anchorSize.height-a,s&&(n-=this.measurements.anchorSize.height)),n},e.prototype.getHorizontalOriginOffset=function(t){var e=this.measurements.anchorSize,i=this.hasBit(t,ii.RIGHT),n=this.hasBit(this.anchorCorner,ii.RIGHT);if(i){var o=n?e.width-this.anchorMargin.left:this.anchorMargin.right;return this.isHoistedElement||this.isFixedPosition?o-(this.measurements.viewportSize.width-this.measurements.bodySize.width):o}return n?e.width-this.anchorMargin.right:this.anchorMargin.left},e.prototype.getVerticalOriginOffset=function(t){var e=this.measurements.anchorSize,i=this.hasBit(t,ii.BOTTOM),n=this.hasBit(this.anchorCorner,ii.BOTTOM);return i?n?e.height-this.anchorMargin.top:-this.anchorMargin.bottom:n?e.height+this.anchorMargin.bottom:this.anchorMargin.top},e.prototype.adjustPositionForHoistedElement=function(t){var e,i,n=this.measurements,o=n.windowScroll,s=n.viewportDistance,a=n.surfaceSize,r=n.viewportSize,c=Object.keys(t);try{for(var l=G(c),d=l.next();!d.done;d=l.next()){var h=d.value,u=t[h]||0;!this.isHorizontallyCenteredOnViewport||"left"!==h&&"right"!==h?(u+=s[h],this.isFixedPosition||("top"===h?u+=o.y:"bottom"===h?u-=o.y:"left"===h?u+=o.x:u-=o.x),t[h]=u):t[h]=(r.width-a.width)/2}}catch(t){e={error:t}}finally{try{d&&!d.done&&(i=l.return)&&i.call(l)}finally{if(e)throw e.error}}},e.prototype.maybeRestoreFocus=function(){var t=this,e=this.adapter.isFocused(),i=document.activeElement&&this.adapter.isElementInContainer(document.activeElement);(e||i)&&setTimeout((function(){t.adapter.restoreFocus()}),ai.TOUCH_EVENT_WAIT_MS)},e.prototype.hasBit=function(t,e){return Boolean(t&e)},e.prototype.setBit=function(t,e){return t|e},e.prototype.unsetBit=function(t,e){return t^e},e.prototype.isFinite=function(t){return"number"==typeof t&&isFinite(t)},e}(P),ci=ri;const li={TOP_LEFT:ni.TOP_LEFT,TOP_RIGHT:ni.TOP_RIGHT,BOTTOM_LEFT:ni.BOTTOM_LEFT,BOTTOM_RIGHT:ni.BOTTOM_RIGHT,TOP_START:ni.TOP_START,TOP_END:ni.TOP_END,BOTTOM_START:ni.BOTTOM_START,BOTTOM_END:ni.BOTTOM_END};class di extends S{constructor(){super(...arguments),this.mdcFoundationClass=ci,this.absolute=!1,this.fullwidth=!1,this.fixed=!1,this.x=null,this.y=null,this.quick=!1,this.open=!1,this.stayOpenOnBodyClick=!1,this.bitwiseCorner=ni.TOP_START,this.previousMenuCorner=null,this.menuCorner="START",this.corner="TOP_START",this.styleTop="",this.styleLeft="",this.styleRight="",this.styleBottom="",this.styleMaxHeight="",this.styleTransformOrigin="",this.anchor=null,this.previouslyFocused=null,this.previousAnchor=null,this.onBodyClickBound=()=>{}}render(){const t={"mdc-menu-surface--fixed":this.fixed,"mdc-menu-surface--fullwidth":this.fullwidth},e={top:this.styleTop,left:this.styleLeft,right:this.styleRight,bottom:this.styleBottom,"max-height":this.styleMaxHeight,"transform-origin":this.styleTransformOrigin};return l`
      <div
          class="mdc-menu-surface ${d(t)}"
          style="${L(e)}"
          @keydown=${this.onKeydown}
          @opened=${this.registerBodyClick}
          @closed=${this.deregisterBodyClick}>
        <slot></slot>
      </div>`}createAdapter(){return Object.assign(Object.assign({},W(this.mdcRoot)),{hasAnchor:()=>!!this.anchor,notifyClose:()=>{const t=new CustomEvent("closed",{bubbles:!0,composed:!0});this.open=!1,this.mdcRoot.dispatchEvent(t)},notifyClosing:()=>{const t=new CustomEvent("closing",{bubbles:!0,composed:!0});this.mdcRoot.dispatchEvent(t)},notifyOpen:()=>{const t=new CustomEvent("opened",{bubbles:!0,composed:!0});this.open=!0,this.mdcRoot.dispatchEvent(t)},isElementInContainer:()=>!1,isRtl:()=>!!this.mdcRoot&&"rtl"===getComputedStyle(this.mdcRoot).direction,setTransformOrigin:t=>{this.mdcRoot&&(this.styleTransformOrigin=t)},isFocused:()=>H(this),saveFocus:()=>{const t=V(),e=t.length;e||(this.previouslyFocused=null),this.previouslyFocused=t[e-1]},restoreFocus:()=>{this.previouslyFocused&&"focus"in this.previouslyFocused&&this.previouslyFocused.focus()},getInnerDimensions:()=>{const t=this.mdcRoot;return t?{width:t.offsetWidth,height:t.offsetHeight}:{width:0,height:0}},getAnchorDimensions:()=>{const t=this.anchor;return t?t.getBoundingClientRect():null},getBodyDimensions:()=>({width:document.body.clientWidth,height:document.body.clientHeight}),getWindowDimensions:()=>({width:window.innerWidth,height:window.innerHeight}),getWindowScroll:()=>({x:window.pageXOffset,y:window.pageYOffset}),setPosition:t=>{this.mdcRoot&&(this.styleLeft="left"in t?t.left+"px":"",this.styleRight="right"in t?t.right+"px":"",this.styleTop="top"in t?t.top+"px":"",this.styleBottom="bottom"in t?t.bottom+"px":"")},setMaxHeight:async t=>{this.mdcRoot&&(this.styleMaxHeight=t,await this.updateComplete,this.styleMaxHeight=`var(--mdc-menu-max-height, ${t})`)}})}onKeydown(t){this.mdcFoundation&&this.mdcFoundation.handleKeydown(t)}onBodyClick(t){if(this.stayOpenOnBodyClick)return;-1===t.composedPath().indexOf(this)&&this.close()}registerBodyClick(){this.onBodyClickBound=this.onBodyClick.bind(this),document.body.addEventListener("click",this.onBodyClickBound,{passive:!0,capture:!0})}deregisterBodyClick(){document.body.removeEventListener("click",this.onBodyClickBound,{capture:!0})}close(){this.open=!1}show(){this.open=!0}}i([n(".mdc-menu-surface")],di.prototype,"mdcRoot",void 0),i([n("slot")],di.prototype,"slotElement",void 0),i([s({type:Boolean}),q((function(t){this.mdcFoundation&&!this.fixed&&this.mdcFoundation.setIsHoisted(t)}))],di.prototype,"absolute",void 0),i([s({type:Boolean})],di.prototype,"fullwidth",void 0),i([s({type:Boolean}),q((function(t){this.mdcFoundation&&!this.absolute&&this.mdcFoundation.setFixedPosition(t)}))],di.prototype,"fixed",void 0),i([s({type:Number}),q((function(t){this.mdcFoundation&&null!==this.y&&null!==t&&(this.mdcFoundation.setAbsolutePosition(t,this.y),this.mdcFoundation.setAnchorMargin({left:t,top:this.y,right:-t,bottom:this.y}))}))],di.prototype,"x",void 0),i([s({type:Number}),q((function(t){this.mdcFoundation&&null!==this.x&&null!==t&&(this.mdcFoundation.setAbsolutePosition(this.x,t),this.mdcFoundation.setAnchorMargin({left:this.x,top:t,right:-this.x,bottom:t}))}))],di.prototype,"y",void 0),i([s({type:Boolean}),q((function(t){this.mdcFoundation&&this.mdcFoundation.setQuickOpen(t)}))],di.prototype,"quick",void 0),i([s({type:Boolean,reflect:!0}),q((function(t,e){this.mdcFoundation&&(t?this.mdcFoundation.open():void 0!==e&&this.mdcFoundation.close())}))],di.prototype,"open",void 0),i([s({type:Boolean})],di.prototype,"stayOpenOnBodyClick",void 0),i([a(),q((function(t){this.mdcFoundation&&this.mdcFoundation.setAnchorCorner(t)}))],di.prototype,"bitwiseCorner",void 0),i([s({type:String}),q((function(t){if(this.mdcFoundation){const e="START"===t||"END"===t,i=null===this.previousMenuCorner,n=!i&&t!==this.previousMenuCorner,o=i&&"END"===t;e&&(n||o)&&(this.bitwiseCorner=this.bitwiseCorner^ii.RIGHT,this.mdcFoundation.flipCornerHorizontally(),this.previousMenuCorner=t)}}))],di.prototype,"menuCorner",void 0),i([s({type:String}),q((function(t){if(this.mdcFoundation&&t){let e=li[t];"END"===this.menuCorner&&(e^=ii.RIGHT),this.bitwiseCorner=e}}))],di.prototype,"corner",void 0),i([a()],di.prototype,"styleTop",void 0),i([a()],di.prototype,"styleLeft",void 0),i([a()],di.prototype,"styleRight",void 0),i([a()],di.prototype,"styleBottom",void 0),i([a()],di.prototype,"styleMaxHeight",void 0),i([a()],di.prototype,"styleTransformOrigin",void 0);const hi=h`.mdc-menu-surface{display:none;position:absolute;box-sizing:border-box;max-width:calc(100vw - 32px);max-width:var(--mdc-menu-max-width, calc(100vw - 32px));max-height:calc(100vh - 32px);max-height:var(--mdc-menu-max-height, calc(100vh - 32px));margin:0;padding:0;transform:scale(1);transform-origin:top left;opacity:0;overflow:auto;will-change:transform,opacity;z-index:8;transition:opacity .03s linear,transform .12s cubic-bezier(0, 0, 0.2, 1),height 250ms cubic-bezier(0, 0, 0.2, 1);box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12);background-color:#fff;background-color:var(--mdc-theme-surface, #fff);color:#000;color:var(--mdc-theme-on-surface, #000);border-radius:4px;border-radius:var(--mdc-shape-medium, 4px);transform-origin-left:top left;transform-origin-right:top right}.mdc-menu-surface:focus{outline:none}.mdc-menu-surface--animating-open{display:inline-block;transform:scale(0.8);opacity:0}.mdc-menu-surface--open{display:inline-block;transform:scale(1);opacity:1}.mdc-menu-surface--animating-closed{display:inline-block;opacity:0;transition:opacity .075s linear}[dir=rtl] .mdc-menu-surface,.mdc-menu-surface[dir=rtl]{transform-origin-left:top right;transform-origin-right:top left}.mdc-menu-surface--anchor{position:relative;overflow:visible}.mdc-menu-surface--fixed{position:fixed}.mdc-menu-surface--fullwidth{width:100%}:host(:not([open])){display:none}.mdc-menu-surface{z-index:8;z-index:var(--mdc-menu-z-index, 8);min-width:112px;min-width:var(--mdc-menu-min-width, 112px)}`;let ui=class extends di{};ui.styles=[hi],ui=i([u("mwc-menu-surface")],ui);var pi,mi={MENU_SELECTED_LIST_ITEM:"mdc-menu-item--selected",MENU_SELECTION_GROUP:"mdc-menu__selection-group",ROOT:"mdc-menu"},_i={ARIA_CHECKED_ATTR:"aria-checked",ARIA_DISABLED_ATTR:"aria-disabled",CHECKBOX_SELECTOR:'input[type="checkbox"]',LIST_SELECTOR:".mdc-list,.mdc-deprecated-list",SELECTED_EVENT:"MDCMenu:selected",SKIP_RESTORE_FOCUS:"data-menu-item-skip-restore-focus"},bi={FOCUS_ROOT_INDEX:-1};!function(t){t[t.NONE=0]="NONE",t[t.LIST_ROOT=1]="LIST_ROOT",t[t.FIRST_ITEM=2]="FIRST_ITEM",t[t.LAST_ITEM=3]="LAST_ITEM"}(pi||(pi={}));var fi=function(t){function e(i){var n=t.call(this,K(K({},e.defaultAdapter),i))||this;return n.closeAnimationEndTimerId=0,n.defaultFocusState=pi.LIST_ROOT,n.selectedIndex=-1,n}return U(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return mi},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return _i},enumerable:!1,configurable:!0}),Object.defineProperty(e,"numbers",{get:function(){return bi},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClassToElementAtIndex:function(){},removeClassFromElementAtIndex:function(){},addAttributeToElementAtIndex:function(){},removeAttributeFromElementAtIndex:function(){},getAttributeFromElementAtIndex:function(){return null},elementContainsClass:function(){return!1},closeSurface:function(){},getElementIndex:function(){return-1},notifySelected:function(){},getMenuItemCount:function(){return 0},focusItemAtIndex:function(){},focusListRoot:function(){},getSelectedSiblingOfItemAtIndex:function(){return-1},isSelectableItemAtIndex:function(){return!1}}},enumerable:!1,configurable:!0}),e.prototype.destroy=function(){this.closeAnimationEndTimerId&&clearTimeout(this.closeAnimationEndTimerId),this.adapter.closeSurface()},e.prototype.handleKeydown=function(t){var e=t.key,i=t.keyCode;("Tab"===e||9===i)&&this.adapter.closeSurface(!0)},e.prototype.handleItemAction=function(t){var e=this,i=this.adapter.getElementIndex(t);if(!(i<0)){this.adapter.notifySelected({index:i});var n="true"===this.adapter.getAttributeFromElementAtIndex(i,_i.SKIP_RESTORE_FOCUS);this.adapter.closeSurface(n),this.closeAnimationEndTimerId=setTimeout((function(){var i=e.adapter.getElementIndex(t);i>=0&&e.adapter.isSelectableItemAtIndex(i)&&e.setSelectedIndex(i)}),ri.numbers.TRANSITION_CLOSE_DURATION)}},e.prototype.handleMenuSurfaceOpened=function(){switch(this.defaultFocusState){case pi.FIRST_ITEM:this.adapter.focusItemAtIndex(0);break;case pi.LAST_ITEM:this.adapter.focusItemAtIndex(this.adapter.getMenuItemCount()-1);break;case pi.NONE:break;default:this.adapter.focusListRoot()}},e.prototype.setDefaultFocusState=function(t){this.defaultFocusState=t},e.prototype.getSelectedIndex=function(){return this.selectedIndex},e.prototype.setSelectedIndex=function(t){if(this.validatedIndex(t),!this.adapter.isSelectableItemAtIndex(t))throw new Error("MDCMenuFoundation: No selection group at specified index.");var e=this.adapter.getSelectedSiblingOfItemAtIndex(t);e>=0&&(this.adapter.removeAttributeFromElementAtIndex(e,_i.ARIA_CHECKED_ATTR),this.adapter.removeClassFromElementAtIndex(e,mi.MENU_SELECTED_LIST_ITEM)),this.adapter.addClassToElementAtIndex(t,mi.MENU_SELECTED_LIST_ITEM),this.adapter.addAttributeToElementAtIndex(t,_i.ARIA_CHECKED_ATTR,"true"),this.selectedIndex=t},e.prototype.setEnabled=function(t,e){this.validatedIndex(t),e?(this.adapter.removeClassFromElementAtIndex(t,$e),this.adapter.addAttributeToElementAtIndex(t,_i.ARIA_DISABLED_ATTR,"false")):(this.adapter.addClassToElementAtIndex(t,$e),this.adapter.addAttributeToElementAtIndex(t,_i.ARIA_DISABLED_ATTR,"true"))},e.prototype.validatedIndex=function(t){var e=this.adapter.getMenuItemCount();if(!(t>=0&&t<e))throw new Error("MDCMenuFoundation: No list item at specified index.")},e}(P);class gi extends S{constructor(){super(...arguments),this.mdcFoundationClass=fi,this.listElement_=null,this.anchor=null,this.open=!1,this.quick=!1,this.wrapFocus=!1,this.innerRole="menu",this.innerAriaLabel=null,this.corner="TOP_START",this.x=null,this.y=null,this.absolute=!1,this.multi=!1,this.activatable=!1,this.fixed=!1,this.forceGroupSelection=!1,this.fullwidth=!1,this.menuCorner="START",this.stayOpenOnBodyClick=!1,this.defaultFocus="LIST_ROOT",this._listUpdateComplete=null}get listElement(){return this.listElement_||(this.listElement_=this.renderRoot.querySelector("mwc-list")),this.listElement_}get items(){const t=this.listElement;return t?t.items:[]}get index(){const t=this.listElement;return t?t.index:-1}get selected(){const t=this.listElement;return t?t.selected:null}render(){const t="menu"===this.innerRole?"menuitem":"option";return l`
      <mwc-menu-surface
          ?hidden=${!this.open}
          .anchor=${this.anchor}
          .open=${this.open}
          .quick=${this.quick}
          .corner=${this.corner}
          .x=${this.x}
          .y=${this.y}
          .absolute=${this.absolute}
          .fixed=${this.fixed}
          .fullwidth=${this.fullwidth}
          .menuCorner=${this.menuCorner}
          ?stayOpenOnBodyClick=${this.stayOpenOnBodyClick}
          class="mdc-menu mdc-menu-surface"
          @closed=${this.onClosed}
          @opened=${this.onOpened}
          @keydown=${this.onKeydown}>
        <mwc-list
          rootTabbable
          .innerAriaLabel=${this.innerAriaLabel}
          .innerRole=${this.innerRole}
          .multi=${this.multi}
          class="mdc-deprecated-list"
          .itemRoles=${t}
          .wrapFocus=${this.wrapFocus}
          .activatable=${this.activatable}
          @action=${this.onAction}>
        <slot></slot>
      </mwc-list>
    </mwc-menu-surface>`}createAdapter(){return{addClassToElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const n=i.items[t];n&&("mdc-menu-item--selected"===e?this.forceGroupSelection&&!n.selected&&i.toggle(t,!0):n.classList.add(e))},removeClassFromElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const n=i.items[t];n&&("mdc-menu-item--selected"===e?n.selected&&i.toggle(t,!1):n.classList.remove(e))},addAttributeToElementAtIndex:(t,e,i)=>{const n=this.listElement;if(!n)return;const o=n.items[t];o&&o.setAttribute(e,i)},removeAttributeFromElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return;const n=i.items[t];n&&n.removeAttribute(e)},getAttributeFromElementAtIndex:(t,e)=>{const i=this.listElement;if(!i)return null;const n=i.items[t];return n?n.getAttribute(e):null},elementContainsClass:(t,e)=>t.classList.contains(e),closeSurface:()=>{this.open=!1},getElementIndex:t=>{const e=this.listElement;return e?e.items.indexOf(t):-1},notifySelected:()=>{},getMenuItemCount:()=>{const t=this.listElement;return t?t.items.length:0},focusItemAtIndex:t=>{const e=this.listElement;if(!e)return;const i=e.items[t];i&&i.focus()},focusListRoot:()=>{this.listElement&&this.listElement.focus()},getSelectedSiblingOfItemAtIndex:t=>{const e=this.listElement;if(!e)return-1;const i=e.items[t];if(!i||!i.group)return-1;for(let n=0;n<e.items.length;n++){if(n===t)continue;const o=e.items[n];if(o.selected&&o.group===i.group)return n}return-1},isSelectableItemAtIndex:t=>{const e=this.listElement;if(!e)return!1;const i=e.items[t];return!!i&&i.hasAttribute("group")}}}onKeydown(t){this.mdcFoundation&&this.mdcFoundation.handleKeydown(t)}onAction(t){const e=this.listElement;if(this.mdcFoundation&&e){const i=t.detail.index,n=e.items[i];n&&this.mdcFoundation.handleItemAction(n)}}onOpened(){this.open=!0,this.mdcFoundation&&this.mdcFoundation.handleMenuSurfaceOpened()}onClosed(){this.open=!1}async getUpdateComplete(){await this._listUpdateComplete;return await super.getUpdateComplete()}async firstUpdated(){super.firstUpdated();const t=this.listElement;t&&(this._listUpdateComplete=t.updateComplete,await this._listUpdateComplete)}select(t){const e=this.listElement;e&&e.select(t)}close(){this.open=!1}show(){this.open=!0}getFocusedItemIndex(){const t=this.listElement;return t?t.getFocusedItemIndex():-1}focusItemAtIndex(t){const e=this.listElement;e&&e.focusItemAtIndex(t)}layout(t=!0){const e=this.listElement;e&&e.layout(t)}}i([n(".mdc-menu")],gi.prototype,"mdcRoot",void 0),i([n("slot")],gi.prototype,"slotElement",void 0),i([s({type:Object})],gi.prototype,"anchor",void 0),i([s({type:Boolean,reflect:!0})],gi.prototype,"open",void 0),i([s({type:Boolean})],gi.prototype,"quick",void 0),i([s({type:Boolean})],gi.prototype,"wrapFocus",void 0),i([s({type:String})],gi.prototype,"innerRole",void 0),i([s({type:String})],gi.prototype,"innerAriaLabel",void 0),i([s({type:String})],gi.prototype,"corner",void 0),i([s({type:Number})],gi.prototype,"x",void 0),i([s({type:Number})],gi.prototype,"y",void 0),i([s({type:Boolean})],gi.prototype,"absolute",void 0),i([s({type:Boolean})],gi.prototype,"multi",void 0),i([s({type:Boolean})],gi.prototype,"activatable",void 0),i([s({type:Boolean})],gi.prototype,"fixed",void 0),i([s({type:Boolean})],gi.prototype,"forceGroupSelection",void 0),i([s({type:Boolean})],gi.prototype,"fullwidth",void 0),i([s({type:String})],gi.prototype,"menuCorner",void 0),i([s({type:Boolean})],gi.prototype,"stayOpenOnBodyClick",void 0),i([s({type:String}),q((function(t){this.mdcFoundation&&this.mdcFoundation.setDefaultFocusState(pi[t])}))],gi.prototype,"defaultFocus",void 0);const vi=h`mwc-list ::slotted([mwc-list-item]:not([twoline])),mwc-list ::slotted([noninteractive]:not([twoline])){height:var(--mdc-menu-item-height, 48px)}`;let yi=class extends gi{};yi.styles=[vi],yi=i([u("mwc-menu")],yi),E([u("ha-button-menu")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[s()],key:"corner",value:()=>"TOP_START"},{kind:"field",decorators:[s({type:Boolean})],key:"multi",value:()=>!1},{kind:"field",decorators:[s({type:Boolean})],key:"activatable",value:()=>!1},{kind:"field",decorators:[s({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[s({type:Boolean})],key:"fixed",value:()=>!1},{kind:"field",decorators:[n("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var t;return null===(t=this._menu)||void 0===t?void 0:t.items}},{kind:"get",key:"selected",value:function(){var t;return null===(t=this._menu)||void 0===t?void 0:t.selected}},{kind:"method",key:"render",value:function(){return l`
      <div @click=${this._handleClick}>
        <slot name="trigger"></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .fixed=${this.fixed}
        .multi=${this.multi}
        .activatable=${this.activatable}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this,this._menu.show())}},{kind:"get",static:!0,key:"styles",value:function(){return h`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),r);export{ni as C,he as F,Pt as I,_e as K,se as P,ie as a,Vt as b,j as c,ae as d,J as e,ee as f,Bt as g,De as h,Ge as n,q as o,Lt as r,ot as s};
