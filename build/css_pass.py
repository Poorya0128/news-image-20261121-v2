p='tools/style.css'; s=open(p).read()
def rep(a,b):
    global s
    assert a in s, a[:90]; s=s.replace(a,b)
rep('@font-face { font-family: "Head"; font-weight: 700;','''@font-face { font-family: "Small"; font-weight: 400; src: url(fonts/NotoSans-Regular.ttf); }
@font-face { font-family: "Small"; font-weight: 500; src: url(fonts/NotoSans-Medium.ttf); }
@font-face { font-family: "Small"; font-weight: 600; src: url(fonts/NotoSans-SemiBold.ttf); }
@font-face { font-family: "Small"; font-weight: 700; src: url(fonts/NotoSans-Bold.ttf); }
@font-face { font-family: "Small"; font-weight: 800; src: url(fonts/NotoSans-ExtraBold.ttf); }
@font-face { font-family: "Head"; font-weight: 700;''')
rep('.title { font-size: 44px; line-height: 44px; font-weight: 900; }','.title { font-size: 41px; line-height: 45px; font-weight: 900; }')
rep('.sub { font-size: 11.5px; line-height: 13.5px; color: #d6deee; }','.sub { font-family: "Small"; font-size: 10.5px; line-height: 14px; color: #d6deee; white-space: nowrap; }')
rep('.trust { width: 190px; flex: none; border-left: 1px solid #3a4a6a; padding-left: 10px; font-size: 11px; line-height: 15px; color: #f1f4fa; }',
    '.trust { width: 226px; flex: none; border-left: 1px solid #3a4a6a; padding-left: 10px; font-family: "Small"; font-size: 10.5px; line-height: 14px; color: #f1f4fa; }\n.trust .nb { color: #f2c94c; font-weight: 700; font-size: 10px; }')
rep('.trust > div { display: flex; align-items: center; gap: 6px; }','.trust > div { display: flex; align-items: center; gap: 6px; white-space: nowrap; }\n.ok { display: inline-block; flex: none; vertical-align: -2px; margin: 0 1px; }')
rep('padding: 5px 12px 4px; background: #0f1a2e; color: #fff; display: flex; gap: 12px; align-items: center; height: 80px;','padding: 4px 12px 4px; background: #0f1a2e; color: #fff; display: flex; gap: 12px; align-items: center; height: 88px;')
rep('.tline { display: flex; margin-top: 4px; border: 1px solid #c8bea8; background: #fbf8f1; height: 32px; }','.tline { display: flex; margin-top: 5px; border: 1px solid #c8bea8; background: #fbf8f1; height: 44px; }')
rep('.tlh { background: #0f1a2e; color: #fff; font-size: 10px; line-height: 12px;','.tlh { background: #0f1a2e; color: #fff; font-size: 11px; line-height: 13px;')
rep('.tl { flex: 1; min-width: 0; padding: 1px 6px; border-left: 1px solid #ddd3bf; font-size: 11px; line-height: 13px; white-space: nowrap; overflow: hidden; }',
    '.tl { flex: 1; min-width: 0; padding: 4px 7px; border-left: 1px solid #ddd3bf; font-family: "Small"; font-size: 12px; line-height: 15px; white-space: nowrap; overflow: hidden; }')
