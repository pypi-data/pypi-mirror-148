/*! For license information please see 96f1e57a.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[4027,8670],{18601:function(t,e,r){r.d(e,{qN:function(){return p.q},Wg:function(){return y}});var n,o,i=r(87480),a=r(33310),p=r(78220);function c(t){return c="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},c(t)}function d(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function l(t,e){for(var r=0;r<e.length;r++){var n=e[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}function s(t,e,r){return s="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(t,e,r){var n=function(t,e){for(;!Object.prototype.hasOwnProperty.call(t,e)&&null!==(t=h(t)););return t}(t,e);if(n){var o=Object.getOwnPropertyDescriptor(n,e);return o.get?o.get.call(r):o.value}},s(t,e,r||t)}function u(t,e){return u=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},u(t,e)}function f(t){var e=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}();return function(){var r,n=h(t);if(e){var o=h(this).constructor;r=Reflect.construct(n,arguments,o)}else r=n.apply(this,arguments);return m(this,r)}}function m(t,e){if(e&&("object"===c(e)||"function"==typeof e))return e;if(void 0!==e)throw new TypeError("Derived constructors may only return object or undefined");return function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t)}function h(t){return h=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},h(t)}var b=null!==(o=null===(n=window.ShadyDOM)||void 0===n?void 0:n.inUse)&&void 0!==o&&o,y=function(t){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&u(t,e)}(i,t);var e,r,n,o=f(i);function i(){var t;return d(this,i),(t=o.apply(this,arguments)).disabled=!1,t.containingForm=null,t.formDataListener=function(e){t.disabled||t.setFormData(e.formData)},t}return e=i,r=[{key:"findFormElement",value:function(){if(!this.shadowRoot||b)return null;for(var t=this.getRootNode().querySelectorAll("form"),e=0,r=Array.from(t);e<r.length;e++){var n=r[e];if(n.contains(this))return n}return null}},{key:"connectedCallback",value:function(){var t;s(h(i.prototype),"connectedCallback",this).call(this),this.containingForm=this.findFormElement(),null===(t=this.containingForm)||void 0===t||t.addEventListener("formdata",this.formDataListener)}},{key:"disconnectedCallback",value:function(){var t;s(h(i.prototype),"disconnectedCallback",this).call(this),null===(t=this.containingForm)||void 0===t||t.removeEventListener("formdata",this.formDataListener),this.containingForm=null}},{key:"click",value:function(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}},{key:"firstUpdated",value:function(){var t=this;s(h(i.prototype),"firstUpdated",this).call(this),this.shadowRoot&&this.mdcRoot.addEventListener("change",(function(e){t.dispatchEvent(new Event("change",e))}))}}],r&&l(e.prototype,r),n&&l(e,n),i}(p.H);y.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,i.__decorate)([(0,a.Cb)({type:Boolean})],y.prototype,"disabled",void 0)},14114:function(t,e,r){r.d(e,{P:function(){return n}});var n=function(t){return function(e,r){if(e.constructor._observers){if(!e.constructor.hasOwnProperty("_observers")){var n=e.constructor._observers;e.constructor._observers=new Map,n.forEach((function(t,r){return e.constructor._observers.set(r,t)}))}}else{e.constructor._observers=new Map;var o=e.updated;e.updated=function(t){var e=this;o.call(this,t),t.forEach((function(t,r){var n=e.constructor._observers.get(r);void 0!==n&&n.call(e,e[r],t)}))}}e.constructor._observers.set(r,t)}}},92685:function(t,e,r){r.d(e,{a:function(){return O}});var n,o=r(87480),i=r(72774),a={ROOT:"mdc-form-field"},p={LABEL_SELECTOR:".mdc-form-field > label"},c=function(t){function e(r){var n=t.call(this,(0,o.__assign)((0,o.__assign)({},e.defaultAdapter),r))||this;return n.click=function(){n.handleClick()},n}return(0,o.__extends)(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return a},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return p},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!1,configurable:!0}),e.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},e.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},e.prototype.handleClick=function(){var t=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){t.adapter.deactivateInputRipple()}))},e}(i.K),d=r(78220),l=r(18601),s=r(14114),u=r(37500),f=r(33310),m=r(8636);function h(t){return h="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},h(t)}function b(t,e,r,n,o,i,a){try{var p=t[i](a),c=p.value}catch(d){return void r(d)}p.done?e(c):Promise.resolve(c).then(n,o)}function y(t){return function(){var e=this,r=arguments;return new Promise((function(n,o){var i=t.apply(e,r);function a(t){b(i,n,o,a,p,"next",t)}function p(t){b(i,n,o,a,p,"throw",t)}a(void 0)}))}}function g(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function v(t,e){for(var r=0;r<e.length;r++){var n=e[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}function _(t,e){return _=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},_(t,e)}function w(t){var e=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}();return function(){var r,n=k(t);if(e){var o=k(this).constructor;r=Reflect.construct(n,arguments,o)}else r=n.apply(this,arguments);return x(this,r)}}function x(t,e){if(e&&("object"===h(e)||"function"==typeof e))return e;if(void 0!==e)throw new TypeError("Derived constructors may only return object or undefined");return function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t)}function k(t){return k=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},k(t)}var O=function(t){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&_(t,e)}(a,t);var e,r,o,i=w(a);function a(){var t;return g(this,a),(t=i.apply(this,arguments)).alignEnd=!1,t.spaceBetween=!1,t.nowrap=!1,t.label="",t.mdcFoundationClass=c,t}return e=a,r=[{key:"createAdapter",value:function(){var t,e,r=this;return{registerInteractionHandler:function(t,e){r.labelEl.addEventListener(t,e)},deregisterInteractionHandler:function(t,e){r.labelEl.removeEventListener(t,e)},activateInputRipple:(e=y(regeneratorRuntime.mark((function t(){var e,n;return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(!((e=r.input)instanceof l.Wg)){t.next=6;break}return t.next=4,e.ripple;case 4:(n=t.sent)&&n.startPress();case 6:case"end":return t.stop()}}),t)}))),function(){return e.apply(this,arguments)}),deactivateInputRipple:(t=y(regeneratorRuntime.mark((function t(){var e,n;return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(!((e=r.input)instanceof l.Wg)){t.next=6;break}return t.next=4,e.ripple;case 4:(n=t.sent)&&n.endPress();case 6:case"end":return t.stop()}}),t)}))),function(){return t.apply(this,arguments)})}}},{key:"input",get:function(){var t,e;return null!==(e=null===(t=this.slottedInputs)||void 0===t?void 0:t[0])&&void 0!==e?e:null}},{key:"render",value:function(){var t={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return(0,u.dy)(n||(n=function(t,e){return e||(e=t.slice(0)),Object.freeze(Object.defineProperties(t,{raw:{value:Object.freeze(e)}}))}(['\n      <div class="mdc-form-field ','">\n        <slot></slot>\n        <label class="mdc-label"\n               @click="','">',"</label>\n      </div>"])),(0,m.$)(t),this._labelClick,this.label)}},{key:"click",value:function(){this._labelClick()}},{key:"_labelClick",value:function(){var t=this.input;t&&(t.focus(),t.click())}}],r&&v(e.prototype,r),o&&v(e,o),a}(d.H);(0,o.__decorate)([(0,f.Cb)({type:Boolean})],O.prototype,"alignEnd",void 0),(0,o.__decorate)([(0,f.Cb)({type:Boolean})],O.prototype,"spaceBetween",void 0),(0,o.__decorate)([(0,f.Cb)({type:Boolean})],O.prototype,"nowrap",void 0),(0,o.__decorate)([(0,f.Cb)({type:String}),(0,s.P)(function(){var t=y(regeneratorRuntime.mark((function t(e){var r;return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:null===(r=this.input)||void 0===r||r.setAttribute("aria-label",e);case 1:case"end":return t.stop()}}),t,this)})));return function(e){return t.apply(this,arguments)}}())],O.prototype,"label",void 0),(0,o.__decorate)([(0,f.IO)(".mdc-form-field")],O.prototype,"mdcRoot",void 0),(0,o.__decorate)([(0,f.vZ)("",!0,"*")],O.prototype,"slottedInputs",void 0),(0,o.__decorate)([(0,f.IO)("label")],O.prototype,"labelEl",void 0)},92038:function(t,e,r){var n;r.d(e,{W:function(){return a}});var o,i,a=(0,r(37500).iv)(n||(o=[".mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{margin-left:auto;margin-right:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{margin-left:0;margin-right:auto}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}[dir=rtl] .mdc-form-field--space-between>label,.mdc-form-field--space-between>label[dir=rtl]{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}::slotted(mwc-switch){margin-right:10px}[dir=rtl] ::slotted(mwc-switch),::slotted(mwc-switch[dir=rtl]){margin-left:10px}"],i||(i=o.slice(0)),n=Object.freeze(Object.defineProperties(o,{raw:{value:Object.freeze(i)}}))))},1819:function(t,e,r){var n=r(87480),o=r(33310),i=r(92685),a=r(92038);function p(t){return p="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},p(t)}function c(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function d(t,e){return d=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},d(t,e)}function l(t){var e=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}();return function(){var r,n=u(t);if(e){var o=u(this).constructor;r=Reflect.construct(n,arguments,o)}else r=n.apply(this,arguments);return s(this,r)}}function s(t,e){if(e&&("object"===p(e)||"function"==typeof e))return e;if(void 0!==e)throw new TypeError("Derived constructors may only return object or undefined");return function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t)}function u(t){return u=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},u(t)}var f=function(t){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&d(t,e)}(r,t);var e=l(r);function r(){return c(this,r),e.apply(this,arguments)}return r}(i.a);f.styles=[a.W],f=(0,n.__decorate)([(0,o.Mo)("mwc-formfield")],f)},63207:function(t,e,r){r(65660),r(15112);var n,o,i,a=r(9672),p=r(87156),c=r(50856),d=r(48175);(0,a.k)({_template:(0,c.d)(n||(o=["\n    <style>\n      :host {\n        @apply --layout-inline;\n        @apply --layout-center-center;\n        position: relative;\n\n        vertical-align: middle;\n\n        fill: var(--iron-icon-fill-color, currentcolor);\n        stroke: var(--iron-icon-stroke-color, none);\n\n        width: var(--iron-icon-width, 24px);\n        height: var(--iron-icon-height, 24px);\n        @apply --iron-icon;\n      }\n\n      :host([hidden]) {\n        display: none;\n      }\n    </style>\n"],i||(i=o.slice(0)),n=Object.freeze(Object.defineProperties(o,{raw:{value:Object.freeze(i)}})))),is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:d.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var e=(t||"").split(":");this._iconName=e.pop(),this._iconsetName=e.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,p.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,p.vz)(this.root).appendChild(this._img))}})},15112:function(t,e,r){r.d(e,{P:function(){return i}});r(48175);var n=r(9672);function o(t,e){for(var r=0;r<e.length;r++){var n=e[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}var i=function(){function t(e){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),t[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}var e,r,n;return e=t,(r=[{key:"value",get:function(){var e=this.type,r=this.key;if(e&&r)return t.types[e]&&t.types[e][r]},set:function(e){var r=this.type,n=this.key;r&&n&&(r=t.types[r]=t.types[r]||{},null==e?delete r[n]:r[n]=e)}},{key:"list",get:function(){if(this.type){var e=t.types[this.type];return e?Object.keys(e).map((function(t){return a[this.type][t]}),this):[]}}},{key:"byKey",value:function(t){return this.key=t,this.value}}])&&o(e.prototype,r),n&&o(e,n),t}();i[" "]=function(){},i.types={};var a=i.types;(0,n.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(t,e,r){var n=new i({type:t,key:e});return void 0!==r&&r!==n.value?n.value=r:this.value!==n.value&&(this.value=n.value),n},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(t){t&&(this.value=this)},byKey:function(t){return new i({type:this.type,key:t}).value}})},21560:function(t,e,r){r.d(e,{ZH:function(){return l},MT:function(){return a},U2:function(){return c},RV:function(){return i},t8:function(){return d}});var n,o=function(){var t;return!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent)&&indexedDB.databases?new Promise((function(e){var r=function(){return indexedDB.databases().finally(e)};t=setInterval(r,100),r()})).finally((function(){return clearInterval(t)})):Promise.resolve()};function i(t){return new Promise((function(e,r){t.oncomplete=t.onsuccess=function(){return e(t.result)},t.onabort=t.onerror=function(){return r(t.error)}}))}function a(t,e){var r=o().then((function(){var r=indexedDB.open(t);return r.onupgradeneeded=function(){return r.result.createObjectStore(e)},i(r)}));return function(t,n){return r.then((function(r){return n(r.transaction(e,t).objectStore(e))}))}}function p(){return n||(n=a("keyval-store","keyval")),n}function c(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:p();return e("readonly",(function(e){return i(e.get(t))}))}function d(t,e){var r=arguments.length>2&&void 0!==arguments[2]?arguments[2]:p();return r("readwrite",(function(r){return r.put(e,t),i(r.transaction)}))}function l(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:p();return t("readwrite",(function(t){return t.clear(),i(t.transaction)}))}},44636:function(t){t.exports="/**\n * @license\n * Copyright Google LLC All Rights Reserved.\n *\n * Use of this source code is governed by an MIT-style license that can be\n * found in the LICENSE file at https://github.com/material-components/material-components-web/blob/master/LICENSE\n */\n.mdc-top-app-bar{background-color:#6200ee;background-color:var(--mdc-theme-primary, #6200ee);color:white;display:flex;position:fixed;flex-direction:column;justify-content:space-between;box-sizing:border-box;width:100%;z-index:4}.mdc-top-app-bar .mdc-top-app-bar__action-item,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon{color:#fff;color:var(--mdc-theme-on-primary, #fff)}.mdc-top-app-bar .mdc-top-app-bar__action-item::before,.mdc-top-app-bar .mdc-top-app-bar__action-item::after,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon::after{background-color:#fff;background-color:var(--mdc-ripple-color, var(--mdc-theme-on-primary, #fff))}.mdc-top-app-bar .mdc-top-app-bar__action-item:hover::before,.mdc-top-app-bar .mdc-top-app-bar__action-item.mdc-ripple-surface--hover::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon:hover::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon.mdc-ripple-surface--hover::before{opacity:0.08;opacity:var(--mdc-ripple-hover-opacity, 0.08)}.mdc-top-app-bar .mdc-top-app-bar__action-item.mdc-ripple-upgraded--background-focused::before,.mdc-top-app-bar .mdc-top-app-bar__action-item:not(.mdc-ripple-upgraded):focus::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon.mdc-ripple-upgraded--background-focused::before,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:0.24;opacity:var(--mdc-ripple-focus-opacity, 0.24)}.mdc-top-app-bar .mdc-top-app-bar__action-item:not(.mdc-ripple-upgraded)::after,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-top-app-bar .mdc-top-app-bar__action-item:not(.mdc-ripple-upgraded):active::after,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:0.24;opacity:var(--mdc-ripple-press-opacity, 0.24)}.mdc-top-app-bar .mdc-top-app-bar__action-item.mdc-ripple-upgraded,.mdc-top-app-bar .mdc-top-app-bar__navigation-icon.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.24)}.mdc-top-app-bar__row{display:flex;position:relative;box-sizing:border-box;width:100%;height:64px}.mdc-top-app-bar__section{display:inline-flex;flex:1 1 auto;align-items:center;min-width:0;padding:8px 12px;z-index:1}.mdc-top-app-bar__section--align-start{justify-content:flex-start;order:-1}.mdc-top-app-bar__section--align-end{justify-content:flex-end;order:1}.mdc-top-app-bar__title{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-headline6-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:1.25rem;font-size:var(--mdc-typography-headline6-font-size, 1.25rem);line-height:2rem;line-height:var(--mdc-typography-headline6-line-height, 2rem);font-weight:500;font-weight:var(--mdc-typography-headline6-font-weight, 500);letter-spacing:0.0125em;letter-spacing:var(--mdc-typography-headline6-letter-spacing, 0.0125em);text-decoration:inherit;-webkit-text-decoration:var(--mdc-typography-headline6-text-decoration, inherit);text-decoration:var(--mdc-typography-headline6-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-headline6-text-transform, inherit);padding-left:20px;padding-right:0;text-overflow:ellipsis;white-space:nowrap;overflow:hidden;z-index:1}[dir=rtl] .mdc-top-app-bar__title,.mdc-top-app-bar__title[dir=rtl]{padding-left:0;padding-right:20px}.mdc-top-app-bar--short-collapsed{border-top-left-radius:0;border-top-right-radius:0;border-bottom-right-radius:24px;border-bottom-left-radius:0}[dir=rtl] .mdc-top-app-bar--short-collapsed,.mdc-top-app-bar--short-collapsed[dir=rtl]{border-top-left-radius:0;border-top-right-radius:0;border-bottom-right-radius:0;border-bottom-left-radius:24px}.mdc-top-app-bar--short{top:0;right:auto;left:0;width:100%;transition:width 250ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-top-app-bar--short,.mdc-top-app-bar--short[dir=rtl]{right:0;left:auto}.mdc-top-app-bar--short .mdc-top-app-bar__row{height:56px}.mdc-top-app-bar--short .mdc-top-app-bar__section{padding:4px}.mdc-top-app-bar--short .mdc-top-app-bar__title{transition:opacity 200ms cubic-bezier(0.4, 0, 0.2, 1);opacity:1}.mdc-top-app-bar--short-collapsed{box-shadow:0px 2px 4px -1px rgba(0, 0, 0, 0.2),0px 4px 5px 0px rgba(0, 0, 0, 0.14),0px 1px 10px 0px rgba(0,0,0,.12);width:56px;transition:width 300ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-top-app-bar--short-collapsed .mdc-top-app-bar__title{display:none}.mdc-top-app-bar--short-collapsed .mdc-top-app-bar__action-item{transition:padding 150ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-top-app-bar--short-collapsed.mdc-top-app-bar--short-has-action-item{width:112px}.mdc-top-app-bar--short-collapsed.mdc-top-app-bar--short-has-action-item .mdc-top-app-bar__section--align-end{padding-left:0;padding-right:12px}[dir=rtl] .mdc-top-app-bar--short-collapsed.mdc-top-app-bar--short-has-action-item .mdc-top-app-bar__section--align-end,.mdc-top-app-bar--short-collapsed.mdc-top-app-bar--short-has-action-item .mdc-top-app-bar__section--align-end[dir=rtl]{padding-left:12px;padding-right:0}.mdc-top-app-bar--dense .mdc-top-app-bar__row{height:48px}.mdc-top-app-bar--dense .mdc-top-app-bar__section{padding:0 4px}.mdc-top-app-bar--dense .mdc-top-app-bar__title{padding-left:12px;padding-right:0}[dir=rtl] .mdc-top-app-bar--dense .mdc-top-app-bar__title,.mdc-top-app-bar--dense .mdc-top-app-bar__title[dir=rtl]{padding-left:0;padding-right:12px}.mdc-top-app-bar--prominent .mdc-top-app-bar__row{height:128px}.mdc-top-app-bar--prominent .mdc-top-app-bar__title{align-self:flex-end;padding-bottom:2px}.mdc-top-app-bar--prominent .mdc-top-app-bar__action-item,.mdc-top-app-bar--prominent .mdc-top-app-bar__navigation-icon{align-self:flex-start}.mdc-top-app-bar--fixed{transition:box-shadow 200ms linear}.mdc-top-app-bar--fixed-scrolled{box-shadow:0px 2px 4px -1px rgba(0, 0, 0, 0.2),0px 4px 5px 0px rgba(0, 0, 0, 0.14),0px 1px 10px 0px rgba(0,0,0,.12);transition:box-shadow 200ms linear}.mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__row{height:96px}.mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__section{padding:0 12px}.mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__title{padding-left:20px;padding-right:0;padding-bottom:9px}[dir=rtl] .mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__title,.mdc-top-app-bar--dense.mdc-top-app-bar--prominent .mdc-top-app-bar__title[dir=rtl]{padding-left:0;padding-right:20px}.mdc-top-app-bar--fixed-adjust{padding-top:64px}.mdc-top-app-bar--dense-fixed-adjust{padding-top:48px}.mdc-top-app-bar--short-fixed-adjust{padding-top:56px}.mdc-top-app-bar--prominent-fixed-adjust{padding-top:128px}.mdc-top-app-bar--dense-prominent-fixed-adjust{padding-top:96px}@media(max-width: 599px){.mdc-top-app-bar__row{height:56px}.mdc-top-app-bar__section{padding:4px}.mdc-top-app-bar--short{transition:width 200ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-top-app-bar--short-collapsed{transition:width 250ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-top-app-bar--short-collapsed .mdc-top-app-bar__section--align-end{padding-left:0;padding-right:12px}[dir=rtl] .mdc-top-app-bar--short-collapsed .mdc-top-app-bar__section--align-end,.mdc-top-app-bar--short-collapsed .mdc-top-app-bar__section--align-end[dir=rtl]{padding-left:12px;padding-right:0}.mdc-top-app-bar--prominent .mdc-top-app-bar__title{padding-bottom:6px}.mdc-top-app-bar--fixed-adjust{padding-top:56px}}\n\n/*# sourceMappingURL=mdc.top-app-bar.min.css.map*/"},81563:function(t,e,r){function n(t){return n="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},n(t)}r.d(e,{E_:function(){return h},i9:function(){return f},_Y:function(){return d},pt:function(){return i},OR:function(){return p},hN:function(){return a},ws:function(){return m},fk:function(){return l},hl:function(){return u}});var o=r(15304).Al.H,i=function(t){return null===t||"object"!=n(t)&&"function"!=typeof t},a=function(t,e){var r,n;return void 0===e?void 0!==(null===(r=t)||void 0===r?void 0:r._$litType$):(null===(n=t)||void 0===n?void 0:n._$litType$)===e},p=function(t){return void 0===t.strings},c=function(){return document.createComment("")},d=function(t,e,r){var n,i=t._$AA.parentNode,a=void 0===e?t._$AB:e._$AA;if(void 0===r){var p=i.insertBefore(c(),a),d=i.insertBefore(c(),a);r=new o(p,d,t,t.options)}else{var l,s=r._$AB.nextSibling,u=r._$AM,f=u!==t;if(f)null===(n=r._$AQ)||void 0===n||n.call(r,t),r._$AM=t,void 0!==r._$AP&&(l=t._$AU)!==u._$AU&&r._$AP(l);if(s!==a||f)for(var m=r._$AA;m!==s;){var h=m.nextSibling;i.insertBefore(m,a),m=h}}return r},l=function(t,e){var r=arguments.length>2&&void 0!==arguments[2]?arguments[2]:t;return t._$AI(e,r),t},s={},u=function(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:s;return t._$AH=e},f=function(t){return t._$AH},m=function(t){var e;null===(e=t._$AP)||void 0===e||e.call(t,!1,!0);for(var r=t._$AA,n=t._$AB.nextSibling;r!==n;){var o=r.nextSibling;r.remove(),r=o}},h=function(t){t._$AR()}},57835:function(t,e,r){r.d(e,{Xe:function(){return n.Xe},pX:function(){return n.pX},XM:function(){return n.XM}});var n=r(38941)},40015:function(t,e,r){r.d(e,{F:function(){return m}});var n=r(15304),o=r(38941),i=r(81563);function a(t){return a="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},a(t)}function p(t,e){return function(t){if(Array.isArray(t))return t}(t)||function(t,e){var r=null==t?null:"undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(null==r)return;var n,o,i=[],a=!0,p=!1;try{for(r=r.call(t);!(a=(n=r.next()).done)&&(i.push(n.value),!e||i.length!==e);a=!0);}catch(c){p=!0,o=c}finally{try{a||null==r.return||r.return()}finally{if(p)throw o}}return i}(t,e)||function(t,e){if(!t)return;if("string"==typeof t)return c(t,e);var r=Object.prototype.toString.call(t).slice(8,-1);"Object"===r&&t.constructor&&(r=t.constructor.name);if("Map"===r||"Set"===r)return Array.from(t);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return c(t,e)}(t,e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function c(t,e){(null==e||e>t.length)&&(e=t.length);for(var r=0,n=new Array(e);r<e;r++)n[r]=t[r];return n}function d(t,e){for(var r=0;r<e.length;r++){var n=e[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}function l(t,e){return l=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},l(t,e)}function s(t){var e=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}();return function(){var r,n=f(t);if(e){var o=f(this).constructor;r=Reflect.construct(n,arguments,o)}else r=n.apply(this,arguments);return u(this,r)}}function u(t,e){if(e&&("object"===a(e)||"function"==typeof e))return e;if(void 0!==e)throw new TypeError("Derived constructors may only return object or undefined");return function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t)}function f(t){return f=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},f(t)}var m=(0,o.XM)(function(t){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&l(t,e)}(c,t);var e,r,o,a=s(c);function c(t){var e;return function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,c),(e=a.call(this,t)).tt=new WeakMap,e}return e=c,(r=[{key:"render",value:function(t){return[t]}},{key:"update",value:function(t,e){var r=p(e,1)[0];if((0,i.hN)(this.it)&&(!(0,i.hN)(r)||this.it.strings!==r.strings)){var o=(0,i.i9)(t).pop(),a=this.tt.get(this.it.strings);if(void 0===a){var c=document.createDocumentFragment();(a=(0,n.sY)(n.Ld,c)).setConnected(!1),this.tt.set(this.it.strings,a)}(0,i.hl)(a,[o]),(0,i._Y)(a,void 0,o)}if((0,i.hN)(r)){if(!(0,i.hN)(this.it)||this.it.strings!==r.strings){var d=this.tt.get(r.strings);if(void 0!==d){var l=(0,i.i9)(d).pop();(0,i.E_)(t),(0,i._Y)(t,void 0,l),(0,i.hl)(t,[l])}}this.it=r}else this.it=void 0;return this.render(r)}}])&&d(e.prototype,r),o&&d(e,o),c}(o.Xe))}}]);