# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lightgbm_embedding']

package_data = \
{'': ['*']}

install_requires = \
['lightgbm>=3.0.0,<4.0.0', 'pandas>=1.0.0,<2.0.0', 'scikit-learn>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'lightgbm-embedding',
    'version': '0.1.0',
    'description': 'Feature embeddings with LightGBM',
    'long_description': '# LightGBM Embeddings\n\nFeature embeddings with LightGBM\n\n\n## Examples\n```python\nimport pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom lightgbm_embedding import LightgbmEmbedding\n\ndf = pd.read_csv(\n    "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv"\n)\ncols = df.columns[:-1]\ntarget = df.columns[-1]\nnum_classes = df[target].nunique()\n\nX_train, X_test = train_test_split(\n    df, test_size=0.2, stratify=df[target], random_state=42\n)\n\nn_dim = 20\nemb = LightgbmEmbedding(n_dim=n_dim)\nemb.fit(X_train[cols], X_train[target])\nX_train_embed = emb.transform(X_train[cols])\nX_test_embed = emb.transform(X_test[cols])\n```\n',
    'author': 'Atilla Karaahmetoğlu',
    'author_email': 'atilla.karaahmetoglu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
