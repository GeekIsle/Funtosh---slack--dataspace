const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
const jobs=[['bb-q4w7-bf-banner',1920,640,'BB-Q4W7-Banner-BlackFridayWeek-1920x640.jpg'],['bb-q4w7-xmas-banner',1920,640,'BB-Q4W7-Banner-Christmas-1920x640.jpg'],['bb-q4w7-xmas-promo',1100,540,'BB-Q4W7-Promo-Christmas-1100x540.jpg'],['bb-q4w7-bf-promo',1100,540,'BB-Q4W7-Promo-BlackFridayWeek-1100x540.jpg']];
for(const [n,w,h,o] of jobs){const p=await b.newPage({viewport:{width:w,height:h}});await p.goto('file://'+process.cwd()+'/'+n+'.html');await p.waitForTimeout(800);await p.screenshot({path:o,type:'jpeg',quality:92});await p.close();}
await b.close();})();
