"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6050],{27269:function(e,t,r){r.d(t,{p:function(){return n}});var n=function(e){return e.substr(e.indexOf(".")+1)}},91741:function(e,t,r){r.d(t,{C:function(){return i}});var n=r(27269),i=function(e){return void 0===e.attributes.friendly_name?(0,n.p)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||""}},45485:function(e,t,r){r.d(t,{E:function(){return i},h:function(){return o}});var n=r(58831),i=function(e){return e.include_domains.length+e.include_entities.length+e.exclude_domains.length+e.exclude_entities.length===0},o=function(e,t,r,i){var o=new Set(e),s=new Set(t),a=new Set(r),c=new Set(i),u=o.size>0||s.size>0,l=a.size>0||c.size>0;return u||l?u&&!l?function(e){return s.has(e)||o.has((0,n.M)(e))}:!u&&l?function(e){return!c.has(e)&&!a.has((0,n.M)(e))}:o.size?function(e){return o.has((0,n.M)(e))?!c.has(e):s.has(e)}:a.size?function(e){return a.has((0,n.M)(e))?s.has(e):!c.has(e)}:function(e){return s.has(e)}:function(){return!0}}},21780:function(e,t,r){r.d(t,{f:function(){return n}});var n=function(e){return e.charAt(0).toUpperCase()+e.slice(1)}},83927:function(e,t,r){var n,i=r(92685),o=r(92038),s=r(37500),a=r(33310),c=r(47181);function u(e){return u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},u(e)}function l(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function f(e,t){return f=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e},f(e,t)}function d(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=y(e);if(t){var i=y(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return p(this,r)}}function p(e,t){if(t&&("object"===u(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return h(e)}function h(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function y(e){return y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},y(e)}function m(){m=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!g(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var u=c.extras;if(u){for(var l=0;l<u.length;l++)this.addElementPlacement(u[l],t);r.push.apply(r,u)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=E(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:k(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=k(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function v(e){var t,r=E(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function b(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function g(e){return e.decorators&&e.decorators.length}function w(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function k(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function E(e){var t=function(e,t){if("object"!==u(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==u(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===u(t)?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}!function(e,t,r,n){var i=m();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var s=t((function(e){i.initializeInstanceElements(e,a.elements)}),r),a=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(w(o.descriptor)||w(i.descriptor)){if(g(o)||g(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(g(o)){if(g(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}b(o,i)}else t.push(o)}return t}(s.d.map(v)),e);i.initializeClassElements(s.F,a.elements),i.runClassFinishers(s.F,a.finishers)}([(0,a.Mo)("ha-formfield")],(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&f(e,t)}(n,t);var r=d(n);function n(){var t;l(this,n);for(var i=arguments.length,o=new Array(i),s=0;s<i;s++)o[s]=arguments[s];return t=r.call.apply(r,[this].concat(o)),e(h(t)),t}return n}(t);return{F:r,d:[{kind:"method",key:"_labelClick",value:function(){var e=this.input;if(e)switch(e.focus(),e.tagName){case"HA-CHECKBOX":case"HA-RADIO":e.checked=!e.checked,(0,c.B)(e,"change");break;default:e.click()}}},{kind:"field",static:!0,key:"styles",value:function(){return[o.W,(0,s.iv)(n||(e=['\n      :host(:not([alignEnd])) ::slotted(ha-switch) {\n        margin-right: 10px;\n      }\n      :host([dir="rtl"]:not([alignEnd])) ::slotted(ha-switch) {\n        margin-left: 10px;\n        margin-right: auto;\n      }\n    '],t||(t=e.slice(0)),n=Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))))];var e,t}}]}}),i.a)},74186:function(e,t,r){r.d(t,{eD:function(){return a},Mw:function(){return c},vA:function(){return u},L3:function(){return l},Nv:function(){return f},z3:function(){return d},hg:function(){return p},LM:function(){return y},_V:function(){return m}});var n=r(97330),i=r(91741),o=r(85415),s=r(38346),a=function(e,t){return t.find((function(t){return e.states[t.entity_id]&&"battery"===e.states[t.entity_id].attributes.device_class}))},c=function(e,t){return t.find((function(t){return e.states[t.entity_id]&&"battery_charging"===e.states[t.entity_id].attributes.device_class}))},u=function(e,t){if(t.name)return t.name;var r=e.states[t.entity_id];return r?(0,i.C)(r):t.entity_id},l=function(e,t){return e.callWS({type:"config/entity_registry/get",entity_id:t})},f=function(e,t,r){return e.callWS(Object.assign({type:"config/entity_registry/update",entity_id:t},r))},d=function(e,t){return e.callWS({type:"config/entity_registry/remove",entity_id:t})},p=function(e){return e.sendMessagePromise({type:"config/entity_registry/list"})},h=function(e,t){return e.subscribeEvents((0,s.D)((function(){return p(e).then((function(e){return t.setState(e,!0)}))}),500,!0),"entity_registry_updated")},y=function(e,t){return(0,n.B)("_entityRegistry",p,h,e,t)},m=function(e){return e.sort((function(e,t){return(0,o.f)(e.name||"",t.name||"")}))}},24833:function(e,t,r){r.d(t,{oF:function(){return o},kK:function(){return s},k6:function(){return a},zG:function(){return c},BD:function(){return u},hF:function(){return l},Sk:function(){return f},UJ:function(){return d}});var n=r(49706),i=r(40095),o=1,s=2,a=4,c=8,u=16,l=function(e){return e.state===n.uo&&(0,i.e)(e,o)},f=function(e){return function(e){return(0,i.e)(e,a)&&"number"==typeof e.attributes.in_progress}(e)||!!e.attributes.in_progress},d=function(e,t){return e.callWS({type:"update/release_notes",entity_id:t})}},90363:function(e,t,r){r.d(t,{_:function(){return o}});var n=r(47181),i=function(){return Promise.all([r.e(5084),r.e(4821),r.e(8931)]).then(r.bind(r,98931))},o=function(e,t){(0,n.B)(e,"show-dialog",{dialogTag:"dialog-domain-toggler",dialogImport:i,dialogParams:t})}}}]);