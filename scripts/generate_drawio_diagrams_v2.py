#!/usr/bin/env python3
"""Tạo bộ sơ đồ Draw.io v2 với bố cục rõ, đường nối không chồng chéo."""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree

OUT = Path(__file__).resolve().parents[1] / "diagrams" / "drawio"
BOX="rounded=1;whiteSpace=wrap;html=1;fillColor=#e3f2fd;strokeColor=#1565c0;fontSize=13;"
ORANGE="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff3e0;strokeColor=#ef6c00;fontSize=13;"
GREEN="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;fillColor=#e8f5e9;strokeColor=#2e7d32;fontSize=13;"
ACTOR="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fontSize=13;"
USECASE="ellipse;whiteSpace=wrap;html=1;fillColor=#e3f2fd;strokeColor=#1565c0;fontSize=12;"
DECISION="rhombus;whiteSpace=wrap;html=1;fillColor=#fff8e1;strokeColor=#f9a825;fontSize=12;"
ARROW="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;fontSize=12;labelBackgroundColor=#ffffff;"
LINE="edgeStyle=none;rounded=0;html=1;endArrow=none;startArrow=none;strokeWidth=1;"
DASH="edgeStyle=none;rounded=0;html=1;endArrow=open;endFill=0;dashed=1;labelBackgroundColor=#ffffff;"


def graph(name,w=1300,h=850):
    f=Element("mxfile",{"host":"app.diagrams.net","agent":"DSS Laptop v2","version":"24.7.17"})
    d=SubElement(f,"diagram",{"id":name,"name":"Page-1"})
    m=SubElement(d,"mxGraphModel",{"dx":str(w),"dy":str(h),"grid":"1","gridSize":"10","guides":"1","tooltips":"1","connect":"1","arrows":"1","fold":"1","page":"1","pageScale":"1","pageWidth":str(w),"pageHeight":str(h),"math":"0","shadow":"0"})
    r=SubElement(m,"root"); SubElement(r,"mxCell",{"id":"0"}); SubElement(r,"mxCell",{"id":"1","parent":"0"})
    return f,r


def v(r,i,label,x,y,w,h,style=BOX):
    c=SubElement(r,"mxCell",{"id":i,"value":label,"style":style,"vertex":"1","parent":"1"})
    SubElement(c,"mxGeometry",{"x":str(x),"y":str(y),"width":str(w),"height":str(h),"as":"geometry"}); return c


def e(r,i,a,b,label="",style=ARROW,points=()):
    c=SubElement(r,"mxCell",{"id":i,"value":label,"style":style,"edge":"1","parent":"1","source":a,"target":b})
    g=SubElement(c,"mxGeometry",{"relative":"1","as":"geometry"})
    if points:
        arr=SubElement(g,"Array",{"as":"points"})
        for x,y in points: SubElement(arr,"mxPoint",{"x":str(x),"y":str(y)})
    return c


def point(r,i,x,y):
    return v(r,i,"",x,y,1,1,"opacity=0;fillOpacity=0;strokeOpacity=0;")


def save(doc,name): ElementTree(doc).write(OUT/name,encoding="utf-8",xml_declaration=True)


def architecture():
    d,r=graph("architecture-v2",1450,760)
    v(r,"user","Sinh viên / Cố vấn",35,260,150,65)
    v(r,"ui","<b>USER INTERFACE</b><br>Flask · HTML · CSS<br><br>Nhập tham số<br>Xem Top 5 và lý do loại",240,190,225,210)
    v(r,"ctrl","<b>APPLICATION CONTROLLER</b><br><br>Nhận request<br>Kiểm tra tham số<br>Điều phối kết quả",540,190,255,210,ORANGE)
    v(r,"modelbox","<b>MODEL MANAGEMENT</b><br><br>① Validation<br>② Hard Filter<br>③ Min–Max<br>④ WSM Ranking<br>⑤ What-if Analyzer",890,90,240,270,ORANGE)
    v(r,"databox","<b>DATA MANAGEMENT</b><br><br>Đọc dữ liệu<br>Lưu cấu hình<br>Xuất kết quả",890,455,240,175,GREEN)
    v(r,"csv","Laptop mô phỏng<br>CSV",1210,420,175,65,GREEN)
    v(r,"cfg","Tiêu chí · Trọng số<br>Ngưỡng lọc",1210,515,175,65,GREEN)
    v(r,"out","Ranking<br>CSV / JSON",1210,610,175,65,GREEN)
    both=ARROW+"startArrow=block;startFill=1;"
    e(r,"a1","user","ui","Tương tác",both)
    e(r,"a2","ui","ctrl","Yêu cầu / Kết quả",both)
    e(r,"a3","ctrl","modelbox","Tham số / Xếp hạng",both)
    e(r,"a4","ctrl","databox","Đọc / Ghi",both,[(670,545)])
    e(r,"a5","databox","csv","Đọc")
    e(r,"a6","databox","cfg","Cấu hình")
    e(r,"a7","databox","out","Ghi")
    save(d,"01-kien-truc-tong-the.drawio")


