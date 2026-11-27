const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
for(const n of [1,2,3]){const p=await b.newPage({viewport:{width:1920,height:640}});
await p.goto('file://'+process.cwd()+'/bb-q4w8-hs'+n+'-banner.html');await p.waitForTimeout(1000);
await p.screenshot({path:'BB-Q4W8-Banner-HolidaySale-'+n+'-1920x640.jpg',type:'jpeg',quality:92});await p.close();}
await b.close();})();
