import{d as k,V as w,al as t,h as c,a as _,w as r,a2 as i,o as d,b as n,e as o,bX as P,bY as f}from"./index-1ad4f081-98325998.js";import{u as Q}from"./usePageTitle-b23eb992.js";const C=k({__name:"WorkPoolQueueEdit",async setup(N){let e,u;const s=w(),a=t("workPoolName"),l=t("workPoolQueueName"),p=([e,u]=c(()=>s.workPoolQueues.getWorkPoolQueueByName(a.value,l.value)),e=await e,u(),e);return Q("Edit Work Pool Queue"),(h,y)=>{const m=i("p-layout-default");return d(),_(m,null,{header:r(()=>[n(o(P),{"work-pool-name":o(a),"work-pool-queue-name":o(l)},null,8,["work-pool-name","work-pool-queue-name"])]),default:r(()=>[n(o(f),{"work-pool-name":o(a),"work-pool-queue":o(p)},null,8,["work-pool-name","work-pool-queue"])]),_:1})}}});export{C as default};
