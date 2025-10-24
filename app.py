import streamlit as st
import osmnx as ox
import networkx as nx
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Melhor Rota de Rua", layout="wide")

st.title("🚗 Melhor Rota de Rua (OpenStreetMap + Streamlit)")

origem = st.text_input("Digite o ponto de origem (ex: Marina Bay Sands, Singapore):")
destino = st.text_input("Digite o ponto de destino (ex: Orchard Road, Singapore):")

modo = st.selectbox("Modo de transporte", ["drive", "walk", "bike"])
botao = st.button("Calcular rota")

if botao and origem and destino:
    with st.spinner("Calculando rota..."):
        try:
            # Geocodifica endereços
            origem_coord = ox.geocode(origem)
            destino_coord = ox.geocode(destino)

            # Baixa o grafo da região
            G = ox.graph_from_point(origem_coord, dist=3000, network_type=modo)

            # Encontra nós mais próximos
            origem_n = ox.distance.nearest_nodes(G, origem_coord[1], origem_coord[0])
            destino_n = ox.distance.nearest_nodes(G, destino_coord[1], destino_coord[0])

            # Calcula rota mais curta
            rota = nx.shortest_path(G, origem_n, destino_n, weight="length")

            # Extrai coordenadas da rota
            rota_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in rota]

            # Cria mapa
            m = folium.Map(location=origem_coord, zoom_start=14)
            folium.PolyLine(rota_coords, color="red", weight=5, opacity=0.8).add_to(m)
            folium.Marker(origem_coord, popup="Origem", icon=folium.Icon(color="green")).add_to(m)
            folium.Marker(destino_coord, popup="Destino", icon=folium.Icon(color="red")).add_to(m)
