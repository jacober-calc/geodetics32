import os, math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Circle, Arc, FancyArrowPatch
from rpn import Calc
os.makedirs("assets", exist_ok=True)
INK="#1f2933"; GRID="#d9dee3"; BLUE="#2563eb"; ORANGE="#e8702a"; GREEN="#2f9e44"; GREY="#8a949e"; PURPLE="#7048e8"; GOLD="#f2a900"; RED="#c92a2a"; LBLUE="#dbe7fd"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
 "text.color":INK,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":GRID,"grid.linewidth":0.8,
 "figure.facecolor":"white","axes.facecolor":"white","svg.fonttype":"path","axes.titleweight":"bold","axes.titlesize":13})
PREVIEW=os.environ.get("PREVIEW")
def save(fig,name):
    fig.savefig(f"assets/{name}.svg",bbox_inches="tight",facecolor="white",dpi=200)
    if PREVIEW: fig.savefig(f"/tmp/gd_{name}.png",bbox_inches="tight",facecolor="white",dpi=70)
    plt.close(fig)
def box(ax,x,y,w,h,c,lw=1.8): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=.08",fc="white",ec=c,lw=lw))
def L(lat):
    c=Calc(inputs={'L':lat}); c.run('L'); return [float(v) for v in c.st]      # V, R, X, C
def H(h,lat=48.4284):
    c=Calc(inputs={'H':h,'L':lat}); c.run('H'); return [float(v) for v in c.st] # D, P, H, L
CITIES=[("Victoria",48.4284,BLUE),("Windsor",42.3149,GREEN),("Alert",82.5018,PURPLE)]

# 1 Program map
fig,ax=plt.subplots(figsize=(10,3.6)); ax.axis("off"); ax.set_xlim(0,10.2); ax.set_ylim(0,3.45)
ax.text(.1,3.3,"Program Map",fontsize=13,fontweight="bold",va="center")
box(ax,.1,1.25,4.6,1.6,BLUE); ax.text(2.4,2.45,"LBL L",ha="center",fontsize=13,fontweight="bold",color=BLUE)
ax.text(2.4,2.05,"Earth at a latitude",ha="center",fontsize=10.5); ax.text(2.4,1.6,"L?   →   T: C   Z: X   Y: R   X: V",ha="center",fontsize=10,color=GREY,family="DejaVu Sans Mono")
box(ax,5.5,1.25,4.6,1.6,ORANGE); ax.text(7.8,2.45,"LBL H",ha="center",fontsize=13,fontweight="bold",color=ORANGE)
ax.text(7.8,2.05,"Distance to the horizon",ha="center",fontsize=10.5); ax.text(7.8,1.6,"H? L?   →   T: L   Z: H   Y: P   X: D",ha="center",fontsize=10,color=GREY,family="DejaVu Sans Mono")
ax.add_patch(FancyArrowPatch((5.45,2.05),(4.75,2.05),arrowstyle="-|>",mutation_scale=16,color=ORANGE,lw=1.8))
ax.text(5.1,2.25,"XEQ L",ha="center",fontsize=9,color=ORANGE,family="DejaVu Sans Mono")
ax.text(.1,.75,"At the L? prompt, R↓ recalls a stored latitude: once for Victoria 48.4284, twice for Windsor 42.3149, three times for Alert 82.5018",fontsize=9.3,color=GREY)
ax.text(.1,.3,"WGS 84 ellipsoid: equatorial radius 6,378,137 m, flattening 1/298.257223563  ·  sidereal day 23.934472 h",fontsize=9.3,color=GREY)
save(fig,"program_map")

