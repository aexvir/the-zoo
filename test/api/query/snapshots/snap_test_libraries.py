# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_all 1'] = {
    'data': {
        'allLibraries': {
            'edges': [
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy one',
                        'owner': 'platform',
                        'slackChannel': '#slack',
                        'sonarqubeProject': 'sonar'
                    }
                },
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy second',
                        'owner': 'platform soft',
                        'slackChannel': '#slack-second',
                        'sonarqubeProject': 'sonar-qub'
                    }
                },
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy third',
                        'owner': 'platform software',
                        'slackChannel': '#slack-third',
                        'sonarqubeProject': 'sonar-qube'
                    }
                },
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy fourth',
                        'owner': 'platform software plus',
                        'slackChannel': '#slack-fourth',
                        'sonarqubeProject': 'sonar-qubeee'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'NA==',
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 4
        }
    }
}

snapshots['test_empty 1'] = {
    'data': {
        'allLibraries': {
            'edges': [
            ],
            'totalCount': 0
        }
    }
}

snapshots['test_first 1'] = {
    'data': {
        'allLibraries': {
            'edges': [
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy one',
                        'owner': 'platform',
                        'slackChannel': '#slack',
                        'sonarqubeProject': 'sonar'
                    }
                },
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy second',
                        'owner': 'platform soft',
                        'slackChannel': '#slack-second',
                        'sonarqubeProject': 'sonar-qub'
                    }
                },
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy third',
                        'owner': 'platform software',
                        'slackChannel': '#slack-third',
                        'sonarqubeProject': 'sonar-qube'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'Mw==',
                'hasNextPage': True,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 4
        }
    }
}

snapshots['test_first_after 1'] = {
    'data': {
        'allLibraries': {
            'edges': [
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy second',
                        'owner': 'platform soft',
                        'slackChannel': '#slack-second',
                        'sonarqubeProject': 'sonar-qub'
                    }
                },
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy third',
                        'owner': 'platform software',
                        'slackChannel': '#slack-third',
                        'sonarqubeProject': 'sonar-qube'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'Mw==',
                'hasNextPage': True,
                'hasPreviousPage': True,
                'startCursor': 'Mg=='
            },
            'totalCount': 4
        }
    }
}

snapshots['test_last 1'] = {
    'data': {
        'allLibraries': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 7,
                    'line': 3
                }
            ],
            'message': 'Pagination "last" works only in combination with "before" argument.',
            'path': [
                'allLibraries'
            ]
        }
    ]
}

snapshots['test_last_before 1'] = {
    'data': {
        'allLibraries': {
            'edges': [
            ],
            'pageInfo': {
                'endCursor': None,
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': None
            },
            'totalCount': 4
        }
    }
}

snapshots['test_with_repository 1'] = {
    'data': {
        'allLibraries': {
            'edges': [
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy one',
                        'owner': 'platform',
                        'repository': {
                            'name': 'thiwer',
                            'owner': 'jasckson',
                            'remoteId': 125,
                            'url': 'https://gitlab.com/thiwer/thiwer'
                        },
                        'slackChannel': '#slack',
                        'sonarqubeProject': 'sonar'
                    }
                },
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy second',
                        'owner': 'platform soft',
                        'repository': {
                            'name': 'parker',
                            'owner': 'peter',
                            'remoteId': 234,
                            'url': 'https://gitlab.com/peter/parker'
                        },
                        'slackChannel': '#slack-second',
                        'sonarqubeProject': 'sonar-qub'
                    }
                },
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy third',
                        'owner': 'platform software',
                        'repository': {
                            'name': 'smith',
                            'owner': 'black',
                            'remoteId': 2134539,
                            'url': 'https://gitlab.com/black/smith'
                        },
                        'slackChannel': '#slack-third',
                        'sonarqubeProject': 'sonar-qube'
                    }
                },
                {
                    'node': {
                        'docsUrl': None,
                        'id': 'TGlicmFyeTpOb25l',
                        'impact': 'employees',
                        'libraryUrl': None,
                        'lifecycle': 'fixed',
                        'name': 'fancy fourth',
                        'owner': 'platform software plus',
                        'repository': {
                            'name': 'kent',
                            'owner': 'clark',
                            'remoteId': 124,
                            'url': 'https://gitlab.com/clark/kent'
                        },
                        'slackChannel': '#slack-fourth',
                        'sonarqubeProject': 'sonar-qubeee'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'NA==',
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 4
        }
    }
}
