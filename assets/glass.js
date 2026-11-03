/* Liquid-glass menu: builds the refraction map (a rounded-rectangle displacement map sized to the menu) used by backdrop-filter in Chromium browsers. */
(function(){
  var ua=navigator.userAgentData;
  if(!ua||!ua.brands.some(function(b){return /Chromium|Google Chrome|Microsoft Edge/.test(b.brand);})) return;   // refraction only works in Chromium browsers; the others keep the frosted glass
  var NS='http://www.w3.org/2000/svg';
  var svg=document.createElementNS(NS,'svg'); svg.setAttribute('width','0'); svg.setAttribute('height','0'); svg.style.cssText='position:absolute;pointer-events:none';
  svg.innerHTML='<defs><filter id="lgf" x="0" y="0" width="100" height="50" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB"><feImage id="lgmap" x="0" y="0" width="100" height="50" preserveAspectRatio="none" result="map"/><feDisplacementMap in="SourceGraphic" in2="map" scale="64" xChannelSelector="R" yChannelSelector="G"/></filter></defs>';
  document.body.appendChild(svg);
  function build(){
    var el=document.querySelector('.nav-row'); if(!el) return;
    var r=el.getBoundingClientRect(), w=Math.round(r.width), h=Math.round(r.height); if(!w||!h) return;
    var R=20, B=28, cv=document.createElement('canvas'); cv.width=w; cv.height=h;
    var ctx=cv.getContext('2d'), img=ctx.createImageData(w,h), d=img.data, cx=w/2, cy=h/2, hx=w/2-R, hy=h/2-R;
    for(var y=0;y<h;y++) for(var x=0;x<w;x++){
      var px=x+.5-cx, py=y+.5-cy, qx=Math.abs(px)-hx, qy=Math.abs(py)-hy;
      var ox=Math.max(qx,0), oy=Math.max(qy,0);
      var out=Math.sqrt(ox*ox+oy*oy)+Math.min(Math.max(qx,qy),0)-R, dist=-out, nx=0, ny=0;
      if(qx>0&&qy>0){var l=Math.sqrt(qx*qx+qy*qy)||1; nx=Math.sign(px)*qx/l; ny=Math.sign(py)*qy/l;}
      else if(qx>qy){nx=Math.sign(px);} else {ny=Math.sign(py);}
      var t=Math.max(0,Math.min(1,1-dist/B)); t=t*t*(3-2*t);
      var i=(y*w+x)*4; d[i]=128-127*nx*t; d[i+1]=128-127*ny*t; d[i+2]=128; d[i+3]=255;
    }
    ctx.putImageData(img,0,0);
    var f=svg.querySelector('filter'), m=svg.querySelector('#lgmap');
    f.setAttribute('width',w); f.setAttribute('height',h); m.setAttribute('width',w); m.setAttribute('height',h);
    m.setAttributeNS('http://www.w3.org/1999/xlink','href',cv.toDataURL()); m.setAttribute('href',cv.toDataURL());
    document.documentElement.classList.add('lg-refract');
  }
  build(); addEventListener('resize',build); if(document.fonts&&document.fonts.ready) document.fonts.ready.then(build);
  if(window.ResizeObserver){var n=document.querySelector('.nav-row'); if(n) new ResizeObserver(build).observe(n);}
})();
