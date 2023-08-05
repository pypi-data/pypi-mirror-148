"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6136],{26136:function(t,e,r){r.r(e);var n,o=r(37500),i=r(50467);function u(t){return u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},u(t)}function c(t,e){var r="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!r){if(Array.isArray(t)||(r=function(t,e){if(!t)return;if("string"==typeof t)return a(t,e);var r=Object.prototype.toString.call(t).slice(8,-1);"Object"===r&&t.constructor&&(r=t.constructor.name);if("Map"===r||"Set"===r)return Array.from(t);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return a(t,e)}(t))||e&&t&&"number"==typeof t.length){r&&(t=r);var n=0,o=function(){};return{s:o,n:function(){return n>=t.length?{done:!0}:{done:!1,value:t[n++]}},e:function(t){throw t},f:o}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var i,u=!0,c=!1;return{s:function(){r=r.call(t)},n:function(){var t=r.next();return u=t.done,t},e:function(t){c=!0,i=t},f:function(){try{u||null==r.return||r.return()}finally{if(c)throw i}}}}function a(t,e){(null==e||e>t.length)&&(e=t.length);for(var r=0,n=new Array(e);r<e;r++)n[r]=t[r];return n}function f(t,e,r,n,o,i,u){try{var c=t[i](u),a=c.value}catch(f){return void r(f)}c.done?e(a):Promise.resolve(a).then(n,o)}function l(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function s(t,e){for(var r=0;r<e.length;r++){var n=e[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}function p(t,e,r){return p="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(t,e,r){var n=function(t,e){for(;!Object.prototype.hasOwnProperty.call(t,e)&&null!==(t=v(t)););return t}(t,e);if(n){var o=Object.getOwnPropertyDescriptor(n,e);return o.get?o.get.call(r):o.value}},p(t,e,r||t)}function y(t,e){return y=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},y(t,e)}function h(t){var e=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}();return function(){var r,n=v(t);if(e){var o=v(this).constructor;r=Reflect.construct(n,arguments,o)}else r=n.apply(this,arguments);return b(this,r)}}function b(t,e){if(e&&("object"===u(e)||"function"==typeof e))return e;if(void 0!==e)throw new TypeError("Derived constructors may only return object or undefined");return function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t)}function v(t){return v=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},v(t)}var d=function(t){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&y(t,e)}(m,t);var e,r,u,a,b,d=h(m);function m(){return l(this,m),d.apply(this,arguments)}return e=m,r=[{key:"getCardSize",value:(a=regeneratorRuntime.mark((function t(){var e,r,n,o,u;return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(this._cards){t.next=2;break}return t.abrupt("return",0);case 2:e=[],r=c(this._cards);try{for(r.s();!(n=r.n()).done;)o=n.value,e.push((0,i.N)(o))}catch(a){r.e(a)}finally{r.f()}return t.next=7,Promise.all(e);case 7:return u=t.sent,t.abrupt("return",u.reduce((function(t,e){return t+e}),0));case 9:case"end":return t.stop()}}),t,this)})),b=function(){var t=this,e=arguments;return new Promise((function(r,n){var o=a.apply(t,e);function i(t){f(o,r,n,i,u,"next",t)}function u(t){f(o,r,n,i,u,"throw",t)}i(void 0)}))},function(){return b.apply(this,arguments)})}],u=[{key:"styles",get:function(){return[p(v(m),"sharedStyles",this),(0,o.iv)(n||(t=["\n        #root {\n          display: flex;\n          flex-direction: column;\n          height: 100%;\n        }\n        #root > * {\n          margin: var(\n            --vertical-stack-card-margin,\n            var(--stack-card-margin, 4px 0)\n          );\n        }\n        #root > *:first-child {\n          margin-top: 0;\n        }\n        #root > *:last-child {\n          margin-bottom: 0;\n        }\n      "],e||(e=t.slice(0)),n=Object.freeze(Object.defineProperties(t,{raw:{value:Object.freeze(e)}}))))];var t,e}}],r&&s(e.prototype,r),u&&s(e,u),m}(r(99476).p);customElements.define("hui-vertical-stack-card",d)}}]);