rep('.tl b { display: flex; align-items: center; color: #0f1a2e; font-size: 10.5px; font-weight: 800; }','.tl b { display: flex; align-items: center; color: #0f1a2e; font-size: 13px; font-weight: 800; margin-bottom: 2px; }')
rep('.bd.t { width: 14px; height: 14px; font-size: 8.5px; margin-right: 4px; }','.bd.t { width: 17px; height: 17px; font-size: 9.5px; margin-right: 5px; }')
rep('flex: none; font-family: "Body"; }','flex: none; font-family: "Small"; }')
rep('.srcr { margin-left: auto; font-size: 9px; font-weight: 700; color: #4a4a4a;','.srcr { margin-left: auto; font-family: "Small"; font-size: 9px; font-weight: 600; color: #4a4a4a;')
rep('.lead p { font-size: 12.5px; line-height: 15px;','.lead p { font-size: 13px; line-height: 15.5px;')
rep('.card p { font-size: 12px; line-height: 14px;','.card p { font-size: 12.5px; line-height: 14.5px;')
rep('.bottom { display: flex; gap: 12px; margin-top: 6px; height: 242px; }','.bottom { display: flex; gap: 14px; margin-top: 6px; height: 250px; }')
rep('.mapbox { width: 320px; flex: none; }','.mapbox { width: 330px; flex: none; }')
rep('.mh span { font-size: 9.5px; letter-spacing: 0; font-weight: 600; color: #555; margin-left: 6px; }','.mh span, .ah span { font-family: "Small"; font-size: 9.5px; letter-spacing: 0; font-weight: 600; color: #555; margin-left: 6px; }')
rep('.mh2 {','.dc { margin-top: 5px; border: 1px solid #c9a227; background: #fff8dc; padding: 3px 7px 4px; }\n.dch { font-size: 10.5px; font-weight: 800; letter-spacing: .1em; color: #5a4000; margin-bottom: 1px; }\n.dcr { display: flex; align-items: center; gap: 6px; font-family: "Small"; font-size: 11px; line-height: 15px; white-space: nowrap; overflow: hidden; }\n.dcr b { width: 96px; flex: none; color: #3a2c00; font-weight: 700; }\n.dcr > span:last-child { color: #222; overflow: hidden; }\n.dci { width: 14px; height: 14px; border-radius: 50%; color: #fff; font-weight: 800; font-size: 10px; display: inline-flex; align-items: center; justify-content: center; flex: none; }\n.dci.edge { background: #c07400; }\n.dci.out { background: #6b6b6b; }\n.mh2 {')
rep('.br { display: flex; gap: 5px; align-items: center; height: 14.6px;','.br { display: flex; gap: 6px; align-items: center; height: 20.8px;')
rep('.bt { font-size: 12.5px; line-height: 14px; white-space: nowrap; overflow: hidden; min-width: 0; }','.bt { font-size: 14.5px; line-height: 17px; white-space: nowrap; overflow: hidden; min-width: 0; }')
rep('.bs { font-size: 8.5px; font-weight: 700; color: #5a5a5a; letter-spacing: .04em; margin-left: 4px; }','.bs { font-family: "Small"; font-size: 9.5px; font-weight: 600; color: #555; letter-spacing: .02em; margin-left: 5px; }')
rep('.bd.s { width: 17px; height: 17px; font-size: 9.5px; }','.bd.s { width: 19px; height: 19px; font-size: 10px; }')
rep('.claim { display: inline-block; font-size: 8.5px; line-height: 12px;','.claim { display: inline-block; font-family: "Small"; font-size: 9px; line-height: 13px;')
rep('.rep { display: inline-block; font-size: 8.5px; line-height: 12px;','.rep { display: inline-block; font-family: "Small"; font-size: 9px; line-height: 13px;')
rep('.sport { display: flex; margin-top: 6px; border-top: 2px solid #16181d; border-bottom: 2px solid #16181d; height: 34px; align-items: center; }','.sport { display: flex; margin-top: 6px; border-top: 2px solid #16181d; border-bottom: 2px solid #16181d; height: 48px; align-items: center; }')
rep('.sb { display: flex; align-items: center; gap: 5px; width: 110px; flex: none; font-family: "Head"; font-weight: 900; font-size: 13px; line-height: 12px; }','.sb { display: flex; align-items: center; gap: 6px; width: 132px; flex: none; font-family: "Head"; font-weight: 900; font-size: 17px; line-height: 16px; }')
rep('.sb svg { width: 66px; height: 29px; }','.sb svg { width: 74px; height: 33px; }')
rep('.sp { display: flex; gap: 4px; font-size: 11px; line-height: 12.5px; align-items: center; white-space: nowrap; min-width: 0; overflow: hidden; }','.sp { display: flex; gap: 6px; font-size: 13.5px; line-height: 16px; align-items: center; white-space: nowrap; min-width: 0; overflow: hidden; }')
rep('.sp b { display: block; font-size: 8.5px; letter-spacing: .05em; text-transform: uppercase; color: #555; line-height: 10px; }','.sp b { display: block; font-family: "Small"; font-size: 9px; letter-spacing: .04em; text-transform: uppercase; color: #555; line-height: 12px; font-weight: 700; }')
rep('.foot { margin-top: 4px; font-size: 9px;','.foot { font-family: "Small"; margin-top: 5px; font-size: 9.5px;')
open(p,'w').write(s); print('css ok')
