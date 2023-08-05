/*! For license information please see dd8fdb05.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[8663],{28663:function(t,e,i){function s(t,e){for(var i=0;i<e.length;i++){var s=e[i];s.enumerable=s.enumerable||!1,s.configurable=!0,"value"in s&&(s.writable=!0),Object.defineProperty(t,s.key,s)}}i.r(e),i.d(e,{FlowLayout:function(){return O},flow:function(){return R}});var r,n,o=function(){function t(e){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),this._map=new Map,this._roundAverageSize=!0,this.totalSize=0,!1===(null==e?void 0:e.roundAverageSize)&&(this._roundAverageSize=!1)}var e,i,r;return e=t,(i=[{key:"set",value:function(t,e){var i=this._map.get(t)||0;this._map.set(t,e),this.totalSize+=e-i}},{key:"averageSize",get:function(){if(this._map.size>0){var t=this.totalSize/this._map.size;return this._roundAverageSize?Math.round(t):t}return 0}},{key:"getSize",value:function(t){return this._map.get(t)}},{key:"clear",value:function(){this._map.clear(),this.totalSize=0}}])&&s(e.prototype,i),r&&s(e,r),t}();function a(t,e,i,s,r,n,o){try{var a=t[n](o),h=a.value}catch(c){return void i(c)}a.done?e(h):Promise.resolve(h).then(s,r)}function h(t){return function(){var e=this,i=arguments;return new Promise((function(s,r){var n=t.apply(e,i);function o(t){a(n,s,r,o,h,"next",t)}function h(t){a(n,s,r,o,h,"throw",t)}o(void 0)}))}}function c(){return(c=h(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.abrupt("return",n||l());case 1:case"end":return t.stop()}}),t)})))).apply(this,arguments)}function l(){return u.apply(this,arguments)}function u(){return(u=h(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:r=window.EventTarget,t.prev=1,new r,t.next=10;break;case 5:return t.prev=5,t.t0=t.catch(1),t.next=9,i.e(8251).then(i.t.bind(i,98251,19));case 9:r=t.sent.default.EventTarget;case 10:return t.abrupt("return",n=r);case 11:case"end":return t.stop()}}),t,null,[[1,5]])})))).apply(this,arguments)}function _(t,e,i){return e in t?Object.defineProperty(t,e,{value:i,enumerable:!0,configurable:!0,writable:!0}):t[e]=i,t}function f(t,e,i,s,r,n,o){try{var a=t[n](o),h=a.value}catch(c){return void i(c)}a.done?e(h):Promise.resolve(h).then(s,r)}function v(t){return function(){var e=this,i=arguments;return new Promise((function(s,r){var n=t.apply(e,i);function o(t){f(n,s,r,o,a,"next",t)}function a(t){f(n,s,r,o,a,"throw",t)}o(void 0)}))}}function m(t,e){for(var i=0;i<e.length;i++){var s=e[i];s.enumerable=s.enumerable||!1,s.configurable=!0,"value"in s&&(s.writable=!0),Object.defineProperty(t,s.key,s)}}var d=function(){function t(e){var i=this;!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),this._latestCoords={left:0,top:0},this._direction=null,this._viewportSize={width:0,height:0},this._pendingReflow=!1,this._pendingLayoutUpdate=!1,this._scrollToIndex=-1,this._scrollToAnchor=0,this._firstVisible=0,this._lastVisible=0,this._eventTargetPromise=function(){return c.apply(this,arguments)}().then((function(t){i._eventTarget=new t})),this._physicalMin=0,this._physicalMax=0,this._first=-1,this._last=-1,this._sizeDim="height",this._secondarySizeDim="width",this._positionDim="top",this._secondaryPositionDim="left",this._scrollPosition=0,this._scrollError=0,this._totalItems=0,this._scrollSize=1,this._overhang=1e3,this._eventTarget=null,Promise.resolve().then((function(){return i.config=e||i._defaultConfig}))}var e,i,s,r,n,o;return e=t,i=[{key:"_defaultConfig",get:function(){return{direction:"vertical"}}},{key:"config",get:function(){return{direction:this.direction}},set:function(t){Object.assign(this,Object.assign({},this._defaultConfig,t))}},{key:"totalItems",get:function(){return this._totalItems},set:function(t){var e=Number(t);e!==this._totalItems&&(this._totalItems=e,this._scheduleReflow())}},{key:"direction",get:function(){return this._direction},set:function(t){(t="horizontal"===t?t:"vertical")!==this._direction&&(this._direction=t,this._sizeDim="horizontal"===t?"width":"height",this._secondarySizeDim="horizontal"===t?"height":"width",this._positionDim="horizontal"===t?"left":"top",this._secondaryPositionDim="horizontal"===t?"top":"left",this._triggerReflow())}},{key:"viewportSize",get:function(){return this._viewportSize},set:function(t){var e=this._viewDim1,i=this._viewDim2;Object.assign(this._viewportSize,t),i!==this._viewDim2?this._scheduleLayoutUpdate():e!==this._viewDim1&&this._checkThresholds()}},{key:"viewportScroll",get:function(){return this._latestCoords},set:function(t){Object.assign(this._latestCoords,t);var e=this._scrollPosition;this._scrollPosition=this._latestCoords[this._positionDim],e!==this._scrollPosition&&(this._scrollPositionChanged(e,this._scrollPosition),this._updateVisibleIndices({emit:!0})),this._checkThresholds()}},{key:"reflowIfNeeded",value:function(){var t=arguments.length>0&&void 0!==arguments[0]&&arguments[0];(t||this._pendingReflow)&&(this._pendingReflow=!1,this._reflow())}},{key:"scrollToIndex",value:function(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"start";if(Number.isFinite(t)){switch(t=Math.min(this.totalItems,Math.max(0,t)),this._scrollToIndex=t,"nearest"===e&&(e=t>this._first+this._num/2?"end":"start"),e){case"start":this._scrollToAnchor=0;break;case"center":this._scrollToAnchor=.5;break;case"end":this._scrollToAnchor=1;break;default:throw new TypeError("position must be one of: start, center, end, nearest")}this._scheduleReflow()}}},{key:"dispatchEvent",value:(o=v(regeneratorRuntime.mark((function t(e){return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,this._eventTargetPromise;case 2:this._eventTarget.dispatchEvent(e);case 3:case"end":return t.stop()}}),t,this)}))),function(t){return o.apply(this,arguments)})},{key:"addEventListener",value:(n=v(regeneratorRuntime.mark((function t(e,i,s){return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,this._eventTargetPromise;case 2:this._eventTarget.addEventListener(e,i,s);case 3:case"end":return t.stop()}}),t,this)}))),function(t,e,i){return n.apply(this,arguments)})},{key:"removeEventListener",value:(r=v(regeneratorRuntime.mark((function t(e,i,s){return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,this._eventTargetPromise;case 2:this._eventTarget.removeEventListener(e,i,s);case 3:case"end":return t.stop()}}),t,this)}))),function(t,e,i){return r.apply(this,arguments)})},{key:"_updateLayout",value:function(){}},{key:"_viewDim1",get:function(){return this._viewportSize[this._sizeDim]}},{key:"_viewDim2",get:function(){return this._viewportSize[this._secondarySizeDim]}},{key:"_scheduleReflow",value:function(){this._pendingReflow=!0}},{key:"_scheduleLayoutUpdate",value:function(){this._pendingLayoutUpdate=!0,this._scheduleReflow()}},{key:"_triggerReflow",value:function(){var t=this;this._scheduleLayoutUpdate(),Promise.resolve().then((function(){return t.reflowIfNeeded()}))}},{key:"_reflow",value:function(){this._pendingLayoutUpdate&&(this._updateLayout(),this._pendingLayoutUpdate=!1),this._updateScrollSize(),this._getActiveItems(),this._scrollIfNeeded(),this._updateVisibleIndices(),this._emitScrollSize(),this._emitRange(),this._emitChildPositions(),this._emitScrollError()}},{key:"_scrollIfNeeded",value:function(){if(-1!==this._scrollToIndex){var t=this._scrollToIndex,e=this._scrollToAnchor,i=this._getItemPosition(t)[this._positionDim],s=this._getItemSize(t)[this._sizeDim],r=this._scrollPosition+this._viewDim1*e,n=i+s*e,o=Math.floor(Math.min(this._scrollSize-this._viewDim1,Math.max(0,this._scrollPosition-r+n)));this._scrollError+=this._scrollPosition-o,this._scrollPosition=o}}},{key:"_emitRange",value:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:void 0,e=Object.assign({first:this._first,last:this._last,num:this._num,stable:!0,firstVisible:this._firstVisible,lastVisible:this._lastVisible},t);this.dispatchEvent(new CustomEvent("rangechange",{detail:e}))}},{key:"_emitScrollSize",value:function(){var t=_({},this._sizeDim,this._scrollSize);this.dispatchEvent(new CustomEvent("scrollsizechange",{detail:t}))}},{key:"_emitScrollError",value:function(){if(this._scrollError){var t,e=(_(t={},this._positionDim,this._scrollError),_(t,this._secondaryPositionDim,0),t);this.dispatchEvent(new CustomEvent("scrollerrorchange",{detail:e})),this._scrollError=0}}},{key:"_emitChildPositions",value:function(){for(var t={},e=this._first;e<=this._last;e++)t[e]=this._getItemPosition(e);this.dispatchEvent(new CustomEvent("itempositionchange",{detail:t}))}},{key:"_num",get:function(){return-1===this._first||-1===this._last?0:this._last-this._first+1}},{key:"_checkThresholds",value:function(){if(0===this._viewDim1&&this._num>0)this._scheduleReflow();else{var t=Math.max(0,this._scrollPosition-this._overhang),e=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang);(this._physicalMin>t||this._physicalMax<e)&&this._scheduleReflow()}}},{key:"_updateVisibleIndices",value:function(t){if(-1!==this._first&&-1!==this._last){for(var e=this._first;e<this._last&&Math.round(this._getItemPosition(e)[this._positionDim]+this._getItemSize(e)[this._sizeDim])<=Math.round(this._scrollPosition);)e++;for(var i=this._last;i>this._first&&Math.round(this._getItemPosition(i)[this._positionDim])>=Math.round(this._scrollPosition+this._viewDim1);)i--;e===this._firstVisible&&i===this._lastVisible||(this._firstVisible=e,this._lastVisible=i,t&&t.emit&&this._emitRange())}}},{key:"_scrollPositionChanged",value:function(t,e){var i=this._scrollSize-this._viewDim1;(t<i||e<i)&&(this._scrollToIndex=-1)}}],i&&m(e.prototype,i),s&&m(e,s),t}();function g(t){return g="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},g(t)}function y(t,e,i){return e in t?Object.defineProperty(t,e,{value:i,enumerable:!0,configurable:!0,writable:!0}):t[e]=i,t}function p(t,e,i){return p="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(t,e,i){var s=function(t,e){for(;!Object.prototype.hasOwnProperty.call(t,e)&&null!==(t=b(t)););return t}(t,e);if(s){var r=Object.getOwnPropertyDescriptor(s,e);return r.get?r.get.call(i):r.value}},p(t,e,i||t)}function S(t,e){return S=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},S(t,e)}function z(t){var e=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}();return function(){var i,s=b(t);if(e){var r=b(this).constructor;i=Reflect.construct(s,arguments,r)}else i=s.apply(this,arguments);return w(this,i)}}function w(t,e){if(e&&("object"===g(e)||"function"==typeof e))return e;if(void 0!==e)throw new TypeError("Derived constructors may only return object or undefined");return function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t)}function b(t){return b=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},b(t)}function I(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function P(t,e){for(var i=0;i<e.length;i++){var s=e[i];s.enumerable=s.enumerable||!1,s.configurable=!0,"value"in s&&(s.writable=!0),Object.defineProperty(t,s.key,s)}}function k(t,e,i){return e&&P(t.prototype,e),i&&P(t,i),t}function C(t){return function(t){if(Array.isArray(t))return x(t)}(t)||function(t){if("undefined"!=typeof Symbol&&null!=t[Symbol.iterator]||null!=t["@@iterator"])return Array.from(t)}(t)||M(t)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function M(t,e){if(t){if("string"==typeof t)return x(t,e);var i=Object.prototype.toString.call(t).slice(8,-1);return"Object"===i&&t.constructor&&(i=t.constructor.name),"Map"===i||"Set"===i?Array.from(t):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?x(t,e):void 0}}function x(t,e){(null==e||e>t.length)&&(e=t.length);for(var i=0,s=new Array(e);i<e;i++)s[i]=t[i];return s}var R=function(t){return Object.assign({type:O},t)};function D(t){return"horizontal"===t?"marginLeft":"marginTop"}function E(t){return"horizontal"===t?"marginRight":"marginBottom"}function A(t,e){var i=[t,e].sort();return i[1]<=0?Math.min.apply(Math,C(i)):i[0]>=0?Math.max.apply(Math,C(i)):i[0]+i[1]}var T=function(){function t(){I(this,t),this._childSizeCache=new o,this._marginSizeCache=new o,this._metricsCache=new Map}return k(t,[{key:"update",value:function(t,e){var i,s,r=this,n=new Set;Object.keys(t).forEach((function(i){var s=Number(i);r._metricsCache.set(s,t[s]),r._childSizeCache.set(s,t[s][function(t){return"horizontal"===t?"width":"height"}(e)]),n.add(s),n.add(s+1)}));var o,a=function(t,e){var i="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!i){if(Array.isArray(t)||(i=M(t))||e&&t&&"number"==typeof t.length){i&&(t=i);var s=0,r=function(){};return{s:r,n:function(){return s>=t.length?{done:!0}:{done:!1,value:t[s++]}},e:function(t){throw t},f:r}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var n,o=!0,a=!1;return{s:function(){i=i.call(t)},n:function(){var t=i.next();return o=t.done,t},e:function(t){a=!0,n=t},f:function(){try{o||null==i.return||i.return()}finally{if(a)throw n}}}}(n);try{for(a.s();!(o=a.n()).done;){var h=o.value,c=(null===(i=this._metricsCache.get(h))||void 0===i?void 0:i[D(e)])||0,l=(null===(s=this._metricsCache.get(h-1))||void 0===s?void 0:s[E(e)])||0;this._marginSizeCache.set(h,A(c,l))}}catch(u){a.e(u)}finally{a.f()}}},{key:"averageChildSize",get:function(){return this._childSizeCache.averageSize}},{key:"totalChildSize",get:function(){return this._childSizeCache.totalSize}},{key:"averageMarginSize",get:function(){return this._marginSizeCache.averageSize}},{key:"totalMarginSize",get:function(){return this._marginSizeCache.totalSize}},{key:"getLeadingMarginValue",value:function(t,e){var i;return(null===(i=this._metricsCache.get(t))||void 0===i?void 0:i[D(e)])||0}},{key:"getChildSize",value:function(t){return this._childSizeCache.getSize(t)}},{key:"getMarginSize",value:function(t){return this._marginSizeCache.getSize(t)}},{key:"clear",value:function(){this._childSizeCache.clear(),this._marginSizeCache.clear(),this._metricsCache.clear()}}]),t}(),O=function(t){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&S(t,e)}(i,t);var e=z(i);function i(){var t;return I(this,i),(t=e.apply(this,arguments))._itemSize={width:100,height:100},t._physicalItems=new Map,t._newPhysicalItems=new Map,t._metricsCache=new T,t._anchorIdx=null,t._anchorPos=null,t._stable=!0,t._needsRemeasure=!1,t._measureChildren=!0,t._estimate=!0,t}return k(i,[{key:"measureChildren",get:function(){return this._measureChildren}},{key:"updateItemSizes",value:function(t){this._metricsCache.update(t,this.direction),this._scheduleReflow()}},{key:"_getPhysicalItem",value:function(t){var e;return null!==(e=this._newPhysicalItems.get(t))&&void 0!==e?e:this._physicalItems.get(t)}},{key:"_getSize",value:function(t){return this._getPhysicalItem(t)&&this._metricsCache.getChildSize(t)}},{key:"_getAverageSize",value:function(){return this._metricsCache.averageChildSize||this._itemSize[this._sizeDim]}},{key:"_getPosition",value:function(t){var e,i=this._getPhysicalItem(t),s=this._metricsCache.averageMarginSize;return 0===t?null!==(e=this._metricsCache.getMarginSize(0))&&void 0!==e?e:s:i?i.pos:s+t*(s+this._getAverageSize())}},{key:"_calculateAnchor",value:function(t,e){return t<=0?0:e>this._scrollSize-this._viewDim1?this._totalItems-1:Math.max(0,Math.min(this._totalItems-1,Math.floor((t+e)/2/this._delta)))}},{key:"_getAnchor",value:function(t,e){if(0===this._physicalItems.size)return this._calculateAnchor(t,e);if(this._first<0)return console.error("_getAnchor: negative _first"),this._calculateAnchor(t,e);if(this._last<0)return console.error("_getAnchor: negative _last"),this._calculateAnchor(t,e);var i=this._getPhysicalItem(this._first),s=this._getPhysicalItem(this._last),r=i.pos;if(s.pos+this._metricsCache.getChildSize(this._last)<t)return this._calculateAnchor(t,e);if(r>e)return this._calculateAnchor(t,e);for(var n=this._firstVisible-1,o=-1/0;o<t;){o=this._getPhysicalItem(++n).pos+this._metricsCache.getChildSize(n)}return n}},{key:"_getActiveItems",value:function(){0===this._viewDim1||0===this._totalItems?this._clearItems():this._getItems()}},{key:"_clearItems",value:function(){this._first=-1,this._last=-1,this._physicalMin=0,this._physicalMax=0;var t=this._newPhysicalItems;this._newPhysicalItems=this._physicalItems,this._newPhysicalItems.clear(),this._physicalItems=t,this._stable=!0}},{key:"_getItems",value:function(){var t,e,i,s,r=this._newPhysicalItems;if(this._stable=!0,this._scrollToIndex>=0&&(this._anchorIdx=Math.min(this._scrollToIndex,this._totalItems-1),this._anchorPos=this._getPosition(this._anchorIdx),this._scrollIfNeeded()),i=this._scrollPosition-this._overhang,(s=this._scrollPosition+this._viewDim1+this._overhang)<0||i>this._scrollSize)this._clearItems();else{null!==this._anchorIdx&&null!==this._anchorPos||(this._anchorIdx=this._getAnchor(i,s),this._anchorPos=this._getPosition(this._anchorIdx));var n=this._getSize(this._anchorIdx);void 0===n&&(this._stable=!1,n=this._getAverageSize());var o=null!==(t=this._metricsCache.getMarginSize(this._anchorIdx))&&void 0!==t?t:this._metricsCache.averageMarginSize,a=null!==(e=this._metricsCache.getMarginSize(this._anchorIdx+1))&&void 0!==e?e:this._metricsCache.averageMarginSize;0===this._anchorIdx&&(this._anchorPos=o),this._anchorIdx===this._totalItems-1&&(this._anchorPos=this._scrollSize-a-n);var h=0;for(this._anchorPos+n+a<i&&(h=i-(this._anchorPos+n+a)),this._anchorPos-o>s&&(h=s-(this._anchorPos-o)),h&&(this._scrollPosition-=h,i-=h,s-=h,this._scrollError+=h),r.set(this._anchorIdx,{pos:this._anchorPos,size:n}),this._first=this._last=this._anchorIdx,this._physicalMin=this._anchorPos,this._physicalMax=this._anchorPos+n;this._physicalMin>i&&this._first>0;){var c=this._getSize(--this._first);void 0===c&&(this._stable=!1,c=this._getAverageSize());var l=this._metricsCache.getMarginSize(this._first+1);void 0===l&&(this._stable=!1,l=this._metricsCache.averageMarginSize),this._physicalMin-=c+l;var u=this._physicalMin;if(r.set(this._first,{pos:u,size:c}),!1===this._stable&&!1===this._estimate)break}for(;this._physicalMax<s&&this._last<this._totalItems-1;){var _=this._metricsCache.getMarginSize(++this._last);void 0===_&&(this._stable=!1,_=this._metricsCache.averageMarginSize);var f=this._getSize(this._last);void 0===f&&(this._stable=!1,f=this._getAverageSize());var v=this._physicalMax+_;if(r.set(this._last,{pos:v,size:f}),this._physicalMax+=_+f,!1===this._stable&&!1===this._estimate)break}var m=this._calculateError();m&&(this._physicalMin-=m,this._physicalMax-=m,this._anchorPos-=m,this._scrollPosition-=m,r.forEach((function(t){return t.pos-=m})),this._scrollError+=m),this._stable&&(this._newPhysicalItems=this._physicalItems,this._newPhysicalItems.clear(),this._physicalItems=r)}}},{key:"_calculateError",value:function(){var t,e,i=this._metricsCache.averageMarginSize;return 0===this._first?this._physicalMin-(null!==(t=this._metricsCache.getMarginSize(0))&&void 0!==t?t:i):this._physicalMin<=0?this._physicalMin-this._first*this._delta:this._last===this._totalItems-1?this._physicalMax+(null!==(e=this._metricsCache.getMarginSize(this._totalItems))&&void 0!==e?e:i)-this._scrollSize:this._physicalMax>=this._scrollSize?this._physicalMax-this._scrollSize+(this._totalItems-1-this._last)*this._delta:0}},{key:"_reflow",value:function(){var t=this._first,e=this._last,i=this._scrollSize;this._updateScrollSize(),this._getActiveItems(),this._scrollSize!==i&&this._emitScrollSize(),this._updateVisibleIndices(),this._emitRange(),-1===this._first&&-1===this._last?this._resetReflowState():this._first!==t||this._last!==e||this._needsRemeasure?(this._emitChildPositions(),this._emitScrollError()):(this._emitChildPositions(),this._emitScrollError(),this._resetReflowState())}},{key:"_resetReflowState",value:function(){this._anchorIdx=null,this._anchorPos=null,this._stable=!0}},{key:"_updateScrollSize",value:function(){var t=this._metricsCache.averageMarginSize;this._scrollSize=Math.max(1,this._totalItems*(t+this._getAverageSize())+t)}},{key:"_delta",get:function(){var t=this._metricsCache.averageMarginSize;return this._getAverageSize()+t}},{key:"_getItemPosition",value:function(t){var e,i;return y(e={},this._positionDim,this._getPosition(t)),y(e,this._secondaryPositionDim,0),y(e,"horizontal"===this.direction?"xOffset":"yOffset",-(null!==(i=this._metricsCache.getLeadingMarginValue(t,this.direction))&&void 0!==i?i:this._metricsCache.averageMarginSize)),e}},{key:"_getItemSize",value:function(t){var e,i;return y(e={},this._sizeDim,(this._getSize(t)||this._getAverageSize())+(null!==(i=this._metricsCache.getMarginSize(t+1))&&void 0!==i?i:this._metricsCache.averageMarginSize)),y(e,this._secondarySizeDim,this._itemSize[this._secondarySizeDim]),e}},{key:"_viewDim2Changed",value:function(){this._needsRemeasure=!0,this._scheduleReflow()}},{key:"_emitRange",value:function(){var t=this._needsRemeasure,e=this._stable;this._needsRemeasure=!1,p(b(i.prototype),"_emitRange",this).call(this,{remeasure:t,stable:e})}}]),i}(d)}}]);