def usecase():
    d,r=graph("usecase-v2",1400,900)
    v(r,"boundary","HỆ THỐNG DSS LỰA CHỌN LAPTOP",250,35,900,810,"swimlane;fontStyle=1;horizontal=1;startSize=34;fillColor=none;strokeColor=#607d8b;html=1;")
    v(r,"student","Sinh viên",45,300,100,110,ACTOR)
    v(r,"advisor","Cố vấn",45,650,100,110,ACTOR)
    v(r,"admin","Quản trị dữ liệu",1200,650,110,110,ACTOR)
    cases=[("u1","Chọn mục tiêu<br>Android / iOS",330,105),("u2","Nhập ngân sách,<br>RAM và SSD",330,245),("u3","Chọn kịch bản<br>ưu tiên",330,385),("u7","Phân tích<br>What-if",330,610),("u4","Chạy Hard Filter<br>và WSM",650,315),("u5","Xem Top 5<br>và xếp hạng",900,185),("u6","Xem lý do loại",900,445),("u8","Quản lý dữ liệu<br>mô phỏng",900,675)]
    for i,l,x,y in cases: v(r,i,l,x,y,175,90,USECASE)
    assoc=LINE+"strokeColor=#455a64;"
    for n,target in enumerate(["u1","u2","u3","u4"]): e(r,f"s{n}","student",target,"",assoc)
    e(r,"ad1","advisor","u3","",assoc); e(r,"ad2","advisor","u7","",assoc); e(r,"am1","admin","u8","",assoc)
    include=DASH+"fontSize=11;"
    e(r,"i1","u1","u4","«include»",include); e(r,"i2","u2","u4","«include»",include); e(r,"i3","u3","u4","«include»",include)
    e(r,"i4","u4","u5","«include»",include); e(r,"i5","u4","u6","«include»",include); e(r,"i6","u7","u4","«extend»",include)
    save(d,"02-use-case.drawio")


def activity():
    d,r=graph("activity-v2",1200,1050)
    v(r,"start","",585,20,30,30,"ellipse;fillColor=#000000;strokeColor=#000000;")
    v(r,"s1","Chọn mục tiêu Android / iOS / Cross-platform",410,75,380,55)
    v(r,"s2","Nhập ngân sách, RAM, SSD và kịch bản",410,160,380,55)
    v(r,"s3","Đọc và kiểm tra dữ liệu",410,245,380,55)
    v(r,"d1","Đạt<br>hard filter?",515,335,170,100,DECISION)
    v(r,"reject","Ghi phương án<br>và lý do loại",80,355,245,60,ORANGE)
    v(r,"d2","Còn phương án<br>hợp lệ?",515,490,170,100,DECISION)
    v(r,"warn","Thông báo nới lỏng<br>điều kiện",80,510,245,60,ORANGE)
    v(r,"norm","Chuẩn hóa Min–Max",410,640,380,55,ORANGE)
    v(r,"wsm","Tính đóng góp và điểm WSM",410,725,380,55,ORANGE)
    v(r,"result","Sắp xếp và hiển thị Top 5",410,810,380,55)
    v(r,"d3","Chạy<br>What-if?",515,905,170,100,DECISION)
    v(r,"end","",930,940,32,32,"ellipse;shape=doubleEllipse;fillColor=#000000;strokeColor=#000000;")
    links=[("start","s1",""),("s1","s2",""),("s2","s3",""),("s3","d1",""),("d1","reject","Không"),("d1","d2","Có"),("d2","warn","Không"),("d2","norm","Có"),("norm","wsm",""),("wsm","result",""),("result","d3",""),("d3","end","Không")]
    for n,(a,b,l) in enumerate(links): e(r,f"e{n}",a,b,l)
    e(r,"fix-reject","reject","d2","Ghi xong",ARROW,[(390,385),(390,540)])
    e(r,"loop1","warn","s2","Điều chỉnh",ARROW,[(40,540),(40,185)])
    e(r,"loop2","d3","s2","Có",ARROW,[(1040,955),(1040,185)])
    save(d,"03-activity.drawio")


def classdiagram():
    d,r=graph("class-v2",1450,900)
    cls="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=30;fillColor=#e3f2fd;strokeColor=#1565c0;html=1;fontSize=12;"
    v(r,"laptop","<b>Laptop</b><hr>laptop_id: str<br>model: str<br>os_platform: str<br>price: float<br>cpu_score: float<br>gpu_score: float<br>ram_gb: int<br>ssd_gb: int<br>battery_hours: float<br>weight_kg: float",35,85,230,260,cls)
    v(r,"criterion","<b>Criterion</b><hr>criterion_id: str<br>label: str<br>kind: benefit/cost",350,85,210,145,cls)
    v(r,"scenario","<b>Scenario</b><hr>scenario_id: str<br>label: str<br>weights: dict",650,85,210,145,cls)
    v(r,"run","<b>DecisionRun</b><hr>run_id: str<br>max_budget: float<br>min_ram: int<br>min_ssd: int<br>target: str<br>created_at: datetime",970,85,230,205,cls)
    v(r,"engine","<b>DSSEngine</b><hr>validate()<br>hard_filter()<br>normalize()<br>rank_wsm()<br>what_if()",350,520,230,205,cls)
    v(r,"result","<b>RankingResult</b><hr>run_id: str<br>laptop_id: str<br>rank: int<br>score: float<br>reject_reason: str",880,520,240,205,cls)
    assoc=ARROW+"endArrow=none;"
    e(r,"c1","criterion","scenario","1..* trọng số",assoc)
    e(r,"c2","scenario","run","Cấu hình",assoc)
    e(r,"c3","run","result","Sinh 1..*",assoc)
    e(r,"c4","laptop","result","Được đánh giá",assoc,[(150,430),(1000,430)])
    dep=DASH+"fontSize=11;"
    e(r,"c5","engine","laptop","Đọc",dep,[(220,620),(220,390)])
    e(r,"c6","engine","scenario","Sử dụng",dep,[(700,620),(700,280)])
    e(r,"c7","engine","result","Tạo",dep)
    save(d,"04-class-diagram.drawio")


