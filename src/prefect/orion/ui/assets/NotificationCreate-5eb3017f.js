import{d as p,V as m,a as l,w as a,a2 as _,o as d,b as e,e as n,by as C,bz as h,v as b}from"./index-1ad4f081-98325998.js";import{u as y}from"./usePageTitle-b23eb992.js";import{r}from"./index-eb9d0889.js";import{r as i}from"./routes-7f16c85e.js";import"./meta-26546594.js";const B=p({__name:"NotificationCreate",setup(w){const s=m();async function c(t){try{await s.notifications.createNotification(t),r.push(i.notifications())}catch(o){b("Error creating notification","error"),console.warn(o)}}function f(){r.push(i.notifications())}return y("Create Notification"),(t,o)=>{const u=_("p-layout-default");return d(),l(u,{class:"notification-create"},{header:a(()=>[e(n(C))]),default:a(()=>[e(n(h),{action:"Create",onSubmit:c,onCancel:f})]),_:1})}}});export{B as default};
