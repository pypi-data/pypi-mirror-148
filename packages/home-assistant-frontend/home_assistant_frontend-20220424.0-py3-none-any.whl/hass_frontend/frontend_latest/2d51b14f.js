/*! For license information please see 2d51b14f.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[28663],{28663:(t,i,s)=>{s.r(i),s.d(i,{FlowLayout:()=>m,flow:()=>o});class e{constructor(t){this._map=new Map,this._roundAverageSize=!0,this.totalSize=0,!1===(null==t?void 0:t.roundAverageSize)&&(this._roundAverageSize=!1)}set(t,i){const s=this._map.get(t)||0;this._map.set(t,i),this.totalSize+=i-s}get averageSize(){if(this._map.size>0){const t=this.totalSize/this._map.size;return this._roundAverageSize?Math.round(t):t}return 0}getSize(t){return this._map.get(t)}clear(){this._map.clear(),this.totalSize=0}}let h,r;async function a(){return r||async function(){h=window.EventTarget;try{new h}catch(t){h=(await s.e(98251).then(s.t.bind(s,98251,19))).default.EventTarget}return r=h}()}const o=t=>Object.assign({type:m},t);function _(t){return"horizontal"===t?"marginLeft":"marginTop"}function l(t){return"horizontal"===t?"marginRight":"marginBottom"}function n(t,i){const s=[t,i].sort();return s[1]<=0?Math.min(...s):s[0]>=0?Math.max(...s):s[0]+s[1]}class c{constructor(){this._childSizeCache=new e,this._marginSizeCache=new e,this._metricsCache=new Map}update(t,i){var s,e;const h=new Set;Object.keys(t).forEach((s=>{const e=Number(s);this._metricsCache.set(e,t[e]),this._childSizeCache.set(e,t[e][function(t){return"horizontal"===t?"width":"height"}(i)]),h.add(e),h.add(e+1)}));for(const t of h){const h=(null===(s=this._metricsCache.get(t))||void 0===s?void 0:s[_(i)])||0,r=(null===(e=this._metricsCache.get(t-1))||void 0===e?void 0:e[l(i)])||0;this._marginSizeCache.set(t,n(h,r))}}get averageChildSize(){return this._childSizeCache.averageSize}get totalChildSize(){return this._childSizeCache.totalSize}get averageMarginSize(){return this._marginSizeCache.averageSize}get totalMarginSize(){return this._marginSizeCache.totalSize}getLeadingMarginValue(t,i){var s;return(null===(s=this._metricsCache.get(t))||void 0===s?void 0:s[_(i)])||0}getChildSize(t){return this._childSizeCache.getSize(t)}getMarginSize(t){return this._marginSizeCache.getSize(t)}clear(){this._childSizeCache.clear(),this._marginSizeCache.clear(),this._metricsCache.clear()}}class m extends class{constructor(t){this._latestCoords={left:0,top:0},this._direction=null,this._viewportSize={width:0,height:0},this._pendingReflow=!1,this._pendingLayoutUpdate=!1,this._scrollToIndex=-1,this._scrollToAnchor=0,this._firstVisible=0,this._lastVisible=0,this._eventTargetPromise=a().then((t=>{this._eventTarget=new t})),this._physicalMin=0,this._physicalMax=0,this._first=-1,this._last=-1,this._sizeDim="height",this._secondarySizeDim="width",this._positionDim="top",this._secondaryPositionDim="left",this._scrollPosition=0,this._scrollError=0,this._totalItems=0,this._scrollSize=1,this._overhang=1e3,this._eventTarget=null,Promise.resolve().then((()=>this.config=t||this._defaultConfig))}get _defaultConfig(){return{direction:"vertical"}}set config(t){Object.assign(this,Object.assign({},this._defaultConfig,t))}get config(){return{direction:this.direction}}get totalItems(){return this._totalItems}set totalItems(t){const i=Number(t);i!==this._totalItems&&(this._totalItems=i,this._scheduleReflow())}get direction(){return this._direction}set direction(t){(t="horizontal"===t?t:"vertical")!==this._direction&&(this._direction=t,this._sizeDim="horizontal"===t?"width":"height",this._secondarySizeDim="horizontal"===t?"height":"width",this._positionDim="horizontal"===t?"left":"top",this._secondaryPositionDim="horizontal"===t?"top":"left",this._triggerReflow())}get viewportSize(){return this._viewportSize}set viewportSize(t){const{_viewDim1:i,_viewDim2:s}=this;Object.assign(this._viewportSize,t),s!==this._viewDim2?this._scheduleLayoutUpdate():i!==this._viewDim1&&this._checkThresholds()}get viewportScroll(){return this._latestCoords}set viewportScroll(t){Object.assign(this._latestCoords,t);const i=this._scrollPosition;this._scrollPosition=this._latestCoords[this._positionDim],i!==this._scrollPosition&&(this._scrollPositionChanged(i,this._scrollPosition),this._updateVisibleIndices({emit:!0})),this._checkThresholds()}reflowIfNeeded(t=!1){(t||this._pendingReflow)&&(this._pendingReflow=!1,this._reflow())}scrollToIndex(t,i="start"){if(Number.isFinite(t)){switch(t=Math.min(this.totalItems,Math.max(0,t)),this._scrollToIndex=t,"nearest"===i&&(i=t>this._first+this._num/2?"end":"start"),i){case"start":this._scrollToAnchor=0;break;case"center":this._scrollToAnchor=.5;break;case"end":this._scrollToAnchor=1;break;default:throw new TypeError("position must be one of: start, center, end, nearest")}this._scheduleReflow()}}async dispatchEvent(t){await this._eventTargetPromise,this._eventTarget.dispatchEvent(t)}async addEventListener(t,i,s){await this._eventTargetPromise,this._eventTarget.addEventListener(t,i,s)}async removeEventListener(t,i,s){await this._eventTargetPromise,this._eventTarget.removeEventListener(t,i,s)}_updateLayout(){}get _viewDim1(){return this._viewportSize[this._sizeDim]}get _viewDim2(){return this._viewportSize[this._secondarySizeDim]}_scheduleReflow(){this._pendingReflow=!0}_scheduleLayoutUpdate(){this._pendingLayoutUpdate=!0,this._scheduleReflow()}_triggerReflow(){this._scheduleLayoutUpdate(),Promise.resolve().then((()=>this.reflowIfNeeded()))}_reflow(){this._pendingLayoutUpdate&&(this._updateLayout(),this._pendingLayoutUpdate=!1),this._updateScrollSize(),this._getActiveItems(),this._scrollIfNeeded(),this._updateVisibleIndices(),this._emitScrollSize(),this._emitRange(),this._emitChildPositions(),this._emitScrollError()}_scrollIfNeeded(){if(-1===this._scrollToIndex)return;const t=this._scrollToIndex,i=this._scrollToAnchor,s=this._getItemPosition(t)[this._positionDim],e=this._getItemSize(t)[this._sizeDim],h=this._scrollPosition+this._viewDim1*i,r=s+e*i,a=Math.floor(Math.min(this._scrollSize-this._viewDim1,Math.max(0,this._scrollPosition-h+r)));this._scrollError+=this._scrollPosition-a,this._scrollPosition=a}_emitRange(t){const i=Object.assign({first:this._first,last:this._last,num:this._num,stable:!0,firstVisible:this._firstVisible,lastVisible:this._lastVisible},t);this.dispatchEvent(new CustomEvent("rangechange",{detail:i}))}_emitScrollSize(){const t={[this._sizeDim]:this._scrollSize};this.dispatchEvent(new CustomEvent("scrollsizechange",{detail:t}))}_emitScrollError(){if(this._scrollError){const t={[this._positionDim]:this._scrollError,[this._secondaryPositionDim]:0};this.dispatchEvent(new CustomEvent("scrollerrorchange",{detail:t})),this._scrollError=0}}_emitChildPositions(){const t={};for(let i=this._first;i<=this._last;i++)t[i]=this._getItemPosition(i);this.dispatchEvent(new CustomEvent("itempositionchange",{detail:t}))}get _num(){return-1===this._first||-1===this._last?0:this._last-this._first+1}_checkThresholds(){if(0===this._viewDim1&&this._num>0)this._scheduleReflow();else{const t=Math.max(0,this._scrollPosition-this._overhang),i=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang);(this._physicalMin>t||this._physicalMax<i)&&this._scheduleReflow()}}_updateVisibleIndices(t){if(-1===this._first||-1===this._last)return;let i=this._first;for(;i<this._last&&Math.round(this._getItemPosition(i)[this._positionDim]+this._getItemSize(i)[this._sizeDim])<=Math.round(this._scrollPosition);)i++;let s=this._last;for(;s>this._first&&Math.round(this._getItemPosition(s)[this._positionDim])>=Math.round(this._scrollPosition+this._viewDim1);)s--;i===this._firstVisible&&s===this._lastVisible||(this._firstVisible=i,this._lastVisible=s,t&&t.emit&&this._emitRange())}_scrollPositionChanged(t,i){const s=this._scrollSize-this._viewDim1;(t<s||i<s)&&(this._scrollToIndex=-1)}}{constructor(){super(...arguments),this._itemSize={width:100,height:100},this._physicalItems=new Map,this._newPhysicalItems=new Map,this._metricsCache=new c,this._anchorIdx=null,this._anchorPos=null,this._stable=!0,this._needsRemeasure=!1,this._measureChildren=!0,this._estimate=!0}get measureChildren(){return this._measureChildren}updateItemSizes(t){this._metricsCache.update(t,this.direction),this._scheduleReflow()}_getPhysicalItem(t){var i;return null!==(i=this._newPhysicalItems.get(t))&&void 0!==i?i:this._physicalItems.get(t)}_getSize(t){return this._getPhysicalItem(t)&&this._metricsCache.getChildSize(t)}_getAverageSize(){return this._metricsCache.averageChildSize||this._itemSize[this._sizeDim]}_getPosition(t){var i;const s=this._getPhysicalItem(t),{averageMarginSize:e}=this._metricsCache;return 0===t?null!==(i=this._metricsCache.getMarginSize(0))&&void 0!==i?i:e:s?s.pos:e+t*(e+this._getAverageSize())}_calculateAnchor(t,i){return t<=0?0:i>this._scrollSize-this._viewDim1?this._totalItems-1:Math.max(0,Math.min(this._totalItems-1,Math.floor((t+i)/2/this._delta)))}_getAnchor(t,i){if(0===this._physicalItems.size)return this._calculateAnchor(t,i);if(this._first<0)return console.error("_getAnchor: negative _first"),this._calculateAnchor(t,i);if(this._last<0)return console.error("_getAnchor: negative _last"),this._calculateAnchor(t,i);const s=this._getPhysicalItem(this._first),e=this._getPhysicalItem(this._last),h=s.pos;if(e.pos+this._metricsCache.getChildSize(this._last)<t)return this._calculateAnchor(t,i);if(h>i)return this._calculateAnchor(t,i);let r=this._firstVisible-1,a=-1/0;for(;a<t;){a=this._getPhysicalItem(++r).pos+this._metricsCache.getChildSize(r)}return r}_getActiveItems(){0===this._viewDim1||0===this._totalItems?this._clearItems():this._getItems()}_clearItems(){this._first=-1,this._last=-1,this._physicalMin=0,this._physicalMax=0;const t=this._newPhysicalItems;this._newPhysicalItems=this._physicalItems,this._newPhysicalItems.clear(),this._physicalItems=t,this._stable=!0}_getItems(){var t,i;const s=this._newPhysicalItems;let e,h;if(this._stable=!0,this._scrollToIndex>=0&&(this._anchorIdx=Math.min(this._scrollToIndex,this._totalItems-1),this._anchorPos=this._getPosition(this._anchorIdx),this._scrollIfNeeded()),e=this._scrollPosition-this._overhang,h=this._scrollPosition+this._viewDim1+this._overhang,h<0||e>this._scrollSize)return void this._clearItems();null!==this._anchorIdx&&null!==this._anchorPos||(this._anchorIdx=this._getAnchor(e,h),this._anchorPos=this._getPosition(this._anchorIdx));let r=this._getSize(this._anchorIdx);void 0===r&&(this._stable=!1,r=this._getAverageSize());let a=null!==(t=this._metricsCache.getMarginSize(this._anchorIdx))&&void 0!==t?t:this._metricsCache.averageMarginSize,o=null!==(i=this._metricsCache.getMarginSize(this._anchorIdx+1))&&void 0!==i?i:this._metricsCache.averageMarginSize;0===this._anchorIdx&&(this._anchorPos=a),this._anchorIdx===this._totalItems-1&&(this._anchorPos=this._scrollSize-o-r);let _=0;for(this._anchorPos+r+o<e&&(_=e-(this._anchorPos+r+o)),this._anchorPos-a>h&&(_=h-(this._anchorPos-a)),_&&(this._scrollPosition-=_,e-=_,h-=_,this._scrollError+=_),s.set(this._anchorIdx,{pos:this._anchorPos,size:r}),this._first=this._last=this._anchorIdx,this._physicalMin=this._anchorPos,this._physicalMax=this._anchorPos+r;this._physicalMin>e&&this._first>0;){let t=this._getSize(--this._first);void 0===t&&(this._stable=!1,t=this._getAverageSize());let i=this._metricsCache.getMarginSize(this._first+1);void 0===i&&(this._stable=!1,i=this._metricsCache.averageMarginSize),this._physicalMin-=t+i;const e=this._physicalMin;if(s.set(this._first,{pos:e,size:t}),!1===this._stable&&!1===this._estimate)break}for(;this._physicalMax<h&&this._last<this._totalItems-1;){let t=this._metricsCache.getMarginSize(++this._last);void 0===t&&(this._stable=!1,t=this._metricsCache.averageMarginSize);let i=this._getSize(this._last);void 0===i&&(this._stable=!1,i=this._getAverageSize());const e=this._physicalMax+t;if(s.set(this._last,{pos:e,size:i}),this._physicalMax+=t+i,!1===this._stable&&!1===this._estimate)break}const l=this._calculateError();l&&(this._physicalMin-=l,this._physicalMax-=l,this._anchorPos-=l,this._scrollPosition-=l,s.forEach((t=>t.pos-=l)),this._scrollError+=l),this._stable&&(this._newPhysicalItems=this._physicalItems,this._newPhysicalItems.clear(),this._physicalItems=s)}_calculateError(){var t,i;const{averageMarginSize:s}=this._metricsCache;return 0===this._first?this._physicalMin-(null!==(t=this._metricsCache.getMarginSize(0))&&void 0!==t?t:s):this._physicalMin<=0?this._physicalMin-this._first*this._delta:this._last===this._totalItems-1?this._physicalMax+(null!==(i=this._metricsCache.getMarginSize(this._totalItems))&&void 0!==i?i:s)-this._scrollSize:this._physicalMax>=this._scrollSize?this._physicalMax-this._scrollSize+(this._totalItems-1-this._last)*this._delta:0}_reflow(){const{_first:t,_last:i,_scrollSize:s}=this;this._updateScrollSize(),this._getActiveItems(),this._scrollSize!==s&&this._emitScrollSize(),this._updateVisibleIndices(),this._emitRange(),-1===this._first&&-1===this._last?this._resetReflowState():this._first!==t||this._last!==i||this._needsRemeasure?(this._emitChildPositions(),this._emitScrollError()):(this._emitChildPositions(),this._emitScrollError(),this._resetReflowState())}_resetReflowState(){this._anchorIdx=null,this._anchorPos=null,this._stable=!0}_updateScrollSize(){const{averageMarginSize:t}=this._metricsCache;this._scrollSize=Math.max(1,this._totalItems*(t+this._getAverageSize())+t)}get _delta(){const{averageMarginSize:t}=this._metricsCache;return this._getAverageSize()+t}_getItemPosition(t){var i,s;return{[this._positionDim]:this._getPosition(t),[this._secondaryPositionDim]:0,[(s=this.direction,"horizontal"===s?"xOffset":"yOffset")]:-(null!==(i=this._metricsCache.getLeadingMarginValue(t,this.direction))&&void 0!==i?i:this._metricsCache.averageMarginSize)}}_getItemSize(t){var i;return{[this._sizeDim]:(this._getSize(t)||this._getAverageSize())+(null!==(i=this._metricsCache.getMarginSize(t+1))&&void 0!==i?i:this._metricsCache.averageMarginSize),[this._secondarySizeDim]:this._itemSize[this._secondarySizeDim]}}_viewDim2Changed(){this._needsRemeasure=!0,this._scheduleReflow()}_emitRange(){const t=this._needsRemeasure,i=this._stable;this._needsRemeasure=!1,super._emitRange({remeasure:t,stable:i})}}}}]);