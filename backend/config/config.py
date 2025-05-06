"""
Configuration for YKS chatbot: question counts, thresholds, and resources.
"""
QUESTION_COUNTS = {
    'TYT': {
        'matematik': 40,
        'turkce': 40,
        'sosyal': 20,
        'fen': 20
    },
    'AYT': {
        'matematik': 30,
        'fizik': 14,
        'kimya': 13,
        'biyoloji': 13,
        'geometri': 10,
        'sosyal': 40
    }
}

NET_THRESHOLD_PERCENTAGE = 0.5

YOUTUBE_RESOURCES = {
    'matematik': [
        {'channel': 'Mert Hoca', 'link': 'https://www.youtube.com/@MertHoca', 'topics': ['Limit', 'Türev', 'İntegral', 'Logaritma']},
        {'channel': 'Bıyıklı Matematik', 'link': 'https://www.youtube.com/@BiyikliMatematik', 'topics': ['Limit', 'Polinomlar', 'Logaritma']},
    ],
    'fizik': [
        {'channel': 'Fizik Arşivi', 'link': 'https://www.youtube.com/@FizikArsivi', 'topics': ['Atışlar', 'Elektrik', 'Manyetizma']},
        {'channel': 'Hocalara Geldik', 'link': 'https://www.youtube.com/@HocalaraGeldik', 'topics': ['Atışlar', 'Enerji']},
    ],
    'kimya': [
        {'channel': 'Kimya Bilimi', 'link': 'https://www.youtube.com/@KimyaBilimi', 'topics': ['Organik Kimya', 'Asit-Baz']},
    ],
    'biyoloji': [
        {'channel': 'Biyoloji Dersi', 'link': 'https://www.youtube.com/@BiyolojiDersi', 'topics': ['Genden Protein', 'Hücre']},
    ],
    'turkce': [
        {'channel': 'Rüştü Hoca ile Türkçe', 'link': 'https://www.youtube.com/@RustuHocaileTurkce', 'topics': ['Paragraf', 'Dil Bilgisi']},
    ],
    'sosyal': [
        {'channel': 'Benim Hocam', 'link': 'https://www.youtube.com/@BenimHocam', 'topics': ['Tarih', 'Coğrafya']},
    ],
    'geometri': [
        {'channel': 'Eyüp B. Matematik & Geometri', 'link': 'https://www.youtube.com/@EyupBMatematikGeometri', 'topics': ['Prizmalar', 'Küre']},
    ]
}

DEFAULT_TOPICS = {
    'matematik': ['Limit', 'Türev', 'İntegral', 'Logaritma'],
    'fizik': ['Atışlar', 'Elektrik', 'Manyetizma', 'Enerji'],
    'kimya': ['Organik Kimya', 'Çözünürlük Dengesi', 'Asit-Baz'],
    'biyoloji': ['Genden Protein', 'Bitki Biyolojisi', 'Hücre'],
    'turkce': ['Paragraf', 'Dil Bilgisi', 'Anlam'],
    'sosyal': ['Tarih', 'Coğrafya', 'Felsefe'],
    'geometri': ['Prizmalar', 'Küre', 'Silindir']
}
