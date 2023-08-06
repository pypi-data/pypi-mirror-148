# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyeph',
 'pyeph.calc',
 'pyeph.calc.labor_market',
 'pyeph.calc.poverty',
 'pyeph.calc.template',
 'pyeph.get',
 'pyeph.get.basket',
 'pyeph.get.equivalent_adult',
 'pyeph.get.mautic',
 'pyeph.get.microdata',
 'pyeph.tools']

package_data = \
{'': ['*'], 'pyeph': ['.files/*'], 'pyeph.tools': ['.examples/*']}

install_requires = \
['ipykernel>=6.13.0,<7.0.0', 'pandas>=1.1.5,<2.0.0', 'wget>=3.2,<4.0']

setup_kwargs = {
    'name': 'pyeph',
    'version': '1.1.3',
    'description': "PyEPH es una librería para el procesamiento de la Encuesta Permanente de Hogares (eph) en Python. Permite la descarga de archivos de EPH's y otros como la canasta basica y adulto equivalente , como asi también algunos calculos rápidos relacionados con las mismas",
    'long_description': 'PyEPH - Libreria para el procesamiento de la Encuesta Permanente de Hogares para Python\n===\n\n![PyPI](https://img.shields.io/pypi/v/pyeph?color=orange&style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/pyeph?color=purple&style=flat-square)\n\nLa librería Pyeph tiene como objetivo facilitar el procesamiento en Python de las [Encuesta Permanente de Hogares (eph)](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos) publicadas por INDEC de forma periódica. Está pensada como un espacio donde se nuclean y centralizan los cálculos vinculados a las mismas para posteriormente ser utilizadas en investigaciones, artículos, publicaciones, etc.\nEs una librería que hace principal hincapié en la transparencia metodológica utilizando licencias de código abierto y que promueve la colaboración de las comunidades de cientístas de datos, sociales, investigadorxs, desarrolladorxs, periodistas y demás curiosxs.\n\nPermite la descarga de archivos de `EPH\'s` y otros como la `canasta basica` y `adulto equivalente` , como asi también algunos calculos rápidos relacionados con las mismas\n\n# Instalación\n\nPueden probar nuestra notebook de ejemplo en Google Colab\n\n<a href="https://colab.research.google.com/github/institutohumai/pyeph/blob/main/examples.ipynb"> <img src=\'https://colab.research.google.com/assets/colab-badge.svg\' /> </a>\n<div align="center"> Recordá abrir en una nueva pestaña </div>\n\n### Prerequisitos\n- [Python 3](https://www.python.org/)\n- [pip](https://www.pypi.org/)\n### Instalando PyEPH\n\n- Abra una terminal del sistema y escriba \n\n```bash\n$ pip install pyeph\n```\n\n# Uso básico\n\nLos siguientes son algunos ejemplos de uso. Para ver todos los cálculos podés ir para la documentación\n\nEn inglés\n\n```python\nimport pyeph\n\n# Obtención\neph = pyeph.get(data="eph", year=2021, period=2, base_type=\'individual\') # EPH individual\nbasket = pyeph.get(data="canastas") # canasta basica total y alimentaria\nadequi = pyeph.get(data="adulto-equivalente") # adulto equivalente\n\n# Cálculos de ejemplo de pobreza \npoverty = pyeph.Poverty(eph, basket)\npopulation_poverty = poverty.population(group_by=\'CH04\') # Población pobre por sexo \nlabeled_poverty = pyeph.map_labels(population_poverty) # Etiquetado de las variables\n\n# Cálculos de Mercado Laboral\nlabor_market = pyeph.LaborMarket(eph)\nunemployment = labor_market.unemployment(group_by="REGION", div_by="PT") # Desempleo agrupado por region y dividiendo por Población Total\nlabeled_unemployment = pyeph.map_labels(unemployment) # Etiquetado de las variables\n```\n\nEn español\n\n```python\nimport pyeph\n\n# Obtención\neph = pyeph.obtener(data="eph", ano=2021, periodo=2, tipo_base=\'individual\') # EPH individual\ncanastas = pyeph.obtener(data="canastas") # canasta basica total y alimentaria\nadequi = pyeph.obtener(data="adulto-equivalente") # adulto equivalente\n\n# Cálculos de ejemplo de pobreza \npobreza = pyeph.Pobreza(eph, canastas)\npoblacion_pobre = pobreza.poblacion(agrupar_por=\'CH04\') # Población pobre por sexo \netiquetado = pyeph.etiquetar(poblacion_pobre) # Etiquetado de las variables\n\n# Cálculos de Mercado Laboral\nmercado_laboral = pyeph.MercadoLaboral(eph)\ndesempleo = mercado_laboral.desempleo(agrupar_por="REGION", div_por="PT") # Desempleo agrupado por region y dividiendo por Población Total\netiquetada = pyeph.etiquetar(desempleo) # Etiquetado de las variables\n```\n\n# Documentación\n\n[Link del sitio de la documentación](https://github.com/) (Aún en desarrollo)\n\n---\n\n### Tenga en cuenta\n\nEsta librería se encuentra en estado permanente de desarrollo.\n\n> Cualquier colaboración es bienvenida\n\n\n## Agradecimientos\n\nDejamos aquí un especial agradecimiento al equipo de desarrollo de la librería [EPH en R](https://holatam.github.io/eph/authors.html). Todo el amor para elles ❤️\n\n---\n⌨️ con ❤️\n\n',
    'author': 'Maria Carolina Trogliero, Mariano Valdez Anopa, Maria Gaska',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
