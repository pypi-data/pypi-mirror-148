"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[38026],{8330:(e,t,r)=>{r.d(t,{P:()=>i});const i=(e,t,r=!0,i=!0)=>{let n,o=0;return(...s)=>{const a=()=>{o=!1===r?0:Date.now(),n=void 0,e(...s)},c=Date.now();o||!1!==r||(o=c);const l=t-(c-o);l<=0||l>t?(n&&(clearTimeout(n),n=void 0),o=c,e(...s)):n||!1===i||(n=window.setTimeout(a,l))}}},99990:(e,t,r)=>{r.a(e,(async e=>{r.d(t,{W:()=>s});var i=r(58763),n=e([i]);i=(n.then?await n:n)[0];const o={};const s=(e,t,r,n,s)=>{const l=r.cacheKey,h=new Date,f=new Date(h);f.setHours(f.getHours()-r.hoursToShow);let u=f,p=!1,m=o[l+`_${r.hoursToShow}`];if(m&&u>=m.startTime&&u<=m.endTime&&m.language===s){if(u=m.endTime,p=!0,h<=m.endTime)return m.prom}else m=o[l]=function(e,t,r){return{prom:Promise.resolve({line:[],timeline:[]}),language:e,startTime:t,endTime:r,data:{line:[],timeline:[]}}}(s,f,h);const y=m.prom,v=!(0,i.iq)(e,t);return m.prom=(async()=>{let r;try{r=(await Promise.all([y,(0,i.vq)(e,t,u,h,p,void 0,!0,v)]))[1]}catch(e){throw delete o[l],e}const s=(0,i.Nu)(e,r,n);return p?(a(s.line,m.data.line),c(s.timeline,m.data.timeline),d(f,m.data)):m.data=s,m.data})(),m.startTime=f,m.endTime=h,m.prom},a=(e,t)=>{e.forEach((e=>{const r=e.unit,i=t.find((e=>e.unit===r));i?e.data.forEach((e=>{const t=i.data.find((t=>e.entity_id===t.entity_id));t?t.states=t.states.concat(e.states):i.data.push(e)})):t.push(e)}))},c=(e,t)=>{e.forEach((e=>{const r=t.find((t=>t.entity_id===e.entity_id));r?r.data=r.data.concat(e.data):t.push(e)}))},l=(e,t)=>{if(0===t.length)return t;const r=t.findIndex((t=>new Date(t.last_changed)>e));if(0===r)return t;const i=-1===r?t.length-1:r-1;return t[i].last_changed=e,t.slice(i)},d=(e,t)=>{t.line.forEach((t=>{t.data.forEach((t=>{t.states=l(e,t.states)}))})),t.timeline.forEach((t=>{t.data=l(e,t.data)}))}}))},38026:(e,t,r)=>{r.a(e,(async e=>{r.r(t),r.d(t,{HuiHistoryGraphCard:()=>E});var i=r(37500),n=r(33310),o=r(8636),s=r(8330),a=(r(22098),r(77243)),c=r(99990),l=r(53658),d=r(90271),h=e([c,a]);function f(){f=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!m(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return k(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?k(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=g(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:v(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=v(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function u(e){var t,r=g(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function g(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function k(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function w(e,t,r){return w="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=_(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}},w(e,t,r||e)}function _(e){return _=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},_(e)}[c,a]=h.then?await h:h;let E=function(e,t,r,i){var n=f();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(y(o.descriptor)||y(n.descriptor)){if(m(o)||m(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(m(o)){if(m(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}p(o,n)}else t.push(o)}return t}(s.d.map(u)),e);return n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("hui-history-graph-card")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([r.e(29563),r.e(98985),r.e(24103),r.e(41985),r.e(88278),r.e(59799),r.e(6294),r.e(45507),r.e(5906),r.e(57316),r.e(12545),r.e(13701),r.e(77576),r.e(74535),r.e(16381),r.e(1528),r.e(40714)]).then(r.bind(r,52524)),document.createElement("hui-history-graph-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(){return{type:"history-graph",entities:["sun.sun"]}}},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_stateHistory",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_config",value:void 0},{kind:"field",key:"_configEntities",value:void 0},{kind:"field",key:"_names",value:()=>({})},{kind:"field",key:"_cacheConfig",value:void 0},{kind:"field",key:"_fetching",value:()=>!1},{kind:"field",key:"_throttleGetStateHistory",value:void 0},{kind:"method",key:"getCardSize",value:function(){var e,t;return null!==(e=this._config)&&void 0!==e&&e.title?2:0+2*((null===(t=this._configEntities)||void 0===t?void 0:t.length)||1)}},{kind:"method",key:"setConfig",value:function(e){if(!e.entities||!Array.isArray(e.entities))throw new Error("Entities need to be an array");if(!e.entities.length)throw new Error("You must include at least one entity");this._configEntities=e.entities?(0,d.A)(e.entities):[];const t=[];this._configEntities.forEach((e=>{t.push(e.entity),e.name&&(this._names[e.entity]=e.name)})),this._throttleGetStateHistory=(0,s.P)((()=>{this._getStateHistory()}),e.refresh_interval||1e4),this._cacheConfig={cacheKey:t.join(),hoursToShow:e.hours_to_show||24},this._config=e}},{kind:"method",key:"shouldUpdate",value:function(e){return!!e.has("_stateHistory")||(0,l.W)(this,e)}},{kind:"method",key:"updated",value:function(e){if(w(_(a.prototype),"updated",this).call(this,e),!(this._config&&this.hass&&this._throttleGetStateHistory&&this._cacheConfig))return;if(!e.has("_config")&&!e.has("hass"))return;const t=e.get("_config");!e.has("_config")||(null==t?void 0:t.entities)===this._config.entities&&(null==t?void 0:t.hours_to_show)===this._config.hours_to_show?e.has("hass")&&setTimeout(this._throttleGetStateHistory,1e3):this._throttleGetStateHistory()}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?i.dy`
      <ha-card .header=${this._config.title}>
        <div
          class="content ${(0,o.$)({"has-header":!!this._config.title})}"
        >
          <state-history-charts
            .hass=${this.hass}
            .isLoadingData=${!this._stateHistory}
            .historyData=${this._stateHistory}
            .names=${this._names}
            up-to-now
            no-single
          ></state-history-charts>
        </div>
      </ha-card>
    `:i.dy``}},{kind:"method",key:"_getStateHistory",value:async function(){if(!this._fetching){this._fetching=!0;try{this._stateHistory={...await(0,c.W)(this.hass,this._cacheConfig.cacheKey,this._cacheConfig,this.hass.localize,this.hass.language)}}finally{this._fetching=!1}}}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      ha-card {
        height: 100%;
      }
      .content {
        padding: 16px;
      }
      .has-header {
        padding-top: 0;
      }
    `}}]}}),i.oi)}))}}]);
//# sourceMappingURL=ae190874.js.map