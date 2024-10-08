import folium
from folium.plugins import Fullscreen

from django.shortcuts import render

from dashboard.models import Projet


def index(request):
    les_projets = Projet.objects.all()[:5]

    lat = 36.818278
    long = 10.185722

    # Créer la carte
    m = folium.Map(
        location=[lat, long],
        zoom_start=16,
        tiles=None
    )

    folium.TileLayer(
        tiles='https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Maps',
        max_zoom=20,
        subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
        overlay=False,
        control=True
    ).add_to(m)

    folium.Marker(
        [lat, long],
        popup="Espace Design International",
        tooltip="Cliquez pour plus d'information",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

    # Ajouter des contrôles à la carte
    folium.LayerControl().add_to(m)
    Fullscreen().add_to(m)

    map_html = m._repr_html_()

    return render(request, 'landing_page/index.html', {"map": map_html, 'les_projets': les_projets})


def projets(request):
    les_projets = Projet.objects.all()[:5]
    return render(request, 'landing_page/projets.html', context={'les_projets': les_projets})
