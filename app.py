import streamlit as st
import osmnx as ox
import networkx as nx
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Melhor Rota de Rua", layout="wide")

st.title("🚗 Melhor Rota de Rua (OpenStreetMap + Streamlit)")

# Entradas
origem = st.text_input("Origem (ex: Marina Bay Sands, Singapore)")
destino = st.text_input("Destino (ex: Orchard Road, Singapore)")
modo = st.selectbox("Modo de transporte", ["drive", "walk", "bike"])

vel_drive = 80
vel_bike = 35
vel_walk = 10

if modo == 'drive':
    valor = vel_drive
elif modo == 'walk':
    valor = vel_walk
else:
    valor = vel_bike

botao = st.button("Calcular rota")

# Sessão para guardar dados
if "rota_mapa" not in st.session_state:
    st.session_state.rota_mapa = None
    st.session_state.dist_km = None

if botao and origem and destino:
    with st.spinner("Calculando rota..."):
        try:
            origem_coord = ox.geocode(origem)
            destino_coord = ox.geocode(destino)

            G = ox.graph_from_point(origem_coord, dist=50000, network_type=modo)
            origem_n = ox.distance.nearest_nodes(G, origem_coord[1], origem_coord[0])
            destino_n = ox.distance.nearest_nodes(G, destino_coord[1], destino_coord[0])

            rota = nx.shortest_path(G, origem_n, destino_n, weight="length")
            rota_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in rota]

            # Calcula distância total (metros → km)
            comprimento = nx.path_weight(G, rota, weight="length") / 1000

            # Cria o mapa
            m = folium.Map(location=origem_coord, zoom_start=14, control_scale=True)
            folium.PolyLine(rota_coords, color="red", weight=5, opacity=0.8).add_to(m)
            folium.Marker(origem_coord, popup="Origem", icon=folium.Icon(color="green")).add_to(m)
            folium.Marker(destino_coord, popup="Destino", icon=folium.Icon(color="red")).add_to(m)

            # Salva no estado
            st.session_state.rota_mapa = m
            st.session_state.dist_km = round(comprimento, 2)
            duracao =  round(st.session_state.dist_km / valor, 1)

        except Exception as e:
            st.error(f"Erro: {e}")

# Exibe o mapa fixo (sem causar reload)
if st.session_state.rota_mapa:
    st_folium(st.session_state.rota_mapa, width=900, height=600, returned_objects=[])

    if st.session_state.dist_km:
        st.success(f"🛣️ Distância total: {st.session_state.dist_km} km - Tempo estimado: {duracao} horas. ")
