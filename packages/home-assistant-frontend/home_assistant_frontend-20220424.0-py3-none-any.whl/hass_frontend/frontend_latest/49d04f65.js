"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[20020],{20020:(e,s,t)=>{t.r(s),t.d(s,{attachExternalToApp:()=>n});var a=t(47181);const n=e=>{window.addEventListener("haptic",(s=>e.hass.auth.external.fireMessage({type:"haptic",payload:{hapticType:s.detail}}))),e.hass.auth.external.addCommandHandler((s=>i(e,s)))},i=(e,s)=>{const t=e.hass.auth.external;if("restart"===s.command)e.hass.connection.reconnect(!0),t.fireMessage({id:s.id,type:"result",success:!0,result:null});else{if("notifications/show"!==s.command)return!1;(0,a.B)(e,"hass-show-notifications"),t.fireMessage({id:s.id,type:"result",success:!0,result:null})}return!0}}}]);