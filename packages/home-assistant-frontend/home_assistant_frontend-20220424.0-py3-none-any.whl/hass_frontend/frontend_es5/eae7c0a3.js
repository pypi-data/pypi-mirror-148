"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6379],{23682:function(e,t,r){function n(e,t){if(t.length<e)throw new TypeError(e+" argument"+(e>1?"s":"")+" required, but only "+t.length+" present")}r.d(t,{Z:function(){return n}})},90394:function(e,t,r){function n(e){if(null===e||!0===e||!1===e)return NaN;var t=Number(e);return isNaN(t)?t:t<0?Math.ceil(t):Math.floor(t)}r.d(t,{Z:function(){return n}})},59699:function(e,t,r){r.d(t,{Z:function(){return s}});var n=r(90394),i=r(39244),o=r(23682),a=36e5;function s(e,t){(0,o.Z)(2,arguments);var r=(0,n.Z)(t);return(0,i.Z)(e,r*a)}},39244:function(e,t,r){r.d(t,{Z:function(){return a}});var n=r(90394),i=r(34327),o=r(23682);function a(e,t){(0,o.Z)(2,arguments);var r=(0,i.Z)(e).getTime(),a=(0,n.Z)(t);return new Date(r+a)}},4535:function(e,t,r){r.d(t,{Z:function(){return u}});var n=r(34327);function i(e){var t=new Date(Date.UTC(e.getFullYear(),e.getMonth(),e.getDate(),e.getHours(),e.getMinutes(),e.getSeconds(),e.getMilliseconds()));return t.setUTCFullYear(e.getFullYear()),e.getTime()-t.getTime()}var o=r(59429),a=r(23682),s=864e5;function c(e,t){(0,a.Z)(2,arguments);var r=(0,o.Z)(e),n=(0,o.Z)(t),c=r.getTime()-i(r),l=n.getTime()-i(n);return Math.round((c-l)/s)}function l(e,t){var r=e.getFullYear()-t.getFullYear()||e.getMonth()-t.getMonth()||e.getDate()-t.getDate()||e.getHours()-t.getHours()||e.getMinutes()-t.getMinutes()||e.getSeconds()-t.getSeconds()||e.getMilliseconds()-t.getMilliseconds();return r<0?-1:r>0?1:r}function u(e,t){(0,a.Z)(2,arguments);var r=(0,n.Z)(e),i=(0,n.Z)(t),o=l(r,i),s=Math.abs(c(r,i));r.setDate(r.getDate()-o*s);var u=Number(l(r,i)===-o),f=o*(s-u);return 0===f?0:f}},93752:function(e,t,r){r.d(t,{Z:function(){return o}});var n=r(34327),i=r(23682);function o(e){(0,i.Z)(1,arguments);var t=(0,n.Z)(e);return t.setHours(23,59,59,999),t}},70390:function(e,t,r){r.d(t,{Z:function(){return i}});var n=r(93752);function i(){return(0,n.Z)(Date.now())}},47538:function(e,t,r){function n(){var e=new Date,t=e.getFullYear(),r=e.getMonth(),n=e.getDate(),i=new Date(0);return i.setFullYear(t,r,n-1),i.setHours(23,59,59,999),i}r.d(t,{Z:function(){return n}})},59429:function(e,t,r){r.d(t,{Z:function(){return o}});var n=r(34327),i=r(23682);function o(e){(0,i.Z)(1,arguments);var t=(0,n.Z)(e);return t.setHours(0,0,0,0),t}},27088:function(e,t,r){r.d(t,{Z:function(){return i}});var n=r(59429);function i(){return(0,n.Z)(Date.now())}},83008:function(e,t,r){function n(){var e=new Date,t=e.getFullYear(),r=e.getMonth(),n=e.getDate(),i=new Date(0);return i.setFullYear(t,r,n-1),i.setHours(0,0,0,0),i}r.d(t,{Z:function(){return n}})},34327:function(e,t,r){r.d(t,{Z:function(){return o}});var n=r(23682);function i(e){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},i(e)}function o(e){(0,n.Z)(1,arguments);var t=Object.prototype.toString.call(e);return e instanceof Date||"object"===i(e)&&"[object Date]"===t?new Date(e.getTime()):"number"==typeof e||"[object Number]"===t?new Date(e):("string"!=typeof e&&"[object String]"!==t||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://git.io/fjule"),console.warn((new Error).stack)),new Date(NaN))}},19490:function(e,t,r){r.r(t);r(54444);var n,i,o,a,s,c,l,u,f=r(37500),d=r(33310),p=r(70483),h=r(27593),y=(r(22098),r(49915),r(52039),r(55424)),m=r(58763),v=r(73826),g=r(75502),b=r(43283);function w(e){return w="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},w(e)}function k(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function E(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function _(e,t){return _=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},_(e,t)}function S(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=Z(e);if(t){var i=Z(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return D(this,r)}}function D(e,t){if(t&&("object"===w(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return x(e)}function x(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function Z(e){return Z=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},Z(e)}function P(){P=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!T(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return z(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?z(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=A(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:O(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=O(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function j(e){var t,r=A(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function C(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function T(e){return e.decorators&&e.decorators.length}function M(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function O(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function A(e){var t=function(e,t){if("object"!==w(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==w(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===w(t)?t:String(t)}function z(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}!function(e,t,r,n){var i=P();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(M(o.descriptor)||M(i.descriptor)){if(T(o)||T(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(T(o)){if(T(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}C(o,i)}else t.push(o)}return t}(a.d.map(j)),e);i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,d.Mo)("hui-energy-carbon-consumed-gauge-card")],(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&_(e,t)}(n,t);var r=S(n);function n(){var t;E(this,n);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=r.call.apply(r,[this].concat(o)),e(x(t)),t}return n}(t);return{F:r,d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_data",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:function(){return["_config"]}},{kind:"method",key:"getCardSize",value:function(){return 4}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"hassSubscribe",value:function(){var e,t=this;return[(0,y.UB)(this.hass,{key:null===(e=this._config)||void 0===e?void 0:e.collection_key}).subscribe((function(e){t._data=e}))]}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return(0,f.dy)(n||(n=k([""])));if(!this._data)return(0,f.dy)(i||(i=k(["",""])),this.hass.localize("ui.panel.lovelace.cards.energy.loading"));if(!this._data.co2SignalEntity)return(0,f.dy)(o||(o=k([""])));if(!this.hass.states[this._data.co2SignalEntity])return(0,f.dy)(a||(a=k(["<hui-warning>\n        ","\n      </hui-warning>"])),(0,g.i)(this.hass,this._data.co2SignalEntity));var e,t=this._data.prefs,r=(0,y.Jj)(t),u=(0,m.q6)(this._data.stats,r.grid[0].flow_from.map((function(e){return e.stat_energy_from})));if(0===u&&(e=100),this._data.fossilEnergyConsumption&&u){var d=this._data.fossilEnergyConsumption?Object.values(this._data.fossilEnergyConsumption).reduce((function(e,t){return e+t}),0):0,v=r.solar&&(0,m.q6)(this._data.stats,r.solar.map((function(e){return e.stat_energy_from})))||0,b=(0,m.q6)(this._data.stats,r.grid[0].flow_to.map((function(e){return e.stat_energy_to})))||0,w=u+Math.max(0,v-b);e=(0,h.N)(100*(1-d/w))}return(0,f.dy)(s||(s=k(["\n      <ha-card>\n        ","\n      </ha-card>\n    "])),void 0!==e?(0,f.dy)(c||(c=k(['\n              <ha-svg-icon id="info" .path=','></ha-svg-icon>\n              <paper-tooltip animation-delay="0" for="info" position="left">\n                <span>\n                  ','\n                </span>\n              </paper-tooltip>\n              <ha-gauge\n                min="0"\n                max="100"\n                .value=',"\n                .locale=",'\n                label="%"\n                style=','\n              ></ha-gauge>\n              <div class="name">\n                ',"\n              </div>\n            "])),"M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z",this.hass.localize("ui.panel.lovelace.cards.energy.carbon_consumed_gauge.card_indicates_energy_used"),e,this.hass.locale,(0,p.V)({"--gauge-color":this._computeSeverity(e)}),this.hass.localize("ui.panel.lovelace.cards.energy.carbon_consumed_gauge.non_fossil_energy_consumed")):(0,f.dy)(l||(l=k(["",""])),this.hass.localize("ui.panel.lovelace.cards.energy.carbon_consumed_gauge.non_fossil_energy_not_calculated")))}},{kind:"method",key:"_computeSeverity",value:function(e){return e<10?b.severityMap.red:e<30?b.severityMap.yellow:e>75?b.severityMap.green:b.severityMap.normal}},{kind:"get",static:!0,key:"styles",value:function(){return(0,f.iv)(u||(u=k(["\n      ha-card {\n        height: 100%;\n        overflow: hidden;\n        padding: 16px;\n        display: flex;\n        align-items: center;\n        justify-content: center;\n        flex-direction: column;\n        box-sizing: border-box;\n      }\n\n      ha-gauge {\n        width: 100%;\n        max-width: 250px;\n      }\n\n      .name {\n        text-align: center;\n        line-height: initial;\n        color: var(--primary-text-color);\n        width: 100%;\n        font-size: 15px;\n        margin-top: 8px;\n      }\n\n      ha-svg-icon {\n        position: absolute;\n        right: 4px;\n        top: 4px;\n        color: var(--secondary-text-color);\n      }\n      paper-tooltip > span {\n        font-size: 12px;\n        line-height: 12px;\n      }\n      paper-tooltip {\n        width: 80%;\n        max-width: 250px;\n        top: 8px !important;\n      }\n    "])))}}]}}),(0,v.f)(f.oi))}}]);