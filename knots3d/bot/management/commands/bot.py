from django.core.management.base import BaseCommand
import requests
from django.conf import settings
import telebot
from PIL import Image, ImageEnhance, ImageOps
from string import Template
import imageio
import asyncio
import threading
import time

import knots3d.settings
from bot.models import alleknotentabelle, Favorite, Deleting, Language

bot = telebot.TeleBot('1665350063:AAEGFWkNxo3PMWUsX2WPgtt0uSrJdJdtz2E', threaded=False)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('⬅', '🔍Search')


encode = {
    'camping': {
        'type_eng': 'Kind',
        'type_de': 'Nett',
        'type_esp': 'Tipo',
        'type_ru': 'Вид',
        'type_fr': 'Gentil',
        'type_it': 'Genere',
        'type_tuek': 'Tür',
        'type_zh': '種類',
        'type_ja': '種類',
        'type_vi': 'Tốt bụng',
        'type_pt': 'Gentil',
        'type_ko': '종류',
        'name_eng': 'Camping',
        'name_de': 'Camping',
        'name_esp': 'Acampada',
        'name_ru': 'Походы с палатками',
        'name_fr': 'Camping',
        'name_it': 'Campeggio',
        'name_tuek': 'Kamping',
        'name_zh': '野營',
        'name_ja': 'キャンプ',
        'name_vi': 'Cắm trại',
        'name_pt': 'Acampamento',
        'name_ko': '캠핑',
        'img': '⛺'
    },
    'boot': {
        'type_eng': 'Kind',
        'type_de': 'Nett',
        'type_esp': 'Tipo',
        'type_ru': 'Вид',
        'type_fr': 'Gentil',
        'type_it': 'Genere',
        'type_tuek': 'Tür',
        'type_zh': '種類',
        'type_ja': '種類',
        'type_vi': 'Tốt bụng',
        'type_pt': 'Gentil',
        'type_ko': '종류',
        'name_eng': 'Seafaring',
        'name_de': 'Seefahrt',
        'name_esp': 'Marinera',
        'name_ru': 'Лодочный спорт',
        'name_fr': 'Seafaring',
        'name_it': 'Nautica',
        'name_tuek': 'Denizcilik',
        'name_zh': '航海的',
        'name_ja': '船乗り',
        'name_vi': 'Đi biển',
        'name_pt': 'Marítimo',
        'name_ko': '항해',
        'img': '⚓'
    },
    'verschieden': {
        'type_eng': 'Kind',
        'type_de': 'Nett',
        'type_esp': 'Tipo',
        'type_ru': 'Вид',
        'type_fr': 'Gentil',
        'type_it': 'Genere',
        'type_tuek': 'Tür',
        'type_zh': '種類',
        'type_ja': '種類',
        'type_vi': 'Tốt bụng',
        'type_pt': 'Gentil',
        'type_ko': '종류',
        'name_eng': 'Miscellaneous',
        'name_de': 'Verschiedenes',
        'name_esp': 'Misceláneo',
        'name_ru': 'Разное',
        'name_fr': 'Divers',
        'name_it': 'Varie',
        'name_tuek': 'çeşitli',
        'name_zh': '各種各樣的',
        'name_ja': 'その他',
        'name_vi': 'Điều khoản khác',
        'name_pt': 'Diversos',
        'name_ko': '여러 가지 잡다한',
        'img': '🛠'
    },
    'kletter': {
        'type_eng': 'Kind',
        'type_de': 'Nett',
        'type_esp': 'Tipo',
        'type_ru': 'Вид',
        'type_fr': 'Gentil',
        'type_it': 'Genere',
        'type_tuek': 'Tür',
        'type_zh': '種類',
        'type_ja': '種類',
        'type_vi': 'Tốt bụng',
        'type_pt': 'Gentil',
        'type_ko': '종류',
        'name_eng': 'Climbing',
        'name_de': 'Klettern',
        'name_esp': 'Escalada',
        'name_ru': 'Альпинизм',
        'name_fr': 'Escalade',
        'name_it': 'Arrampicata',
        'name_tuek': 'Dağcılık',
        'name_zh': '攀登',
        'name_ja': 'クライミング',
        'name_vi': 'Leo',
        'name_pt': 'Escalando',
        'name_ko': '등반',
        'img': '🏔'
    },
    'feuerwehr': {
        'type_eng': 'Kind',
        'type_de': 'Nett',
        'type_esp': 'Tipo',
        'type_ru': 'Вид',
        'type_fr': 'Gentil',
        'type_it': 'Genere',
        'type_tuek': 'Tür',
        'type_zh': '種類',
        'type_ja': '種類',
        'type_vi': 'Tốt bụng',
        'type_pt': 'Gentil',
        'type_ko': '종류',
        'name_eng': 'Fire + Rescue',
        'name_de': 'Feuerwehr',
        'name_esp': 'Bomberos y Rescate',
        'name_ru': 'Пожары + спасение',
        'name_fr': 'Pompiers',
        'name_it': 'Incendi e Salvataggio',
        'name_tuek': 'İtfaiye',
        'name_zh': '消防+救援',
        'name_ja': '消防+救助',
        'name_vi': 'Cứu hỏa + Cứu hộ',
        'name_pt': 'Fogo + Resgate',
        'name_ko': '화재 + 구조',
        'img': '🔥'
    },
    'angeln': {
        'type_eng': 'Kind',
        'type_de': 'Nett',
        'type_esp': 'Tipo',
        'type_ru': 'Вид',
        'type_fr': 'Gentil',
        'type_it': 'Genere',
        'type_tuek': 'Tür',
        'type_zh': '種類',
        'type_ja': '種類',
        'type_vi': 'Tốt bụng',
        'type_pt': 'Gentil',
        'type_ko': '종류',
        'name_eng': 'Fishing',
        'name_de': 'Angeln',
        'name_esp': 'Pesca',
        'name_ru': 'Рыбалка',
        'name_fr': 'Pêche',
        'name_it': 'Pesca',
        'name_tuek': 'Balık Tutma',
        'name_zh': '釣魚',
        'name_ja': '釣り',
        'name_vi': 'Đánh bắt cá',
        'name_pt': 'pescaria',
        'name_ko': '어업',
        'img': '🎣'
    },
    'hilfe': {
        'type_eng': 'Kind',
        'type_de': 'Nett',
        'type_esp': 'Tipo',
        'type_ru': 'Вид',
        'type_fr': 'Gentil',
        'type_it': 'Genere',
        'type_tuek': 'Tür',
        'type_zh': '種類',
        'type_ja': '種類',
        'type_vi': 'Tốt bụng',
        'type_pt': 'Gentil',
        'type_ko': '종류',
        'name_eng': 'First Aid',
        'name_de': 'Erste Hilfe',
        'name_esp': 'Primeros Auxilios',
        'name_ru': 'Первая помощь',
        'name_fr': 'Premiers Secours',
        'name_it': 'Pronto Soccorso',
        'name_tuek': 'İlk Yardım',
        'name_zh': '急救',
        'name_ja': '応急処置',
        'name_vi': 'Sơ cứu',
        'name_pt': 'Primeiro socorro',
        'name_ko': '응급 처치',
        'img': '⛑'
    },
    'pfadfinder': {
        'type_eng': 'Kind',
        'type_de': 'Nett',
        'type_esp': 'Tipo',
        'type_ru': 'Вид',
        'type_fr': 'Gentil',
        'type_it': 'Genere',
        'type_tuek': 'Tür',
        'type_zh': '種類',
        'type_ja': '種類',
        'type_vi': 'Tốt bụng',
        'type_pt': 'Gentil',
        'type_ko': '종류',
        'name_eng': 'Scouting',
        'name_de': 'Pfadfinder',
        'name_esp': 'Escultismo',
        'name_ru': 'Скаутское движение',
        'name_fr': 'Scoutisme',
        'name_it': 'Scoutismo',
        'name_tuek': 'Izcilik',
        'name_zh': '偵察',
        'name_ja': 'スカウト',
        'name_vi': 'Hướng đạo',
        'name_pt': 'Escotismo',
        'name_ko': '정찰 활동',
        'img': '⛺'
    },
    'deko': {
        'type_eng': 'Kind',
        'type_de': 'Nett',
        'type_esp': 'Tipo',
        'type_ru': 'Вид',
        'type_fr': 'Gentil',
        'type_it': 'Genere',
        'type_tuek': 'Tür',
        'type_zh': '種類',
        'type_ja': '種類',
        'type_vi': 'Tốt bụng',
        'type_pt': 'Gentil',
        'type_ko': '종류',
        'name_eng': 'Decorative',
        'name_de': 'Dekoration',
        'name_esp': 'Decorativos',
        'name_ru': 'Украшения',
        'name_fr': 'Décoratif',
        'name_it': 'Decotazioni',
        'name_tuek': 'Süsleme',
        'name_zh': '裝飾性的',
        'name_ja': '装飾',
        'name_vi': 'Trang trí',
        'name_pt': 'Decorativo',
        'name_ko': '장식',
        'img': '🎉'
    },
    'festmacher': {
        'type_eng': 'Type',
        'type_de': 'Typ',
        'type_esp': 'Tipo',
        'type_ru': 'Тип',
        'type_fr': 'Type',
        'type_it': 'Tipo',
        'type_tuek': 'Tür',
        'type_zh': '類型',
        'type_ja': 'タイプ',
        'type_vi': 'Kiểu',
        'type_pt': 'Modelo',
        'type_ko': '유형',
        'name_eng': 'Hitches',
        'name_de': 'Festmacher',
        'name_esp': 'Cotes',
        'name_ru': 'Прикрепить',
        'name_fr': 'Attelages',
        'name_it': 'Nodi di Ancoraggio',
        'name_tuek': 'Hitches',
        'name_zh': '掛鉤',
        'name_ja': 'ヒッチ',
        'name_vi': 'Chó cái',
        'name_pt': 'Hitches',
        'name_ko': '히치',
        'img': '🔗'
    },
    'schlaufe': {
        'type_eng': 'Type',
        'type_de': 'Typ',
        'type_esp': 'Tipo',
        'type_ru': 'Тип',
        'type_fr': 'Type',
        'type_it': 'Tipo',
        'type_tuek': 'Tür',
        'type_zh': '類型',
        'type_ja': 'タイプ',
        'type_vi': 'Kiểu',
        'type_pt': 'Modelo',
        'type_ko': '유형',
        'name_eng': 'Loops',
        'name_de': 'Schlaufe',
        'name_esp': 'Lazos',
        'name_ru': 'Петли',
        'name_fr': 'Boucles',
        'name_it': 'Nodi ad Occhio',
        'name_tuek': 'Ilmekler',
        'name_zh': '循環',
        'name_ja': 'ループ',
        'name_vi': 'Vòng lặp',
        'name_pt': 'rotações',
        'name_ko': '루프',
        'img': '➰'
    },
    'stop': {
        'type_eng': 'Type',
        'type_de': 'Typ',
        'type_esp': 'Tipo',
        'type_ru': 'Тип',
        'type_fr': 'Type',
        'type_it': 'Tipo',
        'type_tuek': 'Tür',
        'type_zh': '類型',
        'type_ja': 'タイプ',
        'type_vi': 'Kiểu',
        'type_pt': 'Modelo',
        'type_ko': '유형',
        'name_eng': 'Stopper`s',
        'name_de': 'Stoppknoten',
        'name_esp': 'Tapónes',
        'name_ru': 'Стопорные узлы',
        'name_fr': 'Arrêts',
        'name_it': 'Nodi d`arresto',
        'name_tuek': 'Durdurucular',
        'name_zh': '塞子',
        'name_ja': 'ストッパーの',
        'name_vi': 'Nút chặn',
        'name_pt': 'Stopper`s',
        'name_ko': '스토퍼',
        'img': '🛑'
    },
    'verbinder': {
        'type_eng': 'Type',
        'type_de': 'Typ',
        'type_esp': 'Tipo',
        'type_ru': 'Тип',
        'type_fr': 'Type',
        'type_it': 'Tipo',
        'type_tuek': 'Tür',
        'type_zh': '類型',
        'type_ja': 'タイプ',
        'type_vi': 'Kiểu',
        'type_pt': 'Modelo',
        'type_ko': '유형',
        'name_eng': 'Bends',
        'name_de': 'Verbinder',
        'name_esp': 'Empalme',
        'name_ru': 'Соеденительные узлы',
        'name_fr': 'Coudes',
        'name_it': 'Nodi di Giunzione',
        'name_tuek': 'Tutturucular',
        'name_zh': '彎曲',
        'name_ja': 'ベンド',
        'name_vi': 'Uốn cong',
        'name_pt': 'Curvas',
        'name_ko': '벤드',
        'img': '➿'
    },
    'spezi': {
        'type_eng': 'Type',
        'type_de': 'Typ',
        'type_esp': 'Tipo',
        'type_ru': 'Тип',
        'type_fr': 'Type',
        'type_it': 'Tipo',
        'type_tuek': 'Tür',
        'type_zh': '類型',
        'type_ja': 'タイプ',
        'type_vi': 'Kiểu',
        'type_pt': 'Modelo',
        'type_ko': '유형',
        'name_eng': 'Special',
        'name_de': 'Spezial',
        'name_esp': 'Special',
        'name_ru': 'Особый',
        'name_fr': 'Spéciale',
        'name_it': 'Speciale',
        'name_tuek': 'Özel',
        'name_zh': '特別的',
        'name_ja': '特殊な',
        'name_vi': 'Đặc biệt',
        'name_pt': 'Especial',
        'name_ko': '특별한',
        'img': '❌'
    },
    'buende': {
        'type_eng': 'Type',
        'type_de': 'Typ',
        'type_esp': 'Tipo',
        'type_ru': 'Тип',
        'type_fr': 'Type',
        'type_it': 'Tipo',
        'type_tuek': 'Tür',
        'type_zh': '類型',
        'type_ja': 'タイプ',
        'type_vi': 'Kiểu',
        'type_pt': 'Modelo',
        'type_ko': '유형',
        'name_eng': 'Binding',
        'name_de': 'Bünde',
        'name_esp': 'Ligadas',
        'name_ru': 'Связывание обьектов',
        'name_fr': 'Binding',
        'name_it': 'Annodare',
        'name_tuek': 'Bağlayıcı',
        'name_zh': '捆綁',
        'name_ja': '製本',
        'name_vi': 'Ràng buộc',
        'name_pt': 'Vinculativo',
        'name_ko': '제본',
        'img': '🖇'
    },
}

