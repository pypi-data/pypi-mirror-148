"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[999],{60999:function(e,t,r){r.r(t),r.d(t,{SideBarView:function(){return j}});var n,i,o,a=r(37500),l=r(33310),s=r(8636),c=r(47181),d=r(87744),u=r(54324);function f(e){return f="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},f(e)}function p(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function h(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function v(e,t){return v=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},v(e,t)}function m(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=O(e);if(t){var i=O(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return y(this,r)}}function y(e,t){if(t&&("object"===f(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return b(e)}function b(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function k(){k=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!E(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var l=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,i[o])(l)||l);e=s.element,this.addElementPlacement(e,t),s.finisher&&n.push(s.finisher);var c=s.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var l=a+1;l<e.length;l++)if(e[a].key===e[l].key&&e[a].placement===e[l].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return P(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?P(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=_(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:x(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=x(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function w(e){var t,r=_(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function g(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function E(e){return e.decorators&&e.decorators.length}function C(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function x(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function _(e){var t=function(e,t){if("object"!==f(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==f(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===f(t)?t:String(t)}function P(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function S(e,t,r){return S="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=O(e)););return e}(e,t);if(n){var i=Object.getOwnPropertyDescriptor(n,t);return i.get?i.get.call(r):i.value}},S(e,t,r||e)}function O(e){return O=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},O(e)}var j=function(e,t,r,n){var i=k();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,l.elements)}),r),l=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(C(o.descriptor)||C(i.descriptor)){if(E(o)||E(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(E(o)){if(E(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}g(o,i)}else t.push(o)}return t}(a.d.map(w)),e);return i.initializeClassElements(a.F,l.elements),i.runClassFinishers(a.F,l.finishers)}(null,(function(e,t){var f=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&v(e,t)}(n,t);var r=m(n);function n(){var t;h(this,n);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=r.call.apply(r,[this].concat(o)),e(b(t)),t}return n}(t);return{F:f,d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Number})],key:"index",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"isStrategy",value:function(){return!1}},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"cards",value:function(){return[]}},{kind:"field",decorators:[(0,l.SB)()],key:"_config",value:void 0},{kind:"field",key:"_mqlListenerRef",value:void 0},{kind:"field",key:"_mql",value:void 0},{kind:"method",key:"connectedCallback",value:function(){S(O(f.prototype),"connectedCallback",this).call(this),this._mql=window.matchMedia("(min-width: 760px)"),this._mqlListenerRef=this._createCards.bind(this),this._mql.addListener(this._mqlListenerRef)}},{kind:"method",key:"disconnectedCallback",value:function(){var e;S(O(f.prototype),"disconnectedCallback",this).call(this),null===(e=this._mql)||void 0===e||e.removeListener(this._mqlListenerRef),this._mqlListenerRef=void 0,this._mql=void 0}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"willUpdate",value:function(e){var t,n,i;if(S(O(f.prototype),"willUpdate",this).call(this,e),null!==(t=this.lovelace)&&void 0!==t&&t.editMode&&Promise.all([r.e(9071),r.e(4103),r.e(9799),r.e(6294),r.e(5916),r.e(741)]).then(r.bind(r,70741)),e.has("cards")&&this._createCards(),e.has("lovelace")||e.has("_config")){var o=e.get("lovelace");(!e.has("cards")&&(null==o?void 0:o.config)!==(null===(n=this.lovelace)||void 0===n?void 0:n.config)||o&&(null==o?void 0:o.editMode)!==(null===(i=this.lovelace)||void 0===i?void 0:i.editMode))&&this._createCards()}}},{kind:"method",key:"render",value:function(){var e;return(0,a.dy)(n||(n=p(['\n      <div class="container"></div>\n      ',"\n    "])),null!==(e=this.lovelace)&&void 0!==e&&e.editMode?(0,a.dy)(i||(i=p(["\n            <ha-fab\n              .label=","\n              extended\n              @click=","\n              class=",'\n            >\n              <ha-svg-icon slot="icon" .path=',"></ha-svg-icon>\n            </ha-fab>\n          "])),this.hass.localize("ui.panel.lovelace.editor.edit_card.add"),this._addCard,(0,s.$)({rtl:(0,d.HE)(this.hass)}),"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"):"")}},{kind:"method",key:"_addCard",value:function(){(0,c.B)(this,"ll-create-card")}},{kind:"method",key:"_createCards",value:function(){var e,t,r=this,n=document.createElement("div");if(n.id="main",null!==(e=this._mql)&&void 0!==e&&e.matches?(t=document.createElement("div")).id="sidebar":t=n,this.hasUpdated){var i=this.renderRoot.querySelector("#main"),o=this.renderRoot.querySelector("#sidebar"),a=this.renderRoot.querySelector(".container");i&&a.removeChild(i),o&&a.removeChild(o),a.appendChild(n),a.appendChild(t)}else this.updateComplete.then((function(){var e=r.renderRoot.querySelector(".container");e.appendChild(n),e.appendChild(t)}));this.cards.forEach((function(e,i){var o,a,l,s,c,d=null===(o=r._config)||void 0===o||null===(a=o.cards)||void 0===a?void 0:a[i];if(r.isStrategy||null===(l=r.lovelace)||void 0===l||!l.editMode)e.editMode=!1,c=e;else{var f;(c=document.createElement("hui-card-options")).hass=r.hass,c.lovelace=r.lovelace,c.path=[r.index,i],e.editMode=!0;var p=document.createElement("ha-icon-button");p.slot="buttons";var h=document.createElement("ha-svg-icon");h.path="sidebar"!==(null==d||null===(f=d.view_layout)||void 0===f?void 0:f.position)?"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z":"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z",p.appendChild(h),p.addEventListener("click",(function(){var e;r.lovelace.saveConfig((0,u.LG)(r.lovelace.config,[r.index,i],Object.assign({},d,{view_layout:{position:"sidebar"!==(null==d||null===(e=d.view_layout)||void 0===e?void 0:e.position)?"sidebar":"main"}})))})),c.appendChild(p),c.appendChild(e)}"sidebar"!==(null==d||null===(s=d.view_layout)||void 0===s?void 0:s.position)?n.appendChild(c):t.appendChild(c)}))}},{kind:"get",static:!0,key:"styles",value:function(){return(0,a.iv)(o||(o=p(["\n      :host {\n        display: block;\n        padding-top: 4px;\n        height: 100%;\n        box-sizing: border-box;\n      }\n\n      .container {\n        display: flex;\n        justify-content: center;\n        margin-left: 4px;\n        margin-right: 4px;\n      }\n\n      #main {\n        max-width: 1620px;\n        flex-grow: 2;\n      }\n\n      #sidebar {\n        flex-grow: 1;\n        flex-shrink: 0;\n        max-width: 380px;\n      }\n\n      .container > div {\n        min-width: 0;\n        box-sizing: border-box;\n      }\n\n      .container > div > * {\n        display: block;\n        margin: var(--masonry-view-card-margin, 4px 4px 8px);\n      }\n\n      @media (max-width: 500px) {\n        .container > div > * {\n          margin-left: 0;\n          margin-right: 0;\n        }\n      }\n\n      ha-fab {\n        position: sticky;\n        float: right;\n        right: calc(16px + env(safe-area-inset-right));\n        bottom: calc(16px + env(safe-area-inset-bottom));\n        z-index: 1;\n      }\n\n      ha-fab.rtl {\n        float: left;\n        right: auto;\n        left: calc(16px + env(safe-area-inset-left));\n      }\n    "])))}}]}}),a.oi);customElements.define("hui-sidebar-view",j)}}]);