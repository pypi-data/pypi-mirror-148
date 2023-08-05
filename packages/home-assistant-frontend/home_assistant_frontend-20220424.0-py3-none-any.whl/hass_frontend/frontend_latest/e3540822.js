"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[43283],{43283:(e,t,r)=>{r.r(t),r.d(t,{severityMap:()=>x});var i=r(37500),n=r(33310),o=r(70483),s=r(62877),a=r(47181),l=r(91741),c=r(84627),d=(r(22098),r(49915),r(56007)),u=r(15688),f=r(53658),h=r(75502);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!v(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=w(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:k(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=k(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function m(e){var t,r=w(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function y(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function v(e){return e.decorators&&e.decorators.length}function g(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function k(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function w(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function E(e,t,r){return E="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=_(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}},E(e,t,r||e)}function _(e){return _=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},_(e)}const x={red:"var(--error-color)",green:"var(--success-color)",yellow:"var(--warning-color)",normal:"var(--info-color)"};!function(e,t,r,i){var n=p();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(g(o.descriptor)||g(n.descriptor)){if(v(o)||v(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(v(o)){if(v(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}y(o,n)}else t.push(o)}return t}(s.d.map(m)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("hui-gauge-card")],(function(e,t){class p extends t{constructor(...t){super(...t),e(this)}}return{F:p,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([r.e(29563),r.e(98985),r.e(24103),r.e(41985),r.e(88278),r.e(59799),r.e(6294),r.e(45507),r.e(41922),r.e(12545),r.e(13701),r.e(35545)]).then(r.bind(r,97345)),document.createElement("hui-gauge-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(e,t,r){return{type:"gauge",entity:(0,u.j)(e,1,t,r,["counter","input_number","number","sensor"],(e=>!isNaN(Number(e.state))))[0]||""}}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_config",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 4}},{kind:"method",key:"setConfig",value:function(e){if(!e.entity)throw new Error("Entity must be specified");if(!(0,c.T)(e.entity))throw new Error("Invalid entity");this._config={min:0,max:100,...e}}},{kind:"method",key:"render",value:function(){var e,t;if(!this._config||!this.hass)return i.dy``;const r=this.hass.states[this._config.entity];if(!r)return i.dy`
        <hui-warning>
          ${(0,h.i)(this.hass,this._config.entity)}
        </hui-warning>
      `;const n=Number(r.state);if(r.state===d.nZ)return i.dy`
        <hui-warning
          >${this.hass.localize("ui.panel.lovelace.warning.entity_unavailable","entity",this._config.entity)}</hui-warning
        >
      `;if(isNaN(n))return i.dy`
        <hui-warning
          >${this.hass.localize("ui.panel.lovelace.warning.entity_non_numeric","entity",this._config.entity)}</hui-warning
        >
      `;const s=null!==(e=this._config.name)&&void 0!==e?e:(0,l.C)(r);return i.dy`
      <ha-card @click=${this._handleClick} tabindex="0">
        <ha-gauge
          .min=${this._config.min}
          .max=${this._config.max}
          .value=${r.state}
          .locale=${this.hass.locale}
          .label=${this._config.unit||(null===(t=this.hass)||void 0===t?void 0:t.states[this._config.entity].attributes.unit_of_measurement)||""}
          style=${(0,o.V)({"--gauge-color":this._computeSeverity(n)})}
          .needle=${this._config.needle}
          .levels=${this._config.needle?this._severityLevels():void 0}
        ></ha-gauge>
        <div class="name" .title=${s}>${s}</div>
      </ha-card>
    `}},{kind:"method",key:"shouldUpdate",value:function(e){return(0,f.G)(this,e)}},{kind:"method",key:"updated",value:function(e){if(E(_(p.prototype),"updated",this).call(this,e),!this._config||!this.hass)return;const t=e.get("hass"),r=e.get("_config");t&&r&&t.themes===this.hass.themes&&r.theme===this._config.theme||(0,s.R)(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"_computeSeverity",value:function(e){if(this._config.needle)return;const t=this._config.severity;if(!t)return x.normal;const r=Object.keys(t).map((e=>[e,t[e]]));for(const e of r)if(null==x[e[0]]||isNaN(e[1]))return x.normal;return r.sort(((e,t)=>e[1]-t[1])),e>=r[0][1]&&e<r[1][1]?x[r[0][0]]:e>=r[1][1]&&e<r[2][1]?x[r[1][0]]:e>=r[2][1]?x[r[2][0]]:x.normal}},{kind:"method",key:"_severityLevels",value:function(){const e=this._config.severity;if(!e)return[{level:0,stroke:x.normal}];return Object.keys(e).map((t=>({level:e[t],stroke:x[t]})))}},{kind:"method",key:"_handleClick",value:function(){(0,a.B)(this,"hass-more-info",{entityId:this._config.entity})}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      ha-card {
        cursor: pointer;
        height: 100%;
        overflow: hidden;
        padding: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        box-sizing: border-box;
      }

      ha-card:focus {
        outline: none;
        background: var(--divider-color);
      }

      ha-gauge {
        width: 100%;
        max-width: 250px;
      }

      .name {
        text-align: center;
        line-height: initial;
        color: var(--primary-text-color);
        width: 100%;
        font-size: 15px;
        margin-top: 8px;
      }
    `}}]}}),i.oi)}}]);
//# sourceMappingURL=e3540822.js.map