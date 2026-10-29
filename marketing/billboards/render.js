const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const jobs=[['bb-q4w3-banner',1920,1080,'BB-Q4W3-Banner-BlackFriday-1920x1080.jpg'],['bb-q4w3-promoF1',1100,540,'BB-Q4W3-PromoF1-EarthlyChange-1100x540.jpg'],['bb-q4w3-promoF2',1100,540,'BB-Q4W3-PromoF2-MimroOriginals-1100x540.jpg'],['bb-q4w3-promoH1',1000,1000,'BB-Q4W3-PromoH1-EarthlyChange-1000x1000.jpg'],['bb-q4w3-promoH2',1000,1000,'BB-Q4W3-PromoH2-MimroOriginals-1000x1000.jpg']];
  for (const [n,w,h,out] of jobs){ const p=await b.newPage({viewport:{width:w,height:h}}); await p.goto('file://'+process.cwd()+'/'+n+'.html'); await p.waitForTimeout(600); await p.screenshot({path:out,type:'jpeg',quality:92}); await p.close(); }
  await b.close();
})();
