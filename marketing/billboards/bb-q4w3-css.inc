@font-face{font-family:IS;src:url(src/fonts/InstrumentSans.ttf)}
@font-face{font-family:FG;src:url(src/fonts/Figtree.ttf)}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:FG,sans-serif;background:radial-gradient(circle at 72% 60%,#08126c 0%,#020624 62%);color:#fff;position:relative;overflow:hidden}
.kick{display:inline-block;font-weight:800;letter-spacing:4px;text-transform:uppercase;color:#2ad265;border:2px solid #2ad265;border-radius:999px}
.grad{background:linear-gradient(90deg,#007ae7,#2ad265);-webkit-background-clip:text;background-clip:text;color:transparent}
.btn{display:inline-block;background:#fff;color:#020624;font-weight:800;letter-spacing:2px;text-transform:uppercase}
.tile{position:relative;border-radius:30px;background:#f6f9fc;display:flex;align-items:center;justify-content:center;overflow:hidden}
.tile img{object-fit:contain;filter:drop-shadow(0 22px 20px rgba(2,6,36,.22))}
.tile.hero{background:linear-gradient(135deg,#007ae7,#2ad265)}
.chip{position:absolute;top:20px;left:20px;font-family:IS;font-weight:700;color:#fff;background:#020624;border-radius:14px}
.hero .chip{background:#fff;color:#020624}
.lbl{position:absolute;left:22px;right:18px;bottom:18px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#5a5f73;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hero .lbl{color:#fff}
