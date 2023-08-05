"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[1250],{23682:function(t,e,n){function r(t,e){if(e.length<t)throw new TypeError(t+" argument"+(t>1?"s":"")+" required, but only "+e.length+" present")}n.d(e,{Z:function(){return r}})},90394:function(t,e,n){function r(t){if(null===t||!0===t||!1===t)return NaN;var e=Number(t);return isNaN(e)?e:e<0?Math.ceil(e):Math.floor(e)}n.d(e,{Z:function(){return r}})},79021:function(t,e,n){n.d(e,{Z:function(){return a}});var r=n(90394),u=n(34327),o=n(23682);function a(t,e){(0,o.Z)(2,arguments);var n=(0,u.Z)(t),a=(0,r.Z)(e);return isNaN(a)?new Date(NaN):a?(n.setDate(n.getDate()+a),n):n}},59699:function(t,e,n){n.d(e,{Z:function(){return i}});var r=n(90394),u=n(39244),o=n(23682),a=36e5;function i(t,e){(0,o.Z)(2,arguments);var n=(0,r.Z)(e);return(0,u.Z)(t,n*a)}},39244:function(t,e,n){n.d(e,{Z:function(){return a}});var r=n(90394),u=n(34327),o=n(23682);function a(t,e){(0,o.Z)(2,arguments);var n=(0,u.Z)(t).getTime(),a=(0,r.Z)(e);return new Date(n+a)}},32182:function(t,e,n){n.d(e,{Z:function(){return a}});var r=n(90394),u=n(34327),o=n(23682);function a(t,e){(0,o.Z)(2,arguments);var n=(0,u.Z)(t),a=(0,r.Z)(e);if(isNaN(a))return new Date(NaN);if(!a)return n;var i=n.getDate(),s=new Date(n.getTime());s.setMonth(n.getMonth()+a+1,0);var c=s.getDate();return i>=c?s:(n.setFullYear(s.getFullYear(),s.getMonth(),i),n)}},33651:function(t,e,n){n.d(e,{Z:function(){return a}});var r=n(90394),u=n(79021),o=n(23682);function a(t,e){(0,o.Z)(2,arguments);var n=(0,r.Z)(e),a=7*n;return(0,u.Z)(t,a)}},27605:function(t,e,n){n.d(e,{Z:function(){return a}});var r=n(90394),u=n(32182),o=n(23682);function a(t,e){(0,o.Z)(2,arguments);var n=(0,r.Z)(e);return(0,u.Z)(t,12*n)}},4535:function(t,e,n){n.d(e,{Z:function(){return f}});var r=n(34327);function u(t){var e=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return e.setUTCFullYear(t.getFullYear()),t.getTime()-e.getTime()}var o=n(59429),a=n(23682),i=864e5;function s(t,e){(0,a.Z)(2,arguments);var n=(0,o.Z)(t),r=(0,o.Z)(e),s=n.getTime()-u(n),c=r.getTime()-u(r);return Math.round((s-c)/i)}function c(t,e){var n=t.getFullYear()-e.getFullYear()||t.getMonth()-e.getMonth()||t.getDate()-e.getDate()||t.getHours()-e.getHours()||t.getMinutes()-e.getMinutes()||t.getSeconds()-e.getSeconds()||t.getMilliseconds()-e.getMilliseconds();return n<0?-1:n>0?1:n}function f(t,e){(0,a.Z)(2,arguments);var n=(0,r.Z)(t),u=(0,r.Z)(e),o=c(n,u),i=Math.abs(s(n,u));n.setDate(n.getDate()-o*i);var f=Number(c(n,u)===-o),l=o*(i-f);return 0===l?0:l}},93752:function(t,e,n){n.d(e,{Z:function(){return o}});var r=n(34327),u=n(23682);function o(t){(0,u.Z)(1,arguments);var e=(0,r.Z)(t);return e.setHours(23,59,59,999),e}},1905:function(t,e,n){n.d(e,{Z:function(){return o}});var r=n(34327),u=n(23682);function o(t){(0,u.Z)(1,arguments);var e=(0,r.Z)(t),n=e.getMonth();return e.setFullYear(e.getFullYear(),n+1,0),e.setHours(23,59,59,999),e}},59281:function(t,e,n){n.d(e,{Z:function(){return a}});var r=n(34327),u=n(90394),o=n(23682);function a(t,e){(0,o.Z)(1,arguments);var n=e||{},a=n.locale,i=a&&a.options&&a.options.weekStartsOn,s=null==i?0:(0,u.Z)(i),c=null==n.weekStartsOn?s:(0,u.Z)(n.weekStartsOn);if(!(c>=0&&c<=6))throw new RangeError("weekStartsOn must be between 0 and 6 inclusively");var f=(0,r.Z)(t),l=f.getDay(),Z=6+(l<c?-7:0)-(l-c);return f.setDate(f.getDate()+Z),f.setHours(23,59,59,999),f}},70451:function(t,e,n){n.d(e,{Z:function(){return o}});var r=n(34327),u=n(23682);function o(t){(0,u.Z)(1,arguments);var e=(0,r.Z)(t),n=e.getFullYear();return e.setFullYear(n+1,0,0),e.setHours(23,59,59,999),e}},59429:function(t,e,n){n.d(e,{Z:function(){return o}});var r=n(34327),u=n(23682);function o(t){(0,u.Z)(1,arguments);var e=(0,r.Z)(t);return e.setHours(0,0,0,0),e}},13250:function(t,e,n){n.d(e,{Z:function(){return o}});var r=n(34327),u=n(23682);function o(t){(0,u.Z)(1,arguments);var e=(0,r.Z)(t);return e.setDate(1),e.setHours(0,0,0,0),e}},59401:function(t,e,n){n.d(e,{Z:function(){return a}});var r=n(34327),u=n(90394),o=n(23682);function a(t,e){(0,o.Z)(1,arguments);var n=e||{},a=n.locale,i=a&&a.options&&a.options.weekStartsOn,s=null==i?0:(0,u.Z)(i),c=null==n.weekStartsOn?s:(0,u.Z)(n.weekStartsOn);if(!(c>=0&&c<=6))throw new RangeError("weekStartsOn must be between 0 and 6 inclusively");var f=(0,r.Z)(t),l=f.getDay(),Z=(l<c?7:0)+l-c;return f.setDate(f.getDate()-Z),f.setHours(0,0,0,0),f}},69388:function(t,e,n){n.d(e,{Z:function(){return o}});var r=n(34327),u=n(23682);function o(t){(0,u.Z)(1,arguments);var e=(0,r.Z)(t),n=new Date(0);return n.setFullYear(e.getFullYear(),0,1),n.setHours(0,0,0,0),n}},34327:function(t,e,n){n.d(e,{Z:function(){return o}});var r=n(23682);function u(t){return u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},u(t)}function o(t){(0,r.Z)(1,arguments);var e=Object.prototype.toString.call(t);return t instanceof Date||"object"===u(t)&&"[object Date]"===e?new Date(t.getTime()):"number"==typeof t||"[object Number]"===e?new Date(t):("string"!=typeof t&&"[object String]"!==e||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://git.io/fjule"),console.warn((new Error).stack)),new Date(NaN))}}}]);