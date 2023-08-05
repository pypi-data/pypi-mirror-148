/*! For license information please see 6d3783d7.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[9874],{9874:(t,e,i)=>{function s(t,e,i,s){var r,n=arguments.length,l=n<3?e:null===s?s=Object.getOwnPropertyDescriptor(e,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)l=Reflect.decorate(t,e,i,s);else for(var o=t.length-1;o>=0;o--)(r=t[o])&&(l=(n<3?r(l):n>3?r(e,i,l):r(e,i))||l);return n>3&&l&&Object.defineProperty(e,i,l),l}var r=i(37500),n=i(26767),l=i(5701),o=i(17717),h=i(86230);let a,c;async function u(){return c||async function(){if(a)return(await a).default;a=window.ResizeObserver;try{new a((function(){}))}catch(t){a=i.e(5442).then(i.bind(i,5442)),a=(await a).default}return c=a}()}const _=Symbol("virtualizerRef"),d="virtualizer-sizer";class m extends Event{constructor(t){super(m.eventName,{bubbles:!0}),this.first=t.first,this.last=t.last}}m.eventName="rangeChanged";class f extends Event{constructor(t){super(f.eventName,{bubbles:!0}),this.first=t.first,this.last=t.last}}f.eventName="visibilityChanged";class p{constructor(t){if(this._benchmarkStart=null,this._layout=null,this._clippingAncestors=[],this._scrollSize=null,this._scrollError=null,this._childrenPos=null,this._childMeasurements=null,this._toBeMeasured=new Map,this._rangeChanged=!0,this._itemsChanged=!0,this._visibilityChanged=!0,this._isScroller=!1,this._sizer=null,this._hostElementRO=null,this._childrenRO=null,this._mutationObserver=null,this._mutationPromise=null,this._mutationPromiseResolver=null,this._mutationsObserved=!1,this._scrollEventListeners=[],this._scrollEventListenerOptions={passive:!0},this._loadListener=this._childLoaded.bind(this),this._scrollToIndex=null,this._items=[],this._first=-1,this._last=-1,this._firstVisible=-1,this._lastVisible=-1,this._scheduled=new WeakSet,this._measureCallback=null,this._measureChildOverride=null,!t)throw new Error("Virtualizer constructor requires a configuration object");if(!t.hostElement)throw new Error('Virtualizer configuration requires the "hostElement" property');this._init(t)}set items(t){Array.isArray(t)&&t!==this._items&&(this._itemsChanged=!0,this._items=t,this._schedule(this._updateLayout))}_init(t){this._isScroller=!!t.scroller,this._initHostElement(t),this._initLayout(t)}async _initObservers(){this._mutationObserver=new MutationObserver(this._observeMutations.bind(this));const t=await u();this._hostElementRO=new t((()=>this._hostElementSizeChanged())),this._childrenRO=new t(this._childrenSizeChanged.bind(this))}async _initLayout(t){t.layout?this.layout=t.layout:this.layout=(await i.e(28663).then(i.bind(i,28663))).FlowLayout}_initHostElement(t){const e=this._hostElement=t.hostElement;this._applyVirtualizerStyles(),e[_]=this}async connected(){await this._initObservers();const t=this._isScroller;this._clippingAncestors=function(t,e=!1){return function(t,e=!1){const i=[];let s=e?t:y(t);for(;null!==s;)i.push(s),s=y(s);return i}(t,e).filter((t=>"visible"!==getComputedStyle(t).overflow))}(this._hostElement,t),this._schedule(this._updateLayout),this._observeAndListen()}_observeAndListen(){this._mutationObserver.observe(this._hostElement,{childList:!0}),this._mutationPromise=new Promise((t=>this._mutationPromiseResolver=t)),this._hostElementRO.observe(this._hostElement),this._scrollEventListeners.push(window),window.addEventListener("scroll",this,this._scrollEventListenerOptions),this._clippingAncestors.forEach((t=>{t.addEventListener("scroll",this,this._scrollEventListenerOptions),this._scrollEventListeners.push(t),this._hostElementRO.observe(t)})),this._children.forEach((t=>this._childrenRO.observe(t))),this._scrollEventListeners.forEach((t=>t.addEventListener("scroll",this,this._scrollEventListenerOptions)))}disconnected(){this._scrollEventListeners.forEach((t=>t.removeEventListener("scroll",this,this._scrollEventListenerOptions))),this._scrollEventListeners=[],this._clippingAncestors=[],this._mutationObserver.disconnect(),this._hostElementRO.disconnect(),this._childrenRO.disconnect()}_applyVirtualizerStyles(){const t=this._hostElement.style;t.display=t.display||"block",t.position=t.position||"relative",t.contain=t.contain||"strict",this._isScroller&&(t.overflow=t.overflow||"auto",t.minHeight=t.minHeight||"150px")}_getSizer(){const t=this._hostElement;if(!this._sizer){let e=t.querySelector("[virtualizer-sizer]");e||(e=document.createElement("div"),e.setAttribute(d,""),t.appendChild(e)),Object.assign(e.style,{position:"absolute",margin:"-2px 0 0 0",padding:0,visibility:"hidden",fontSize:"2px"}),e.innerHTML="&nbsp;",e.setAttribute(d,""),this._sizer=e}return this._sizer}get layout(){return this._layout}set layout(t){if(this._layout===t)return;let e=null,i={};if("object"==typeof t?(void 0!==t.type&&(e=t.type),i=t):e=t,"function"==typeof e){if(this._layout instanceof e)return void(i&&(this._layout.config=i));e=new e(i)}this._layout&&(this._measureCallback=null,this._measureChildOverride=null,this._layout.removeEventListener("scrollsizechange",this),this._layout.removeEventListener("scrollerrorchange",this),this._layout.removeEventListener("itempositionchange",this),this._layout.removeEventListener("rangechange",this),this._sizeHostElement(void 0),this._hostElement.removeEventListener("load",this._loadListener,!0)),this._layout=e,this._layout&&(this._layout.measureChildren&&"function"==typeof this._layout.updateItemSizes&&("function"==typeof this._layout.measureChildren&&(this._measureChildOverride=this._layout.measureChildren),this._measureCallback=this._layout.updateItemSizes.bind(this._layout)),this._layout.addEventListener("scrollsizechange",this),this._layout.addEventListener("scrollerrorchange",this),this._layout.addEventListener("itempositionchange",this),this._layout.addEventListener("rangechange",this),this._layout.listenForChildLoadEvents&&this._hostElement.addEventListener("load",this._loadListener,!0),this._schedule(this._updateLayout))}startBenchmarking(){null===this._benchmarkStart&&(this._benchmarkStart=window.performance.now())}stopBenchmarking(){if(null!==this._benchmarkStart){const t=window.performance.now(),e=t-this._benchmarkStart,i=performance.getEntriesByName("uv-virtualizing","measure").filter((e=>e.startTime>=this._benchmarkStart&&e.startTime<t)).reduce(((t,e)=>t+e.duration),0);return this._benchmarkStart=null,{timeElapsed:e,virtualizationTime:i}}return null}_measureChildren(){const t={},e=this._children,i=this._measureChildOverride||this._measureChild;for(let s=0;s<e.length;s++){const r=e[s],n=this._first+s;(this._itemsChanged||this._toBeMeasured.has(r))&&(t[n]=i.call(this,r,this._items[n]))}this._childMeasurements=t,this._schedule(this._updateLayout),this._toBeMeasured.clear()}_measureChild(t){const{width:e,height:i}=t.getBoundingClientRect();return Object.assign({width:e,height:i},function(t){const e=window.getComputedStyle(t);return{marginTop:v(e.marginTop),marginRight:v(e.marginRight),marginBottom:v(e.marginBottom),marginLeft:v(e.marginLeft)}}(t))}set scrollToIndex(t){this._scrollToIndex=t,this._schedule(this._updateLayout)}async _schedule(t){this._scheduled.has(t)||(this._scheduled.add(t),await Promise.resolve(),this._scheduled.delete(t),t.call(this))}async _updateDOM(){const{_rangeChanged:t,_itemsChanged:e}=this;this._visibilityChanged&&(this._notifyVisibility(),this._visibilityChanged=!1),(t||e)&&(this._notifyRange(),await this._mutationPromise),this._children.forEach((t=>this._childrenRO.observe(t))),this._positionChildren(this._childrenPos),this._sizeHostElement(this._scrollSize),this._scrollError&&(this._correctScrollError(this._scrollError),this._scrollError=null),this._benchmarkStart&&"mark"in window.performance&&window.performance.mark("uv-end")}_updateLayout(){this._layout&&(this._layout.totalItems=this._items.length,null!==this._scrollToIndex&&(this._layout.scrollToIndex(this._scrollToIndex.index,this._scrollToIndex.position),this._scrollToIndex=null),this._updateView(),null!==this._childMeasurements&&(this._measureCallback&&this._measureCallback(this._childMeasurements),this._childMeasurements=null),this._layout.reflowIfNeeded(this._itemsChanged),this._benchmarkStart&&"mark"in window.performance&&window.performance.mark("uv-end"))}_handleScrollEvent(){if(this._benchmarkStart&&"mark"in window.performance){try{window.performance.measure("uv-virtualizing","uv-start","uv-end")}catch(t){console.warn("Error measuring performance data: ",t)}window.performance.mark("uv-start")}this._schedule(this._updateLayout)}handleEvent(t){switch(t.type){case"scroll":(t.currentTarget===window||this._clippingAncestors.includes(t.currentTarget))&&this._handleScrollEvent();break;case"scrollsizechange":this._scrollSize=t.detail,this._schedule(this._updateDOM);break;case"scrollerrorchange":this._scrollError=t.detail,this._schedule(this._updateDOM);break;case"itempositionchange":this._childrenPos=t.detail,this._schedule(this._updateDOM);break;case"rangechange":this._adjustRange(t.detail),this._schedule(this._updateDOM);break;default:console.warn("event not handled",t)}}get _children(){const t=[];let e=this._hostElement.firstElementChild;for(;e;)e.hasAttribute(d)||t.push(e),e=e.nextElementSibling;return t}_updateView(){const t=this._hostElement,e=this._layout;let i,s,r,n,l,o;const h=t.getBoundingClientRect();i=0,s=0,r=window.innerHeight,n=window.innerWidth;for(let t of this._clippingAncestors){const e=t.getBoundingClientRect();i=Math.max(i,e.top),s=Math.max(s,e.left),r=Math.min(r,e.bottom),n=Math.min(n,e.right)}l=i-h.top+t.scrollTop,o=s-h.left+t.scrollLeft;const a=Math.max(1,r-i),c=Math.max(1,n-s);e.viewportSize={width:c,height:a},e.viewportScroll={top:l,left:o}}_sizeHostElement(t){const e=82e5,i=t&&t.width?Math.min(e,t.width):0,s=t&&t.height?Math.min(e,t.height):0;if(this._isScroller)this._getSizer().style.transform=`translate(${i}px, ${s}px)`;else{const t=this._hostElement.style;t.minWidth=i?`${i}px`:"100%",t.minHeight=s?`${s}px`:"100%"}}_positionChildren(t){if(t){const e=this._children;Object.keys(t).forEach((i=>{const s=i-this._first,r=e[s];if(r){const{top:e,left:s,width:n,height:l,xOffset:o,yOffset:h}=t[i];r.style.position="absolute",r.style.boxSizing="border-box",r.style.transform=`translate(${s}px, ${e}px)`,void 0!==n&&(r.style.width=n+"px"),void 0!==l&&(r.style.height=l+"px"),r.style.left=void 0===o?null:o+"px",r.style.top=void 0===h?null:h+"px"}}))}}async _adjustRange(t){const{_first:e,_last:i,_firstVisible:s,_lastVisible:r}=this;this._first=t.first,this._last=t.last,this._firstVisible=t.firstVisible,this._lastVisible=t.lastVisible,this._rangeChanged=this._rangeChanged||this._first!==e||this._last!==i,this._visibilityChanged=this._visibilityChanged||this._firstVisible!==s||this._lastVisible!==r}_correctScrollError(t){const e=this._clippingAncestors[0];e?(e.scrollTop-=t.top,e.scrollLeft-=t.left):window.scroll(window.pageXOffset-t.left,window.pageYOffset-t.top)}_notifyRange(){this._hostElement.dispatchEvent(new m({first:this._first,last:this._last}))}_notifyVisibility(){this._hostElement.dispatchEvent(new f({first:this._firstVisible,last:this._lastVisible}))}_hostElementSizeChanged(){this._schedule(this._updateLayout)}async _observeMutations(){this._mutationsObserved||(this._mutationsObserved=!0,this._mutationPromiseResolver(),this._mutationPromise=new Promise((t=>this._mutationPromiseResolver=t)),this._mutationsObserved=!1)}_childLoaded(){}_childrenSizeChanged(t){if(this._layout.measureChildren){for(const e of t)this._toBeMeasured.set(e.target,e.contentRect);this._measureChildren()}this._itemsChanged=!1,this._rangeChanged=!1}}function v(t){const e=t?parseFloat(t):NaN;return Number.isNaN(e)?0:e}function y(t){if(null!==t.parentElement)return t.parentElement;const e=t.parentNode;return e&&e.nodeType===Node.DOCUMENT_FRAGMENT_NODE&&e.host||null}const g=t=>t,b=(t,e)=>r.dy`${e}: ${JSON.stringify(t,null,2)}`;let w=class extends r.oi{constructor(){super(...arguments),this._renderItem=(t,e)=>b(t,e+this._first),this._providedRenderItem=b,this.items=[],this.scroller=!1,this.keyFunction=g,this._first=0,this._last=-1}set renderItem(t){this._providedRenderItem=t,this._renderItem=(e,i)=>t(e,i+this._first),this.requestUpdate()}get renderItem(){return this._providedRenderItem}set layout(t){this._layout=t,t&&this._virtualizer&&(this._virtualizer.layout=t)}get layout(){return this[_].layout}scrollToIndex(t,e="start"){this._virtualizer.scrollToIndex={index:t,position:e}}updated(){this._virtualizer&&(void 0!==this._layout&&(this._virtualizer.layout=this._layout),this._virtualizer.items=this.items)}firstUpdated(){const t=this._layout;this._virtualizer=new p({hostElement:this,layout:t,scroller:this.scroller}),this.addEventListener("rangeChanged",(t=>{t.stopPropagation(),this._first=t.first,this._last=t.last})),this._virtualizer.connected()}connectedCallback(){super.connectedCallback(),this._virtualizer&&this._virtualizer.connected()}disconnectedCallback(){this._virtualizer&&this._virtualizer.disconnected(),super.disconnectedCallback()}createRenderRoot(){return this}render(){const{items:t,_renderItem:e,keyFunction:i}=this,s=[];if(this._first>=0&&this._last>=this._first)for(let e=this._first;e<this._last+1;e++)s.push(t[e]);return(0,h.r)(s,i||g,e)}};s([(0,l.C)()],w.prototype,"renderItem",null),s([(0,l.C)({attribute:!1})],w.prototype,"items",void 0),s([(0,l.C)({reflect:!0,type:Boolean})],w.prototype,"scroller",void 0),s([(0,l.C)()],w.prototype,"keyFunction",void 0),s([(0,o.S)()],w.prototype,"_first",void 0),s([(0,o.S)()],w.prototype,"_last",void 0),s([(0,l.C)({attribute:!1})],w.prototype,"layout",null),w=s([(0,n.M)("lit-virtualizer")],w)},86230:(t,e,i)=>{i.d(e,{r:()=>o});var s=i(15304),r=i(38941),n=i(81563);const l=(t,e,i)=>{const s=new Map;for(let r=e;r<=i;r++)s.set(t[r],r);return s},o=(0,r.XM)(class extends r.Xe{constructor(t){if(super(t),t.type!==r.pX.CHILD)throw Error("repeat() can only be used in text expressions")}dt(t,e,i){let s;void 0===i?i=e:void 0!==e&&(s=e);const r=[],n=[];let l=0;for(const e of t)r[l]=s?s(e,l):l,n[l]=i(e,l),l++;return{values:n,keys:r}}render(t,e,i){return this.dt(t,e,i).values}update(t,[e,i,r]){var o;const h=(0,n.i9)(t),{values:a,keys:c}=this.dt(e,i,r);if(!Array.isArray(h))return this.at=c,a;const u=null!==(o=this.at)&&void 0!==o?o:this.at=[],_=[];let d,m,f=0,p=h.length-1,v=0,y=a.length-1;for(;f<=p&&v<=y;)if(null===h[f])f++;else if(null===h[p])p--;else if(u[f]===c[v])_[v]=(0,n.fk)(h[f],a[v]),f++,v++;else if(u[p]===c[y])_[y]=(0,n.fk)(h[p],a[y]),p--,y--;else if(u[f]===c[y])_[y]=(0,n.fk)(h[f],a[y]),(0,n._Y)(t,_[y+1],h[f]),f++,y--;else if(u[p]===c[v])_[v]=(0,n.fk)(h[p],a[v]),(0,n._Y)(t,h[f],h[p]),p--,v++;else if(void 0===d&&(d=l(c,v,y),m=l(u,f,p)),d.has(u[f]))if(d.has(u[p])){const e=m.get(c[v]),i=void 0!==e?h[e]:null;if(null===i){const e=(0,n._Y)(t,h[f]);(0,n.fk)(e,a[v]),_[v]=e}else _[v]=(0,n.fk)(i,a[v]),(0,n._Y)(t,h[f],i),h[e]=null;v++}else(0,n.ws)(h[p]),p--;else(0,n.ws)(h[f]),f++;for(;v<=y;){const e=(0,n._Y)(t,_[y+1]);(0,n.fk)(e,a[v]),_[v++]=e}for(;f<=p;){const t=h[f++];null!==t&&(0,n.ws)(t)}return this.at=c,(0,n.hl)(t,_),s.Jb}})}}]);