# 2 Geometry (flattening exaggerated)
fig,ax=plt.subplots(figsize=(9,6.2)); ax.axis("off"); ax.set_aspect("equal")
A,B=3.0,2.4; WB=dict(fc="white",ec="none",pad=1.5)
ax.add_patch(Ellipse((0,0),2*A,2*B,fc=LBLUE,ec=BLUE,lw=2))
ax.plot([0,0],[-B-.4,B+.9],color=INK,lw=1.2,ls="--"); ax.text(-.1,B+.75,"Axis of rotation",fontsize=10,ha="right")
ax.plot([-A-.3,A+.3],[0,0],color=GREY,lw=1); ax.text(A+.35,-.05,"Equator",fontsize=10,color=GREY,va="center")
phi=math.radians(48.4); t=math.atan(B/A*math.tan(phi)); px,py=A*math.cos(t),B*math.sin(t)
ax.add_patch(Ellipse((0,py),2*px,.35,fc="none",ec=GREEN,lw=1.4,ls="--"))
ax.plot([0,px],[0,py],color=ORANGE,lw=2.4); ax.plot([0,px],[py,py],color=GREEN,lw=2.6); ax.plot(px,py,"o",color=RED,ms=9,zorder=5)
nx,ny=B*B*px, A*A*py; nrm=math.hypot(nx,ny); nx,ny=nx/nrm,ny/nrm; k=py/ny
ax.plot([px-nx*k,px+nx*.5],[0,py+ny*.5],color=INK,lw=1,ls=":")
ax.add_patch(Arc((px-nx*k,0),1.2,1.2,theta1=0,theta2=math.degrees(math.atan2(ny,nx)),color=RED,lw=1.6))
ax.text(px-nx*k+.7,.12,"L",color=RED,fontsize=12,fontweight="bold")
ax.annotate("X: Earth's radius",xy=(px*.5,py*.5),xytext=(-2.6,-.9),color=ORANGE,fontsize=10.5,fontweight="bold",arrowprops=dict(arrowstyle="-",color=ORANGE,lw=1),bbox=WB)
ax.annotate("R: radius of the parallel",xy=(px*.7,py),xytext=(A+.4,py+.75),color=GREEN,fontsize=10.5,fontweight="bold",arrowprops=dict(arrowstyle="-",color=GREEN,lw=1),bbox=WB)
ax.annotate("C = 2πR: circumference\nof the parallel",xy=(-px*.8,py-.1),xytext=(-A-2.3,py+.6),color=GREEN,fontsize=10.5,arrowprops=dict(arrowstyle="-",color=GREEN,lw=1),bbox=WB)
ax.annotate("",xy=(-px*.5,py+.45),xytext=(px*.5,py+.45),arrowprops=dict(arrowstyle="->",color=PURPLE,lw=1.6,connectionstyle="arc3,rad=.3"))
ax.text(0.15,py+1.05,"V: speed, one turn per sidereal day",color=PURPLE,fontsize=10.5,fontweight="bold")
ax.text(A+.4,py-.05,"Point at latitude L",color=RED,fontsize=10)
ax.set_xlim(-A-2.4,A+3.4); ax.set_ylim(-B-.5,B+1.4)
ax.set_title("What LBL L Calculates (flattening exaggerated)",loc="left"); save(fig,"geometry")

# 3 Rotation speed and circumference against latitude
lats=np.linspace(0,90,181); out=np.array([L(l) for l in lats])
fig,ax=plt.subplots(figsize=(10,4.4))
ax.plot(lats,out[:,0],color=PURPLE,lw=2.4,label="V, rotation speed (km/h)")
ax2=ax.twinx(); ax2.plot(lats,out[:,3]/1000,color=GREEN,lw=1.6,ls="--",label="C, circumference (thousand km)"); ax2.set_ylabel("C (thousand km)",color=GREEN); ax2.spines["right"].set_visible(True); ax2.grid(False); ax2.set_ylim(0,44)
v0=L(0); ax.plot(0,v0[0],"o",color=INK,ms=8); ax.text(1.5,v0[0]-130,f"Equator: {v0[0]:,.1f} km/h",fontsize=10)
for n,lat,c in CITIES:
    v=L(lat); ax.plot(lat,v[0],"o",color=c,ms=9,zorder=5)
    tx,ty,ha={"Victoria":(55,1400,"left"),"Windsor":(30,850,"right"),"Alert":(80,60,"right")}[n]
    ax.annotate(f"{n}: {v[0]:,.1f} km/h",xy=(lat,v[0]),xytext=(tx,ty),ha=ha,fontsize=10,color=c,fontweight="bold",arrowprops=dict(arrowstyle="-",color=c,lw=1))
ax.set_xlim(0,90); ax.set_ylim(0,1900); ax.set_xticks(range(0,91,15)); ax.set_xlabel("Latitude L (°)"); ax.set_ylabel("V (km/h)",color=PURPLE)
h1,l1=ax.get_legend_handles_labels(); h2,l2=ax2.get_legend_handles_labels(); ax.legend(h1+h2,l1+l2,frameon=False,loc="lower left",fontsize=9.5)
ax.set_title("Speed of the Earth's Rotation by Latitude",loc="left"); save(fig,"speed_latitude")

