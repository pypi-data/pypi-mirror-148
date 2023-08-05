/*! For license information please see 2ae8442d.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[3171],{63207:function(e,t,n){n(65660),n(15112);var r,i,o,a=n(9672),s=n(87156),u=n(50856),c=n(48175);(0,a.k)({_template:(0,u.d)(r||(i=["\n    <style>\n      :host {\n        @apply --layout-inline;\n        @apply --layout-center-center;\n        position: relative;\n\n        vertical-align: middle;\n\n        fill: var(--iron-icon-fill-color, currentcolor);\n        stroke: var(--iron-icon-stroke-color, none);\n\n        width: var(--iron-icon-width, 24px);\n        height: var(--iron-icon-height, 24px);\n        @apply --iron-icon;\n      }\n\n      :host([hidden]) {\n        display: none;\n      }\n    </style>\n"],o||(o=i.slice(0)),r=Object.freeze(Object.defineProperties(i,{raw:{value:Object.freeze(o)}})))),is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:c.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(e){var t=(e||"").split(":");this._iconName=t.pop(),this._iconsetName=t.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(e){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,s.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,s.vz)(this.root).appendChild(this._img))}})},15112:function(e,t,n){n.d(t,{P:function(){return o}});n(48175);var r=n(9672);function i(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}var o=function(){function e(t){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),e[" "](t),this.type=t&&t.type||"default",this.key=t&&t.key,t&&"value"in t&&(this.value=t.value)}var t,n,r;return t=e,(n=[{key:"value",get:function(){var t=this.type,n=this.key;if(t&&n)return e.types[t]&&e.types[t][n]},set:function(t){var n=this.type,r=this.key;n&&r&&(n=e.types[n]=e.types[n]||{},null==t?delete n[r]:n[r]=t)}},{key:"list",get:function(){if(this.type){var t=e.types[this.type];return t?Object.keys(t).map((function(e){return a[this.type][e]}),this):[]}}},{key:"byKey",value:function(e){return this.key=e,this.value}}])&&i(t.prototype,n),r&&i(t,r),e}();o[" "]=function(){},o.types={};var a=o.types;(0,r.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,n){var r=new o({type:e,key:t});return void 0!==n&&n!==r.value?r.value=n:this.value!==r.value&&(this.value=r.value),r},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new o({type:this.type,key:e}).value}})},25782:function(e,t,n){n(48175),n(65660),n(70019),n(97968);var r,i,o,a=n(9672),s=n(50856),u=n(33760);(0,a.k)({_template:(0,s.d)(r||(i=['\n    <style include="paper-item-shared-styles"></style>\n    <style>\n      :host {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n        @apply --paper-font-subhead;\n\n        @apply --paper-item;\n        @apply --paper-icon-item;\n      }\n\n      .content-icon {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n\n        width: var(--paper-item-icon-width, 56px);\n        @apply --paper-item-icon;\n      }\n    </style>\n\n    <div id="contentIcon" class="content-icon">\n      <slot name="item-icon"></slot>\n    </div>\n    <slot></slot>\n'],o||(o=i.slice(0)),r=Object.freeze(Object.defineProperties(i,{raw:{value:Object.freeze(o)}})))),is:"paper-icon-item",behaviors:[u.U]})},33760:function(e,t,n){n.d(t,{U:function(){return o}});n(48175);var r=n(51644),i=n(26110),o=[r.P,i.a,{hostAttributes:{role:"option",tabindex:"0"}}]},97968:function(e,t,n){n(65660),n(70019);var r=document.createElement("template");r.setAttribute("style","display: none;"),r.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(r.content)},53973:function(e,t,n){n(48175),n(65660),n(97968);var r,i,o,a=n(9672),s=n(50856),u=n(33760);(0,a.k)({_template:(0,s.d)(r||(i=['\n    <style include="paper-item-shared-styles">\n      :host {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n        @apply --paper-font-subhead;\n\n        @apply --paper-item;\n      }\n    </style>\n    <slot></slot>\n'],o||(o=i.slice(0)),r=Object.freeze(Object.defineProperties(i,{raw:{value:Object.freeze(o)}})))),is:"paper-item",behaviors:[u.U]})},51095:function(e,t,n){n(48175);var r,i,o,a=n(98433),s=n(9672),u=n(50856);(0,s.k)({_template:(0,u.d)(r||(i=["\n    <style>\n      :host {\n        display: block;\n        padding: 8px 0;\n\n        background: var(--paper-listbox-background-color, var(--primary-background-color));\n        color: var(--paper-listbox-color, var(--primary-text-color));\n\n        @apply --paper-listbox;\n      }\n    </style>\n\n    <slot></slot>\n"],o||(o=i.slice(0)),r=Object.freeze(Object.defineProperties(i,{raw:{value:Object.freeze(o)}})))),is:"paper-listbox",behaviors:[a.i],hostAttributes:{role:"listbox"}})},21560:function(e,t,n){n.d(t,{ZH:function(){return l},MT:function(){return a},U2:function(){return u},RV:function(){return o},t8:function(){return c}});var r,i=function(){var e;return!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent)&&indexedDB.databases?new Promise((function(t){var n=function(){return indexedDB.databases().finally(t)};e=setInterval(n,100),n()})).finally((function(){return clearInterval(e)})):Promise.resolve()};function o(e){return new Promise((function(t,n){e.oncomplete=e.onsuccess=function(){return t(e.result)},e.onabort=e.onerror=function(){return n(e.error)}}))}function a(e,t){var n=i().then((function(){var n=indexedDB.open(e);return n.onupgradeneeded=function(){return n.result.createObjectStore(t)},o(n)}));return function(e,r){return n.then((function(n){return r(n.transaction(t,e).objectStore(t))}))}}function s(){return r||(r=a("keyval-store","keyval")),r}function u(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:s();return t("readonly",(function(t){return o(t.get(e))}))}function c(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:s();return n("readwrite",(function(n){return n.put(t,e),o(n.transaction)}))}function l(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:s();return e("readwrite",(function(e){return e.clear(),o(e.transaction)}))}},57835:function(e,t,n){n.d(t,{Xe:function(){return r.Xe},pX:function(){return r.pX},XM:function(){return r.XM}});var r=n(38941)},1460:function(e,t,n){n.d(t,{l:function(){return d}});var r=n(15304),i=n(38941);function o(e){return o="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},o(e)}function a(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==n)return;var r,i,o=[],a=!0,s=!1;try{for(n=n.call(e);!(a=(r=n.next()).done)&&(o.push(r.value),!t||o.length!==t);a=!0);}catch(u){s=!0,i=u}finally{try{a||null==n.return||n.return()}finally{if(s)throw i}}return o}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return s(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);"Object"===n&&e.constructor&&(n=e.constructor.name);if("Map"===n||"Set"===n)return Array.from(e);if("Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return s(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function s(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function u(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function c(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function l(e,t){return l=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},l(e,t)}function p(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(h){return!1}}();return function(){var n,r=y(e);if(t){var i=y(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return f(this,n)}}function f(e,t){if(t&&("object"===o(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function y(e){return y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},y(e)}var h={},d=(0,i.XM)(function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&l(e,t)}(s,e);var t,n,i,o=p(s);function s(){var e;return u(this,s),(e=o.apply(this,arguments)).nt=h,e}return t=s,n=[{key:"render",value:function(e,t){return t()}},{key:"update",value:function(e,t){var n=this,i=a(t,2),o=i[0],s=i[1];if(Array.isArray(o)){if(Array.isArray(this.nt)&&this.nt.length===o.length&&o.every((function(e,t){return e===n.nt[t]})))return r.Jb}else if(this.nt===o)return r.Jb;return this.nt=Array.isArray(o)?Array.from(o):o,this.render(o,s)}}],n&&c(t.prototype,n),i&&c(t,i),s}(i.Xe))}}]);