language = {
    'eng': {
        'view': Template('Full list:\nAll knots $all'),
        'view_category': Template('$category_name'),
        'knot': Template('Description:\n$description\n\nABOK: $abok\n\nAlso known as: \n$names\n\n'
                         'Breaking strength: $strength\n\n'
                         'Categories: \n$categories\n\n'
                         'More information on: https://knots.exyte.top/knot_id_$id'),
        'error': 'Sorry, I don`t understand',
        'search': 'What are you looking for?',
        'choose': 'Choose language',
        'all': 'All',
        'fav': 'Favorite',
        'lan': 'Language',
        'end': 'Choose knot',
        'sel': 'Selected',
        'ch': 'Select',
        'ad': 'Add to favorite',
        'del': 'Delete from favorite',
        'lang': 'English',
        'self': 'Language',
        'sub': 'Before using this bot, first of all subscribe to our channel - use the link below!👇',
        'sub_but': 'Subscribe ↗',
    },
    'de': {
        'view': Template('Volle Liste:\nAlle Knoten $all'),
        'view_category': Template('$category_name'),
        'knot': Template('Beschreibung:\n$description\n\nABOK: $abok\n\nAuch bekannt als: \n$names\n\n'
                         'Bruchfestigkeit: $strength\n\n'
                         'Kategorie: \n$categories\n\n'
                         'Weitere Informationen zu: https://knots.exyte.top/knot_id_$id'),
        'error': 'Entschuldigung, ich verstehe nicht',
        'search': 'Wonach suchen Sie?',
        'choose': 'Sprache wählen',
        'all': 'Alle',
        'fav': 'Favorit',
        'lan': 'Wählen',
        'end': 'Wählen knot',
        'sel': 'Wählen',
        'ch': 'Wählen',
        'ad': 'Add to favorit',
        'del': 'Delete from favorit',
        'lang': 'Deutsch',
        'self': 'Sprache',
        'sub': 'Bevor Sie diesen Bot verwenden, abonnieren Sie zunächst unseren Kanal - verwenden Sie den unten stehenden Link!👇',
        'sub_but': 'Аbonnieren ↗',
    },
    'ru':{
        'view': Template('Полный список:\nВсе узлы $all'),
        'view_category': Template('$category_name'),
        'knot': Template('Описание:\n$description\n\nABOK: $abok\n\nТакже извесно как: \n$names\n\n'
                         'Прочность на разрыв: $strength\n\n'
                         'Категории: \n$categories\n\n'
                         'Чтобы унать больше: https://knots.exyte.top/knot_id_$id'),
        'error': 'Извини, не понимаю',
        'search': 'Что вы хотите найти?',
        'choose': 'Выберите язык',
        'all': 'Всё',
        'fav': 'Избранное',
        'lan': 'Язык',
        'end': 'Выберите узел',
        'sel': 'Выбрано',
        'ch': 'Выберете',
        'ad': 'Добавить в избранное',
        'del': 'Удалить из избранного',
        'lang': 'Русский',
        'self': "Язык",
        'sub': 'Перед тем как начать использовать нашего бота, необходимо подписаться на наш канал - ссылка на него снизу!👇',
        'sub_but': 'Подписаться ↗',
    },
    'esp': {
        'view': Template('Lista llena:\nTodos los nudos $all'),
        'view_category': Template('$category_name'),
        'knot': Template('Descripción:\n$description\n\nABOK: $abok\n\nTambién conocido como: \n$names\n\n'
                         'Rompiendo la fuerza: $strength\n\n'
                         'Categoría: \n$categories\n\n'
                         'Más información sobre: https://knots.exyte.top/knot_id_$id'),
        'error': 'Lo siento, no entiendo',
        'search': '¿Qué estás buscando?',
        'choose': 'Elige lengua',
        'all': 'All',
        'fav': 'Favorito',
        'lan': 'Idioma',
        'end': 'Elige knot',
        'sel': 'Elige',
        'ch': 'Elige',
        'ad': 'Add to favorito',
        'del': 'Delete from favorito',
        'lang': 'Espanol',
        'self': 'Lengua',
        'sub': 'Antes de usar este bot, en primer lugar suscríbase a nuestro canal, ¡use el enlace a continuación!👇',
        'sub_but': 'Suscríbase ↗',
    },
    'fr': {
        'view': Template('Liste complète:\nTous les nœuds $all'),
        'view_category': Template('$category_name'),
        'knot': Template('Description:\n$description\n\nABOK: $abok\n\nAussi connu sous le nom: \n$names\n\n'
                         'Résistance à la rupture: $strength\n\n'
                         'Catégories: \n$categories\n\n'
                         'Plus d`informations sur: https://knots.exyte.top/knot_id_$id'),
        'error': 'Désolé, je ne comprends pas',
        'search': 'Que cherchez-vous?',
        'choose': 'Choisissez la langue',
        'all': 'Tout',
        'fav': 'Favori',
        'lan': 'Langue',
        'end': 'Choisissez knot',
        'sel': 'Choisissez',
        'ch': 'Choisissez',
        'ad': 'Add to favori',
        'del': 'Delete from favori',
        'lang': 'Francais',
        'self': 'Langue',
        'sub': 'Avant d`utiliser ce bot, abonnez-vous d`abord à notre chaîne - utilisez le lien ci-dessous!👇',
        'sub_but': 'S`abonner ↗',
    },
    'it': {
        'view': Template('Lista completa:\nTutti i nodi $all'),
        'view_category': Template('$category_name'),
        'knot': Template('Descrizione:\n$description\n\nABOK: $abok\n\nConosciuto anche come: \n$names\n\n'
                         'Forza di rottura: $strength\n\n'
                         'Categoria: \n$categories\n\n'
                         'Maggiori informazioni su: https://knots.exyte.top/knot_id_$id'),
        'error': 'Scusa, non capisco',
        'search': 'Che cosa sta cercando?',
        'choose': 'Scegli la lingua',
        'all': 'Tutti',
        'fav': 'Preferito',
        'lan': 'linguaggio',
        'end': 'Scegli knot',
        'sel': 'Scegli',
        'ch': 'Scegli',
        'ad': 'Add to preferito',
        'del': 'Delete from preferito',
        'lang': 'Italiano',
        'self': 'Lingua',
        'sub': 'Prima di utilizzare questo bot, prima di tutto iscriviti al nostro canale - usa il link qui sotto!👇',
        'sub_but': 'Sottoscrivi ↗',
    },
    'tuek': {
        'view': Template('Tam liste:\nTüm düğümler $all'),
        'view_category': Template('$category_name'),
        'knot': Template('Açıklama:\n$description\n\nABOK: $abok\n\nAyrıca şöyle bilinir: \n$names\n\n'
                         'Kırılma gücü: $strength\n\n'
                         'Kategori: \n$categories\n\n'
                         'Hakkında daha fazla bilgi: https://knots.exyte.top/knot_id_$id'),
        'error': 'Üzgünüm anlamadım',
        'search': 'Ne arıyorsun?',
        'choose': 'Dil seçiniz',
        'all': 'Herşey',
        'fav': 'Favori',
        'lan': 'Seçiniz',
        'end': 'Seçiniz knot',
        'sel': 'Seçiniz',
        'ch': 'Seçiniz',
        'ad': 'Add to favori',
        'del': 'Delete from favori',
        'lang': 'Turkce',
        'self': 'Dil',
        'sub': 'Bu botu kullanmadan önce, öncelikle kanalımıza abone olun - aşağıdaki bağlantıyı kullanın!👇',
        'sub_but': 'Аbone ol ↗',
    },
    'cur_lang': 'eng',
    'stage': 'menu',
    'search': False,
}


