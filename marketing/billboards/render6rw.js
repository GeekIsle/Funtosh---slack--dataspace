const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
const jobs=[['bb-q4w6-bf-banner-rw',1920,640,'rw-BB-Q4W6-Banner-BlackFriday-1920x640.jpg'],['bb-q4w6-xmas-banner-rw',1920,640,'rw-BB-Q4W6-Banner-Christmas-1920x640.jpg'],['bb-q4w6-bf-promo-rw',1100,540,'rw-BB-Q4W6-Promo-BlackFriday-1100x540.jpg'],['bb-q4w6-xmas-promo-rw',1100,540,'rw-BB-Q4W6-Promo-Christmas-1100x540.jpg']];
for(const [n,w,h,o] of jobs){const p=await b.newPage({viewport:{width:w,height:h}});await p.goto('file://'+process.cwd()+'/'+n+'.html');await p.waitForTimeout(900);await p.screenshot({path:o,type:'jpeg',quality:92});await p.close();}
await b.close();})();
