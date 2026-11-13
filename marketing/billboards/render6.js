const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
const jobs=[['bb-q4w6-bf-banner',1920,640,'BB-Q4W6-Banner-BlackFriday-1920x640.jpg'],['bb-q4w6-xmas-banner',1920,640,'BB-Q4W6-Banner-Christmas-1920x640.jpg'],['bb-q4w6-bf-promo',1100,400,'BB-Q4W6-Promo-BlackFriday-1100x400.jpg'],['bb-q4w6-xmas-promo',1100,400,'BB-Q4W6-Promo-Christmas-1100x400.jpg']];
for(const [n,w,h,o] of jobs){const p=await b.newPage({viewport:{width:w,height:h}});await p.goto('file://'+process.cwd()+'/'+n+'.html');await p.waitForTimeout(700);await p.screenshot({path:o,type:'jpeg',quality:92});await p.close();}
await b.close();})();
