import{d as i,V as b,al as d,c as t,az as _,e,a as f,w as s,g as D,a2 as B,a3 as v,o as g,b as n,br as h,bs as w}from"./index-1ad4f081-98325998.js";import{u as C}from"./usePageTitle-b23eb992.js";import"./index-eb9d0889.js";import{r as V}from"./routes-7f16c85e.js";import"./meta-26546594.js";const K=i({__name:"BlockView",setup(x){const u=b(),a=v(),c=d("blockDocumentId"),l=t(()=>c.value?[c.value]:null),r=_(u.blockDocuments.getBlockDocument,l),o=t(()=>r.response),m=()=>{a.push(V.blocks())},p=t(()=>o.value?`Block: ${o.value.name}`:"Block");return C(p),(y,T)=>{const k=B("p-layout-default");return e(o)?(g(),f(k,{key:0,class:"block-view"},{header:s(()=>[n(e(h),{"block-document":e(o),onDelete:m},null,8,["block-document"])]),default:s(()=>[n(e(w),{"block-document":e(o)},null,8,["block-document"])]),_:1})):D("",!0)}}});export{K as default};