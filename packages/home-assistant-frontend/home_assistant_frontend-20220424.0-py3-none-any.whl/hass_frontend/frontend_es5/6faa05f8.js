/*! For license information please see 6faa05f8.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[947],{21157:function(e,n,t){var i;t(48175);var r,o,l=(0,t(50856).d)(i||(r=['\n/* Most common used flex styles*/\n<dom-module id="iron-flex">\n  <template>\n    <style>\n      .layout.horizontal,\n      .layout.vertical {\n        display: -ms-flexbox;\n        display: -webkit-flex;\n        display: flex;\n      }\n\n      .layout.inline {\n        display: -ms-inline-flexbox;\n        display: -webkit-inline-flex;\n        display: inline-flex;\n      }\n\n      .layout.horizontal {\n        -ms-flex-direction: row;\n        -webkit-flex-direction: row;\n        flex-direction: row;\n      }\n\n      .layout.vertical {\n        -ms-flex-direction: column;\n        -webkit-flex-direction: column;\n        flex-direction: column;\n      }\n\n      .layout.wrap {\n        -ms-flex-wrap: wrap;\n        -webkit-flex-wrap: wrap;\n        flex-wrap: wrap;\n      }\n\n      .layout.no-wrap {\n        -ms-flex-wrap: nowrap;\n        -webkit-flex-wrap: nowrap;\n        flex-wrap: nowrap;\n      }\n\n      .layout.center,\n      .layout.center-center {\n        -ms-flex-align: center;\n        -webkit-align-items: center;\n        align-items: center;\n      }\n\n      .layout.center-justified,\n      .layout.center-center {\n        -ms-flex-pack: center;\n        -webkit-justify-content: center;\n        justify-content: center;\n      }\n\n      .flex {\n        -ms-flex: 1 1 0.000000001px;\n        -webkit-flex: 1;\n        flex: 1;\n        -webkit-flex-basis: 0.000000001px;\n        flex-basis: 0.000000001px;\n      }\n\n      .flex-auto {\n        -ms-flex: 1 1 auto;\n        -webkit-flex: 1 1 auto;\n        flex: 1 1 auto;\n      }\n\n      .flex-none {\n        -ms-flex: none;\n        -webkit-flex: none;\n        flex: none;\n      }\n    </style>\n  </template>\n</dom-module>\n/* Basic flexbox reverse styles */\n<dom-module id="iron-flex-reverse">\n  <template>\n    <style>\n      .layout.horizontal-reverse,\n      .layout.vertical-reverse {\n        display: -ms-flexbox;\n        display: -webkit-flex;\n        display: flex;\n      }\n\n      .layout.horizontal-reverse {\n        -ms-flex-direction: row-reverse;\n        -webkit-flex-direction: row-reverse;\n        flex-direction: row-reverse;\n      }\n\n      .layout.vertical-reverse {\n        -ms-flex-direction: column-reverse;\n        -webkit-flex-direction: column-reverse;\n        flex-direction: column-reverse;\n      }\n\n      .layout.wrap-reverse {\n        -ms-flex-wrap: wrap-reverse;\n        -webkit-flex-wrap: wrap-reverse;\n        flex-wrap: wrap-reverse;\n      }\n    </style>\n  </template>\n</dom-module>\n/* Flexbox alignment */\n<dom-module id="iron-flex-alignment">\n  <template>\n    <style>\n      /**\n       * Alignment in cross axis.\n       */\n      .layout.start {\n        -ms-flex-align: start;\n        -webkit-align-items: flex-start;\n        align-items: flex-start;\n      }\n\n      .layout.center,\n      .layout.center-center {\n        -ms-flex-align: center;\n        -webkit-align-items: center;\n        align-items: center;\n      }\n\n      .layout.end {\n        -ms-flex-align: end;\n        -webkit-align-items: flex-end;\n        align-items: flex-end;\n      }\n\n      .layout.baseline {\n        -ms-flex-align: baseline;\n        -webkit-align-items: baseline;\n        align-items: baseline;\n      }\n\n      /**\n       * Alignment in main axis.\n       */\n      .layout.start-justified {\n        -ms-flex-pack: start;\n        -webkit-justify-content: flex-start;\n        justify-content: flex-start;\n      }\n\n      .layout.center-justified,\n      .layout.center-center {\n        -ms-flex-pack: center;\n        -webkit-justify-content: center;\n        justify-content: center;\n      }\n\n      .layout.end-justified {\n        -ms-flex-pack: end;\n        -webkit-justify-content: flex-end;\n        justify-content: flex-end;\n      }\n\n      .layout.around-justified {\n        -ms-flex-pack: distribute;\n        -webkit-justify-content: space-around;\n        justify-content: space-around;\n      }\n\n      .layout.justified {\n        -ms-flex-pack: justify;\n        -webkit-justify-content: space-between;\n        justify-content: space-between;\n      }\n\n      /**\n       * Self alignment.\n       */\n      .self-start {\n        -ms-align-self: flex-start;\n        -webkit-align-self: flex-start;\n        align-self: flex-start;\n      }\n\n      .self-center {\n        -ms-align-self: center;\n        -webkit-align-self: center;\n        align-self: center;\n      }\n\n      .self-end {\n        -ms-align-self: flex-end;\n        -webkit-align-self: flex-end;\n        align-self: flex-end;\n      }\n\n      .self-stretch {\n        -ms-align-self: stretch;\n        -webkit-align-self: stretch;\n        align-self: stretch;\n      }\n\n      .self-baseline {\n        -ms-align-self: baseline;\n        -webkit-align-self: baseline;\n        align-self: baseline;\n      }\n\n      /**\n       * multi-line alignment in main axis.\n       */\n      .layout.start-aligned {\n        -ms-flex-line-pack: start;  /* IE10 */\n        -ms-align-content: flex-start;\n        -webkit-align-content: flex-start;\n        align-content: flex-start;\n      }\n\n      .layout.end-aligned {\n        -ms-flex-line-pack: end;  /* IE10 */\n        -ms-align-content: flex-end;\n        -webkit-align-content: flex-end;\n        align-content: flex-end;\n      }\n\n      .layout.center-aligned {\n        -ms-flex-line-pack: center;  /* IE10 */\n        -ms-align-content: center;\n        -webkit-align-content: center;\n        align-content: center;\n      }\n\n      .layout.between-aligned {\n        -ms-flex-line-pack: justify;  /* IE10 */\n        -ms-align-content: space-between;\n        -webkit-align-content: space-between;\n        align-content: space-between;\n      }\n\n      .layout.around-aligned {\n        -ms-flex-line-pack: distribute;  /* IE10 */\n        -ms-align-content: space-around;\n        -webkit-align-content: space-around;\n        align-content: space-around;\n      }\n    </style>\n  </template>\n</dom-module>\n/* Non-flexbox positioning helper styles */\n<dom-module id="iron-flex-factors">\n  <template>\n    <style>\n      .flex,\n      .flex-1 {\n        -ms-flex: 1 1 0.000000001px;\n        -webkit-flex: 1;\n        flex: 1;\n        -webkit-flex-basis: 0.000000001px;\n        flex-basis: 0.000000001px;\n      }\n\n      .flex-2 {\n        -ms-flex: 2;\n        -webkit-flex: 2;\n        flex: 2;\n      }\n\n      .flex-3 {\n        -ms-flex: 3;\n        -webkit-flex: 3;\n        flex: 3;\n      }\n\n      .flex-4 {\n        -ms-flex: 4;\n        -webkit-flex: 4;\n        flex: 4;\n      }\n\n      .flex-5 {\n        -ms-flex: 5;\n        -webkit-flex: 5;\n        flex: 5;\n      }\n\n      .flex-6 {\n        -ms-flex: 6;\n        -webkit-flex: 6;\n        flex: 6;\n      }\n\n      .flex-7 {\n        -ms-flex: 7;\n        -webkit-flex: 7;\n        flex: 7;\n      }\n\n      .flex-8 {\n        -ms-flex: 8;\n        -webkit-flex: 8;\n        flex: 8;\n      }\n\n      .flex-9 {\n        -ms-flex: 9;\n        -webkit-flex: 9;\n        flex: 9;\n      }\n\n      .flex-10 {\n        -ms-flex: 10;\n        -webkit-flex: 10;\n        flex: 10;\n      }\n\n      .flex-11 {\n        -ms-flex: 11;\n        -webkit-flex: 11;\n        flex: 11;\n      }\n\n      .flex-12 {\n        -ms-flex: 12;\n        -webkit-flex: 12;\n        flex: 12;\n      }\n    </style>\n  </template>\n</dom-module>\n<dom-module id="iron-positioning">\n  <template>\n    <style>\n      .block {\n        display: block;\n      }\n\n      [hidden] {\n        display: none !important;\n      }\n\n      .invisible {\n        visibility: hidden !important;\n      }\n\n      .relative {\n        position: relative;\n      }\n\n      .fit {\n        position: absolute;\n        top: 0;\n        right: 0;\n        bottom: 0;\n        left: 0;\n      }\n\n      body.fullbleed {\n        margin: 0;\n        height: 100vh;\n      }\n\n      .scroll {\n        -webkit-overflow-scrolling: touch;\n        overflow: auto;\n      }\n\n      /* fixed position */\n      .fixed-bottom,\n      .fixed-left,\n      .fixed-right,\n      .fixed-top {\n        position: fixed;\n      }\n\n      .fixed-top {\n        top: 0;\n        left: 0;\n        right: 0;\n      }\n\n      .fixed-right {\n        top: 0;\n        right: 0;\n        bottom: 0;\n      }\n\n      .fixed-bottom {\n        right: 0;\n        bottom: 0;\n        left: 0;\n      }\n\n      .fixed-left {\n        top: 0;\n        bottom: 0;\n        left: 0;\n      }\n    </style>\n  </template>\n</dom-module>\n'],o||(o=r.slice(0)),i=Object.freeze(Object.defineProperties(r,{raw:{value:Object.freeze(o)}}))));l.setAttribute("style","display: none;"),document.head.appendChild(l.content)},24381:function(e,n,t){t.d(n,{Q:function(){return i}});var i=function(e,n){return e?n.map((function(n){return n in e.attributes?"has-"+n:""})).filter((function(e){return""!==e})).join(" "):""}},73139:function(e,n,t){var i,r=t(50856),o=t(28426);t(28007),t(46998);function l(e){return l="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},l(e)}function a(e,n){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}function s(e,n){for(var t=0;t<n.length;t++){var i=n[t];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}function c(e,n){return c=Object.setPrototypeOf||function(e,n){return e.__proto__=n,e},c(e,n)}function f(e){var n=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var t,i=p(e);if(n){var r=p(this).constructor;t=Reflect.construct(i,arguments,r)}else t=i.apply(this,arguments);return u(this,t)}}function u(e,n){if(n&&("object"===l(n)||"function"==typeof n))return n;if(void 0!==n)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function p(e){return p=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},p(e)}var d=function(e){!function(e,n){if("function"!=typeof n&&null!==n)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(n&&n.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),n&&c(e,n)}(u,e);var n,t,o,l=f(u);function u(){return a(this,u),l.apply(this,arguments)}return n=u,o=[{key:"template",get:function(){return(0,r.d)(i||(e=['\n      <style>\n        :host {\n          display: block;\n        }\n\n        .title {\n          margin: 5px 0 8px;\n          color: var(--primary-text-color);\n        }\n\n        .slider-container {\n          display: flex;\n        }\n\n        ha-icon {\n          margin-top: 4px;\n          color: var(--secondary-text-color);\n        }\n\n        ha-slider {\n          flex-grow: 1;\n          background-image: var(--ha-slider-background);\n          border-radius: 4px;\n        }\n      </style>\n\n      <div class="title">[[_getTitle()]]</div>\n      <div class="extra-container"><slot name="extra"></slot></div>\n      <div class="slider-container">\n        <ha-icon icon="[[icon]]" hidden$="[[!icon]]"></ha-icon>\n        <ha-slider\n          min="[[min]]"\n          max="[[max]]"\n          step="[[step]]"\n          pin="[[pin]]"\n          disabled="[[disabled]]"\n          value="{{value}}"\n        ></ha-slider>\n      </div>\n      <template is="dom-if" if="[[helper]]">\n        <ha-input-helper-text>[[helper]]</ha-input-helper-text>\n      </template>\n    '],n||(n=e.slice(0)),i=Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(n)}}))));var e,n}},{key:"properties",get:function(){return{caption:String,disabled:Boolean,required:Boolean,min:Number,max:Number,pin:Boolean,step:Number,helper:String,extra:{type:Boolean,value:!1},ignoreBarTouch:{type:Boolean,value:!0},icon:{type:String,value:""},value:{type:Number,notify:!0}}}}],(t=[{key:"_getTitle",value:function(){return"".concat(this.caption).concat(this.caption&&this.required?" *":"")}}])&&s(n.prototype,t),o&&s(n,o),u}(o.H3);customElements.define("ha-labeled-slider",d)},947:function(e,n,t){t.r(n);t(44577),t(21157);var i,r=t(50856),o=t(28426),l=t(24381),a=t(40095),s=(t(31811),t(28007),t(10983),t(73139),t(86630),t(43709),t(11052));function c(e){return c="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},c(e)}function f(e,n){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}function u(e,n){for(var t=0;t<n.length;t++){var i=n[t];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}function p(e,n){return p=Object.setPrototypeOf||function(e,n){return e.__proto__=n,e},p(e,n)}function d(e){var n=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var t,i=y(e);if(n){var r=y(this).constructor;t=Reflect.construct(i,arguments,r)}else t=i.apply(this,arguments);return b(this,t)}}function b(e,n){if(n&&("object"===c(n)||"function"==typeof n))return n;if(void 0!==n)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function y(e){return y=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},y(e)}var m=function(e){!function(e,n){if("function"!=typeof n&&null!==n)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(n&&n.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),n&&p(e,n)}(c,e);var n,t,o,s=d(c);function c(){return f(this,c),s.apply(this,arguments)}return n=c,o=[{key:"template",get:function(){return(0,r.d)(i||(e=['\n      <style include="iron-flex"></style>\n      <style>\n        .container-preset_modes,\n        .container-direction,\n        .container-percentage,\n        .container-oscillating {\n          display: none;\n        }\n\n        .has-percentage .container-percentage,\n        .has-preset_modes .container-preset_modes,\n        .has-direction .container-direction,\n        .has-oscillating .container-oscillating {\n          display: block;\n          margin-top: 8px;\n        }\n\n        ha-select {\n          width: 100%;\n        }\n      </style>\n\n      <div class$="[[computeClassNames(stateObj)]]">\n        <div class="container-percentage">\n          <ha-labeled-slider\n            caption="[[localize(\'ui.card.fan.speed\')]]"\n            min="0"\n            max="100"\n            step="[[computePercentageStepSize(stateObj)]]"\n            value="{{percentageSliderValue}}"\n            on-change="percentageChanged"\n            pin=""\n            extra=""\n          ></ha-labeled-slider>\n        </div>\n\n        <div class="container-preset_modes">\n          <ha-select\n            label="[[localize(\'ui.card.fan.preset_mode\')]]"\n            value="[[stateObj.attributes.preset_mode]]"\n            on-selected="presetModeChanged"\n            fixedMenuPosition\n            naturalMenuWidth\n            on-closed="stopPropagation"\n          >\n            <template\n              is="dom-repeat"\n              items="[[stateObj.attributes.preset_modes]]"\n            >\n              <mwc-list-item value="[[item]]">[[item]]</mwc-list-item>\n            </template>\n          </ha-select>\n        </div>\n\n        <div class="container-oscillating">\n          <div class="center horizontal layout single-row">\n            <div class="flex">[[localize(\'ui.card.fan.oscillate\')]]</div>\n            <ha-switch\n              checked="[[oscillationToggleChecked]]"\n              on-change="oscillationToggleChanged"\n            >\n            </ha-switch>\n          </div>\n        </div>\n\n        <div class="container-direction">\n          <div class="direction">\n            <div>[[localize(\'ui.card.fan.direction\')]]</div>\n            <ha-icon-button\n              on-click="onDirectionReverse"\n              title="[[localize(\'ui.card.fan.reverse\')]]"\n              disabled="[[computeIsRotatingReverse(stateObj)]]"\n            >\n              <ha-icon icon="hass:rotate-left"></ha-icon>\n            </ha-icon-button>\n            <ha-icon-button\n              on-click="onDirectionForward"\n              title="[[localize(\'ui.card.fan.forward\')]]"\n              disabled="[[computeIsRotatingForward(stateObj)]]"\n            >\n              <ha-icon icon="hass:rotate-right"></ha-icon>\n            </ha-icon-button>\n          </div>\n        </div>\n      </div>\n\n      <ha-attributes\n        hass="[[hass]]"\n        state-obj="[[stateObj]]"\n        extra-filters="percentage_step,speed,preset_mode,preset_modes,speed_list,percentage,oscillating,direction"\n      ></ha-attributes>\n    '],n||(n=e.slice(0)),i=Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(n)}}))));var e,n}},{key:"properties",get:function(){return{hass:{type:Object},stateObj:{type:Object,observer:"stateObjChanged"},oscillationToggleChecked:{type:Boolean},percentageSliderValue:{type:Number}}}}],(t=[{key:"stateObjChanged",value:function(e,n){var t=this;e&&this.setProperties({oscillationToggleChecked:e.attributes.oscillating,percentageSliderValue:e.attributes.percentage}),n&&setTimeout((function(){t.fire("iron-resize")}),500)}},{key:"computePercentageStepSize",value:function(e){return e.attributes.percentage_step?e.attributes.percentage_step:1}},{key:"computeClassNames",value:function(e){return"more-info-fan "+((0,a.e)(e,1)?"has-percentage ":"")+(e.attributes.preset_modes&&e.attributes.preset_modes.length?"has-preset_modes ":"")+(0,l.Q)(e,["oscillating","direction"])}},{key:"presetModeChanged",value:function(e){var n=this.stateObj.attributes.preset_mode,t=e.target.value;t&&n!==t&&this.hass.callService("fan","set_preset_mode",{entity_id:this.stateObj.entity_id,preset_mode:t})}},{key:"stopPropagation",value:function(e){e.stopPropagation()}},{key:"percentageChanged",value:function(e){var n=parseInt(this.stateObj.attributes.percentage,10),t=e.target.value;isNaN(t)||n===t||this.hass.callService("fan","set_percentage",{entity_id:this.stateObj.entity_id,percentage:t})}},{key:"oscillationToggleChanged",value:function(e){var n=this.stateObj.attributes.oscillating,t=e.target.checked;n!==t&&this.hass.callService("fan","oscillate",{entity_id:this.stateObj.entity_id,oscillating:t})}},{key:"onDirectionReverse",value:function(){this.hass.callService("fan","set_direction",{entity_id:this.stateObj.entity_id,direction:"reverse"})}},{key:"onDirectionForward",value:function(){this.hass.callService("fan","set_direction",{entity_id:this.stateObj.entity_id,direction:"forward"})}},{key:"computeIsRotatingReverse",value:function(e){return"reverse"===e.attributes.direction}},{key:"computeIsRotatingForward",value:function(e){return"forward"===e.attributes.direction}}])&&u(n.prototype,t),o&&u(n,o),c}((0,t(1265).Z)((0,s.I)(o.H3)));customElements.define("more-info-fan",m)},1265:function(e,n,t){var i=t(76389);function r(e){return r="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},r(e)}function o(e,n){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}function l(e,n){for(var t=0;t<n.length;t++){var i=n[t];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}function a(e,n){return a=Object.setPrototypeOf||function(e,n){return e.__proto__=n,e},a(e,n)}function s(e){var n=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var t,i=f(e);if(n){var r=f(this).constructor;t=Reflect.construct(i,arguments,r)}else t=i.apply(this,arguments);return c(this,t)}}function c(e,n){if(n&&("object"===r(n)||"function"==typeof n))return n;if(void 0!==n)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function f(e){return f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},f(e)}n.Z=(0,i.o)((function(e){return function(e){!function(e,n){if("function"!=typeof n&&null!==n)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(n&&n.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),n&&a(e,n)}(c,e);var n,t,i,r=s(c);function c(){return o(this,c),r.apply(this,arguments)}return n=c,i=[{key:"properties",get:function(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}}],(t=[{key:"__computeLocalize",value:function(e){return e}}])&&l(n.prototype,t),i&&l(n,i),c}(e)}))}}]);