# 4 Earth's radius against latitude
fig,ax=plt.subplots(figsize=(10,3.6))
ax.plot(lats,out[:,2],color=ORANGE,lw=2.4)
for n,lat,c in CITIES:
    v=L(lat); ax.plot(lat,v[2],"o",color=c,ms=8,zorder=5); ax.text(lat+1.2,v[2]+.9,f"{n}: {v[2]:,.3f} km",fontsize=10,color=c,fontweight="bold")
ax.text(1,6378.6,"Equator: 6,378.137 km",fontsize=10); ax.text(89,6355.2,"Pole: 6,356.752 km",fontsize=10,ha="right")
ax.set_xlim(0,90); ax.set_ylim(6354,6381); ax.set_xticks(range(0,91,15)); ax.set_xlabel("Latitude L (°)"); ax.set_ylabel("X (km)")
ax.set_title("Earth's Radius by Latitude, WGS 84",loc="left"); save(fig,"radius_latitude")

# 5 Horizon geometry
fig,ax=plt.subplots(figsize=(7.5,5.6)); ax.axis("off"); ax.set_aspect("equal")
Rr=3.0; Hh=1.1
ax.add_patch(Circle((0,0),Rr,fc=LBLUE,ec=BLUE,lw=2))
O=(0,Rr+Hh); ax.plot(*O,"o",color=RED,ms=9,zorder=5); ax.text(.15,Rr+Hh+.1,"Observer",color=RED,fontsize=10.5,fontweight="bold")
ang=math.acos(Rr/(Rr+Hh)); T=(Rr*math.sin(ang),Rr*math.cos(ang))
ax.plot([O[0],T[0]],[O[1],T[1]],color=ORANGE,lw=2.6); ax.plot(*T,"o",color=ORANGE,ms=8)
ax.text((O[0]+T[0])/2+.15,(O[1]+T[1])/2+.15,"D",color=ORANGE,fontsize=13,fontweight="bold")
ax.text(T[0]+.15,T[1]+.05,"Horizon",color=ORANGE,fontsize=10.5)
ax.plot([0,0],[0,Rr],color=INK,lw=1.4); ax.text(-.35,Rr/2,"R",fontsize=13,fontweight="bold")
ax.plot([0,0],[Rr,Rr+Hh],color=PURPLE,lw=2.4); ax.text(-.35,Rr+Hh/2,"H",fontsize=13,fontweight="bold",color=PURPLE)
ax.plot([0,T[0]],[0,T[1]],color=INK,lw=1.4); ax.text(T[0]/2+.12,T[1]/2-.25,"R",fontsize=13,fontweight="bold")
s=.25; ux,uy=-T[0]/Rr,-T[1]/Rr; vx,vy=(O[0]-T[0]),(O[1]-T[1]); n=math.hypot(vx,vy); vx,vy=vx/n,vy/n
ax.plot([T[0]+ux*s,T[0]+ux*s+vx*s,T[0]+vx*s],[T[1]+uy*s,T[1]+uy*s+vy*s,T[1]+vy*s],color=INK,lw=1)
ax.text(-3.6,-3.55,"(R + H)² = R² + D²   →   D = √(2RH + H²)",fontsize=11.5,family="DejaVu Sans Mono")
ax.set_xlim(-3.7,4.2); ax.set_ylim(-3.8,4.6); ax.set_title("Line of Sight to the Horizon (height exaggerated)",loc="left"); save(fig,"horizon_geometry")

# 6 Horizon distance against height
hs=np.logspace(0,6,200); ds=[H(h)[0]/1000 for h in hs]
fig,ax=plt.subplots(figsize=(10,4.5))
ax.plot(hs,ds,color=ORANGE,lw=2.4)
for h,lab in ((1.7,"Eye height, 1.7 m"),(100,"100 m"),(10668,"Airliner, 10,668 m"),(408000,"Space station, 408 km")):
    d=H(h)[0]/1000; ax.plot(h,d,"o",color=RED,ms=8,zorder=5); ax.text(h*1.4,d*.62,f"{lab}\n{d:,.2f} km",fontsize=9.5,color=RED)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(1,1.2e6); ax.set_ylim(2,4000)
ax.set_xlabel("Height H (m)"); ax.set_ylabel("Distance to horizon D (km)")
ax.set_title("Distance to the Horizon from Victoria (LBL H)",loc="left"); save(fig,"horizon_height")
