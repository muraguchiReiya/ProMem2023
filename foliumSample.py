import sys
import folium

print(f"""Python
{sys.version}

folium
{folium.__version__}""")

# 公立千歳科学技術大学の緯度経度
office_lat = 42.7935359
office_lng = 141.6938043

#科技大周辺をhtml形式で表示
fmap1 = folium.Map(
    location=[office_lat, office_lng],
    tiles = "OpenStreetMap",
    zoom_start = 20 # 描画時の倍率 1〜20
    #width = 800, height = 800 # 地図のサイズ
)

#マップをhtml形式で保存
fmap1.save("./html/map.html")

#マーカーの設置
fmap2 = folium.Map(
    location=[office_lat, office_lng],
    zoom_start=20
)
folium.Marker([office_lat, office_lng], popup="公立千歳科学技術大学").add_to(fmap2)

fmap2.save("./html/marker_on_map.html")

#地図上に線を引く
import itertools as it

# 千歳科技大を中心にした四角形の頂点
sq = [
    (office_lat + dy * pow(10, -3), office_lng + dx * pow(10, -3))
    for dx, dy in it.product([-1, 1], [-1, 1])
]
fmap3 = folium.Map(location=[office_lat, office_lng], zoom_start=20)
folium.PolyLine(locations=sq).add_to(fmap3)
fmap3.save("./html/line_on_map.html")

#面を塗る
sw, nw, se, ne = sq
fmap4 = folium.Map(location=[office_lat, office_lng], zoom_start=20)
folium.Polygon(
    locations=[sw, se, ne, nw], # 多角形の頂点
    color="red", # 線の色
    weight=10, # 線の太さ
    fill=True, # 塗りつぶす
    fill_opacity=0.5 # 透明度（1=不透明）
).add_to(fmap4)

fmap4.save("./html/square_on_map.html")

#GeoJSONを用いた描画

import geojson as gj

# (lat、lng)のリスト
# ポイント1. 最初と最後の要素が同じ値
lat_lng = [sw, se, ne, nw, sw]

# ポイント2. (lng, lat)に変換する
def swap(p):
    return p[1], p[0]
lng_lat = list(map(swap, lat_lng))

# ポイント3. （lng、lat）のリストのリストにする
lng_lat2 = [lng_lat]

poly5 = gj.Polygon(lng_lat2)
fmap5 = folium.Map(location=[office_lat, office_lng], zoom_start=20)
folium.GeoJson(poly5).add_to(fmap5)
fmap5.save("./html/Sample1.html")


#複数ポリゴン描画
def slide(poly, i):
    """
    ポリゴンを、ちょっとズラす関数
    """
    vtx = poly["coordinates"][0] # gj.Polygonのcoodinateは、頂点のリスト"のリスト"
    vtx2 = [
        (lng + i * pow(10, -3), lat + i * pow(10, -3))
        for lng, lat in vtx
    ]
    return gj.Polygon([vtx2]) # gj.Polygonのcoodinateは（略）

fmap6 = folium.Map(location=[office_lat, office_lng], zoom_start=16)
polys6 = [slide(poly5, i) for i in range(-2, 3)]
fc6 = gj.FeatureCollection(polys6)
folium.GeoJson(fc6).add_to(fmap6)
fmap6.save("./html/Sample2.html")

fmap7 = folium.Map(location=[office_lat, office_lng], zoom_start=16)
fc7 = gj.FeatureCollection(
    features=[
        gj.Feature(
            geometry=p,
            id=i
        ) for i, p in enumerate(polys6)
    ]
)
folium.GeoJson(fc7).add_to(fmap7)
fmap7.save("./html/Sample3.html")

#Polygonの書式を変更
fmap8 = folium.Map(location=[office_lat, office_lng], zoom_start=16)
folium.GeoJson(
    fc7,
    style_function=lambda feature: {
        "fillColor": "red",
        "color": "black",
        "weight": 10 / (feature["id"] + 1),
        "fillOpacity": feature["id"] * 0.2
    }).add_to(fmap8)
fmap8.save("./html/Sample4.html")