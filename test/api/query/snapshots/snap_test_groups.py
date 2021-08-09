# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_all 1'] = {
    'data': {
        'allGroups': {
            'edges': [
                {
                    'node': {
                        'id': 'R3JvdXA6MQ==',
                        'maintainers': [
                            'clark',
                            'kent'
                        ],
                        'productOwner': 'john',
                        'projectOwner': 'doe'
                    }
                },
                {
                    'node': {
                        'id': 'R3JvdXA6MjQ=',
                        'maintainers': [
                            'black',
                            'smith'
                        ],
                        'productOwner': 'black',
                        'projectOwner': 'smith'
                    }
                },
                {
                    'node': {
                        'id': 'R3JvdXA6MjQ0',
                        'maintainers': [
                            'vanguard',
                            'shield'
                        ],
                        'productOwner': 'vanguard',
                        'projectOwner': 'shield'
                    }
                },
                {
                    'node': {
                        'id': 'R3JvdXA6MjQ2',
                        'maintainers': [
                            'lich',
                            'king'
                        ],
                        'productOwner': 'lich',
                        'projectOwner': 'king'
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
        'allGroups': {
            'edges': [
            ],
            'totalCount': 0
        }
    }
}

snapshots['test_first 1'] = {
    'data': {
        'allGroups': {
            'edges': [
                {
                    'node': {
                        'id': 'R3JvdXA6MQ==',
                        'maintainers': [
                            'clark',
                            'kent'
                        ],
                        'productOwner': 'john',
                        'projectOwner': 'doe'
                    }
                },
                {
                    'node': {
                        'id': 'R3JvdXA6MjQ=',
                        'maintainers': [
                            'black',
                            'smith'
                        ],
                        'productOwner': 'black',
                        'projectOwner': 'smith'
                    }
                },
                {
                    'node': {
                        'id': 'R3JvdXA6MjQ0',
                        'maintainers': [
                            'vanguard',
                            'shield'
                        ],
                        'productOwner': 'vanguard',
                        'projectOwner': 'shield'
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
        'allGroups': {
            'edges': [
                {
                    'node': {
                        'id': 'R3JvdXA6MjQ=',
                        'maintainers': [
                            'black',
                            'smith'
                        ],
                        'productOwner': 'black',
                        'projectOwner': 'smith'
                    }
                },
                {
                    'node': {
                        'id': 'R3JvdXA6MjQ0',
                        'maintainers': [
                            'vanguard',
                            'shield'
                        ],
                        'productOwner': 'vanguard',
                        'projectOwner': 'shield'
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
        'allGroups': None
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
                'allGroups'
            ]
        }
    ]
}

snapshots['test_last_before 1'] = {
    'data': {
        'allGroups': {
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
