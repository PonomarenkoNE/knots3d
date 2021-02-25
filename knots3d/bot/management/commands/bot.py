from django.core.management.base import BaseCommand
import requests
from django.conf import settings
import telebot
from PIL import Image, ImageEnhance, ImageOps
from string import Template

import knots3d.settings
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

language = {
    'eng': {
        'view': Template('Full list:\nAll knots $all\n\nCategory:\n$category'),
        'view_category': Template('$category_name\n\n$knots'),
        'knot': Template('$knot_name\n\nDescription:\n$description\n\nABOK: $abok\n\nAlso known as: \n$names\n\n'
                         'Breaking strength: $strength\n\n'
                         'Categories: \n$categories\n\n'
                         'More information on: https://knots.exyte.top/knot_id_$id')
    },
    'de': {
        'view': Template('Volle Liste:\nAlle Knoten $all\n\nKategorie:\n$category'),
        'view_category': Template('$category_name\n\n$knots'),
        'knot': Template('$knot_name\n\nBeschreibung:\n$description\n\nABOK: $abok\n\nAuch bekannt als: \n$names\n\n'
                         'Bruchfestigkeit: $strength\n\n'
                         'Kategorie: \n$categories\n\n'
                         'Weitere Informationen zu: https://knots.exyte.top/knot_id_$id')
    },
    'ru':{
        'view': Template('Полный список:\nВсе узлы $all\n\nКатегории:\n$category'),
        'view_category': Template('$category_name\n\n$knots'),
        'knot': Template('$knot_name\n\nОписание:\n$description\n\nABOK: $abok\n\nТакже извесно как: \n$names\n\n'
                         'Прочность на разрыв: $strength\n\n'
                         'Категории: \n$categories\n\n'
                         'Чтобы унать больше: https://knots.exyte.top/knot_id_$id')
    },
    'esp': {
        'view': Template('Lista llena:\nTodos los nudos $all\n\nCategoría:\n$category'),
        'view_category': Template('$category_name\n\n$knots'),
        'knot': Template('$knot_name\n\nDescripción:\n$description\n\nABOK: $abok\n\nTambién conocido como: \n$names\n\n'
                         'Rompiendo la fuerza: $strength\n\n'
                         'Categoría: \n$categories\n\n'
                         'Más información sobre: https://knots.exyte.top/knot_id_$id')
    },
    'fr': {
        'view': Template('Liste complète:\nTous les nœuds $all\n\nCatégorie:\n$category'),
        'view_category': Template('$category_name\n\n$knots'),
        'knot': Template('$knot_name\n\nDescription:\n$description\n\nABOK: $abok\n\nAussi connu sous le nom: \n$names\n\n'
                         'Résistance à la rupture: $strength\n\n'
                         'Catégories: \n$categories\n\n'
                         'Plus d`informations sur: https://knots.exyte.top/knot_id_$id')
    },
    'it': {
        'view': Template('Lista completa:\nTutti i nodi $all\n\nCategoria:\n$category'),
        'view_category': Template('$category_name\n\n$knots'),
        'knot': Template('$knot_name\n\nDescrizione:\n$description\n\nABOK: $abok\n\nConosciuto anche come: \n$names\n\n'
                         'Forza di rottura: $strength\n\n'
                         'Categoria: \n$categories\n\n'
                         'Maggiori informazioni su: https://knots.exyte.top/knot_id_$id')
    },
    'tuek': {
        'view': Template('Tam liste:\nTüm düğümler $all\n\nKategori:\n$category'),
        'view_category': Template('$category_name\n\n$knots'),
        'knot': Template('$knot_name\n\nAçıklama:\n$description\n\nABOK: $abok\n\nAyrıca şöyle bilinir: \n$names\n\n'
                         'Kırılma gücü: $strength\n\n'
                         'Kategori: \n$categories\n\n'
                         'Hakkında daha fazla bilgi: https://knots.exyte.top/knot_id_$id')
    },
    'cur_lang': 'eng'
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
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard1.row('/view', '/language')

        inline_btn_1 = telebot.types.InlineKeyboardButton('English', callback_data='eng')
        inline_btn_2 = telebot.types.InlineKeyboardButton('Deutish', callback_data='de')
        inline_btn_3 = telebot.types.InlineKeyboardButton('Русский', callback_data='ru')
        inline_btn_4 = telebot.types.InlineKeyboardButton('Espaniola', callback_data='esp')
        inline_btn_5 = telebot.types.InlineKeyboardButton('Francish', callback_data='fr')
        inline_btn_6 = telebot.types.InlineKeyboardButton('Italiano', callback_data='it')
        inline_btn_7 = telebot.types.InlineKeyboardButton('Turkish', callback_data='turk')
        inline_kb1 = telebot.types.InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4,
                                                              inline_btn_5, inline_btn_6, inline_btn_7)

        @bot.message_handler(commands=['start'])
        def start(message):
            bot.send_message(message.chat.id, 'Hello, this is Knots3D Bot!\n'
                                              '\n'
                                              'Type /view to see all categories of knots\n'
                                              'Type /view_[category code] to see knots in this category\n'
                                              'Type /knot_[knot_id] to see info about knot\n'
                                              'Type /language to set language', reply_markup=keyboard1)

        @bot.message_handler(commands=['language'])
        def lang(message):
            bot.send_message(message.chat.id, "Choose language:", reply_markup=inline_kb1)

        @bot.callback_query_handler(func=lambda c: c.data)
        def process_callback(callback_query: telebot.types.CallbackQuery):
            language.update({"cur_lang": callback_query.data})
            bot.send_message(callback_query.from_user.id, "Language changed", reply_markup=keyboard1)
            return

        @bot.message_handler(commands=all_types())
        def view(message):
            parsing = message.text.split('_')
            enter = '\n'
            if len(parsing) == 1:
                knots = alleknotentabelle.objects.all()
                bot.send_message(message.chat.id, language[language['cur_lang']]['view'].substitute(
                    all={len(knots)},
                    category="\n".join([str(encode[el][f"name_{language['cur_lang']}"] + f" (/view_{el})")
                                       for el in encode.keys()]))
                                , reply_markup=keyboard1)
            elif parsing[1] == 'all':
                knots = alleknotentabelle.objects.all()
                knots_dict = dict()
                for el in knots:
                    knots_dict.update({str(el.id): str(' or '.join(i for i in
                                                                   eval(f'el.knotenname_'
                                                                        f'{language["cur_lang"]}').split('_')))})
                bot.send_message(message.chat.id, f'All:\n\n')
                for el in knots_dict.keys():
                    bot.send_message(message.chat.id, f'{str(knots_dict[el] + f"(type /knot_{el} - see info about knot)")}')
            elif len(parsing) == 2:
                knots = alleknotentabelle.objects.filter(knoten_typ__startswith=parsing[1])
                knots_dict = dict()
                for el in knots:
                    knots_dict.update({str(el.id): str(' or '.join(i for i in
                                                                   eval(f'el.knotenname_'
                                                                        f'{language["cur_lang"]}').split('_')))})
                bot.send_message(message.chat.id, language[language['cur_lang']]['view_category'].substitute(
                    category_name=encode[parsing[1]][f"name_{language['cur_lang']}"],
                    knots="\n".join(str(knots_dict[el] + f"(/knot_{el})")
                                      for el in knots_dict.keys())
                ), reply_markup=keyboard1)
            else:
                bot.send_message(message.chat.id, "No such category or type")

        @bot.message_handler(commands=all_knots())
        def knot(message):
            parsing = message.text.split('_')
            enter = '\n'
            if len(parsing) == 2:
                obj = alleknotentabelle.objects.get(id=int(parsing[1]))
                categories = [el for el in obj.knoten_typ.split("_")]
                img = Image.open(settings.BASE_DIR / f"images/{obj.knotenbild2d[5:-8]}title.png").convert("RGB")
                img = ImageOps.invert(img)
                enhancer = ImageEnhance.Sharpness(img)
                enhancer = ImageEnhance.Contrast(enhancer.enhance(1.5))
                enhancer = ImageEnhance.Brightness(enhancer.enhance(1.5))
                img = enhancer.enhance(0.9)
                img = img.convert("RGBA")
                bot.send_photo(message.chat.id, img, caption=language[language['cur_lang']]['knot'].substitute(
                    knot_name=eval(f'obj.knotenname_{language["cur_lang"]}'),
                    description=eval(f'obj.knotenbeschreibung_{language["cur_lang"]}'),
                    abok=obj.knoten_abok,
                    names="\n".join([str("--"+el) for el in eval(f'obj.knotenname_{language["cur_lang"]}').split("_")]),
                    strength=obj.knotenfestigkeit,
                    categories="\n".join([str("--"+encode[el][f"name_{language['cur_lang']}"]) for el in categories]),
                    id=int(parsing[1])))

        bot.polling()
