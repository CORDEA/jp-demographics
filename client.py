import os
from dataclasses import dataclass

import requests

APP_ID = os.environ['APP_ID']
LANG = 'J'
BASE_URL = 'https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?appId={id}&lang={lang}'.format(id=APP_ID,
                                                                                                   lang=LANG
                                                                                                   )


@dataclass
class Response:
    labels: dict[str, dict]
    data: dict


def fetch_stats(sid: str) -> Response:
    json = requests.get('{url}&statsDataId={id}'.format(url=BASE_URL, id=sid)).json()
    stats = json['GET_STATS_DATA']['STATISTICAL_DATA']
    labels = stats['CLASS_INF']['CLASS_OBJ']
    label_map = {label['@id']: {l['@code']: l['@name'] for l in label['CLASS']} for label in labels}
    data = stats['DATA_INF']['VALUE']
    return Response(data=data, labels=label_map)
