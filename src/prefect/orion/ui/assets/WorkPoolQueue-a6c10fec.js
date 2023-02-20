import{d as v,V as Q,al as c,a0 as y,c as r,aG as g,e as o,a as N,w as e,g as h,a2 as n,Z as W,o as C,b as u,bS as x,b8 as U,bT as k,bU as V,aK as B}from"./index-1ad4f081-98325998.js";import{u as R}from"./usePageTitle-b23eb992.js";const S=v({__name:"WorkPoolQueue",setup(T){const w=Q(),l=c("workPoolName"),a=c("workPoolQueueName"),m={interval:3e5},p=y(w.workPoolQueues.getWorkPoolQueueByName,[l.value,a.value],m),t=r(()=>p.response),i=r(()=>`prefect agent start --pool ${l.value} --work-queue ${a.value}`),_=g({workPoolQueueName:[a.value],workPoolName:[l.value]}),f=r(()=>{const s=["Upcoming Runs","Runs"];return W.xl||s.unshift("Details"),s}),d=r(()=>a.value?`Work Pool Queue: ${a.value}`:"Work Pool Queue");return R(d),(s,$)=>{const P=n("p-tabs"),q=n("p-layout-well"),b=n("p-layout-default");return o(t)?(C(),N(b,{key:0,class:"work-pool-queue"},{header:e(()=>[u(o(x),{"work-pool-queue":o(t),"work-pool-name":o(l),onUpdate:o(p).refresh},null,8,["work-pool-queue","work-pool-name","onUpdate"])]),default:e(()=>[u(q,{class:"work-pool-queue__body"},{header:e(()=>[u(o(U),{command:o(i),title:"Work queue is ready to go!",subtitle:"Work queues are scoped to a work pool to allow agents to pull from groups of queues with different priorities."},null,8,["command"])]),well:e(()=>[u(o(k),{alternate:"","work-pool-name":o(l),"work-pool-queue":o(t)},null,8,["work-pool-name","work-pool-queue"])]),default:e(()=>[u(P,{tabs:o(f)},{details:e(()=>[u(o(k),{"work-pool-name":o(l),"work-pool-queue":o(t)},null,8,["work-pool-name","work-pool-queue"])]),"upcoming-runs":e(()=>[u(o(V),{"work-pool-name":o(l),"work-pool-queue":o(t)},null,8,["work-pool-name","work-pool-queue"])]),runs:e(()=>[u(o(B),{"flow-run-filter":o(_)},null,8,["flow-run-filter"])]),_:1},8,["tabs"])]),_:1})]),_:1})):h("",!0)}}});export{S as default};
