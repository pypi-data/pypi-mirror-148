/*! For license information please see cd1860e0.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[3099,2268],{14166:function(t,e,n){n.d(e,{W:function(){return i}});var r=function(){return r=Object.assign||function(t){for(var e,n=1,r=arguments.length;n<r;n++)for(var i in e=arguments[n])Object.prototype.hasOwnProperty.call(e,i)&&(t[i]=e[i]);return t},r.apply(this,arguments)};function i(t,e,n){void 0===e&&(e=Date.now()),void 0===n&&(n={});var i=r(r({},o),n||{}),a=(+t-+e)/1e3;if(Math.abs(a)<i.second)return{value:Math.round(a),unit:"second"};var u=a/60;if(Math.abs(u)<i.minute)return{value:Math.round(u),unit:"minute"};var c=a/3600;if(Math.abs(c)<i.hour)return{value:Math.round(c),unit:"hour"};var s=a/86400;if(Math.abs(s)<i.day)return{value:Math.round(s),unit:"day"};var l=new Date(t),f=new Date(e),h=l.getFullYear()-f.getFullYear();if(Math.round(Math.abs(h))>0)return{value:Math.round(h),unit:"year"};var p=12*h+l.getMonth()-f.getMonth();if(Math.round(Math.abs(p))>0)return{value:Math.round(p),unit:"month"};var y=a/604800;return{value:Math.round(y),unit:"week"}}var o={second:45,minute:45,hour:22,day:5}},63207:function(t,e,n){n(65660),n(15112);var r,i,o,a=n(9672),u=n(87156),c=n(50856),s=n(48175);(0,a.k)({_template:(0,c.d)(r||(i=["\n    <style>\n      :host {\n        @apply --layout-inline;\n        @apply --layout-center-center;\n        position: relative;\n\n        vertical-align: middle;\n\n        fill: var(--iron-icon-fill-color, currentcolor);\n        stroke: var(--iron-icon-stroke-color, none);\n\n        width: var(--iron-icon-width, 24px);\n        height: var(--iron-icon-height, 24px);\n        @apply --iron-icon;\n      }\n\n      :host([hidden]) {\n        display: none;\n      }\n    </style>\n"],o||(o=i.slice(0)),r=Object.freeze(Object.defineProperties(i,{raw:{value:Object.freeze(o)}})))),is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:s.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var e=(t||"").split(":");this._iconName=e.pop(),this._iconsetName=e.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,u.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,u.vz)(this.root).appendChild(this._img))}})},15112:function(t,e,n){n.d(e,{P:function(){return o}});n(48175);var r=n(9672);function i(t,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,r.key,r)}}var o=function(){function t(e){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),t[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}var e,n,r;return e=t,(n=[{key:"value",get:function(){var e=this.type,n=this.key;if(e&&n)return t.types[e]&&t.types[e][n]},set:function(e){var n=this.type,r=this.key;n&&r&&(n=t.types[n]=t.types[n]||{},null==e?delete n[r]:n[r]=e)}},{key:"list",get:function(){if(this.type){var e=t.types[this.type];return e?Object.keys(e).map((function(t){return a[this.type][t]}),this):[]}}},{key:"byKey",value:function(t){return this.key=t,this.value}}])&&i(e.prototype,n),r&&i(e,r),t}();o[" "]=function(){},o.types={};var a=o.types;(0,r.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(t,e,n){var r=new o({type:t,key:e});return void 0!==n&&n!==r.value?r.value=n:this.value!==r.value&&(this.value=r.value),r},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(t){t&&(this.value=this)},byKey:function(t){return new o({type:this.type,key:t}).value}})},21560:function(t,e,n){n.d(e,{ZH:function(){return l},MT:function(){return a},U2:function(){return c},RV:function(){return o},t8:function(){return s}});var r,i=function(){var t;return!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent)&&indexedDB.databases?new Promise((function(e){var n=function(){return indexedDB.databases().finally(e)};t=setInterval(n,100),n()})).finally((function(){return clearInterval(t)})):Promise.resolve()};function o(t){return new Promise((function(e,n){t.oncomplete=t.onsuccess=function(){return e(t.result)},t.onabort=t.onerror=function(){return n(t.error)}}))}function a(t,e){var n=i().then((function(){var n=indexedDB.open(t);return n.onupgradeneeded=function(){return n.result.createObjectStore(e)},o(n)}));return function(t,r){return n.then((function(n){return r(n.transaction(e,t).objectStore(e))}))}}function u(){return r||(r=a("keyval-store","keyval")),r}function c(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:u();return e("readonly",(function(e){return o(e.get(t))}))}function s(t,e){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:u();return n("readwrite",(function(n){return n.put(e,t),o(n.transaction)}))}function l(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:u();return t("readwrite",(function(t){return t.clear(),o(t.transaction)}))}},93217:function(t,e,n){function r(t,e){return function(t){if(Array.isArray(t))return t}(t)||function(t,e){var n=null==t?null:"undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(null==n)return;var r,i,o=[],a=!0,u=!1;try{for(n=n.call(t);!(a=(r=n.next()).done)&&(o.push(r.value),!e||o.length!==e);a=!0);}catch(c){u=!0,i=c}finally{try{a||null==n.return||n.return()}finally{if(u)throw i}}return o}(t,e)||s(t,e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function i(t,e,n){return e in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}function o(t,e,n){return o=a()?Reflect.construct:function(t,e,n){var r=[null];r.push.apply(r,e);var i=new(Function.bind.apply(t,r));return n&&u(i,n.prototype),i},o.apply(null,arguments)}function a(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}function u(t,e){return u=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},u(t,e)}function c(t){return function(t){if(Array.isArray(t))return l(t)}(t)||function(t){if("undefined"!=typeof Symbol&&null!=t[Symbol.iterator]||null!=t["@@iterator"])return Array.from(t)}(t)||s(t)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function s(t,e){if(t){if("string"==typeof t)return l(t,e);var n=Object.prototype.toString.call(t).slice(8,-1);return"Object"===n&&t.constructor&&(n=t.constructor.name),"Map"===n||"Set"===n?Array.from(t):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?l(t,e):void 0}}function l(t,e){(null==e||e>t.length)&&(e=t.length);for(var n=0,r=new Array(e);n<e;n++)r[n]=t[n];return r}function f(t){return f="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},f(t)}n.d(e,{Ud:function(){return _}});var h=Symbol("Comlink.proxy"),p=Symbol("Comlink.endpoint"),y=Symbol("Comlink.releaseProxy"),d=Symbol("Comlink.thrown"),v=function(t){return"object"===f(t)&&null!==t||"function"==typeof t},m=new Map([["proxy",{canHandle:function(t){return v(t)&&t[h]},serialize:function(t){var e=new MessageChannel,n=e.port1,r=e.port2;return g(t,n),[r,[r]]},deserialize:function(t){return t.start(),_(t)}}],["throw",{canHandle:function(t){return v(t)&&d in t},serialize:function(t){var e=t.value;return[e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[]]},deserialize:function(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function g(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:self;e.addEventListener("message",(function n(a){if(a&&a.data){var u,s=Object.assign({path:[]},a.data),l=s.id,f=s.type,h=s.path,p=(a.data.argumentList||[]).map(I);try{var y=h.slice(0,-1).reduce((function(t,e){return t[e]}),t),v=h.reduce((function(t,e){return t[e]}),t);switch(f){case"GET":u=v;break;case"SET":y[h.slice(-1)[0]]=I(a.data.value),u=!0;break;case"APPLY":u=v.apply(y,p);break;case"CONSTRUCT":var m;u=M(o(v,c(p)));break;case"ENDPOINT":var _=new MessageChannel,w=_.port1,S=_.port2;g(t,S),u=A(w,[w]);break;case"RELEASE":u=void 0;break;default:return}}catch(m){u=i({value:m},d,0)}Promise.resolve(u).catch((function(t){return i({value:t},d,0)})).then((function(t){var i=r(O(t),2),o=i[0],a=i[1];e.postMessage(Object.assign(Object.assign({},o),{id:l}),a),"RELEASE"===f&&(e.removeEventListener("message",n),b(e))}))}})),e.start&&e.start()}function b(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function _(t,e){return S(t,[],e)}function w(t){if(t)throw new Error("Proxy has been released and is not useable")}function S(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:[],n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:function(){},i=!1,o=new Proxy(n,{get:function(n,r){if(w(i),r===y)return function(){return C(t,{type:"RELEASE",path:e.map((function(t){return t.toString()}))}).then((function(){b(t),i=!0}))};if("then"===r){if(0===e.length)return{then:function(){return o}};var a=C(t,{type:"GET",path:e.map((function(t){return t.toString()}))}).then(I);return a.then.bind(a)}return S(t,[].concat(c(e),[r]))},set:function(n,o,a){w(i);var u=r(O(a),2),s=u[0],l=u[1];return C(t,{type:"SET",path:[].concat(c(e),[o]).map((function(t){return t.toString()})),value:s},l).then(I)},apply:function(n,o,a){w(i);var u=e[e.length-1];if(u===p)return C(t,{type:"ENDPOINT"}).then(I);if("bind"===u)return S(t,e.slice(0,-1));var c=r(E(a),2),s=c[0],l=c[1];return C(t,{type:"APPLY",path:e.map((function(t){return t.toString()})),argumentList:s},l).then(I)},construct:function(n,o){w(i);var a=r(E(o),2),u=a[0],c=a[1];return C(t,{type:"CONSTRUCT",path:e.map((function(t){return t.toString()})),argumentList:u},c).then(I)}});return o}function E(t){var e,n=t.map(O);return[n.map((function(t){return t[0]})),(e=n.map((function(t){return t[1]})),Array.prototype.concat.apply([],e))]}var k=new WeakMap;function A(t,e){return k.set(t,e),t}function M(t){return Object.assign(t,i({},h,!0))}function O(t){var e,n=function(t,e){var n="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!n){if(Array.isArray(t)||(n=s(t))||e&&t&&"number"==typeof t.length){n&&(t=n);var r=0,i=function(){};return{s:i,n:function(){return r>=t.length?{done:!0}:{done:!1,value:t[r++]}},e:function(t){throw t},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,a=!0,u=!1;return{s:function(){n=n.call(t)},n:function(){var t=n.next();return a=t.done,t},e:function(t){u=!0,o=t},f:function(){try{a||null==n.return||n.return()}finally{if(u)throw o}}}}(m);try{for(n.s();!(e=n.n()).done;){var i=r(e.value,2),o=i[0],a=i[1];if(a.canHandle(t)){var u=r(a.serialize(t),2);return[{type:"HANDLER",name:o,value:u[0]},u[1]]}}}catch(c){n.e(c)}finally{n.f()}return[{type:"RAW",value:t},k.get(t)||[]]}function I(t){switch(t.type){case"HANDLER":return m.get(t.name).deserialize(t.value);case"RAW":return t.value}}function C(t,e,n){return new Promise((function(r){var i=new Array(4).fill(0).map((function(){return Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16)})).join("-");t.addEventListener("message",(function e(n){n.data&&n.data.id&&n.data.id===i&&(t.removeEventListener("message",e),r(n.data))})),t.start&&t.start(),t.postMessage(Object.assign({id:i},e),n)}))}}}]);