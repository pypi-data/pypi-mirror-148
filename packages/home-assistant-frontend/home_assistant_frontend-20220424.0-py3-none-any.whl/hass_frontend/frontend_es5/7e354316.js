"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2979],{54531:function(e,t,r){function n(e,t){var r="undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(!r){if(Array.isArray(e)||(r=function(e,t){if(!e)return;if("string"==typeof e)return i(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return i(e,t)}(e))||t&&e&&"number"==typeof e.length){r&&(e=r);var n=0,o=function(){};return{s:o,n:function(){return n>=e.length?{done:!0}:{done:!1,value:e[n++]}},e:function(e){throw e},f:o}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var a,s=!0,c=!1;return{s:function(){r=r.call(e)},n:function(){var e=r.next();return s=e.done,e},e:function(e){c=!0,a=e},f:function(){try{s||null==r.return||r.return()}finally{if(c)throw a}}}}function i(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}r.d(t,{zJ:function(){return l},Xr:function(){return d},Qc:function(){return u}});var o=["zone","persistent_notification"],a=function(e,t){if("call-service"===t.action&&t.service_data&&t.service_data.entity_id){var r=t.service_data.entity_id;Array.isArray(r)||(r=[r]);var i,o=n(r);try{for(o.s();!(i=o.n()).done;){var a=i.value;e.add(a)}}catch(s){o.e(s)}finally{o.f()}}},s=function(e,t){"string"!=typeof t?(t.entity&&e.add(t.entity),t.camera_image&&e.add(t.camera_image),t.tap_action&&a(e,t.tap_action),t.hold_action&&a(e,t.hold_action)):e.add(t)},c=function e(t,r){r.entity&&s(t,r.entity),r.entities&&Array.isArray(r.entities)&&r.entities.forEach((function(e){return s(t,e)})),r.card&&e(t,r.card),r.cards&&Array.isArray(r.cards)&&r.cards.forEach((function(r){return e(t,r)})),r.elements&&Array.isArray(r.elements)&&r.elements.forEach((function(r){return e(t,r)})),r.badges&&Array.isArray(r.badges)&&r.badges.forEach((function(e){return s(t,e)}))},l=function(e){var t=new Set;return e.views.forEach((function(e){return c(t,e)})),t},d=function(e,t){for(var r=new Set,n=0,i=Object.keys(e.states);n<i.length;n++){var a=i[n];t.has(a)||o.includes(a.split(".",1)[0])||r.add(a)}return r},u=function(e,t){var r=l(t);return d(e,r)}},32979:function(e,t,r){r(22001),r(27303);var n=r(81480),i=r(37500),o=r(33310),a=r(8636),s=r(70483),c=r(65813),l=r(14516),d=r(47181),u=(r(65040),r(31206),r(56007)),f=r(9893),h=r(54531),p=r(51153);function m(e,t,r,n,i,o,a){try{var s=e[o](a),c=s.value}catch(l){return void r(l)}s.done?t(c):Promise.resolve(c).then(n,i)}var y,v,g,w,b,k,E=function(){var e,t=(e=regeneratorRuntime.mark((function e(t,r,n,i){var o,a,s;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return o={type:r},e.next=3,(0,p.Do)(r);case 3:if(!(a=e.sent)||!a.getStubConfig){e.next=9;break}return e.next=7,a.getStubConfig(t,n,i);case 7:s=e.sent,o=Object.assign({},o,s);case 9:return e.abrupt("return",o);case 10:case"end":return e.stop()}}),e)})),function(){var t=this,r=arguments;return new Promise((function(n,i){var o=e.apply(t,r);function a(e){m(o,n,i,a,s,"next",e)}function s(e){m(o,n,i,a,s,"throw",e)}a(void 0)}))});return function(e,r,n,i){return t.apply(this,arguments)}}(),_=[{type:"alarm-panel",showElement:!0},{type:"button",showElement:!0},{type:"calendar",showElement:!0},{type:"entities",showElement:!0},{type:"entity",showElement:!0},{type:"gauge",showElement:!0},{type:"glance",showElement:!0},{type:"history-graph",showElement:!0},{type:"statistics-graph",showElement:!1},{type:"humidifier",showElement:!0},{type:"light",showElement:!0},{type:"map",showElement:!0},{type:"markdown",showElement:!0},{type:"media-control",showElement:!0},{type:"picture",showElement:!0},{type:"picture-elements",showElement:!0},{type:"picture-entity",showElement:!0},{type:"picture-glance",showElement:!0},{type:"plant-status",showElement:!0},{type:"sensor",showElement:!0},{type:"thermostat",showElement:!0},{type:"weather-forecast",showElement:!0},{type:"area",showElement:!0},{type:"conditional"},{type:"entity-filter"},{type:"grid"},{type:"horizontal-stack"},{type:"iframe"},{type:"logbook"},{type:"vertical-stack"},{type:"shopping-list"}];function x(e){return x="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},x(e)}function C(e,t,r,n,i,o,a){try{var s=e[o](a),c=s.value}catch(l){return void r(l)}s.done?t(c):Promise.resolve(c).then(n,i)}function A(e){return function(e){if(Array.isArray(e))return L(e)}(e)||N(e)||H(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function S(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function P(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function z(e,t){return z=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},z(e,t)}function O(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=R(e);if(t){var i=R(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return j(this,r)}}function j(e,t){if(t&&("object"===x(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return D(e)}function D(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function R(e){return R=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},R(e)}function T(){T=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!F(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||N(t)||H(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=$(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:M(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=M(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function I(e){var t,r=$(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function B(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function F(e){return e.decorators&&e.decorators.length}function U(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function M(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function $(e){var t=function(e,t){if("object"!==x(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==x(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===x(t)?t:String(t)}function H(e,t){if(e){if("string"==typeof e)return L(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?L(e,t):void 0}}function L(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function N(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}!function(e,t,r,n){var i=T();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(U(o.descriptor)||U(i.descriptor)){if(F(o)||F(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(F(o)){if(F(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}B(o,i)}else t.push(o)}return t}(a.d.map(I)),e);i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,o.Mo)("hui-card-picker")],(function(e,t){var r,m,x=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&z(e,t)}(n,t);var r=O(n);function n(){var t;P(this,n);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=r.call.apply(r,[this].concat(o)),e(D(t)),t}return n}(t);return{F:x,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_cards",value:function(){return[]}},{kind:"field",key:"lovelace",value:void 0},{kind:"field",key:"cardPicked",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_filter",value:function(){return""}},{kind:"field",decorators:[(0,o.SB)()],key:"_width",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_height",value:void 0},{kind:"field",key:"_unusedEntities",value:void 0},{kind:"field",key:"_usedEntities",value:void 0},{kind:"field",key:"_filterCards",value:function(){return(0,l.Z)((function(e,t){if(!t)return e;var r=e.map((function(e){return e.card})),i=new n.Z(r,{keys:["type","name","description"],isCaseSensitive:!1,minMatchCharLength:2,threshold:.2});return r=i.search(t).map((function(e){return e.item})),e.filter((function(e){return r.includes(e.card)}))}))}},{kind:"method",key:"render",value:function(){return this.hass&&this.lovelace&&this._unusedEntities&&this._usedEntities?(0,i.dy)(v||(v=S(["\n      <search-input\n        .hass=","\n        .filter=","\n        @value-changed=","\n        .label=",'\n      ></search-input>\n      <div\n        id="content"\n        style=','\n      >\n        <div class="cards-container">\n          ','\n        </div>\n        <div class="cards-container">\n          <div\n            class="card manual"\n            @click=',"\n            .config=",'\n          >\n            <div class="card-header">\n              ','\n            </div>\n            <div class="preview description">\n              ',"\n            </div>\n          </div>\n        </div>\n      </div>\n    "])),this.hass,this._filter,this._handleSearchChange,this.hass.localize("ui.panel.lovelace.editor.edit_card.search_cards"),(0,s.V)({width:this._width?"".concat(this._width,"px"):"auto",height:this._height?"".concat(this._height,"px"):"auto"}),this._filterCards(this._cards,this._filter).map((function(e){return e.element})),this._cardPicked,{type:""},this.hass.localize("ui.panel.lovelace.editor.card.generic.manual"),this.hass.localize("ui.panel.lovelace.editor.card.generic.manual_description")):(0,i.dy)(y||(y=S([""])))}},{kind:"method",key:"shouldUpdate",value:function(e){var t=e.get("hass");return!t||t.locale!==this.hass.locale}},{kind:"method",key:"firstUpdated",value:function(){var e=this;if(this.hass&&this.lovelace){var t=(0,h.zJ)(this.lovelace),r=(0,h.Xr)(this.hass,t);this._usedEntities=A(t).filter((function(t){return e.hass.states[t]&&!u.V_.includes(e.hass.states[t].state)})),this._unusedEntities=A(r).filter((function(t){return e.hass.states[t]&&!u.V_.includes(e.hass.states[t].state)})),this._loadCards()}}},{kind:"method",key:"_loadCards",value:function(){var e=this,t=_.map((function(t){return Object.assign({name:e.hass.localize("ui.panel.lovelace.editor.card.".concat(t.type,".name")),description:e.hass.localize("ui.panel.lovelace.editor.card.".concat(t.type,".description"))},t)}));f.kb.length>0&&(t=t.concat(f.kb.map((function(e){return{type:e.type,name:e.name,description:e.description,showElement:e.preview,isCustom:!0}})))),this._cards=t.map((function(t){return{card:t,element:(0,i.dy)(g||(g=S(["",""])),(0,c.C)(e._renderCardElement(t),(0,i.dy)(w||(w=S(['\n          <div class="card spinner">\n            <ha-circular-progress active alt="Loading"></ha-circular-progress>\n          </div>\n        '])))))}}))}},{kind:"method",key:"_handleSearchChange",value:function(e){var t=e.detail.value;if(t){if(!this._width||!this._height){var r=this.shadowRoot.getElementById("content");if(r&&!this._width){var n=r.clientWidth;n&&(this._width=n)}if(r&&!this._height){var i=r.clientHeight;i&&(this._height=i)}}}else this._width=void 0,this._height=void 0;this._filter=t}},{kind:"method",key:"_cardPicked",value:function(e){var t=e.currentTarget.config;(0,d.B)(this,"config-changed",{config:t})}},{kind:"method",key:"_tryCreateCardElement",value:function(e){var t=this,r=(0,p.l$)(e);return r.hass=this.hass,r.addEventListener("ll-rebuild",(function(n){n.stopPropagation(),t._rebuildCard(r,e)}),{once:!0}),r}},{kind:"method",key:"_rebuildCard",value:function(e,t){var r;try{r=this._tryCreateCardElement(t)}catch(n){return}e.parentElement&&e.parentElement.replaceChild(r,e)}},{kind:"method",key:"_renderCardElement",value:(r=regeneratorRuntime.mark((function e(t){var r,n,o,s,c,l,d,u;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(r=t.type,n=t.showElement,o=t.isCustom,s=t.name,c=t.description,l=o?(0,f.cs)(r):void 0,o&&(r="".concat(f.Qo).concat(r)),u={type:r},!this.hass||!this.lovelace){e.next=10;break}return e.next=8,E(this.hass,r,this._unusedEntities,this._usedEntities);case 8:if(u=e.sent,n)try{d=this._tryCreateCardElement(u)}catch(h){d=void 0}case 10:return e.abrupt("return",(0,i.dy)(b||(b=S(['\n      <div class="card">\n        <div\n          class="overlay"\n          @click=',"\n          .config=",'\n        ></div>\n        <div class="card-header">\n          ','\n        </div>\n        <div\n          class="preview ','"\n        >\n          ',"\n        </div>\n      </div>\n    "])),this._cardPicked,u,l?"".concat(this.hass.localize("ui.panel.lovelace.editor.cardpicker.custom_card"),": ").concat(l.name||l.type):s,(0,a.$)({description:!d||"HUI-ERROR-CARD"===d.tagName}),d&&"HUI-ERROR-CARD"!==d.tagName?d:l?l.description||this.hass.localize("ui.panel.lovelace.editor.cardpicker.no_description"):c));case 11:case"end":return e.stop()}}),e,this)})),m=function(){var e=this,t=arguments;return new Promise((function(n,i){var o=r.apply(e,t);function a(e){C(o,n,i,a,s,"next",e)}function s(e){C(o,n,i,a,s,"throw",e)}a(void 0)}))},function(e){return m.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return[(0,i.iv)(k||(k=S(["\n        search-input {\n          display: block;\n          --mdc-shape-small: var(--card-picker-search-shape);\n          margin: var(--card-picker-search-margin);\n        }\n\n        .cards-container {\n          display: grid;\n          grid-gap: 8px 8px;\n          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));\n          margin-top: 20px;\n        }\n\n        .card {\n          height: 100%;\n          max-width: 500px;\n          display: flex;\n          flex-direction: column;\n          border-radius: var(--ha-card-border-radius, 4px);\n          background: var(--primary-background-color, #fafafa);\n          cursor: pointer;\n          position: relative;\n        }\n\n        .card-header {\n          color: var(--ha-card-header-color, --primary-text-color);\n          font-family: var(--ha-card-header-font-family, inherit);\n          font-size: 16px;\n          font-weight: bold;\n          letter-spacing: -0.012em;\n          line-height: 20px;\n          padding: 12px 16px;\n          display: block;\n          text-align: center;\n          background: var(\n            --ha-card-background,\n            var(--card-background-color, white)\n          );\n          border-bottom: 1px solid var(--divider-color);\n        }\n\n        .preview {\n          pointer-events: none;\n          margin: 20px;\n          flex-grow: 1;\n          display: flex;\n          align-items: center;\n          justify-content: center;\n        }\n\n        .preview > :first-child {\n          zoom: 0.6;\n          display: block;\n          width: 100%;\n        }\n\n        .description {\n          text-align: center;\n        }\n\n        .spinner {\n          align-items: center;\n          justify-content: center;\n        }\n\n        .overlay {\n          position: absolute;\n          width: 100%;\n          height: 100%;\n          z-index: 1;\n          box-sizing: border-box;\n          border: var(--ha-card-border-width, 1px) solid\n            var(--ha-card-border-color, var(--divider-color));\n          border-radius: var(--ha-card-border-radius, 4px);\n        }\n\n        .manual {\n          max-width: none;\n        }\n      "])))]}}]}}),i.oi)}}]);