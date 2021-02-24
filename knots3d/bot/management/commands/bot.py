from django.core.management.base import BaseCommand
import requests
from django.conf import settings
import telebot

from bot.models import alleknotentabelle

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
        'name_ko': '캠핑'
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
        'name_ko': '항해'
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
        'name_ko': '여러 가지 잡다한'
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
        'name_ko': '등반'
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
        'name_ko': '화재 + 구조'
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
        'name_ko': '어업'
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
        'name_ko': '응급 처치'
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
        'name_ko': '정찰 활동'
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
        'name_ko': '장식'
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
        'name_ko': '히치'
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
        'name_ko': '루프'
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
        'name_ko': '스토퍼'
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
        'name_ko': '벤드'
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
        'name_ko': '특별한'
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
        'name_ko': '제본'
    },
}


def all_types():
    lst = ['view']
    for el in encode.keys():
        lst.append('view_' + el)
    lst.append('view_all')
    return lst


def all_knots():
    lst = list()
    for i in range(1, 130):
        lst.append('knot_' + str(i))
    return lst


class Command(BaseCommand):
    help = "Telegram-bot"

    def handle(self, *args, **options):
        bot = telebot.TeleBot('1592562907:AAGdFFwaQ2f6QotTEuWeYFs3PohgsEHvuiE')
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
        keyboard1.row('/view')

        @bot.message_handler(commands=['start'])
        def start(message):
            bot.send_message(message.chat.id, 'Hello, this is Knots3D Bot!\n'
                                              '\n'
                                              'Type /view to see all categories of knots\n'
                                              'Type /view_[category code] to see knots in this category\n'
                                              'Type /knot_[knot_id] to see info about knot', reply_markup=keyboard1)

        @bot.message_handler(commands=all_types())
        def view(message):
            parsing = message.text.split('_')
            enter = '\n'
            if len(parsing) == 1:
                knots = alleknotentabelle.objects.all()
                bot.send_message(message.chat.id, f'Full list:\n'
                                                  f'All knots ({len(knots)}) '
                                                  f'\n'
                                                  f'\n'
                                                  f'Category:\n'
                                                  f'{f"{enter}".join([str(encode[el]["name_eng"] + f" (type /view_{el} - see all knotes in this category)") for el in encode.keys()])}', reply_markup=keyboard1)
            elif parsing[1] == 'all':
                knots = alleknotentabelle.objects.all()
                knots_dict = dict()
                for el in knots:
                    knots_dict.update({str(el.id): str(' or '.join(i for i in el.knotenname_eng.split('_')))})
                bot.send_message(message.chat.id, f'All:\n\n')
                for el in knots_dict.keys():
                    bot.send_message(message.chat.id, f'{str(knots_dict[el] + f"(type /knot_{el} - see info about knot)")}')
            elif len(parsing) == 2:
                knots = alleknotentabelle.objects.filter(knoten_typ__startswith=parsing[1])
                knots_dict = dict()
                for el in knots:
                    knots_dict.update({str(el.id): str(' or '.join(i for i in el.knotenname_eng.split('_')))})
                bot.send_message(message.chat.id, f'{encode[parsing[1]]["name_eng"]}\n\n'
                                                  f'{f"{enter}".join(str(knots_dict[el] + f"(type /knot_{el} - see info about knot)") for el in knots_dict.keys())}', reply_markup=keyboard1)
            else:
                bot.send_message(message.chat.id, "No such category or type")

        @bot.message_handler(commands=all_knots())
        def knot(message):
            parsing = message.text.split('_')
            enter = '\n'
            if len(parsing) == 2:
                obj = alleknotentabelle.objects.get(id=int(parsing[1]))
                categories = [el for el in obj.knoten_typ.split("_")]
                bot.send_message(message.chat.id, f'{obj.knotenname_eng}\n\n'
                                                  f'Description:\n{obj.knotenbeschreibung_eng}\n\n'
                                                  f'ABOK: {obj.knoten_abok}\n\n'
                                                  f'Also known as: \n{f"{enter}".join([str("--"+el) for el in obj.knotenname_eng.split("_")])}\n\n'
                                                  f'Breaking strength: {obj.knotenfestigkeit}\n\n'
                                                  f'Categories: \n{f"{enter}".join([str("--"+encode[el]["name_eng"]) for el in categories])}\n\n'
                                                  f'More information on: https://knots.exyte.top/knot_id_{int(parsing[1])}', reply_markup=keyboard1)

        bot.polling()
