/*! For license information please see 9dfdb2bc.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[7949],{44577:function(e,t,r){var n=r(87480),i=r(33310),o=r(61092),a=r(96762);function c(e){return c="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},c(e)}function s(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function l(e,t){return l=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},l(e,t)}function f(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=d(e);if(t){var i=d(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return u(this,r)}}function u(e,t){if(t&&("object"===c(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function d(e){return d=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},d(e)}var p=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&l(e,t)}(r,e);var t=f(r);function r(){return s(this,r),t.apply(this,arguments)}return r}(o.K);p.styles=[a.W],p=(0,n.__decorate)([(0,i.Mo)("mwc-list-item")],p)},85415:function(e,t,r){r.d(t,{$:function(){return n},f:function(){return i}});var n=function(e,t){return e<t?-1:e>t?1:0},i=function(e,t){return n(e.toLowerCase(),t.toLowerCase())}},76270:function(e,t,r){r.d(t,{Q:function(){return n}});var n=["relative","total","date","time","datetime"]},45890:function(e,t,r){var n;r.d(t,{A:function(){return a}});var i,o,a=(0,r(37500).iv)(n||(i=["\n  .card-config {\n    /* Cancels overlapping Margins for HAForm + Card Config options */\n    overflow: auto;\n  }\n  ha-switch {\n    padding: 16px 6px;\n  }\n  .side-by-side {\n    display: flex;\n    align-items: flex-end;\n  }\n  .side-by-side > * {\n    flex: 1;\n    padding-right: 8px;\n  }\n  .side-by-side > *:last-child {\n    flex: 1;\n    padding-right: 0;\n  }\n  .suffix {\n    margin: 0 8px;\n  }\n  hui-action-editor,\n  ha-select,\n  ha-textfield,\n  ha-icon-picker {\n    margin-top: 8px;\n    display: block;\n  }\n"],o||(o=i.slice(0)),n=Object.freeze(Object.defineProperties(i,{raw:{value:Object.freeze(o)}}))))},87071:function(e,t,r){r.r(t),r.d(t,{HuiGraphFooterEditor:function(){return x}});var n,i,o=r(37500),a=r(33310),c=r(69505),s=r(47181),l=(r(74535),r(83927),r(43709),r(3555),r(61173)),f=r(45890);function u(e){return u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},u(e)}function d(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function p(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function h(e,t){return h=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},h(e,t)}function y(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=g(e);if(t){var i=g(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return m(this,r)}}function m(e,t){if(t&&("object"===u(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return v(e)}function v(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function g(e){return g=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},g(e)}function b(){b=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!k(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var c=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,i[o])(c)||c);e=s.element,this.addElementPlacement(e,t),s.finisher&&n.push(s.finisher);var l=s.extras;if(l){for(var f=0;f<l.length;f++)this.addElementPlacement(l[f],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var c=a+1;c<e.length;c++)if(e[a].key===e[c].key&&e[a].placement===e[c].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return C(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?C(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=O(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:E(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=E(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function _(e){var t,r=O(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function w(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function k(e){return e.decorators&&e.decorators.length}function j(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function E(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function O(e){var t=function(e,t){if("object"!==u(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==u(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===u(t)?t:String(t)}function C(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}var P=["sensor"],x=function(e,t,r,n){var i=b();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,c.elements)}),r),c=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(j(o.descriptor)||j(i.descriptor)){if(k(o)||k(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(k(o)){if(k(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}w(o,i)}else t.push(o)}return t}(a.d.map(_)),e);return i.initializeClassElements(a.F,c.elements),i.runClassFinishers(a.F,c.finishers)}([(0,a.Mo)("hui-graph-footer-editor")],(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&h(e,t)}(n,t);var r=y(n);function n(){var t;p(this,n);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=r.call.apply(r,[this].concat(o)),e(v(t)),t}return n}(t);return{F:r,d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){(0,c.hu)(e,l.gg),this._config=e}},{kind:"get",key:"_entity",value:function(){return this._config.entity||""}},{kind:"get",key:"_detail",value:function(){var e;return null!==(e=this._config.detail)&&void 0!==e?e:1}},{kind:"get",key:"_hours_to_show",value:function(){return this._config.hours_to_show||24}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?(0,o.dy)(i||(i=d(['\n      <div class="card-config">\n        <ha-entity-picker\n          allow-custom-entity\n          .label=',"\n          .hass=","\n          .value=","\n          .configValue=","\n          .includeDomains=","\n          .required=","\n          @change=",'\n        ></ha-entity-picker>\n        <div class="side-by-side">\n          <ha-formfield\n            label=',"\n          >\n            <ha-switch\n              .checked=","\n              .configValue=","\n              @change=",'\n            ></ha-switch>\n          </ha-formfield>\n          <ha-textfield\n            type="number"\n            .label="'," (",')"\n            .value=','\n            min="1"\n            .configValue=',"\n            @input=","\n          ></ha-textfield>\n        </div>\n      </div>\n    "])),this.hass.localize("ui.panel.lovelace.editor.card.generic.entity"),this.hass,this._entity,"entity",P,!0,this._valueChanged,this.hass.localize("ui.panel.lovelace.editor.card.sensor.show_more_detail"),2===this._detail,"detail",this._change,this.hass.localize("ui.panel.lovelace.editor.card.generic.hours_to_show"),this.hass.localize("ui.panel.lovelace.editor.card.config.optional"),this._hours_to_show,"hours_to_show",this._valueChanged):(0,o.dy)(n||(n=d([""])))}},{kind:"method",key:"_change",value:function(e){if(this._config&&this.hass){var t=e.target.checked?2:1;this._detail!==t&&(this._config=Object.assign({},this._config,{detail:t}),(0,s.B)(this,"config-changed",{config:this._config}))}}},{kind:"method",key:"_valueChanged",value:function(e){if(this._config&&this.hass){var t=e.target;if(this["_".concat(t.configValue)]!==t.value){if(t.configValue)if(""===t.value||"number"===t.type&&isNaN(Number(t.value)))this._config=Object.assign({},this._config),delete this._config[t.configValue];else{var r=t.value;"number"===t.type&&(r=Number(r)),this._config=Object.assign({},this._config,function(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}({},t.configValue,r))}(0,s.B)(this,"config-changed",{config:this._config})}}}},{kind:"get",static:!0,key:"styles",value:function(){return f.A}}]}}),o.oi)},85677:function(e,t,r){r.d(t,{C:function(){return u}});var n=r(69505),i=(0,n.Ry)({user:(0,n.Z_)()}),o=(0,n.G0)([(0,n.O7)(),(0,n.Ry)({text:(0,n.jt)((0,n.Z_)()),excemptions:(0,n.jt)((0,n.IX)(i))})]),a=(0,n.Ry)({action:(0,n.i0)("url"),url_path:(0,n.Z_)(),confirmation:(0,n.jt)(o)}),c=(0,n.Ry)({action:(0,n.i0)("call-service"),service:(0,n.Z_)(),service_data:(0,n.jt)((0,n.Ry)()),target:(0,n.jt)((0,n.Ry)({entity_id:(0,n.jt)((0,n.G0)([(0,n.Z_)(),(0,n.IX)((0,n.Z_)())])),device_id:(0,n.jt)((0,n.G0)([(0,n.Z_)(),(0,n.IX)((0,n.Z_)())])),area_id:(0,n.jt)((0,n.G0)([(0,n.Z_)(),(0,n.IX)((0,n.Z_)())]))})),confirmation:(0,n.jt)(o)}),s=(0,n.Ry)({action:(0,n.i0)("navigate"),navigation_path:(0,n.Z_)(),confirmation:(0,n.jt)(o)}),l=(0,n.dt)({action:(0,n.i0)("fire-dom-event")}),f=(0,n.Ry)({action:(0,n.kE)(["none","toggle","more-info","call-service","url","navigate"]),confirmation:(0,n.jt)(o)}),u=(0,n.G0)([f,a,s,c,l])},30232:function(e,t,r){r.d(t,{K:function(){return a}});var n=r(69505),i=r(76270),o=r(85677),a=(0,n.G0)([(0,n.Ry)({entity:(0,n.Z_)(),name:(0,n.jt)((0,n.Z_)()),icon:(0,n.jt)((0,n.Z_)()),image:(0,n.jt)((0,n.Z_)()),secondary_info:(0,n.jt)((0,n.Z_)()),format:(0,n.jt)((0,n.kE)(i.Q)),state_color:(0,n.jt)((0,n.O7)()),tap_action:(0,n.jt)(o.C),hold_action:(0,n.jt)(o.C),double_tap_action:(0,n.jt)(o.C)}),(0,n.Z_)()])},61173:function(e,t,r){r.d(t,{gg:function(){return s},ds:function(){return l}});var n=r(69505),i=r(85677),o=r(30232),a=(0,n.Ry)({type:(0,n.Z_)(),image:(0,n.Z_)(),tap_action:(0,n.jt)(i.C),hold_action:(0,n.jt)(i.C),double_tap_action:(0,n.jt)(i.C)}),c=(0,n.Ry)({type:(0,n.Z_)(),entities:(0,n.IX)(o.K)}),s=(0,n.Ry)({type:(0,n.Z_)(),entity:(0,n.Z_)(),detail:(0,n.jt)((0,n.Rx)()),hours_to_show:(0,n.jt)((0,n.Rx)())}),l=(0,n.G0)([a,c,s])}}]);