def sequence():
    d,r=graph("sequence-v2",1400,950)
    actors=[("user","Sinh viên",65,ACTOR),("ui","Web UI",320,BOX),("ctrl","Controller",575,BOX),("engine","DSS Engine",830,ORANGE),("data","CSV Data",1085,GREEN)]
    for ident,label,x,sty in actors:
        v(r,ident,label,x,25,160,55,sty)
        v(r,ident+"life","",x+79,100,2,760,"dashed=1;strokeColor=#78909c;")
    msgs=[("user","ui","1. Nhập mục tiêu, ngưỡng, kịch bản"),("ui","ctrl","2. POST /"),("ctrl","data","3. load_laptops()"),("data","ctrl","4. Trả về rows"),("ctrl","engine","5. evaluate(rows, constraints, weights)"),("engine","engine","6. Hard Filter"),("engine","engine","7. Min–Max + WSM"),("engine","ctrl","8. ranking + rejected"),("ctrl","ui","9. render_template()"),("ui","user","10. Top 5 + lý do loại")]
    y=145
    for n,(a,b,label) in enumerate(msgs):
        if a==b:
            v(r,f"act{n}",label,930,y-12,210,28,"rounded=1;whiteSpace=wrap;html=1;fillColor=#fff3e0;strokeColor=#ef6c00;fontSize=11;")
        else:
            p1=point(r,f"p{n}a",dict((i,x) for i,_,x,_ in actors)[a]+80,y)
            p2=point(r,f"p{n}b",dict((i,x) for i,_,x,_ in actors)[b]+80,y)
            e(r,f"m{n}",f"p{n}a",f"p{n}b",label,DASH if n in {3,7,8,9} else "edgeStyle=none;rounded=0;html=1;endArrow=block;endFill=1;labelBackgroundColor=#ffffff;fontSize=11;")
        y+=70
    save(d,"05-sequence.drawio")


def component():
    d,r=graph("component-v2",1400,850)
    boundary="swimlane;fontStyle=1;horizontal=1;startSize=34;fillColor=#fafafa;strokeColor=#607d8b;html=1;"
    v(r,"clientlayer","CLIENT LAYER",25,45,300,730,boundary)
    v(r,"applayer","APPLICATION LAYER",375,45,600,730,boundary)
    v(r,"datalayer","DATA LAYER",1025,45,340,730,boundary)
    v(r,"web","<b>Web UI</b><br><br>Form cấu hình<br>Top 5 / Ranking<br>Lý do loại",85,140,180,190)
    v(r,"flask","<b>Flask Controller</b><br>app.py",435,140,190,80,ORANGE)
    v(r,"template","<b>Jinja + CSS</b><br>templates / static",720,140,190,80,BOX)
    v(r,"engine","<b>DSS Engine</b><br>model.py",435,350,190,80,ORANGE)
    v(r,"modules","Validation<br>Hard Filter<br>Min–Max<br>WSM<br>What-if",720,320,190,145,ORANGE)
    v(r,"cli","<b>CLI Analysis</b><br>run_analysis.py",435,590,190,80,ORANGE)
    v(r,"csv","laptops_simulated.csv",1100,150,190,75,GREEN)
    v(r,"cfg","Scenario / Criteria",1100,350,190,75,GREEN)
    v(r,"results","Ranking CSV / JSON",1100,590,190,75,GREEN)
    e(r,"x1","web","flask","HTTP / HTML",ARROW+"startArrow=block;startFill=1;")
    e(r,"x2","flask","template","Render")
    e(r,"x3","flask","engine","Gọi model")
    e(r,"x4","engine","modules","Sử dụng")
    e(r,"x5","cli","engine","Gọi model")
    e(r,"x6","engine","csv","Đọc laptop",ARROW,[(670,390),(670,265),(1060,265),(1060,188)])
    e(r,"x7","modules","cfg","Đọc cấu hình",ARROW)
    e(r,"x8","cli","results","Ghi",ARROW)
    save(d,"06-component-deployment.drawio")


if __name__=="__main__":
    OUT.mkdir(parents=True,exist_ok=True)
    architecture(); usecase(); activity(); classdiagram(); sequence(); component()
    print("Đã tạo 6 sơ đồ Draw.io v2")