def set_default():
    if Language.objects.filter(usr=Command.user_id).exists():
        language.update({'cur_lang': Language.objects.get(usr=Command.user_id).lang})


def all_types():
    lst = ['view']
    for el in encode.keys():
        lst.append('view_' + el)
    lst.append('view_all')
    return lst


def all_knots():
    lst = list()
    for i in range(1, 131):
        lst.append('knot_' + str(i))
    return lst


def delete_history(_to, _id):
    it = 0
    for i in range(_to-1, -1, -1):
        try:
            bot.delete_message(_id, i)
            it = 0
        except Exception:
            if it > 1000:
                print('fin')
                return
            it += 1


def delete_thread(_to, _id):
    it = 0
    for i in range(_to-1, -1, -1):
        try:
            bot.delete_message(_id, i)
            it = 0
        except Exception:
            if it > 10:
                return
            it += 1


def create_gif(el):
    img = Image.open(
        settings.BASE_DIR / f"animations/draw_{el.knotenbild2d[5:-8]}2d_1.png").convert("RGBA")
    height = int(el.knoten_frameweite)
    weight = int(el.knoten_framehoehe)
    images = []
    for y in range(0, int(el.knoten_count_y_2d)):
        for x in range(0, int(el.knoten_count_x_2d)):
            images.append(img.crop((x*height, y*weight, x*height+height, y*weight+weight)))
    imageio.mimsave(settings.BASE_DIR / f'gifs/{el.id}_2d.gif', images)
    img = Image.open(
        settings.BASE_DIR / f"animations/draw_{el.knotenbild2d[5:-8]}360_1.png").convert("RGBA")
    height = int(el.knoten_frameweite)
    weight = int(el.knoten_framehoehe)
    images360 = []
    for y in range(0, int(el.knoten_count_y_360)):
        for x in range(0, int(el.knoten_count_x_360)):
            images360.append(img.crop((x*height, y*weight, x*height+height, y*weight+weight)))
    imageio.mimsave(settings.BASE_DIR / f'gifs/{el.id}_3d.gif', images360)


