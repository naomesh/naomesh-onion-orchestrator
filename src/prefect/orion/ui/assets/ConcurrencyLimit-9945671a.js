import{d as k,V as h,al as w,c as s,aN as g,a0 as x,a as c,w as n,a2 as i,a3 as T,Z as V,o as r,e,bB as B,g as o,bC as u,b as D,bD as N}from"./index-1ad4f081-98325998.js";import{u as S}from"./usePageTitle-b23eb992.js";import"./index-eb9d0889.js";import{r as q}from"./routes-7f16c85e.js";import"./meta-26546594.js";const Y=k({__name:"ConcurrencyLimit",setup(I){const l=h(),m=w("concurrencyLimitId"),p=T(),y=s(()=>[{label:"Details",hidden:V.xl},{label:"Active Task Runs"}]),_=g(y),d={interval:3e5},b=x(l.concurrencyLimits.getConcurrencyLimit,[m.value],d),t=s(()=>b.response);function L(){p.push(q.concurrencyLimits())}const v=s(()=>t.value?`Concurrency Limit: ${t.value.tag}`:"Concurrency Limit");return S(v),(R,Z)=>{const f=i("p-tabs"),C=i("p-layout-well");return r(),c(C,{class:"concurrencyLimit"},{header:n(()=>[e(t)?(r(),c(e(B),{key:0,"concurrency-limit":e(t),onDelete:L},null,8,["concurrency-limit"])):o("",!0)]),well:n(()=>[e(t)?(r(),c(e(u),{key:0,alternate:"","concurrency-limit":e(t)},null,8,["concurrency-limit"])):o("",!0)]),default:n(()=>[D(f,{tabs:e(_)},{details:n(()=>[e(t)?(r(),c(e(u),{key:0,"concurrency-limit":e(t)},null,8,["concurrency-limit"])):o("",!0)]),"active-task-runs":n(()=>{var a;return[(a=e(t))!=null&&a.activeSlots?(r(),c(e(N),{key:0,"active-slots":e(t).activeSlots},null,8,["active-slots"])):o("",!0)]}),_:1},8,["tabs"])]),_:1})}}});export{Y as default};
