from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Alborz

# Auto-generated `LayerMapping` dictionary for alborz model
alborz_mapping = {
    'per_nam': 'PER_NAM',
    'center': 'CENTER',
    'bakhsh': 'BAKHSH',
    'shahrestan': 'SHAHRESTAN',
    'ostan': 'OSTAN',
    'area': 'Area',
    'hectares': 'Hectares',
    'geom': 'POLYGON',
}

alborz_shp = Path(__file__).resolve().parent / 'data' / 'alborz.shp'


def run(verbose=True):
    lm_alborz = LayerMapping(Alborz, alborz_shp, alborz_mapping, transform=False)
    lm_alborz.save(strict=True, verbose=verbose)

run()