def favorite(_id):
    if Deleting.objects.filter(usr=Command.user_id).exists():
        del_obj = Deleting.objects.get(usr=Command.user_id)
    else:
        bot.send_message(_id, 'To begin type /start')
    if (bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'left' or
                    bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'kicked' or
                    bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'restricted'):
        link = telebot.types.InlineKeyboardMarkup()
        link.row(telebot.types.InlineKeyboardButton(text=f'{language[language["cur_lang"]]["sub_but"]}', callback_data='none',
                                                    url='https://t.me/Knots360'))
        _to = bot.send_message(_id, f'{language[language["cur_lang"]]["sub"]}', reply_markup=link)
        del_obj.begin_delete = del_obj.end_delete
        del_obj.end_delete = _to.message_id + 1
        del_obj.save()
        return
    buf = threading.Thread(target=delete)
    buf.start()
    language.update({'stage': 'favorite'})
    knots = alleknotentabelle.objects.filter(id__in=Favorite.objects.filter
                                             (usr=_id).values('knot'))
    buf = None
    img_buf = None
    if len(knots) % 2 == 0:
        fl = False
    else:
        fl = True
    buf2 = None
    img_buf2 = None
    bot.send_chat_action(_id, 'typing')
    bot.send_message(_id, language[language['cur_lang']]['fav'], reply_markup=keyboard1)
    _from = del_obj.end_delete
    _to = _from
    for el in knots:
        kb = telebot.types.InlineKeyboardMarkup()
        kb_button = telebot.types.InlineKeyboardButton(
            f'{str(eval("el.knotenname_" + language["cur_lang"]).split("_")[0])}',
            callback_data=str(el.id))
        img = Image.open(
            settings.BASE_DIR / f"images/draw_{el.knotenbild2d[5:-8]}2d_1.png")
        bot.send_chat_action(_id, 'typing')
        if buf is not None:
            if fl:
                try:
                    two_in_one = Image.open(settings.BASE_DIR / f"done_img/{kb_button.text}_{buf.text}.png")
                except Exception:
                    two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
                    two_in_one.paste(img, (0, 0))
                    two_in_one.paste(img_buf, (248, 0))
                    two_in_one.save(settings.BASE_DIR / f"done_img/{kb_button.text}_{buf.text}.png", 'PNG')
                kb.row(kb_button, buf)
                bot.send_photo(_id, two_in_one, reply_markup=kb)
                _to += 1
        elif fl:
            buf2 = kb_button
            img_buf2 = img
        buf = kb_button
        img_buf = img
        fl = not fl
    if buf2 is not None:
        kb1 = telebot.types.InlineKeyboardMarkup()
        try:
            two_in_one = Image.open(settings.BASE_DIR / f"done_img/{buf2.text}_green.png")
        except Exception:
            two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
            two_in_one.paste(img_buf2, (0, 0))
            two_in_one.paste(Image.open(settings.BASE_DIR / "images/green.png"), (248, 0))
            two_in_one.save(settings.BASE_DIR / f"done_img/{buf2.text}_green.png", 'PNG')
        kb1.row(buf2, telebot.types.InlineKeyboardButton('-', callback_data='-'))
        bot.send_photo(_id, two_in_one, reply_markup=kb1)
        _to += 1
    del_obj.begin_delete = _from
    del_obj.end_delete = _to + 1
    del_obj.save()


def view_all_data(data, _id):
    set_default()
    if Deleting.objects.filter(usr=Command.user_id).exists():
        del_obj = Deleting.objects.get(usr=Command.user_id)
    else:
        bot.send_message(_id, 'To begin type /start')
    if (bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'left' or
                    bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'kicked' or
                    bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'restricted'):
        link = telebot.types.InlineKeyboardMarkup()
        link.row(telebot.types.InlineKeyboardButton(text=f'{language[language["cur_lang"]]["sub_but"]}', callback_data='none',
                                                    url='https://t.me/Knots360'))
        _to = bot.send_message(_id, f'{language[language["cur_lang"]]["sub"]}', reply_markup=link)
        del_obj.begin_delete = del_obj.end_delete
        del_obj.end_delete = _to.message_id + 1
        del_obj.save()
        return
    buf = threading.Thread(target=delete)
    buf.start()
    language.update({'stage': 'all'})
    knots = alleknotentabelle.objects.all()
    buf = None
    img_buf = None
    if len(knots) % 2 == 0:
        fl = False
    else:
        fl = True
    bot.send_chat_action(_id, 'typing')
    bot.send_message(_id, '*All:*',  parse_mode="Markdown", reply_markup=keyboard1)
    _from = del_obj.end_delete
    _to = _from
    buf2 = None
    img_buf2 = None
    for el in knots:
        kb = telebot.types.InlineKeyboardMarkup()
        kb_button = telebot.types.InlineKeyboardButton(
            f'{str(eval("el.knotenname_" + language["cur_lang"]).split("_")[0])}',
            callback_data=str(el.id))
        img = Image.open(
            settings.BASE_DIR / f"images/draw_{el.knotenbild2d[5:-8]}2d_1.png")
        bot.send_chat_action(_id, 'typing')
        if buf is not None:
            if fl:
                try:
                    two_in_one = Image.open(settings.BASE_DIR / f"done_img/{kb_button.text}_{buf.text}.png")
                except Exception:
                    two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
                    two_in_one.paste(img, (0, 0))
                    two_in_one.paste(img_buf, (248, 0))
                    two_in_one.save(settings.BASE_DIR / f"done_img/{kb_button.text}_{buf.text}.png", 'PNG')
                kb.row(kb_button, buf)
                bot.send_photo(_id, two_in_one, reply_markup=kb)
                _to += 1
        elif fl:
            buf2 = kb_button
            img_buf2 = img
        buf = kb_button
        img_buf = img
        fl = not fl
    if buf2 is not None:
        kb1 = telebot.types.InlineKeyboardMarkup()
        try:
            two_in_one = Image.open(settings.BASE_DIR / f"done_img/{buf2.text}_green.png")
        except Exception:
            two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
            two_in_one.paste(img_buf2, (0, 0))
            two_in_one.paste(Image.open(settings.BASE_DIR / "images/green.png"), (248, 0))
            two_in_one.save(settings.BASE_DIR / f"done_img/{buf2.text}_green.png", 'PNG')
        kb1.row(buf2, telebot.types.InlineKeyboardButton('-', callback_data='-'))
        bot.send_photo(_id, two_in_one, reply_markup=kb1)
        _to += 1
    del_obj.begin_delete = _from
    del_obj.end_delete = _to + 2
    del_obj.save()


def knot_data(data, _id):
    set_default()
    if Deleting.objects.filter(usr=Command.user_id).exists():
        del_obj = Deleting.objects.get(usr=Command.user_id)
    else:
        bot.send_message(_id, 'To begin type /start')
    if (bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'left' or
                    bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'kicked' or
                    bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'restricted'):
        link = telebot.types.InlineKeyboardMarkup()
        link.row(telebot.types.InlineKeyboardButton(text=f'{language[language["cur_lang"]]["sub_but"]}', callback_data='none',
                                                    url='https://t.me/Knots360'))
        _to = bot.send_message(_id, f'{language[language["cur_lang"]]["sub"]}', reply_markup=link)
        del_obj.begin_delete = del_obj.end_delete
        del_obj.end_delete = _to.message_id + 1
        del_obj.save()
        return
    buf = threading.Thread(target=delete)
    buf.start()
    if language['stage'] == 'other':
        language.update({'stage': 'menu'})
    elif language['stage'][:3] != 'obj':
        language.update({'stage': 'obj' + language['stage']})
    kb1 = telebot.types.InlineKeyboardMarkup()
    obj = alleknotentabelle.objects.get(id=int(data))
    if Favorite.objects.filter(usr=_id, knot=obj).exists():
        kb_button = telebot.types.InlineKeyboardButton("⭐" + language[language['cur_lang']]['del'],
                                                       callback_data=f'?{data}')
    else:
        kb_button = telebot.types.InlineKeyboardButton("⭐" + language[language['cur_lang']]['ad'],
                                                       callback_data=f'!{data}')
    kb1.row(kb_button)
    categories = [el for el in obj.knoten_typ.split("_")]
    try:
        d2 = open(settings.BASE_DIR / f'gifs/{obj.id}_2d.gif', 'rb')
        d3 = open(settings.BASE_DIR / f'gifs/{obj.id}_3d.gif', 'rb')
    except Exception:
        create_gif(obj)
        d2 = open(settings.BASE_DIR / f'gifs/{obj.id}_2d.gif', 'rb')
        d3 = open(settings.BASE_DIR / f'gifs/{obj.id}_3d.gif', 'rb')
    _from = del_obj.end_delete
    bot.send_chat_action(_id, 'typing')
    bot.send_animation(_id, d2)
    bot.send_animation(_id, d3, reply_markup=keyboard1)
    bot.send_message(_id, str(str(eval(f'obj.knotenname_{language["cur_lang"]}').split('_')[0]) + '\n\n' +
                              language[language['cur_lang']]['knot'].substitute(
                       description=eval(f'obj.knotenbeschreibung_{language["cur_lang"]}'),
                       abok=obj.knoten_abok,
                       names="\n".join(
                           [str("--" + el) for el in
                            eval(f'obj.knotenname_{language["cur_lang"]}').split("_")]),
                       strength=obj.knotenfestigkeit,
                       categories="\n".join(
                           [str("--" + encode[el][f"name_{language['cur_lang']}"]) for el in
                            categories]),
                       id=int(data))), reply_markup=kb1)
    _to = _from + 1
    del_obj.begin_delete = _from
    del_obj.end_delete = _to + 3
    del_obj.save()


