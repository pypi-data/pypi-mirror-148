/*! For license information please see 11526eb1.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[492],{89833:function(e,t,n){n.d(t,{O:function(){return _}});var r,i,o=n(87480),a=n(86251),c=n(37500),s=n(33310),l=n(8636),u=n(51346),f=n(71260);function d(e){return d="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},d(e)}function h(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function p(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function m(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function y(e,t){return y=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},y(e,t)}function v(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=g(e);if(t){var i=g(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return b(this,n)}}function b(e,t){if(t&&("object"===d(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function g(e){return g=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},g(e)}var _=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&y(e,t)}(s,e);var t,n,o,a=v(s);function s(){var e;return p(this,s),(e=a.apply(this,arguments)).rows=2,e.cols=20,e.charCounter=!1,e}return t=s,(n=[{key:"render",value:function(){var e=this.charCounter&&-1!==this.maxLength,t=e&&"internal"===this.charCounter,n=e&&!t,i=!!this.helper||!!this.validationMessage||n,o={"mdc-text-field--disabled":this.disabled,"mdc-text-field--no-label":!this.label,"mdc-text-field--filled":!this.outlined,"mdc-text-field--outlined":this.outlined,"mdc-text-field--end-aligned":this.endAligned,"mdc-text-field--with-internal-counter":t};return(0,c.dy)(r||(r=h(['\n      <label class="mdc-text-field mdc-text-field--textarea ','">\n        ',"\n        ","\n        ","\n        ","\n        ","\n      </label>\n      ","\n    "])),(0,l.$)(o),this.renderRipple(),this.outlined?this.renderOutline():this.renderLabel(),this.renderInput(),this.renderCharCounter(t),this.renderLineRipple(),this.renderHelperText(i,n))}},{key:"renderInput",value:function(){var e=this.label?"label":void 0,t=-1===this.minLength?void 0:this.minLength,n=-1===this.maxLength?void 0:this.maxLength,r=this.autocapitalize?this.autocapitalize:void 0;return(0,c.dy)(i||(i=h(["\n      <textarea\n          aria-labelledby=",'\n          class="mdc-text-field__input"\n          .value="','"\n          rows="','"\n          cols="','"\n          ?disabled="','"\n          placeholder="','"\n          ?required="','"\n          ?readonly="','"\n          minlength="','"\n          maxlength="','"\n          name="','"\n          inputmode="','"\n          autocapitalize="','"\n          @input="','"\n          @blur="','">\n      </textarea>'])),(0,u.o)(e),(0,f.a)(this.value),this.rows,this.cols,this.disabled,this.placeholder,this.required,this.readOnly,(0,u.o)(t),(0,u.o)(n),(0,u.o)(""===this.name?void 0:this.name),(0,u.o)(this.inputMode),(0,u.o)(r),this.handleInputChange,this.onInputBlur)}}])&&m(t.prototype,n),o&&m(t,o),s}(a.P);(0,o.__decorate)([(0,s.IO)("textarea")],_.prototype,"formElement",void 0),(0,o.__decorate)([(0,s.Cb)({type:Number})],_.prototype,"rows",void 0),(0,o.__decorate)([(0,s.Cb)({type:Number})],_.prototype,"cols",void 0),(0,o.__decorate)([(0,s.Cb)({converter:{fromAttribute:function(e){return null!==e&&(""===e||e)},toAttribute:function(e){return"boolean"==typeof e?e?"":null:e}}})],_.prototype,"charCounter",void 0)},96791:function(e,t,n){var r;n.d(t,{W:function(){return a}});var i,o,a=(0,n(37500).iv)(r||(i=[".mdc-text-field{height:100%}.mdc-text-field__input{resize:none}"],o||(o=i.slice(0)),r=Object.freeze(Object.defineProperties(i,{raw:{value:Object.freeze(o)}}))))},89194:function(e,t,n){n(48175),n(65660),n(70019);var r,i,o,a=n(9672),c=n(50856);(0,a.k)({_template:(0,c.d)(r||(i=["\n    <style>\n      :host {\n        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */\n        @apply --layout-vertical;\n        @apply --layout-center-justified;\n        @apply --layout-flex;\n      }\n\n      :host([two-line]) {\n        min-height: var(--paper-item-body-two-line-min-height, 72px);\n      }\n\n      :host([three-line]) {\n        min-height: var(--paper-item-body-three-line-min-height, 88px);\n      }\n\n      :host > ::slotted(*) {\n        overflow: hidden;\n        text-overflow: ellipsis;\n        white-space: nowrap;\n      }\n\n      :host > ::slotted([secondary]) {\n        @apply --paper-font-body1;\n\n        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));\n\n        @apply --paper-item-body-secondary;\n      }\n    </style>\n\n    <slot></slot>\n"],o||(o=i.slice(0)),r=Object.freeze(Object.defineProperties(i,{raw:{value:Object.freeze(o)}})))),is:"paper-item-body"})},76270:function(e,t,n){n.d(t,{Q:function(){return r}});var r=["relative","total","date","time","datetime"]},33785:function(e,t,n){n.r(t),n.d(t,{HuiPictureGlanceCardEditor:function(){return T}});var r,i,o=n(37500),a=n(33310),c=n(69505),s=n(47181),l=(n(13701),n(26431),n(1528),n(14748)),u=n(85677),f=n(98346),d=n(30232),h=n(45890);function p(e){return p="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},p(e)}function m(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function y(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function v(e,t){return v=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},v(e,t)}function b(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=w(e);if(t){var i=w(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return g(this,n)}}function g(e,t){if(t&&("object"===p(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return _(e)}function _(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function w(e){return w=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},w(e)}function k(){k=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var i=t.placement;if(t.kind===r&&("static"===i||"prototype"===i)){var o="static"===i?e:n;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!O(e))return n.push(e);var t=this.decorateElement(e,i);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:n,finishers:r};var o=this.decorateConstructor(n,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var c=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,i[o])(c)||c);e=s.element,this.addElementPlacement(e,t),s.finisher&&r.push(s.finisher);var l=s.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);n.push.apply(n,l)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(i)||i);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var c=a+1;c<e.length;c++)if(e[a].key===e[c].key&&e[a].placement===e[c].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return z(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?z(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=P(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:n,placement:r,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:C(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=C(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function j(e){var t,n=P(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function E(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function O(e){return e.decorators&&e.decorators.length}function x(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function C(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function P(e){var t=function(e,t){if("object"!==p(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==p(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===p(t)?t:String(t)}function z(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}var S=(0,c.f0)(f.I,(0,c.Ry)({title:(0,c.jt)((0,c.Z_)()),entity:(0,c.jt)((0,c.Z_)()),image:(0,c.jt)((0,c.Z_)()),camera_image:(0,c.jt)((0,c.Z_)()),camera_view:(0,c.jt)((0,c.Z_)()),aspect_ratio:(0,c.jt)((0,c.Z_)()),tap_action:(0,c.jt)(u.C),hold_action:(0,c.jt)(u.C),entities:(0,c.IX)(d.K),theme:(0,c.jt)((0,c.Z_)())})),A=["more-info","toggle","navigate","call-service","none"],D=[{name:"title",selector:{text:{}}},{name:"image",selector:{text:{}}},{name:"camera_image",selector:{entity:{domain:"camera"}}},{name:"",type:"grid",schema:[{name:"camera_view",selector:{select:{options:["auto","live"]}}},{name:"aspect_ratio",selector:{text:{}}}]},{name:"entity",selector:{entity:{}}},{name:"theme",selector:{theme:{}}}],T=function(e,t,n,r){var i=k();if(r)for(var o=0;o<r.length;o++)i=r[o](i);var a=t((function(e){i.initializeInstanceElements(e,c.elements)}),n),c=i.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var i,o=e[r];if("method"===o.kind&&(i=t.find(n)))if(x(o.descriptor)||x(i.descriptor)){if(O(o)||O(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(O(o)){if(O(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}E(o,i)}else t.push(o)}return t}(a.d.map(j)),e);return i.initializeClassElements(a.F,c.elements),i.runClassFinishers(a.F,c.finishers)}([(0,a.Mo)("hui-picture-glance-card-editor")],(function(e,t){var n=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&v(e,t)}(r,t);var n=b(r);function r(){var t;y(this,r);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=n.call.apply(n,[this].concat(o)),e(_(t)),t}return r}(t);return{F:n,d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_configEntities",value:void 0},{kind:"method",key:"setConfig",value:function(e){(0,c.hu)(e,S),this._config=e,this._configEntities=(0,l.Q)(e.entities)}},{kind:"get",key:"_tap_action",value:function(){return this._config.tap_action||{action:"toggle"}}},{kind:"get",key:"_hold_action",value:function(){return this._config.hold_action||{action:"more-info"}}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return(0,o.dy)(r||(r=m([""])));var e=Object.assign({camera_view:"auto"},this._config);return(0,o.dy)(i||(i=m(["\n      <ha-form\n        .hass=","\n        .data=","\n        .schema=","\n        .computeLabel=","\n        @value-changed=",'\n      ></ha-form>\n      <div class="card-config">\n        <hui-action-editor\n          .label=',"\n          .hass=","\n          .config=","\n          .actions=","\n          .configValue=","\n          @value-changed=","\n        ></hui-action-editor>\n        <hui-action-editor\n          .label=","\n          .hass=","\n          .config=","\n          .actions=","\n          .configValue=","\n          @value-changed=","\n        ></hui-action-editor>\n        <hui-entity-editor\n          .hass=","\n          .entities=","\n          @entities-changed=","\n        ></hui-entity-editor>\n      </div>\n    "])),this.hass,e,D,this._computeLabelCallback,this._valueChanged,this.hass.localize("ui.panel.lovelace.editor.card.generic.tap_action"),this.hass,this._tap_action,A,"tap_action",this._valueChanged,this.hass.localize("ui.panel.lovelace.editor.card.generic.hold_action"),this.hass,this._hold_action,A,"hold_action",this._valueChanged,this.hass,this._configEntities,this._changed)}},{kind:"method",key:"_valueChanged",value:function(e){(0,s.B)(this,"config-changed",{config:e.detail.value})}},{kind:"method",key:"_changed",value:function(e){if(this._config&&this.hass){var t=e.target,n=e.detail.value;if(e.detail&&e.detail.entities)this._config=Object.assign({},this._config,{entities:e.detail.entities}),this._configEntities=(0,l.Q)(this._config.entities);else if(t.configValue){if(this["_".concat(t.configValue)]===n)return;!1===n||n?this._config=Object.assign({},this._config,function(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}({},t.configValue,n)):(this._config=Object.assign({},this._config),delete this._config[t.configValue])}(0,s.B)(this,"config-changed",{config:this._config})}}},{kind:"field",key:"_computeLabelCallback",value:function(){var e=this;return function(t){return"entity"===t.name?e.hass.localize("ui.panel.lovelace.editor.card.picture-glance.state_entity"):"theme"===t.name?"".concat(e.hass.localize("ui.panel.lovelace.editor.card.generic.theme")," (").concat(e.hass.localize("ui.panel.lovelace.editor.card.config.optional"),")"):e.hass.localize("ui.panel.lovelace.editor.card.generic.".concat(t.name))||e.hass.localize("ui.panel.lovelace.editor.card.picture-glance.".concat(t.name))}}},{kind:"field",static:!0,key:"styles",value:function(){return h.A}}]}}),o.oi)},30232:function(e,t,n){n.d(t,{K:function(){return a}});var r=n(69505),i=n(76270),o=n(85677),a=(0,r.G0)([(0,r.Ry)({entity:(0,r.Z_)(),name:(0,r.jt)((0,r.Z_)()),icon:(0,r.jt)((0,r.Z_)()),image:(0,r.jt)((0,r.Z_)()),secondary_info:(0,r.jt)((0,r.Z_)()),format:(0,r.jt)((0,r.kE)(i.Q)),state_color:(0,r.jt)((0,r.O7)()),tap_action:(0,r.jt)(o.C),hold_action:(0,r.jt)(o.C),double_tap_action:(0,r.jt)(o.C)}),(0,r.Z_)()])}}]);