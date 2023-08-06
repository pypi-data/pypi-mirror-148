from .models import Dashboard
from .session import APISession


class GrafanaError(Exception):
    pass


class Grafana:
    def __init__(self, url, api_key):
        self.session = APISession(url, api_key)

    def __str__(self):
        return self.session.url

    def __repr__(self):
        return f'Grafana("{self.session.url}")'

    def health(self):
        r = self.session.get('/api/health')
        if r.status_code != 200:
            raise GrafanaError('no 200 on /api/health')
        elif r.json()['database'] != 'ok':
            raise GrafanaError('database nok')
        else:
            return True

    def dashboards(self):
        result = []
        # https://grafana.com/docs/grafana/latest/http_api/folder_dashboard_search/
        r = self.session.get('/api/search?query=&starred=false')
        r.raise_for_status()
        search_results = r.json()
        uids = [sr['uid'] for sr in search_results if sr['type'] == 'dash-db']
        for uid in uids:
            d = self.session.get(f'/api/dashboards/uid/{uid}').json()['dashboard']
            result.append(Dashboard(d))
        return result