def view_category_data(data, _id):
    set_default()
    if Deleting.objects.filter(usr=Command.user_id).exists():
        del_obj = Deleting.objects.get(usr=Command.user_id)
    else:
        bot.send_message(_id, 'To begin type /start')
    if (bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'left' or
                    bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'kicked' or
                    bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'restricted'):
        link = telebot.types.InlineKeyboardMarkup()
        link.row(telebot.types.InlineKeyboardButton(text=f'{language[language["cur_lang"]]["sub_but"]}', callback_data='none',
                                                    url='https://t.me/Knots360'))
        _to = bot.send_message(_id, f'{language[language["cur_lang"]]["sub"]}', reply_markup=link)
        del_obj.begin_delete = del_obj.end_delete
        del_obj.end_delete = _to.message_id + 1
        del_obj.save()
        return
    buf = threading.Thread(target=delete)
    buf.start()
    language.update({'stage': data})
    knots = alleknotentabelle.objects.filter(knoten_typ__contains=data)
    buf = None
    img_buf = None
    if len(knots) % 2 == 0:
        fl = False
    else:
        fl = True
    buf2 = None
    img_buf2 = None
    bot.send_message(_id, '*' + language[language['cur_lang']]['sel'] + ' ' +
                     language[language['cur_lang']]['view_category'].substitute(
        category_name=encode[data][f"name_{language['cur_lang']}"]) + '*', parse_mode='Markdown', reply_markup=keyboard1)
    _from = del_obj.end_delete
    _to = _from
    for el in knots:
        kb = telebot.types.InlineKeyboardMarkup()
        kb_button = telebot.types.InlineKeyboardButton(
            f'{str(eval("el.knotenname_" + language["cur_lang"]).split("_")[0])}',
            callback_data=str(el.id))
        img = Image.open(
            settings.BASE_DIR / f"images/draw_{el.knotenbild2d[5:-8]}2d_1.png")
        bot.send_chat_action(_id, 'typing')
        if buf is not None:
            if fl:
                try:
                    two_in_one = Image.open(settings.BASE_DIR / f"done_img/{kb_button.text}_{buf.text}.png")
                except Exception:
                    two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
                    two_in_one.paste(img, (0, 0))
                    two_in_one.paste(img_buf, (248, 0))
                    two_in_one.save(settings.BASE_DIR / f"done_img/{kb_button.text}_{buf.text}.png", 'PNG')
                kb.row(kb_button, buf)
                bot.send_photo(_id, two_in_one, reply_markup=kb)
                _to += 1
        elif fl:
            buf2 = kb_button
            img_buf2 = img
        buf = kb_button
        img_buf = img
        fl = not fl
    if buf2 is not None:
        kb1 = telebot.types.InlineKeyboardMarkup()
        try:
            two_in_one = Image.open(settings.BASE_DIR / f"done_img/{buf2.text}_green.png")
        except Exception:
            two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
            two_in_one.paste(img_buf2, (0, 0))
            two_in_one.paste(Image.open(settings.BASE_DIR / "images/green.png"), (248, 0))
            two_in_one.save(settings.BASE_DIR / f"done_img/{buf2.text}_green.png", 'PNG')
        kb1.row(buf2, telebot.types.InlineKeyboardButton('-', callback_data='-'))
        bot.send_photo(_id, two_in_one, reply_markup=kb1)
        _to += 1
    del_obj.begin_delete = _from
    del_obj.end_delete = _to + 2
    del_obj.save()


def search(data, _id):
    set_default()
    if Deleting.objects.filter(usr=Command.user_id).exists():
        del_obj = Deleting.objects.get(usr=Command.user_id)
    else:
        bot.send_message(_id, 'To begin type /start')
    if (bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'left' or
                    bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'kicked' or
                    bot.get_chat_member(chat_id=-1001178378858, user_id=Command.user_id).status == 'restricted'):
        link = telebot.types.InlineKeyboardMarkup()
        link.row(telebot.types.InlineKeyboardButton(text=f'{language[language["cur_lang"]]["sub_but"]}', callback_data='none',
                                                    url='https://t.me/Knots360'))
        _to = bot.send_message(_id, f'{language[language["cur_lang"]]["sub"]}', reply_markup=link)
        del_obj.begin_delete = del_obj.end_delete
        del_obj.end_delete = _to.message_id + 1
        del_obj.save()
        return
    buf = threading.Thread(target=delete)
    buf.start()
    language.update({'stage': 'search'})
    if language['cur_lang'] == 'eng':
        knots = alleknotentabelle.objects.filter(knotenname_eng__contains=data)
    elif language['cur_lang'] == 'de':
        knots = alleknotentabelle.objects.filter(knotenname_de__contains=data)
    elif language['cur_lang'] == 'ru':
        knots = alleknotentabelle.objects.filter(knotenname_ru__contains=data)
    elif language['cur_lang'] == 'esp':
        knots = alleknotentabelle.objects.filter(knotenname_esp__contains=data)
    elif language['cur_lang'] == 'fr':
        knots = alleknotentabelle.objects.filter(knotenname_fr__contains=data)
    elif language['cur_lang'] == 'it':
        knots = alleknotentabelle.objects.filter(knotenname_it__contains=data)
    elif language['cur_lang'] == 'tuek':
        knots = alleknotentabelle.objects.filter(knotenname_tuek__contains=data)
    buf = None
    bot.send_chat_action(_id, 'typing')
    bot.send_message(_id, "🔍", reply_markup=keyboard1)
    _to = del_obj.begin_delete + 3
    img_buf = None
    if len(knots) % 2 == 0:
        fl = False
    else:
        fl = True
    buf2 = None
    img_buf2 = None
    for el in knots:
        kb = telebot.types.InlineKeyboardMarkup()
        kb_button = telebot.types.InlineKeyboardButton(
            f'{str(eval("el.knotenname_" + language["cur_lang"]).split("_")[0])}',
            callback_data=str(el.id))
        img = Image.open(
            settings.BASE_DIR / f"images/draw_{el.knotenbild2d[5:-8]}2d_1.png").convert("RGB")
        bot.send_chat_action(_id, 'typing')
        if buf is not None:
            if fl:
                try:
                    two_in_one = Image.open(settings.BASE_DIR / f"done_img/{kb_button.text}_{buf.text}.png")
                except Exception:
                    two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
                    two_in_one.paste(img, (0, 0))
                    two_in_one.paste(img_buf, (248, 0))
                    two_in_one.save(settings.BASE_DIR / f"done_img/{kb_button.text}_{buf.text}.png", 'PNG')
                kb.row(kb_button, buf)
                bot.send_photo(_id, two_in_one, reply_markup=kb)
                _to += 1
        elif fl:
            buf2 = kb_button
            img_buf2 = img
        buf = kb_button
        img_buf = img
        fl = not fl
    if buf2 is not None:
        kb1 = telebot.types.InlineKeyboardMarkup()
        try:
            two_in_one = Image.open(settings.BASE_DIR / f"done_img/{buf2.text}_green.png")
        except Exception:
            two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
            two_in_one.paste(img_buf2, (0, 0))
            two_in_one.paste(Image.open(settings.BASE_DIR / "images/green.png"), (248, 0))
            two_in_one.save(settings.BASE_DIR / f"done_img/{buf2.text}_green.png", 'PNG')
        kb1.row(buf2, telebot.types.InlineKeyboardButton('-', callback_data='-'))
        bot.send_photo(_id, two_in_one, reply_markup=kb1)
        _to += 1
    del_obj.end_delete = _to + 1
    del_obj.save()


