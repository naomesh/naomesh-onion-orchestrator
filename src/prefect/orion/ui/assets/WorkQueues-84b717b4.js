import{d as i,V as f,a0 as _,c as a,a as u,w as r,a2 as w,o,b,e,b3 as y,k as Q,b4 as g,b5 as v,a6 as x,g as C}from"./index-1ad4f081-98325998.js";import{u as q}from"./usePageTitle-b23eb992.js";const N=i({__name:"WorkQueues",setup(B){const l=f(),p={interval:3e4},s=_(l.workQueues.getWorkQueues,[{}],p),n=a(()=>s.response??[]),c=a(()=>s.executed&&n.value.length==0),m=a(()=>s.executed);return q("Work Queues"),(V,t)=>{const k=w("p-layout-default");return o(),u(k,{class:"queues"},{header:r(()=>[b(e(y))]),default:r(()=>[e(m)?(o(),Q(x,{key:0},[e(c)?(o(),u(e(g),{key:0})):(o(),u(e(v),{key:1,"work-queues":e(n),onUpdate:t[0]||(t[0]=d=>e(s).refresh()),onDelete:t[1]||(t[1]=d=>e(s).refresh())},null,8,["work-queues"]))],64)):C("",!0)]),_:1})}}});export{N as default};