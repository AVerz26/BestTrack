import streamlit as st
import osmnx as ox
import networkx as nx
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Melhor Rota de Rua", layout="wide")

st.title("🚗 Melhor Rota de Rua (OpenStreetMap + Streamlit)")

# Entradas do usuário
origem = st.text_input("Digite o ponto de origem:")
destino = st.text_input("Digite o ponto de destino:")

modo = st.selectbox("Modo de transporte", ["car", "bike", "walk"])
botao = st.button("Calcular rota")

if botao and origem and destino:
    with st.spinner("Calculando rota..."):
        try:
            # Geocodificar os endereços
            orig_coord = ox.geocode(origem)
            dest_coord = ox.geocode(destino)

            # Baixar o grafo da área
            G = ox.graph_from_point(orig_coord, dist=3000, network_type=modo)

            # Pegar os nós mais próximos
            origem_n = ox.distance.nearest_nodes(G, orig_coord[1], orig_coord[0])
            destino_n = ox.distance.nearest_nodes(G, dest_coord[1], dest_coord[0])

            # Calcular a rota mais curta
            rota = nx.shortest_path(G, origem_n, destino_n, weight='length')

            # Criar o mapa
            m = ox.plot_graph_folium(G, route=rota, route_color='red', route_width=5)
            folium.Marker(origem, popup="Origem", icon=folium.Icon(color="green")).add_to(m)
            folium.Marker(destino, popup="Destino", icon=folium.Icon(color="red")).add_to(m)

            st_folium(m, width=900, height=600)

        except Exception as e:
            st.error(f"Erro: {e}")
