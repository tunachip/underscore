ELEMENTS: dict = {
    'water': { 
        'color': 4,
        'icon': '🌊',
        'weak_to':   ['thunder', 'plant'],
        'resists':   ['stone'],
        'immune_to': [],
        'absorbs':   ['fire'],
    },
    'stone': { 
        'color': 136,
        'icon': '🪨',
        'weak_to':   ['water', 'force'],
        'resists':   ['fire'],
        'immune_to': ['thunder'],
        'absorbs':   [],
    },
    'fire': {
        'color': 196,
        'icon': '🔥',
        'weak_to':   ['water', 'stone'],
        'resists':   [],
        'immune_to': [],
        'absorbs':   ['plant'],
    },
    'plant': { 
        'color': 112,
        'icon': '🌿',
        'weak_to':   ['fire', 'vital'],
        'resists':   [],
        'immune_to': [],
        'absorbs':   ['water'],
    },
    'vital': { 
        'color': 198,
        'icon': '❤️',
        'weak_to':   ['vital', 'force'],
        'resists':   [],
        'immune_to': [],
        'absorbs':   [],
    },
    'force': {
        'color': 36,
        'icon': '💨',
        'weak_to':   ['thunder'],
        'resists':   ['vital'],
        'immune_to': ['stone'],
        'absorbs':   [],
    },
    'thunder':  { 
        'color': 184,
        'icon': '⚡',
        'weak_to':   ['stone'],
        'resists':   ['water'],
        'immune_to': ['force'],
        'absorbs':   [],
    },
}

STATUSES: dict = {
    'burn': {
        'color': 167,
        'icon': '🔥',
        'deals': 'fire',
        'max_amount': 3,
    },
    'wound': {
        'color': 168,
        'icon': '🩸',
        'deals': 'vital',
        'max_amount': 1000,
    },
    'decay': {
        'color': 30,
        'icon': '💀',
        'deals': 'force',
        'max_amount': 5,
    },
    'regen': {
        'color': 70,
        'icon': '✨',
        'deals': 'plant',
        'max_amount': 5,
    },
    'slow': {
        'color': 172,
        'icon': '🐌',
        'deals': 'none',
        'max_amount': 1,
    },
    'quick': {
        'color': 229,
        'icon': '⚡',
        'deals': 'none',
        'max_amount': 1,
    },
    'angry': {
        'color': 174,
        'icon': '😡',
        'deals': 'none',
        'max_amount': 3,
    },
    'curse': {
        'color': 56,
        'icon': '😈',
        'deals': 'none',
        'max_amount': 3,
    },
    'stun': {
        'color': 184,
        'icon': '😵',
        'deals': 'none',
        'max_amount': 3,
    },
    'sleep': {
        'color': 107,
        'icon': '💤',
        'deals': 'none',
        'max_amount': 3,
    },
    'tough': {
        'color': 94,
        'icon': '🛡️',
        'deals': 'none',
        'max_amount': 3,
    },
    'strong': {
        'color': 1,
        'icon': '💪',
        'deals': 'none',
        'max_amount': 3,
    }
}


