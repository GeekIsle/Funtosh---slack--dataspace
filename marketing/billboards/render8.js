const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1920,height:640}});
await p.goto('file://'+process.cwd()+'/bb-q4w8-bf-banner.html');await p.waitForTimeout(1000);
await p.screenshot({path:'BB-Q4W8-Banner-BlackFriday-1920x640.jpg',type:'jpeg',quality:92});
await b.close();})();
