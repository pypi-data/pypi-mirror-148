"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[69225],{69810:(e,t,r)=>{r.d(t,{CP:()=>o,Lm:()=>s,NC:()=>a});var i=r(63864),n=r(41682);const o=async e=>(0,i.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/supervisor/info",method:"get"}):(0,n.rY)(await e.callApi("GET","hassio/supervisor/info")),s=async e=>(0,i.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/info",method:"get"}):(0,n.rY)(await e.callApi("GET","hassio/info")),a=async(e,t)=>e.callApi("GET",`hassio/${t}/logs`)},91135:(e,t,r)=>{r.r(t);var i=r(37500),n=r(33310),o=r(7323);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=p(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function a(e){var t,r=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=s();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var f=t((function(e){n.initializeInstanceElements(e,p.elements)}),r),p=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(d(o.descriptor)||d(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}l(o,n)}else t.push(o)}return t}(f.d.map(a)),e);n.initializeClassElements(f.F,p.elements),n.runClassFinishers(f.F,p.finishers)}([(0,n.Mo)("ha-logo-svg")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"render",value:function(){return i.YP`
      <svg version="1.1" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <rect fill="#41bdf5" width="200" height="200" ry="16.4"/>
        <path fill="#fff" d="m38.416 165.29v-53.456h-13.901a3.7332 3.7332 0 0 1-2.662-6.3504l74.804-76.084c1.8068-1.8376 4.7612-1.8628 6.5992-0.056l0.048 0.048 39.04 39.518v-7.3188a3.1112 3.1112 0 0 1 3.1112-3.1112h12.964a3.1112 3.1112 0 0 1 3.1116 3.1112v26.855l16.627 17.047a3.7332 3.7332 0 0 1-2.6728 6.34h-13.954v53.456a3.1112 3.1112 0 0 1-3.1112 3.1112h-116.89a3.1112 3.1112 0 0 1-3.1112-3.1112zm82.556-65.304a6.0116 6.0116 0 0 0 0.584-2.5944c0-3.3232-2.684-6.0172-5.9956-6.0172-3.3112 0-5.9956 2.694-5.9956 6.0172s2.6844 6.0176 5.996 6.0176c0.9256 0 1.802-0.2108 2.5848-0.5868l8.6072 8.6384v8.3672l-10.792 10.831v-7.936a6.0184 6.0184 0 0 0 3.9972-5.6748c0-3.3232-2.6844-6.0176-5.996-6.0176-3.3112 0-5.996 2.6944-5.996 6.0176 0 2.62 1.6688 4.8488 3.9976 5.6748v11.947l-9.9932 10.029v-58.912l8.2076-8.2368a5.9544 5.9544 0 0 0 2.5848 0.5864c3.3116 0 5.996-2.694 5.996-6.0176 0-3.3232-2.6844-6.0172-5.996-6.0172-3.3112 0-5.9956 2.694-5.9956 6.0172 0 0.9292 0.2096 1.8088 0.584 2.5944l-7.3792 7.406-7.3796-7.406a6.0116 6.0116 0 0 0 0.584-2.5944c0-3.3232-2.684-6.0172-5.9956-6.0172-3.3112 0-5.9956 2.694-5.9956 6.0172 0 3.3236 2.6844 6.0176 5.996 6.0176 0.9256 0 1.802-0.2108 2.5848-0.5864l8.2072 8.2368v42.064l-14.39-14.442v-11.546a6.0184 6.0184 0 0 0 3.9972-5.6748c0-3.3236-2.6844-6.0176-5.996-6.0176-3.3112 0-5.996 2.694-5.996 6.0176 0 2.62 1.6688 4.8488 3.9976 5.6748v7.5348l-11.192-11.232v-11.145a6.0184 6.0184 0 0 0 3.9972-5.6748c0-3.3232-2.6844-6.0176-5.996-6.0176-3.3112 0-5.996 2.6944-5.996 6.0176 0 2.62 1.6688 4.8488 3.9976 5.6748v12.807l12.363 12.407h-7.108c-0.8232-2.3372-3.044-4.0116-5.6548-4.0116-3.3112 0-5.996 2.694-5.996 6.0172 0 3.3236 2.6848 6.0176 5.996 6.0176 2.6108 0 4.832-1.6744 5.6548-4.012h11.105l17.216 17.278v30.03l-9.1932-9.2264v-11.546a6.0184 6.0184 0 0 0 3.9972-5.6748c0-3.3232-2.6844-6.0172-5.996-6.0172-3.3112 0-5.996 2.694-5.996 6.0172 0 2.62 1.6688 4.8488 3.9976 5.6748v7.5348l-13.376-13.423a6.0116 6.0116 0 0 0 0.5844-2.5944c0-3.3232-2.684-6.0172-5.996-6.0172-3.3112 0-5.9956 2.694-5.9956 6.0172s2.6844 6.0172 5.996 6.0172c0.9256 0 1.8024-0.2104 2.5848-0.5864l13.376 13.424h-7.108c-0.8232-2.3372-3.044-4.012-5.6548-4.012-3.3112 0-5.996 2.6944-5.996 6.0176s2.6848 6.0172 5.996 6.0172c2.6108 0 4.8316-1.6744 5.6548-4.0116h11.105l11.192 11.232h5.6528l11.592-11.633h10.705c0.8232 2.3368 3.044 4.0112 5.6548 4.0112 3.3112 0 5.996-2.694 5.996-6.0172s-2.6848-6.0172-5.996-6.0172c-2.6108 0-4.8316 1.6744-5.6548 4.0116h-12.361l-10.764 10.802v-13.18l12.82-12.866h20.698c0.8232 2.3372 3.044 4.0116 5.6544 4.0116 3.3116 0 5.996-2.694 5.996-6.0172 0-3.3236-2.6844-6.0176-5.996-6.0176-2.6104 0-4.8312 1.6744-5.6544 4.012h-16.702l11.963-12.006v-10.029l8.6068-8.6384a5.9544 5.9544 0 0 0 2.5852 0.5868c3.3112 0 5.996-2.6944 5.996-6.0176s-2.6848-6.0172-5.996-6.0172-5.996 2.694-5.996 6.0172c0 0.9292 0.21 1.8088 0.5844 2.5944l-5.7804 5.8016v-18.367a6.0184 6.0184 0 0 0 3.9972-5.6748c0-3.3236-2.6844-6.0176-5.996-6.0176-3.3112 0-5.996 2.694-5.996 6.0176 0 2.62 1.6688 4.8488 3.9976 5.6748v18.366l-5.7808-5.8016zm-51.78 57.58c-1.3244 0-2.3984-1.0776-2.3984-2.4068s1.074-2.4068 2.3984-2.4068c1.3248 0 2.3984 1.0776 2.3984 2.4068s-1.0736 2.4068-2.3984 2.4068zm17.588-18.052c-1.3248 0-2.3988-1.0776-2.3988-2.4068s1.074-2.4068 2.3984-2.4068c1.3248 0 2.3984 1.0776 2.3984 2.4068s-1.0736 2.4068-2.3984 2.4068zm-20.786-2.808c-1.3248 0-2.3984-1.0776-2.3984-2.4068s1.0736-2.4068 2.3984-2.4068c1.3244 0 2.3984 1.0776 2.3984 2.4068s-1.074 2.4068-2.3984 2.4068zm-1.9988-20.058c-1.3244 0-2.398-1.0776-2.398-2.4072 0-1.3292 1.0736-2.4068 2.398-2.4068 1.3248 0 2.3984 1.0776 2.3984 2.4068 0 1.3296-1.0736 2.4072-2.3984 2.4072zm49.964 2.808c-1.3244 0-2.398-1.0776-2.398-2.4068 0-1.3296 1.0736-2.4072 2.398-2.4072 1.3248 0 2.3984 1.0776 2.3984 2.4072 0 1.3292-1.0736 2.4068-2.3984 2.4068zm27.181 18.453c-1.324 0-2.398-1.0776-2.398-2.4068 0-1.3296 1.0736-2.4072 2.398-2.4072 1.3248 0 2.3984 1.0776 2.3984 2.4072 0 1.3292-1.0736 2.4068-2.3984 2.4068zm-10.392 19.255c-1.3248 0-2.3984-1.0776-2.3984-2.4068s1.0736-2.4068 2.3984-2.4068c1.3244 0 2.3984 1.0776 2.3984 2.4068s-1.074 2.4068-2.3984 2.4068zm11.192-57.364c-1.3244 0-2.3984-1.078-2.3984-2.4072s1.074-2.4068 2.3984-2.4068 2.3984 1.0776 2.3984 2.4068-1.074 2.4072-2.3984 2.4072zm-13.191-15.645c-1.3244 0-2.3984-1.0776-2.3984-2.4068 0-1.3296 1.074-2.4072 2.3984-2.4072 1.3248 0 2.3984 1.0776 2.3984 2.4072 0 1.3292-1.0736 2.4068-2.3984 2.4068zm-15.989-9.628c-1.3244 0-2.398-1.0772-2.398-2.4068 0-1.3292 1.0736-2.4068 2.398-2.4068 1.3248 0 2.3984 1.0776 2.3984 2.4068 0 1.3296-1.0736 2.4072-2.3984 2.4072zm-25.582 0c-1.324 0-2.398-1.0772-2.398-2.4068 0-1.3292 1.0736-2.4068 2.398-2.4068 1.3248 0 2.3984 1.0776 2.3984 2.4068 0 1.3296-1.0736 2.4072-2.3984 2.4072zm-20.785 9.2268c-1.3244 0-2.3984-1.0776-2.3984-2.4068 0-1.3296 1.074-2.4072 2.3984-2.4072s2.3984 1.0776 2.3984 2.4072c0 1.3292-1.074 2.4068-2.3984 2.4068zm15.189 14.843c-1.3244 0-2.398-1.0776-2.398-2.4068 0-1.3296 1.0736-2.4072 2.398-2.4072 1.3248 0 2.3984 1.0776 2.3984 2.4072 0 1.3292-1.0736 2.4068-2.3984 2.4068zm33.976 1.2036c-1.324 0-2.398-1.078-2.398-2.4072s1.0736-2.4068 2.398-2.4068c1.3248 0 2.3984 1.0776 2.3984 2.4068s-1.0736 2.4072-2.3984 2.4072z"/>
      </svg>`}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        display: var(--ha-icon-display, inline-flex);
        align-items: center;
        justify-content: center;
        position: relative;
        vertical-align: middle;
        fill: currentcolor;
        width: var(--mdc-icon-size, 24px);
        height: var(--mdc-icon-size, 24px);
      }
      svg {
        width: 100%;
        height: 100%;
        pointer-events: none;
        display: block;
      }
    `}}]}}),i.oi);var u=r(35460),m=r(69810),v=(r(60010),r(11654)),y=r(27322),g=r(14516),b=(r(22098),r(5986)),w=r(11254);function k(){k=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!z(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return x(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?x(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=S(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:A(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=A(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function E(e){var t,r=S(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function P(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function z(e){return e.decorators&&e.decorators.length}function _(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function A(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function S(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function x(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function $(e,t,r){return $="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=C(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}},$(e,t,r||e)}function C(e){return C=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},C(e)}!function(e,t,r,i){var n=k();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(_(o.descriptor)||_(n.descriptor)){if(z(o)||z(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(z(o)){if(z(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}P(o,n)}else t.push(o)}return t}(s.d.map(E)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("integrations-card")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,n.SB)()],key:"_manifests",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_setups",value:void 0},{kind:"field",key:"_sortedIntegrations",value:()=>(0,g.Z)((e=>Array.from(new Set(e.map((e=>e.includes(".")?e.split(".")[1]:e)))).sort()))},{kind:"method",key:"firstUpdated",value:function(e){$(C(r.prototype),"firstUpdated",this).call(this,e),this._fetchManifests(),this._fetchSetups()}},{kind:"method",key:"render",value:function(){return i.dy`
      <ha-card
        .header=${this.hass.localize("ui.panel.config.info.integrations")}
      >
        <table class="card-content">
          <thead>
            <tr>
              <th></th>
              ${this.narrow?"":i.dy`<th></th>
                    <th></th>
                    <th></th>`}
              <th>${this.hass.localize("ui.panel.config.info.setup_time")}</th>
            </tr>
          </thead>
          <tbody>
            ${this._sortedIntegrations(this.hass.config.components).map((e=>{var t,r,n,o;const s=this._manifests&&this._manifests[e],a=s?i.dy`<a
                      href=${s.is_built_in?(0,y.R)(this.hass,`/integrations/${s.domain}`):s.documentation}
                      target="_blank"
                      rel="noreferrer"
                      >${this.hass.localize("ui.panel.config.info.documentation")}</a
                    >`:"",l=s&&(s.is_built_in||s.issue_tracker)?i.dy`
                        <a
                          href=${(0,b.H0)(e,s)}
                          target="_blank"
                          rel="noreferrer"
                          >${this.hass.localize("ui.panel.config.info.issues")}</a
                        >
                      `:"",c=null===(t=this._setups)||void 0===t||null===(r=t[e])||void 0===r||null===(n=r.seconds)||void 0===n?void 0:n.toFixed(2);return i.dy`
                  <tr>
                    <td>
                      <img
                        loading="lazy"
                        src=${(0,w.X)({domain:e,type:"icon",useFallback:!0,darkOptimized:null===(o=this.hass.themes)||void 0===o?void 0:o.darkMode})}
                        referrerpolicy="no-referrer"
                      />
                    </td>
                    <td class="name">
                      ${(0,b.Lh)(this.hass.localize,e,s)}<br />
                      <span class="domain">${e}</span>
                      ${this.narrow?i.dy`<div class="mobile-row">
                            <div>${a} ${l}</div>
                            ${c?i.dy`${c} s`:""}
                          </div>`:""}
                    </td>
                    ${this.narrow?"":i.dy`
                          <td>${a}</td>
                          <td>${l}</td>
                          <td class="setup">
                            ${c?i.dy`${c} s`:""}
                          </td>
                        `}
                  </tr>
                `}))}
          </tbody>
        </table>
      </ha-card>
    `}},{kind:"method",key:"_fetchManifests",value:async function(){const e={};for(const t of await(0,b.F3)(this.hass))e[t.domain]=t;this._manifests=e}},{kind:"method",key:"_fetchSetups",value:async function(){const e={};for(const t of await(0,b.Mt)(this.hass))e[t.domain]=t;this._setups=e}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      table {
        width: 100%;
      }
      td,
      th {
        padding: 0 8px;
      }
      td:first-child {
        padding-left: 0;
      }
      td.name {
        padding: 8px;
      }
      td.setup {
        text-align: right;
        white-space: nowrap;
        direction: ltr;
      }
      th {
        text-align: right;
      }
      .domain {
        color: var(--secondary-text-color);
      }
      .mobile-row {
        display: flex;
        justify-content: space-between;
      }
      .mobile-row a:not(:last-of-type) {
        margin-right: 4px;
      }
      img {
        display: block;
        max-height: 40px;
        max-width: 40px;
      }
      a {
        color: var(--primary-color);
      }
    `}}]}}),i.oi);function D(){D=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!I(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return M(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?M(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=R(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:F(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=F(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function T(e){var t,r=R(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function O(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function I(e){return e.decorators&&e.decorators.length}function j(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function F(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function R(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function M(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function U(e,t,r){return U="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=B(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}},U(e,t,r||e)}function B(e){return B=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},B(e)}let L=function(e,t,r,i){var n=D();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(j(o.descriptor)||j(n.descriptor)){if(I(o)||I(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(I(o)){if(I(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}O(o,n)}else t.push(o)}return t}(s.d.map(T)),e);return n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}(null,(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"showAdvanced",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_hostInfo",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_osInfo",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_hassioInfo",value:void 0},{kind:"method",key:"render",value:function(){const e=this.hass,t=window.CUSTOM_UI_LIST||[];return i.dy`
      <hass-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        back-path="/config"
        .header=${this.hass.localize("ui.panel.config.info.caption")}
      >
        <div class="about">
          <a
            href=${(0,y.R)(this.hass,"")}
            target="_blank"
            rel="noreferrer"
          >
            <ha-logo-svg
              title=${this.hass.localize("ui.panel.config.info.home_assistant_logo")}
            >
            </ha-logo-svg>
          </a>
          <br />
          <h2>Home Assistant Core ${e.connection.haVersion}</h2>
          ${this._hassioInfo?i.dy`<h2>
                Home Assistant Supervisor ${this._hassioInfo.supervisor}
              </h2>`:""}
          ${this._osInfo?i.dy`<h2>Home Assistant OS ${this._osInfo.version}</h2>`:""}
          ${this._hostInfo?i.dy`<h4>Kernel version ${this._hostInfo.kernel}</h4>
                <h4>Agent version ${this._hostInfo.agent_version}</h4>`:""}
          <p>
            ${this.hass.localize("ui.panel.config.info.path_configuration","path",e.config.config_dir)}
          </p>
          <p class="develop">
            <a
              href=${(0,y.R)(this.hass,"/developers/credits/")}
              target="_blank"
              rel="noreferrer"
            >
              ${this.hass.localize("ui.panel.config.info.developed_by")}
            </a>
          </p>
          <p>
            ${this.hass.localize("ui.panel.config.info.license")}<br />
            ${this.hass.localize("ui.panel.config.info.source")}
            <a
              href="https://github.com/home-assistant/core"
              target="_blank"
              rel="noreferrer"
              >${this.hass.localize("ui.panel.config.info.server")}</a
            >
            &mdash;
            <a
              href="https://github.com/home-assistant/frontend"
              target="_blank"
              rel="noreferrer"
              >${this.hass.localize("ui.panel.config.info.frontend")}</a
            >
          </p>
          <p>
            ${this.hass.localize("ui.panel.config.info.built_using")}
            <a href="https://www.python.org" target="_blank" rel="noreferrer"
              >Python 3</a
            >,
            <a href="https://lit.dev" target="_blank" rel="noreferrer">Lit</a>,
            ${this.hass.localize("ui.panel.config.info.icons_by")}
            <a
              href="https://fonts.google.com/icons?selected=Material+Icons"
              target="_blank"
              rel="noreferrer"
              >Google</a
            >
            ${this.hass.localize("ui.common.and")}
            <a
              href="https://materialdesignicons.com/"
              target="_blank"
              rel="noreferrer"
              >Material Design Icons</a
            >.
          </p>
          <p>
            ${this.hass.localize("ui.panel.config.info.frontend_version","version","20220425.0","type","latest")}
            ${t.length>0?i.dy`
                  <div>
                    ${this.hass.localize("ui.panel.config.info.custom_uis")}
                    ${t.map((e=>i.dy`
                        <div>
                          <a href=${e.url} target="_blank"> ${e.name}</a>:
                          ${e.version}
                        </div>
                      `))}
                  </div>
                `:""}
          </p>
        </div>
        <div>
          <integrations-card
            .hass=${this.hass}
            .narrow=${this.narrow}
          ></integrations-card>
        </div>
      </hass-subpage>
    `}},{kind:"method",key:"firstUpdated",value:function(e){U(B(r.prototype),"firstUpdated",this).call(this,e);const t=(window.CUSTOM_UI_LIST||[]).length;setTimeout((()=>{(window.CUSTOM_UI_LIST||[]).length!==t.length&&this.requestUpdate()}),1e3),(0,o.p)(this.hass,"hassio")&&this._loadSupervisorInfo()}},{kind:"method",key:"_loadSupervisorInfo",value:async function(){const[e,t,r]=await Promise.all([(0,u.Sj)(this.hass),(0,u.AP)(this.hass),(0,m.Lm)(this.hass)]);this._hassioInfo=r,this._osInfo=t,this._hostInfo=e}},{kind:"get",static:!0,key:"styles",value:function(){return[v.Qx,i.iv`
        :host {
          -ms-user-select: initial;
          -webkit-user-select: initial;
          -moz-user-select: initial;
        }

        .about {
          text-align: center;
          line-height: 2em;
        }

        .version {
          @apply --paper-font-headline;
        }

        .develop {
          @apply --paper-font-subhead;
        }

        .about a {
          color: var(--primary-color);
        }

        integrations-card {
          display: block;
          max-width: 600px;
          margin: 0 auto;
          padding-bottom: 16px;
        }
        ha-logo-svg {
          padding: 12px;
          height: 180px;
          width: 180px;
        }
      `]}}]}}),i.oi);customElements.define("ha-config-info",L)},11254:(e,t,r)=>{r.d(t,{X:()=>i,u:()=>n});const i=e=>`https://brands.home-assistant.io/${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,n=e=>e.split("/")[4]},27322:(e,t,r)=>{r.d(t,{R:()=>i});const i=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}}]);
//# sourceMappingURL=75ddfc19.js.map