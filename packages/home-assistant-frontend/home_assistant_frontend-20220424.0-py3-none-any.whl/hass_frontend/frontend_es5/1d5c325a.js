"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[1866],{24734:function(e,t,n){n.d(t,{B:function(){return i}});var r=n(47181),i=function(e,t){(0,r.B)(e,"show-dialog",{dialogTag:"dialog-media-player-browse",dialogImport:function(){return Promise.all([n.e(9563),n.e(8985),n.e(9071),n.e(4103),n.e(8278),n.e(9799),n.e(6294),n.e(5084),n.e(4444),n.e(5906),n.e(5916),n.e(3555),n.e(6630),n.e(4821),n.e(7576),n.e(4535),n.e(546),n.e(9792),n.e(3271),n.e(8882)]).then(n.bind(n,52809))},dialogParams:t})}},11866:function(e,t,n){n.r(t),n.d(t,{HuiMediaControlCard:function(){return ee}});n(62744);var r=n(37500),i=n(33310),o=n(8636),a=n(70483),s=n(62877),c=n(47181),l=n(91741),d=n(40095),u=n(67794),h=n.n(u),f=n(74790),p=!1;h()._pipeline.generator.register("default",(function(e){e.sort((function(e,t){return t.population-e.population}));for(var t,n=e[0],r=new Map,i=function(e,t){return r.has(e)||r.set(e,(0,f.$o)(n.rgb,t)),r.get(e)>4.5},o=1;o<e.length&&void 0===t;o++){if(i(e[o].hex,e[o].rgb)){p,t=e[o].rgb;break}var a=e[o];p;for(var s=o+1;s<e.length;s++){var c=e[s],l=Math.abs(a.rgb[0]-c.rgb[0])+Math.abs(a.rgb[1]-c.rgb[1])+Math.abs(a.rgb[2]-c.rgb[2]);if(!(l>150)&&i(c.hex,c.rgb)){p,t=c.rgb;break}}}return void 0===t&&(t=n.getYiq()<200?[255,255,255]:[0,0,0]),{foreground:new n.constructor(t,0),background:n}}));var m,v,g,y,b,_,k,w,x,C,E,O=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:16;return new(h())(e,{colorCount:t}).getPalette().then((function(e){var t=e.foreground;return{background:e.background,foreground:t}}))},P=n(38346),A=(n(22098),n(10983),n(99724),n(24734)),j=n(56007),z=n(69371),S=n(15688),I=n(53658),B=n(54845),M=(n(9829),n(75502));function D(e){return D="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},D(e)}function R(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function T(e,t,n,r,i,o,a){try{var s=e[o](a),c=s.value}catch(l){return void n(l)}s.done?t(c):Promise.resolve(c).then(r,i)}function q(e){return function(){var t=this,n=arguments;return new Promise((function(r,i){var o=e.apply(t,n);function a(e){T(o,r,i,a,s,"next",e)}function s(e){T(o,r,i,a,s,"throw",e)}a(void 0)}))}}function V(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function H(e,t){return H=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},H(e,t)}function F(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=Q(e);if(t){var i=Q(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return U(this,n)}}function U(e,t){if(t&&("object"===D(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return N(e)}function N(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function L(){L=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var i=t.placement;if(t.kind===r&&("static"===i||"prototype"===i)){var o="static"===i?e:n;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!Z(e))return n.push(e);var t=this.decorateElement(e,i);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:n,finishers:r};var o=this.decorateConstructor(n,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);n.push.apply(n,l)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(i)||i);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return J(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?J(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=Y(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:n,placement:r,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:X(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=X(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function W(e){var t,n=Y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function $(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function Z(e){return e.decorators&&e.decorators.length}function G(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function X(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function Y(e){var t=function(e,t){if("object"!==D(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==D(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===D(t)?t:String(t)}function J(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function K(e,t,n){return K="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=Q(e)););return e}(e,t);if(r){var i=Object.getOwnPropertyDescriptor(r,t);return i.get?i.get.call(n):i.value}},K(e,t,n||e)}function Q(e){return Q=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},Q(e)}var ee=function(e,t,n,r){var i=L();if(r)for(var o=0;o<r.length;o++)i=r[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),n),s=i.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var i,o=e[r];if("method"===o.kind&&(i=t.find(n)))if(G(o.descriptor)||G(i.descriptor)){if(Z(o)||Z(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(Z(o)){if(Z(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}$(o,i)}else t.push(o)}return t}(a.d.map(W)),e);return i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,i.Mo)("hui-media-control-card")],(function(e,t){var u,h,f,p=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&H(e,t)}(r,t);var n=F(r);function r(){var t;V(this,r);for(var i=arguments.length,o=new Array(i),a=0;a<i;a++)o[a]=arguments[a];return t=n.call.apply(n,[this].concat(o)),e(N(t)),t}return r}(t);return{F:p,d:[{kind:"method",static:!0,key:"getConfigElement",value:(f=q(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Promise.all([n.e(9563),n.e(8985),n.e(9071),n.e(4103),n.e(8278),n.e(9799),n.e(6294),n.e(5906),n.e(3555),n.e(6630),n.e(7576),n.e(4535),n.e(423)]).then(n.bind(n,52105));case 2:return e.abrupt("return",document.createElement("hui-media-control-card-editor"));case 3:case"end":return e.stop()}}),e)}))),function(){return f.apply(this,arguments)})},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,n){return{type:"media-control",entity:(0,S.j)(e,1,t,n,["media_player"])[0]||""}}},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,i.SB)()],key:"_foregroundColor",value:void 0},{kind:"field",decorators:[(0,i.SB)()],key:"_backgroundColor",value:void 0},{kind:"field",decorators:[(0,i.SB)()],key:"_narrow",value:function(){return!1}},{kind:"field",decorators:[(0,i.SB)()],key:"_veryNarrow",value:function(){return!1}},{kind:"field",decorators:[(0,i.SB)()],key:"_cardHeight",value:function(){return 0}},{kind:"field",decorators:[(0,i.IO)("mwc-linear-progress")],key:"_progressBar",value:void 0},{kind:"field",decorators:[(0,i.SB)()],key:"_marqueeActive",value:function(){return!1}},{kind:"field",key:"_progressInterval",value:void 0},{kind:"field",key:"_resizeObserver",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){if(!e.entity||"media_player"!==e.entity.split(".")[0])throw new Error("Specify an entity from within the media_player domain");this._config=e}},{kind:"method",key:"connectedCallback",value:function(){var e=this;if(K(Q(p.prototype),"connectedCallback",this).call(this),this.updateComplete.then((function(){return e._attachObserver()})),this.hass&&this._config){var t=this._stateObj;t&&!this._progressInterval&&this._showProgressBar&&"playing"===t.state&&(this._progressInterval=window.setInterval((function(){return e._updateProgressBar()}),1e3))}}},{kind:"method",key:"disconnectedCallback",value:function(){this._progressInterval&&(clearInterval(this._progressInterval),this._progressInterval=void 0),this._resizeObserver&&this._resizeObserver.disconnect()}},{kind:"method",key:"render",value:function(){var e=this;if(!this.hass||!this._config)return(0,r.dy)(m||(m=R([""])));var t=this._stateObj;if(!t)return(0,r.dy)(v||(v=R(["\n        <hui-warning>\n          ","\n        </hui-warning>\n      "])),(0,M.i)(this.hass,this._config.entity));var n={"background-image":this._image?"url(".concat(this.hass.hassUrl(this._image),")"):"none",width:"".concat(this._cardHeight,"px"),"background-color":this._backgroundColor||""},i={"background-image":"linear-gradient(to right, ".concat(this._backgroundColor,", ").concat(this._backgroundColor+"00",")"),width:"".concat(this._cardHeight,"px")},s=t.state,c="off"===s,u=j.V_.includes(s)||"off"===s&&!(0,d.e)(t,z.rv),h=!this._image,f=(0,z.xt)(t,!1),p=f&&(!this._veryNarrow||c||"idle"===s||"on"===s),E=(0,z.Mj)(t),O=(0,z.WL)(t.attributes.media_title);return(0,r.dy)(g||(g=R(['\n      <ha-card>\n        <div\n          class="background ','"\n        >\n          <div\n            class="color-block"\n            style=','\n          ></div>\n          <div\n            class="no-img"\n            style=','\n          ></div>\n          <div class="image" style=',"></div>\n          ",'\n        </div>\n        <div\n          class="player ','"\n          style=','\n        >\n          <div class="top-info">\n            <div class="icon-name">\n              <ha-state-icon class="icon" .state=',"></ha-state-icon>\n              <div>\n                ","\n              </div>\n            </div>\n            <div>\n              <ha-icon-button\n                .path=","\n                .label=",'\n                class="more-info"\n                @click=',"\n              ></ha-icon-button>\n            </div>\n          </div>\n          ","\n        </div>\n      </ha-card>\n    "])),(0,o.$)({"no-image":h,off:c||u,unavailable:u}),(0,a.V)({"background-color":this._backgroundColor||""}),(0,a.V)({"background-color":this._backgroundColor||""}),(0,a.V)(n),h?"":(0,r.dy)(y||(y=R(['\n                <div\n                  class="color-gradient"\n                  style=',"\n                ></div>\n              "])),(0,a.V)(i)),(0,o.$)({"no-image":h,narrow:this._narrow&&!this._veryNarrow,off:c||u,"no-progress":this._veryNarrow||!this._showProgressBar,"no-controls":!p}),(0,a.V)({color:this._foregroundColor||""}),t,this._config.name||(0,l.C)(this.hass.states[this._config.entity]),"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z",this.hass.localize("ui.panel.lovelace.cards.show_more_info"),this._handleMoreInfo,!u&&(E||O||p)?(0,r.dy)(b||(b=R(['\n                <div>\n                  <div class="title-controls">\n                    ',"\n                    ","\n                  </div>\n                  ","\n                </div>\n              "])),E||O?(0,r.dy)(_||(_=R(['\n                          <div class="media-info">\n                            <hui-marquee\n                              .text=',"\n                              .active=","\n                              @mouseover=","\n                              @mouseleave=","\n                            ></hui-marquee>\n                            ","\n                          </div>\n                        "])),O||E,this._marqueeActive,this._marqueeMouseOver,this._marqueeMouseLeave,O?E:""):"",p?(0,r.dy)(k||(k=R(['\n                          <div class="controls">\n                            ',"\n                            ","\n                          </div>\n                        "])),f.map((function(t){return(0,r.dy)(w||(w=R(["\n                                <ha-icon-button\n                                  .label=","\n                                  .path=","\n                                  action=","\n                                  @click=","\n                                >\n                                </ha-icon-button>\n                              "])),e.hass.localize("ui.card.media_player.".concat(t.action)),t.icon,t.action,e._handleClick)})),(0,d.e)(t,z.pu)?(0,r.dy)(x||(x=R(['\n                                  <ha-icon-button\n                                    class="browse-media"\n                                    .label=',"\n                                    .path=","\n                                    @click=","\n                                  ></ha-icon-button>\n                                "])),this.hass.localize("ui.card.media_player.browse_media"),"M4,6H2V20A2,2 0 0,0 4,22H18V20H4V6M20,2H8A2,2 0 0,0 6,4V16A2,2 0 0,0 8,18H20A2,2 0 0,0 22,16V4A2,2 0 0,0 20,2M12,14.5V5.5L18,10L12,14.5Z",this._handleBrowseMedia):""):"",this._showProgressBar?(0,r.dy)(C||(C=R(["\n                        <mwc-linear-progress\n                          determinate\n                          style=","\n                          @click=","\n                        >\n                        </mwc-linear-progress>\n                      "])),(0,a.V)({"--mdc-theme-primary":this._foregroundColor||"var(--accent-color)",cursor:(0,d.e)(t,z.xh)?"pointer":"initial"}),this._handleSeek):""):"")}},{kind:"method",key:"shouldUpdate",value:function(e){return(0,I.G)(this,e)}},{kind:"method",key:"firstUpdated",value:function(){this._attachObserver()}},{kind:"method",key:"willUpdate",value:function(e){var t,n;if(K(Q(p.prototype),"willUpdate",this).call(this,e),this.hasUpdated||this._measureCard(),this._config&&this.hass&&(e.has("_config")||e.has("hass"))){if(!this._stateObj)return this._progressInterval&&(clearInterval(this._progressInterval),this._progressInterval=void 0),this._foregroundColor=void 0,void(this._backgroundColor=void 0);var r=e.get("hass"),i=(null==r||null===(t=r.states[this._config.entity])||void 0===t?void 0:t.attributes.entity_picture_local)||(null==r||null===(n=r.states[this._config.entity])||void 0===n?void 0:n.attributes.entity_picture);if(!this._image)return this._foregroundColor=void 0,void(this._backgroundColor=void 0);this._image!==i&&this._setColors()}}},{kind:"method",key:"updated",value:function(e){var t=this;if(this._config&&this.hass&&this._stateObj&&(e.has("_config")||e.has("hass"))){var n=this._stateObj,r=e.get("hass"),i=e.get("_config");r&&i&&r.themes===this.hass.themes&&i.theme===this._config.theme||(0,s.R)(this,this.hass.themes,this._config.theme),this._updateProgressBar(),!this._progressInterval&&this._showProgressBar&&"playing"===n.state?this._progressInterval=window.setInterval((function(){return t._updateProgressBar()}),1e3):!this._progressInterval||this._showProgressBar&&"playing"===n.state||(clearInterval(this._progressInterval),this._progressInterval=void 0)}}},{kind:"get",key:"_image",value:function(){if(this.hass&&this._config){var e=this._stateObj;if(e)return e.attributes.entity_picture_local||e.attributes.entity_picture}}},{kind:"get",key:"_showProgressBar",value:function(){if(!this.hass||!this._config||this._narrow)return!1;var e=this._stateObj;return!!e&&(("playing"===e.state||"paused"===e.state)&&"media_duration"in e.attributes&&"media_position"in e.attributes)}},{kind:"method",key:"_measureCard",value:function(){var e=this.shadowRoot.querySelector("ha-card");e&&(this._narrow=e.offsetWidth<350,this._veryNarrow=e.offsetWidth<300,this._cardHeight=e.offsetHeight)}},{kind:"method",key:"_attachObserver",value:(h=q(regeneratorRuntime.mark((function e(){var t,n=this;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this._resizeObserver){e.next=4;break}return e.next=3,(0,B.P)();case 3:this._resizeObserver=new ResizeObserver((0,P.D)((function(){return n._measureCard()}),250,!1));case 4:if(t=this.shadowRoot.querySelector("ha-card")){e.next=7;break}return e.abrupt("return");case 7:this._resizeObserver.observe(t);case 8:case"end":return e.stop()}}),e,this)}))),function(){return h.apply(this,arguments)})},{kind:"method",key:"_handleMoreInfo",value:function(){(0,c.B)(this,"hass-more-info",{entityId:this._config.entity})}},{kind:"method",key:"_handleBrowseMedia",value:function(){var e=this;(0,A.B)(this,{action:"play",entityId:this._config.entity,mediaPickedCallback:function(t){return e._playMedia(t.item.media_content_id,t.item.media_content_type)}})}},{kind:"method",key:"_playMedia",value:function(e,t){this.hass.callService("media_player","play_media",{entity_id:this._config.entity,media_content_id:e,media_content_type:t})}},{kind:"method",key:"_handleClick",value:function(e){(0,z.kr)(this.hass,this._stateObj,e.currentTarget.getAttribute("action"))}},{kind:"method",key:"_updateProgressBar",value:function(){var e;this._progressBar&&null!==(e=this._stateObj)&&void 0!==e&&e.attributes.media_duration&&(this._progressBar.progress=(0,z.rs)(this._stateObj)/this._stateObj.attributes.media_duration)}},{kind:"get",key:"_stateObj",value:function(){return this.hass.states[this._config.entity]}},{kind:"method",key:"_handleSeek",value:function(e){var t=this._stateObj;if((0,d.e)(t,z.xh)){var n=this._progressBar.offsetWidth,r=e.offsetX/n,i=this._stateObj.attributes.media_duration*r;this.hass.callService("media_player","media_seek",{entity_id:this._config.entity,seek_position:i})}}},{kind:"method",key:"_setColors",value:(u=q(regeneratorRuntime.mark((function e(){var t,n,r;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this._image){e.next=2;break}return e.abrupt("return");case 2:return e.prev=2,e.next=5,O(this.hass.hassUrl(this._image));case 5:t=e.sent,n=t.foreground,r=t.background,this._backgroundColor=r.hex,this._foregroundColor=n.hex,e.next=17;break;case 12:e.prev=12,e.t0=e.catch(2),console.error("Error getting Image Colors",e.t0),this._foregroundColor=void 0,this._backgroundColor=void 0;case 17:case"end":return e.stop()}}),e,this,[[2,12]])}))),function(){return u.apply(this,arguments)})},{kind:"method",key:"_marqueeMouseOver",value:function(){this._marqueeActive||(this._marqueeActive=!0)}},{kind:"method",key:"_marqueeMouseLeave",value:function(){this._marqueeActive&&(this._marqueeActive=!1)}},{kind:"get",static:!0,key:"styles",value:function(){return(0,r.iv)(E||(E=R(['\n      ha-card {\n        overflow: hidden;\n        height: 100%;\n      }\n\n      .background {\n        display: flex;\n        position: absolute;\n        top: 0;\n        left: 0;\n        height: 100%;\n        width: 100%;\n        transition: filter 0.8s;\n      }\n\n      .color-block {\n        background-color: var(--primary-color);\n        transition: background-color 0.8s;\n        width: 100%;\n      }\n\n      .color-gradient {\n        position: absolute;\n        background-image: linear-gradient(\n          to right,\n          var(--primary-color),\n          transparent\n        );\n        height: 100%;\n        right: 0;\n        opacity: 1;\n        transition: width 0.8s, opacity 0.8s linear 0.8s;\n      }\n\n      .image {\n        background-color: var(--primary-color);\n        background-position: center;\n        background-size: cover;\n        background-repeat: no-repeat;\n        position: absolute;\n        right: 0;\n        height: 100%;\n        opacity: 1;\n        transition: width 0.8s, background-image 0.8s, background-color 0.8s,\n          background-size 0.8s, opacity 0.8s linear 0.8s;\n      }\n\n      .no-image .image {\n        opacity: 0;\n      }\n\n      .no-img {\n        background-color: var(--primary-color);\n        background-size: initial;\n        background-repeat: no-repeat;\n        background-position: center center;\n        padding-bottom: 0;\n        position: absolute;\n        right: 0;\n        height: 100%;\n        background-image: url("/static/images/card_media_player_bg.png");\n        width: 50%;\n        transition: opacity 0.8s, background-color 0.8s;\n      }\n\n      .off .image,\n      .off .color-gradient {\n        opacity: 0;\n        transition: opacity 0s, width 0.8s;\n        width: 0;\n      }\n\n      .unavailable .no-img,\n      .background:not(.off):not(.no-image) .no-img {\n        opacity: 0;\n      }\n\n      .player {\n        position: relative;\n        padding: 16px;\n        height: 100%;\n        box-sizing: border-box;\n        display: flex;\n        flex-direction: column;\n        justify-content: space-between;\n        color: var(--text-primary-color);\n        transition-property: color, padding;\n        transition-duration: 0.4s;\n      }\n\n      .controls {\n        padding: 8px 8px 8px 0;\n        display: flex;\n        justify-content: flex-start;\n        align-items: center;\n        transition: padding, color;\n        transition-duration: 0.4s;\n        margin-left: -12px;\n      }\n\n      .controls > div {\n        display: flex;\n        align-items: center;\n      }\n\n      .controls ha-icon-button {\n        --mdc-icon-button-size: 44px;\n        --mdc-icon-size: 30px;\n      }\n\n      ha-icon-button[action="media_play"],\n      ha-icon-button[action="media_play_pause"],\n      ha-icon-button[action="media_pause"],\n      ha-icon-button[action="media_stop"],\n      ha-icon-button[action="turn_on"],\n      ha-icon-button[action="turn_off"] {\n        --mdc-icon-button-size: 56px;\n        --mdc-icon-size: 40px;\n      }\n\n      ha-icon-button.browse-media {\n        position: absolute;\n        right: 4px;\n        --mdc-icon-size: 24px;\n      }\n\n      .top-info {\n        display: flex;\n        justify-content: space-between;\n      }\n\n      .icon-name {\n        display: flex;\n        height: fit-content;\n        align-items: center;\n      }\n\n      .icon-name ha-state-icon {\n        padding-right: 8px;\n      }\n\n      .more-info {\n        position: absolute;\n        top: 4px;\n        right: 4px;\n      }\n\n      .media-info {\n        text-overflow: ellipsis;\n        white-space: nowrap;\n        overflow: hidden;\n      }\n\n      hui-marquee {\n        font-size: 1.2em;\n        margin: 0px 0 4px;\n      }\n\n      .title-controls {\n        padding-top: 16px;\n      }\n\n      mwc-linear-progress {\n        width: 100%;\n        margin-top: 4px;\n        --mdc-linear-progress-buffer-color: rgba(200, 200, 200, 0.5);\n      }\n\n      .no-image .controls {\n        padding: 0;\n      }\n\n      .off.background {\n        filter: grayscale(1);\n      }\n\n      .narrow .controls,\n      .no-progress .controls {\n        padding-bottom: 0;\n      }\n\n      .narrow ha-icon-button {\n        --mdc-icon-button-size: 40px;\n        --mdc-icon-size: 28px;\n      }\n\n      .narrow ha-icon-button[action="media_play"],\n      .narrow ha-icon-button[action="media_play_pause"],\n      .narrow ha-icon-button[action="media_pause"],\n      .narrow ha-icon-button[action="turn_on"] {\n        --mdc-icon-button-size: 50px;\n        --mdc-icon-size: 36px;\n      }\n\n      .narrow ha-icon-button.browse-media {\n        --mdc-icon-size: 24px;\n      }\n\n      .no-progress.player:not(.no-controls) {\n        padding-bottom: 0px;\n      }\n    '])))}}]}}),r.oi)}}]);