def thread():
    if Command.flag:
        print('start')
        my_thread = threading.Thread(target=delete_history,
                                     args=(Command.my_thread_message, Command.my_thread_id,))
        my_thread.start()
        my_thread.join()
        Command.flag = False
        return


def delete():
    obj = Deleting.objects.get(usr=Command.user_id)
    del_thread = threading.Thread(target=delete_thread, args=(obj.end_delete, Command.user_id))
    del_thread.start()
    del_thread.join()
    return


class Command(BaseCommand):
    help = "Telegram-bot"
    user_id = None
    flag = False
    my_thread_id = None
    my_thread_message = None
    _message = None
    main_thread = threading.Thread(target=thread)
    side_thread = threading.Thread(target=delete)
    menu = None

    def handle(self, *args, **options):

        inline_kb1 = telebot.types.ReplyKeyboardMarkup()
        inline_kb1.row('English', 'Deutsch')
        inline_kb1.row('Русский', 'Espanol')
        inline_kb1.row('Francais', 'Italiano', 'Turkce')

        @bot.message_handler(commands=['start'])
        def start(message):
            Command._message = message
            Command.user_id = message.from_user.id
            if Language.objects.filter(usr=Command.user_id).exists():
                set_default()
                if Deleting.objects.filter(usr=Command.user_id).exists():
                    del_obj = Deleting.objects.get(usr=Command.user_id)
                else:
                    del_obj = Deleting.objects.create(usr=Command.user_id, begin_delete=0, end_delete=0)
                buf = threading.Thread(target=delete)
                buf.start()
                if message.text == '/start':
                    _from = message.message_id
                else:
                    _from = del_obj.end_delete
                knots = alleknotentabelle.objects.all()
                kb = telebot.types.InlineKeyboardMarkup()
                buf = None
                img_buf2 = None
                buf2 = None
                img_buf = None
                fl = True
                language.update({'stage': 'menu'})
                bot.send_chat_action(message.chat.id, 'typing')
                kb_rep = telebot.types.ReplyKeyboardMarkup()
                kb_rep.row(f'{language[language["cur_lang"]]["all"]}')
                type = list()
                cat = list()
                for el in encode.keys():
                    if encode[el]['type_eng'] == 'Type':
                        type.append(encode[el]['img'] + encode[el][f'name_{language["cur_lang"]}'])
                    elif encode[el]['type_eng'] == 'Kind':
                        cat.append(encode[el]['img'] + encode[el][f'name_{language["cur_lang"]}'])
                kb_rep.row(f'⭐{language[language["cur_lang"]]["fav"]}',
                           f'🌍{language[language["cur_lang"]]["lan"]}')
                kb_rep.row(encode['camping'][f"type_{language['cur_lang']}"])
                kb_rep.row(cat[0], cat[1])
                kb_rep.row(cat[2], cat[3])
                kb_rep.row(cat[4], cat[5])
                kb_rep.row(cat[6], cat[7], cat[8])
                kb_rep.row(encode['festmacher'][f"type_{language['cur_lang']}"])
                kb_rep.row(type[0], type[1])
                kb_rep.row(type[2], type[3])
                kb_rep.row(type[4], type[5])
                Command.menu = kb_rep
                '''if (bot.get_chat_member(chat_id='-1001178378858', user_id=Command.user_id).status == 'left' or
                    bot.get_chat_member(chat_id='-1001178378858', user_id=Command.user_id).status == 'kicked' or
                    bot.get_chat_member(chat_id='-1001178378858', user_id=Command.user_id).status == 'restricted'):
                    link = telebot.types.InlineKeyboardMarkup()
                    link.row(telebot.types.InlineKeyboardButton(text=f'{language[language["cur_lang"]]["sub_but"]}',
                                                                callback_data='none',
                                                                url='https://t.me/Knots360'))
                    _to = bot.send_message(message.chat.id, f'{language[language["cur_lang"]]["sub"]}', reply_markup=link)
                    del_obj.begin_delete = _from
                    del_obj.end_delete = _to.message_id + 1
                    del_obj.save()
                    return'''
                for el in encode.keys():

                    if el == 'camping':
                        bot.send_chat_action(message.chat.id, 'typing')
                        _to = bot.send_message(message.chat.id, '<em><b>' + language[language['cur_lang']]['ch'] + ' ' +
                                               encode[el][f"type_{language['cur_lang']}"] + '</b></em>',
                                               reply_markup=telebot.types.ReplyKeyboardRemove(keyboard1),
                                               parse_mode="HTML")
                    if el == 'festmacher':
                        kb1 = telebot.types.InlineKeyboardMarkup()
                        try:
                            two_in_one = Image.open(settings.BASE_DIR / f"done_img/{buf2}_green.png")
                        except Exception:
                            two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
                            two_in_one.paste(img_buf2, (0, 0))
                            two_in_one.paste(Image.open(settings.BASE_DIR / "images/green.png"), (248, 0))
                            two_in_one.save(settings.BASE_DIR / f"done_img/{buf2.text}_green.png", 'PNG')
                        kb1.row(buf2, telebot.types.InlineKeyboardButton('-', callback_data='-'))
                        _to = bot.send_photo(message.chat.id, two_in_one, reply_markup=kb1)
                        bot.send_chat_action(message.chat.id, 'typing')
                        _to = bot.send_message(message.chat.id, '<em><b>' + language[language['cur_lang']]['ch'] + ' ' +
                                               encode[el][f"type_{language['cur_lang']}"] + '</b></em>',
                                               reply_markup=kb_rep,
                                               parse_mode="HTML")

                    kb1 = telebot.types.InlineKeyboardMarkup()
                    kb_button = telebot.types.InlineKeyboardButton(
                        encode[el]['img'] + encode[el][f'name_{language["cur_lang"]}'], callback_data=el)
                    obj = alleknotentabelle.objects.filter(knoten_typ__contains=el)[0]
                    img = Image.open(settings.BASE_DIR / f"images/draw_{obj.knotenbild2d[5:-8]}2d_1.png")
                    bot.send_chat_action(message.chat.id, 'typing')
                    if buf is not None:
                        if fl:
                            try:
                                two_in_one = Image.open(settings.BASE_DIR / f"done_img/{kb_button.text}_{buf.text}.png")
                            except Exception:
                                two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
                                two_in_one.paste(img, (0, 0))
                                two_in_one.paste(img_buf, (248, 0))
                                two_in_one.save(settings.BASE_DIR / f"done_img/{kb_button.text}_{buf.text}.png", 'PNG')
                            kb1.row(kb_button, buf)
                            _to = bot.send_photo(message.chat.id, two_in_one, reply_markup=kb1)
                    elif fl:
                        buf2 = kb_button
                        img_buf2 = img
                    img_buf = img
                    buf = kb_button
                    fl = not fl
                del_obj.begin_delete = _from
                del_obj.end_delete = _to.message_id + 1
                del_obj.save()
            else:
                if Deleting.objects.filter(usr=Command.user_id).exists():
                    del_obj = Deleting.objects.get(usr=Command.user_id)
                    del_obj.save()
                    lang(message)
                else:
                    del_obj = Deleting.objects.create(usr=Command.user_id, begin_delete=0, end_delete=0)
                    Command.flag = True
                    Command.my_thread_id = message.chat.id
                    Command.my_thread_message = message.message_id
                    main_thread = threading.Thread(target=thread)
                    main_thread.start()
                    del_obj.save()
                    lang(message)

        @bot.message_handler(commands=['delete_history'])
        def delete_all(message):
            delete_history(message.message_id, message.chat.id)

        def helper(data):
            obj = alleknotentabelle.objects.get(id=int(data))
            type = str()
            categories = str()
            for el in obj.knoten_typ.split("_"):
                if encode[el]['type_eng'] == 'Kind':
                    categories += '#' + encode[el][f'name_{language["cur_lang"]}'] + '\n'
                elif encode[el]['type_eng'] == 'Type':
                    type += '#' + encode[el][f'name_{language["cur_lang"]}'] + '\n'
            try:
                d2 = open(settings.BASE_DIR / f'gifs/{obj.id}_2d.gif', 'rb')
                d3 = open(settings.BASE_DIR / f'gifs/{obj.id}_3d.gif', 'rb')
            except Exception:
                create_gif(obj)
                d2 = open(settings.BASE_DIR / f'gifs/{obj.id}_2d.gif', 'rb')
                d3 = open(settings.BASE_DIR / f'gifs/{obj.id}_3d.gif', 'rb')
            img = Image.open(settings.BASE_DIR / f"images/draw_{obj.knotenbild2d[5:-8]}2d_1.png")
            bot.send_animation(chat_id='-1001178378858', animation=d2)
            bot.send_animation(chat_id='-1001178378858', animation=d3)
            bot.send_photo(chat_id='-1001178378858', photo=img)
            bot.send_message(chat_id='-1001178378858', text='<b>' + str(
                               str(eval(f'obj.knotenname_{language["cur_lang"]}')).split('_')[0]) + '</b>'
                                   + '\n\n' + language[language['cur_lang']]['knot'].substitute(
                               description=eval(f'obj.knotenbeschreibung_{language["cur_lang"]}'),
                               abok=obj.knoten_abok,
                               names="\n".join(
                                   [str("--" + el) for el in
                                    eval(f'obj.knotenname_{language["cur_lang"]}').split("_")]),
                               strength=obj.knotenfestigkeit,
                               categories=str(categories).replace(' ', '_') + '\n' +
                                          encode["spezi"][f'type_{language["cur_lang"]}'] + ':\n' +
                                          str(type).replace(' ', '_') + f'\n{language[language["cur_lang"]]["self"]}\n#'
                                          + language[language['cur_lang']]['lang'],
                               id=int(data)), parse_mode='HTML')

        '''@bot.message_handler(commands=['upload'])
        def upload(message):
            counter = 0
            language.update(({'cur_lang': 'eng'}))
            for data in range(1, 125):
                counter += 1
                helper(data)
                if counter == 3:
                    time.sleep(300)
                    counter = 0
            time.sleep(300)
            for data in range(127, 131):
                counter += 1
                helper(data)
                if counter == 3:
                    time.sleep(300)
                    counter = 0'''

        @bot.message_handler(commands=['language'])
        def lang(message):
            if Deleting.objects.filter(usr=Command.user_id).exists():
                del_obj = Deleting.objects.get(usr=Command.user_id)
            else:
                bot.send_message(message.chat.id, 'To begin type /start')
            bot.send_message(message.chat.id, language[language['cur_lang']]['choose'], reply_markup=inline_kb1)
            language.update({'stage': 'language'})
            buf = threading.Thread(target=delete)
            Command._message = message
            buf.start()
            del_obj.begin_delete = message.message_id
            del_obj.save()

        @bot.callback_query_handler(func=lambda c: c.data)
        def process_callback(callback_query: telebot.types.CallbackQuery):
            if Command.user_id is None:
                Command.user_id = callback_query.from_user.id
            if callback_query.data in language:
                del_obj = Deleting.objects.get(usr=Command.user_id)
                if Language.objects.filter(usr=Command.user_id).exists():
                    l_obj = Language.objects.get(usr=Command.user_id)
                    l_obj.lang = callback_query.data
                    language.update({"cur_lang": callback_query.data})
                    l_obj.save()
                    del_obj.end_delete = del_obj.begin_delete + 1
                    del_obj.save()
                    start(Command._message)
                else:
                    l_obj = Language.objects.create(usr=Command.user_id, lang= callback_query.data)
                    language.update({"cur_lang": callback_query.data})
                    l_obj.save()
                    del_obj.end_delete = del_obj.begin_delete + 2
                    del_obj.save()
                    start(Command._message)
            elif callback_query.data == 'language':
                if Deleting.objects.filter(usr=Command.user_id).exists():
                    del_obj = Deleting.objects.get(usr=Command.user_id)
                else:
                    Command._message = bot.send_message(callback_query.from_user.id, 'To begin type /start')
                language.update({'stage': 'language'})
                buf = threading.Thread(target=delete)
                buf.start()
                del_obj.begin_delete = del_obj.end_delete
                del_obj.save()
                bot.send_message(callback_query.from_user.id, language[language['cur_lang']]['choose'],
                                 reply_markup=inline_kb1)
            elif callback_query.data == 'favorite':
                favorite(callback_query.from_user.id)
            elif callback_query.data == 'all':
                view_all_data(callback_query.data, callback_query.from_user.id)
            elif callback_query.data[0] == '!':
                if Deleting.objects.filter(usr=Command.user_id).exists():
                    del_obj = Deleting.objects.get(usr=Command.user_id)
                else:
                    bot.send_message(callback_query.from_user.id, 'To begin type /start')
                k = alleknotentabelle.objects.get(id=int(callback_query.data[1:]))
                obj = Favorite.objects.create(usr=callback_query.from_user.id, knot=k)
                obj.save()
                del_obj.end_delete += 1
                del_obj.save()
                knot_data(int(callback_query.data[1:]), callback_query.from_user.id)
            elif callback_query.data[0] == '?':
                if Deleting.objects.filter(usr=Command.user_id).exists():
                    del_obj = Deleting.objects.get(usr=Command.user_id)
                else:
                    bot.send_message(callback_query.from_user.id, 'To begin type /start')
                k = alleknotentabelle.objects.get(id=int(callback_query.data[1:]))
                Favorite.objects.filter(usr=callback_query.from_user.id, knot=k).delete()
                del_obj.end_delete += 1
                del_obj.save()
                knot_data(int(callback_query.data[1:]), callback_query.from_user.id)
            elif callback_query.data == '-':
                return
            elif callback_query.data == 'none':
                if Deleting.objects.filter(usr=Command.user_id).exists():
                    del_obj = Deleting.objects.get(usr=Command.user_id)
                else:
                    bot.send_message(callback_query.from_user.id, 'To begin type /start')
                buf = threading.Thread(target=delete)
                buf.start()
                _to = bot.send_message(callback_query.from_user.id, f'{language[language["cur_lang"]]["sub"]}',
                                       reply_markup=Command.menu)
                del_obj.begin_delete = del_obj.end_delete
                del_obj.end_delete = _to.message_id + 1
                del_obj.save()
            else:
                if callback_query.data.isdigit():
                    knot_data(callback_query.data, callback_query.from_user.id)
                else:
                    view_category_data(callback_query.data, callback_query.from_user.id)

        @bot.message_handler(commands=all_types())
        def view(message):
            parsing = message.text.split('_')
            if len(parsing) == 1:
                start(message)
            elif parsing[1] == 'all':
                view_all_data(parsing[1], message.chat.id)
            elif len(parsing) == 2:
                view_category_data(parsing[1], message.chat.id)
            else:
                bot.send_message(message.chat.id, language[language['curr_lang']]['error'])

        @bot.message_handler(commands=all_knots())
        def knot(message):
            parsing = message.text.split('_')
            enter = '\n'
            if len(parsing) == 2:
                knot_data(parsing[1], message.chat.id)
            else:
                bot.send_message(message.chat.id, language[language['curr_lang']]['error'])

        def new_lang(data):
            del_obj = Deleting.objects.get(usr=Command.user_id)
            if Language.objects.filter(usr=Command.user_id).exists():
                l_obj = Language.objects.get(usr=Command.user_id)
                l_obj.lang = data
                language.update({"cur_lang": data})
                l_obj.save()
                del_obj.end_delete = del_obj.begin_delete + 1
                del_obj.save()
                start(Command._message)
            else:
                l_obj = Language.objects.create(usr=Command.user_id, lang=data)
                language.update({"cur_lang": data})
                l_obj.save()
                del_obj.end_delete = del_obj.begin_delete + 2
                del_obj.save()
                start(Command._message)

        @bot.message_handler(content_types=['text'])
        def text_parser(message):
            if Command.user_id is None:
                Command.user_id = message.from_user.id
            if message.text == language[language['cur_lang']]['all']:
                view_all_data(message.text, message.chat.id)
            if message.text == '⬅':
                if Deleting.objects.filter(usr=Command.user_id).exists():
                    del_obj = Deleting.objects.get(usr=Command.user_id)
                else:
                    bot.send_message(message.chat.id, 'To begin type /start')
                del_obj.end_delete = message.message_id + 1
                del_obj.save()
                if language['stage'] == 'menu':
                    start(message)
                elif language['stage'][:3] == 'obj':
                    if language['stage'][3:] == 'favorite':
                        favorite(language['stage'][3:], message.chat.id)
                    elif language['stage'][3:] == 'all':
                        view_all_data(language['stage'][3:], message.chat.id)
                    elif language['stage'][:9] == 'objsearch':
                        start(message)
                    else:
                        view_category_data(language['stage'][3:], message.chat.id)
                else:
                    language.update({'stage': 'menu'})
                    start(message)
            elif message.text[0] == '🔍':
                if Deleting.objects.filter(usr=Command.user_id).exists():
                    del_obj = Deleting.objects.get(usr=Command.user_id)
                else:
                    bot.send_message(message.chat.id, 'To begin type /start')
                buf = threading.Thread(target=delete)
                buf.start()
                language.update({'search': True})
                bot.send_message(message.chat.id, language[language['cur_lang']]['search'], reply_markup=keyboard1)
                del_obj.begin_delete = message.message_id
                del_obj.save()
            elif language['search']:
                search(message.text, message.chat.id)
                language.update({'search': False})
            elif message.text[0] == '⭐':
                favorite(message.chat.id)
            elif message.text == language['eng']['lang']:
                new_lang('eng')
            elif message.text == language['de']['lang']:
                new_lang('de')
            elif message.text == language['esp']['lang']:
                new_lang('esp')
            elif message.text == language['ru']['lang']:
                new_lang('ru')
            elif message.text == language['fr']['lang']:
                new_lang('fr')
            elif message.text == language['it']['lang']:
                new_lang('it')
            elif message.text == language['tuek']['lang']:
                new_lang('tuek')
            elif message.text[0] == '🌍':
                if Deleting.objects.filter(usr=Command.user_id).exists():
                    del_obj = Deleting.objects.get(usr=Command.user_id)
                else:
                    Command._message = bot.send_message(message.chat.id, 'To begin type /start')
                language.update({'stage': 'language'})
                buf = threading.Thread(target=delete)
                buf.start()
                del_obj.begin_delete = del_obj.end_delete
                del_obj.save()
                bot.send_message(message.chat.id, language[language['cur_lang']]['choose'],
                                 reply_markup=inline_kb1)
            elif message.text == encode['camping'][f'type_{language["cur_lang"]}']:
                language.update({'stage': 'menu'})
                set_default()
                if Deleting.objects.filter(usr=Command.user_id).exists():
                    del_obj = Deleting.objects.get(usr=Command.user_id)
                else:
                    del_obj = Deleting.objects.create(usr=Command.user_id, begin_delete=0, end_delete=0)
                buf = threading.Thread(target=delete)
                buf.start()
                buf = None
                buf2 = None
                img_buf2 = None
                img_buf = None
                fl = True
                _to = bot.send_message(message.chat.id, '<em><b>' + language[language['cur_lang']]['ch'] + ' ' +
                                       encode['camping'][f"type_{language['cur_lang']}"] + '</b></em>',
                                       reply_markup=keyboard1,
                                       parse_mode="HTML")
                for el in encode.keys():
                    if encode[el]['type_eng'] == 'Type':
                        kb1 = telebot.types.InlineKeyboardMarkup()
                        two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
                        two_in_one.paste(img_buf2, (0, 0))
                        two_in_one.paste(Image.open(settings.BASE_DIR / "images/green.png"), (248, 0))
                        kb1.row(buf2, telebot.types.InlineKeyboardButton('-', callback_data='-'))
                        _to = bot.send_photo(message.chat.id, two_in_one, reply_markup=kb1)
                        del_obj.begin_delete = message.message_id
                        del_obj.end_delete = _to.message_id + 1
                        del_obj.save()
                        return
                    kb1 = telebot.types.InlineKeyboardMarkup()
                    kb_button = telebot.types.InlineKeyboardButton(
                        encode[el]['img'] + encode[el][f'name_{language["cur_lang"]}'], callback_data=el)
                    obj = alleknotentabelle.objects.filter(knoten_typ__contains=el)[0]
                    img = Image.open(settings.BASE_DIR / f"images/draw_{obj.knotenbild2d[5:-8]}2d_1.png")
                    bot.send_chat_action(message.chat.id, 'typing')
                    if buf is not None:
                        if fl:
                            two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
                            two_in_one.paste(img, (0, 0))
                            two_in_one.paste(img_buf, (248, 0))
                            kb1.row(kb_button, buf)
                            _to = bot.send_photo(message.chat.id, two_in_one, reply_markup=kb1)
                    elif fl:
                        buf2 = kb_button
                        img_buf2 = img
                    img_buf = img
                    buf = kb_button
                    fl = not fl
            elif message.text == encode['festmacher'][f"type_{language['cur_lang']}"]:
                language.update({'stage': 'menu'})
                set_default()
                if Deleting.objects.filter(usr=Command.user_id).exists():
                    del_obj = Deleting.objects.get(usr=Command.user_id)
                else:
                    del_obj = Deleting.objects.create(usr=Command.user_id, begin_delete=0, end_delete=0)
                buf = threading.Thread(target=delete)
                buf.start()
                buf = None
                img_buf = None
                fl = False
                _to = bot.send_message(message.chat.id, '<em><b>' + language[language['cur_lang']]['ch'] + ' ' +
                                       encode['festmacher'][f"type_{language['cur_lang']}"] + '</b></em>',
                                       reply_markup=keyboard1,
                                       parse_mode="HTML")
                for el in encode.keys():
                    if encode[el]['type_eng'] == 'Kind':
                        continue
                    kb1 = telebot.types.InlineKeyboardMarkup()
                    kb_button = telebot.types.InlineKeyboardButton(
                        encode[el]['img'] + encode[el][f'name_{language["cur_lang"]}'], callback_data=el)
                    obj = alleknotentabelle.objects.filter(knoten_typ__contains=el)[0]
                    img = Image.open(settings.BASE_DIR / f"images/draw_{obj.knotenbild2d[5:-8]}2d_1.png")
                    bot.send_chat_action(message.chat.id, 'typing')
                    if buf is not None:
                        if fl:
                            two_in_one = Image.new("RGBA", (244 * 2 + 4, 244))
                            two_in_one.paste(img, (0, 0))
                            two_in_one.paste(img_buf, (248, 0))
                            kb1.row(kb_button, buf)
                            _to = bot.send_photo(message.chat.id, two_in_one, reply_markup=kb1)
                    img_buf = img
                    buf = kb_button
                    fl = not fl
                del_obj.begin_delete = message.message_id
                del_obj.end_delete = _to.message_id + 1
                del_obj.save()
            else:
                cat = message.text[1:]
                for el in encode.keys():
                    if encode[el][f'name_{language["cur_lang"]}'] == cat:
                        if Deleting.objects.filter(usr=Command.user_id).exists():
                            del_obj = Deleting.objects.get(usr=Command.user_id)
                        else:
                            bot.send_message(message.chat.id, 'To begin type /start')
                        del_obj.end_delete = message.message_id + 1
                        del_obj.save()
                        view_category_data(el, message.chat.id)
                        return

        while True:
            try:
                bot.polling(none_stop=True)
            except Exception as err:
                print(err)
                time.sleep(5)

