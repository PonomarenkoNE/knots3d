from django.core.management.base import BaseCommand
import requests
from django.conf import settings
import telebot
from PIL import Image, ImageEnhance, ImageOps
from string import Template

import knots3d.settings
from bot.models import alleknotentabelle, Favorite


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
        'view': Template('Full list:\nAll knots $all\n\nCategories:'),
        'view_category': Template('$category_name'),
        'knot': Template('$knot_name\n\nDescription:\n$description\n\nABOK: $abok\n\nAlso known as: \n$names\n\n'
                         'Breaking strength: $strength\n\n'
                         'Categories: \n$categories\n\n'
                         'More information on: https://knots.exyte.top/knot_id_$id')
    },
    'de': {
        'view': Template('Volle Liste:\nAlle Knoten $all\n\nKategorie:'),
        'view_category': Template('$category_name'),
        'knot': Template('$knot_name\n\nBeschreibung:\n$description\n\nABOK: $abok\n\nAuch bekannt als: \n$names\n\n'
                         'Bruchfestigkeit: $strength\n\n'
                         'Kategorie: \n$categories\n\n'
                         'Weitere Informationen zu: https://knots.exyte.top/knot_id_$id')
    },
    'ru':{
        'view': Template('Полный список:\nВсе узлы $all\n\nКатегории:'),
        'view_category': Template('$category_name'),
        'knot': Template('$knot_name\n\nОписание:\n$description\n\nABOK: $abok\n\nТакже извесно как: \n$names\n\n'
                         'Прочность на разрыв: $strength\n\n'
                         'Категории: \n$categories\n\n'
                         'Чтобы унать больше: https://knots.exyte.top/knot_id_$id')
    },
    'esp': {
        'view': Template('Lista llena:\nTodos los nudos $all\n\nCategoría:'),
        'view_category': Template('$category_name'),
        'knot': Template('$knot_name\n\nDescripción:\n$description\n\nABOK: $abok\n\nTambién conocido como: \n$names\n\n'
                         'Rompiendo la fuerza: $strength\n\n'
                         'Categoría: \n$categories\n\n'
                         'Más información sobre: https://knots.exyte.top/knot_id_$id')
    },
    'fr': {
        'view': Template('Liste complète:\nTous les nœuds $all\n\nCatégories:'),
        'view_category': Template('$category_name'),
        'knot': Template('$knot_name\n\nDescription:\n$description\n\nABOK: $abok\n\nAussi connu sous le nom: \n$names\n\n'
                         'Résistance à la rupture: $strength\n\n'
                         'Catégories: \n$categories\n\n'
                         'Plus d`informations sur: https://knots.exyte.top/knot_id_$id')
    },
    'it': {
        'view': Template('Lista completa:\nTutti i nodi $all\n\nCategoria:'),
        'view_category': Template('$category_name'),
        'knot': Template('$knot_name\n\nDescrizione:\n$description\n\nABOK: $abok\n\nConosciuto anche come: \n$names\n\n'
                         'Forza di rottura: $strength\n\n'
                         'Categoria: \n$categories\n\n'
                         'Maggiori informazioni su: https://knots.exyte.top/knot_id_$id')
    },
    'tuek': {
        'view': Template('Tam liste:\nTüm düğümler $all\n\nKategori:'),
        'view_category': Template('$category_name'),
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
        keyboard1.row('👁️View', '🌍Language')

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
            knots = alleknotentabelle.objects.all()
            kb = telebot.types.ReplyKeyboardMarkup()
            buf1 = None
            buf2 = None
            fl = 0
            kb.row('📚All')
            for el in encode.keys():
                kb_button = telebot.types.KeyboardButton(
                    encode[el]['img'] + encode[el][f'name_{language["cur_lang"]}'])
                if buf1 is not None and buf2 is not None:
                    if fl == 2:
                        kb.row(kb_button, buf1, buf2)
                        fl = 0
                        buf2 = buf1
                        buf1 = kb_button
                        continue
                buf2 = buf1
                buf1 = kb_button
                fl += 1
            kb.row('⭐Favorite', '🌍Language')
            bot.send_message(message.chat.id, language[language['cur_lang']]['view'].substitute(
                all=f'({len(knots)})'), reply_markup=kb)

        @bot.message_handler(commands=['language'])
        def lang(message):
            bot.send_message(message.chat.id, "Choose language:", reply_markup=inline_kb1)

        @bot.callback_query_handler(func=lambda c: c.data)
        def process_callback(callback_query: telebot.types.CallbackQuery):
            if callback_query.data in language:
                language.update({"cur_lang": callback_query.data})
                bot.send_message(callback_query.from_user.id, "Language changed", reply_markup=keyboard1)
                return
            elif callback_query.data[0] == 's':
                k = alleknotentabelle.objects.get(id=int(callback_query.data[1:]))
                obj = Favorite.objects.create(usr=callback_query.from_user.id, knot=k)
                obj.save()
                bot.send_message(callback_query.from_user.id, "Added to favorite")
            elif callback_query.data[0] == 'r':
                k = alleknotentabelle.objects.get(id=int(callback_query.data[1:]))
                obj = Favorite.objects.filter(usr=callback_query.from_user.id, knot=k).delete()
                obj.save()
                bot.send_message(callback_query.from_user.id, "Removed from favorite")
            else:
                kb1 = telebot.types.InlineKeyboardMarkup()
                obj = alleknotentabelle.objects.get(id=int(callback_query.data))
                if Favorite.objects.filter(usr=callback_query.from_user.id, knot=obj).exists():
                    kb_button = telebot.types.InlineKeyboardButton("⭐Delete from Favorite", callback_data=f'r{callback_query.data}')
                else:
                    kb_button = telebot.types.InlineKeyboardButton("⭐Add to Favorite",
                                                                   callback_data=f's{callback_query.data}')
                kb1.row(kb_button)
                categories = [el for el in obj.knoten_typ.split("_")]
                img = Image.open(settings.BASE_DIR / f"images/{obj.knotenbild2d[5:-8]}title.png").convert("RGB")
                img = ImageOps.invert(img)
                enhancer = ImageEnhance.Sharpness(img)
                enhancer = ImageEnhance.Contrast(enhancer.enhance(1.5))
                enhancer = ImageEnhance.Brightness(enhancer.enhance(1.5))
                img = enhancer.enhance(0.9)
                img = img.convert("RGBA")
                bot.send_photo(callback_query.from_user.id, img, caption=language[language['cur_lang']]['knot'].substitute(
                    knot_name=str(eval(f'obj.knotenname_{language["cur_lang"]}').split('_')[0]),
                    description=eval(f'obj.knotenbeschreibung_{language["cur_lang"]}'),
                    abok=obj.knoten_abok,
                    names="\n".join(
                        [str("--" + el) for el in eval(f'obj.knotenname_{language["cur_lang"]}').split("_")]),
                    strength=obj.knotenfestigkeit,
                    categories="\n".join([str("--" + encode[el][f"name_{language['cur_lang']}"]) for el in categories]),
                    id=int(callback_query.data)), reply_markup=kb1)

        @bot.message_handler(commands=all_types())
        def view(message):
            parsing = message.text.split('_')
            enter = '\n'
            if len(parsing) == 1:
                knots = alleknotentabelle.objects.all()
                kb = telebot.types.ReplyKeyboardMarkup()
                buf = None
                fl = True
                for el in encode.keys():
                    kb_button = telebot.types.KeyboardButton(encode[el]['img']+encode[el][f'name_{language["cur_lang"]}'])
                    if buf is not None:
                        if fl:
                            kb.row(kb_button, buf)
                    else:
                        kb.row(kb_button)
                    buf = kb_button
                    fl = not fl
                kb.row('⭐Favorite', '🌍Language')
                bot.send_message(message.chat.id, language[language['cur_lang']]['view'].substitute(
                    all=f'({len(knots)})'), reply_markup=kb)
            elif parsing[1] == 'all':
                knots = alleknotentabelle.objects.all()
                knots_dict = dict()
                for el in knots:
                    knots_dict.update({str(el.id): str(' or '.join(i for i in
                                                                   eval(f'el.knotenname_'
                                                                        f'{language["cur_lang"]}').split('_')))})
                bot.send_message(message.chat.id, f'All:\n\n')
                for el in knots_dict.keys():
                    bot.send_message(message.chat.id,
                                     f'{str(knots_dict[el] + f"(type /knot_{el} - see info about knot)")}')
            elif len(parsing) == 2:
                knots = alleknotentabelle.objects.filter(knoten_typ__startswith=parsing[1])
                buf1 = None
                buf2 = None
                fl = 0
                bot.send_message(message.chat.id, language[language['cur_lang']]['view_category'].substitute(
                    category_name=encode[parsing[1]][f"name_{language['cur_lang']}"]))
                for el in knots:
                    kb = telebot.types.InlineKeyboardMarkup()
                    kb_button = telebot.types.InlineKeyboardButton(
                        f'{str(eval("el.knotenname_" + language["cur_lang"]).split("_")[0])}',
                        callback_data=f'{str(el.id)}')
                    kb.add(kb_button)
                    img = Image.open(settings.BASE_DIR / f"images/{el.knotenbild2d[5:-8]}title.png").convert("RGB")
                    img = ImageOps.invert(img)
                    enhancer = ImageEnhance.Sharpness(img)
                    enhancer = ImageEnhance.Contrast(enhancer.enhance(1.5))
                    enhancer = ImageEnhance.Brightness(enhancer.enhance(1.5))
                    img = enhancer.enhance(0.9)
                    img = img.convert("RGBA")
                    bot.send_photo(message.chat.id, img, reply_markup=kb)
            else:
                bot.send_message(message.chat.id, "No such category or type")

        @bot.message_handler(commands=all_knots())
        def knot(message):
            parsing = message.text.split('_')
            enter = '\n'
            if len(parsing) == 2:
                kb1 = telebot.types.InlineKeyboardMarkup()
                obj = alleknotentabelle.objects.get(id=int(parsing[1]))
                if Favorite.objects.filter(usr=message.from_user.id, knot=obj).exists():
                    kb_button = telebot.types.InlineKeyboardButton("⭐Add to Favorite", callback_data=f's{parsing[1]}')
                else:
                    kb_button = telebot.types.InlineKeyboardButton("⭐Delete from Favorite", callback_data=f'r{parsing[1]}')
                kb1.row(kb_button)
                categories = [el for el in obj.knoten_typ.split("_")]
                img = Image.open(settings.BASE_DIR / f"images/{obj.knotenbild2d[5:-8]}title.png").convert("RGB")
                img = ImageOps.invert(img)
                enhancer = ImageEnhance.Sharpness(img)
                enhancer = ImageEnhance.Contrast(enhancer.enhance(1.5))
                enhancer = ImageEnhance.Brightness(enhancer.enhance(1.5))
                img = enhancer.enhance(0.9)
                img = img.convert("RGBA")
                bot.send_photo(message.chat.id, img, caption=language[language['cur_lang']]['knot'].substitute(
                    knot_name=str(eval(f'obj.knotenname_{language["cur_lang"]}').split('_')[0]),
                    description=eval(f'obj.knotenbeschreibung_{language["cur_lang"]}'),
                    abok=obj.knoten_abok,
                    names="\n".join(
                        [str("--" + el) for el in eval(f'obj.knotenname_{language["cur_lang"]}').split("_")]),
                    strength=obj.knotenfestigkeit,
                    categories="\n".join([str("--" + encode[el][f"name_{language['cur_lang']}"]) for el in categories]),
                    id=int(parsing[1])), reply_markup=kb1)
            else:
                bot.send_message(message.chat.id, "Opps, something went wrong")

        @bot.message_handler(content_types=['text'])
        def view_all(message):
            if message.text[2:] == 'View':
                knots = alleknotentabelle.objects.all()
                kb = telebot.types.ReplyKeyboardMarkup()
                buf1 = None
                buf2 = None
                fl = 0
                for el in encode.keys():
                    kb_button = telebot.types.KeyboardButton(encode[el]['img']+encode[el][f'name_{language["cur_lang"]}'])
                    if buf1 is not None and buf2 is not None:
                        if fl == 2:
                            kb.row(kb_button, buf1, buf2)
                            fl = 0
                            buf2 = buf1
                            buf1 = kb_button
                            continue
                    buf2 = buf1
                    buf1 = kb_button
                    fl += 1
                kb.row('👁️View', '🌍Language')
                bot.send_message(message.chat.id, language[language['cur_lang']]['view'].substitute(
                    all=f'({len(knots)})'), reply_markup=kb)
            elif message.text[1:] == 'Language':
                bot.send_message(message.chat.id, "Choose language:", reply_markup=inline_kb1)
            elif message.text[1:] == 'All':
                knots = alleknotentabelle.objects.all()
                buf = None
                img_buf = None
                if len(knots) % 2 == 0:
                    fl = False
                else:
                    fl = True
                bot.send_message(message.chat.id, 'All:')
                for el in knots:
                    kb = telebot.types.InlineKeyboardMarkup()
                    kb_button = telebot.types.InlineKeyboardButton(
                        f'{str(eval("el.knotenname_" + language["cur_lang"]).split("_")[0])}',
                        callback_data=str(el.id))
                    img = Image.open(
                        settings.BASE_DIR / f"images/{el.knotenbild2d[5:-8]}title.png").convert("RGB")
                    img = ImageOps.invert(img)
                    enhancer = ImageEnhance.Sharpness(img)
                    enhancer = ImageEnhance.Contrast(enhancer.enhance(1.5))
                    enhancer = ImageEnhance.Brightness(enhancer.enhance(1.5))
                    img = enhancer.enhance(0.9)
                    img = img.convert("RGBA")
                    if buf is not None:
                        if fl:
                            two_in_one = Image.new("RGBA", (244 * 2, 244))
                            two_in_one.paste(img, (0, 0))
                            two_in_one.paste(img_buf, (244, 0))
                            kb.row(kb_button, buf)
                            bot.send_photo(message.chat.id, two_in_one, reply_markup=kb)
                    elif fl:
                        kb.row(kb_button)
                        bot.send_photo(message.chat.id, img, reply_markup=kb)
                    buf = kb_button
                    img_buf = img
                    fl = not fl
            elif message.text[1:] == 'Favorite':
                knots = alleknotentabelle.objects.filter(id__in=Favorite.objects.filter
                                                         (usr=message.from_user.id).values('knot'))
                buf = None
                img_buf = None
                if len(knots) % 2 == 0:
                    fl = False
                else:
                    fl = True
                bot.send_message(message.chat.id, "Favorite:")
                for el in knots:
                    kb = telebot.types.InlineKeyboardMarkup()
                    kb_button = telebot.types.InlineKeyboardButton(
                        f'{str(eval("el.knotenname_" + language["cur_lang"]).split("_")[0])}',
                        callback_data=str(el.id))
                    img = Image.open(
                        settings.BASE_DIR / f"images/{el.knotenbild2d[5:-8]}title.png").convert("RGB")
                    img = ImageOps.invert(img)
                    enhancer = ImageEnhance.Sharpness(img)
                    enhancer = ImageEnhance.Contrast(enhancer.enhance(1.5))
                    enhancer = ImageEnhance.Brightness(enhancer.enhance(1.5))
                    img = enhancer.enhance(0.9)
                    img = img.convert("RGBA")
                    if buf is not None:
                        if fl:
                            two_in_one = Image.new("RGBA", (244 * 2, 244))
                            two_in_one.paste(img, (0, 0))
                            two_in_one.paste(img_buf, (244, 0))
                            kb.row(kb_button, buf)
                            bot.send_photo(message.chat.id, two_in_one, reply_markup=kb)
                    elif fl:
                        kb.row(kb_button)
                        bot.send_photo(message.chat.id, img, reply_markup=kb)
                    buf = kb_button
                    img_buf = img
                    fl = not fl
            else:
                category = message.text[1:]
                res = None
                for el in encode.keys():
                    if encode[el][f'name_{language["cur_lang"]}'] == category:
                        res = el
                if res is not None:
                    knots = alleknotentabelle.objects.filter(knoten_typ__startswith=res)
                    buf = None
                    img_buf = None
                    if len(knots) % 2 == 0:
                        fl = False
                    else:
                        fl = True
                    bot.send_message(message.chat.id, language[language['cur_lang']]['view_category'].substitute(
                        category_name=encode[res][f"name_{language['cur_lang']}"]))
                    for el in knots:
                        kb = telebot.types.InlineKeyboardMarkup()
                        kb_button = telebot.types.InlineKeyboardButton(f'{str(eval("el.knotenname_" + language["cur_lang"]).split("_")[0])}',
                                                                       callback_data=str(el.id))
                        img = Image.open(
                            settings.BASE_DIR / f"images/{el.knotenbild2d[5:-8]}title.png").convert("RGB")
                        img = ImageOps.invert(img)
                        enhancer = ImageEnhance.Sharpness(img)
                        enhancer = ImageEnhance.Contrast(enhancer.enhance(1.5))
                        enhancer = ImageEnhance.Brightness(enhancer.enhance(1.5))
                        img = enhancer.enhance(0.9)
                        img = img.convert("RGBA")
                        if buf is not None:
                            if fl:
                                two_in_one = Image.new("RGBA", (244*2, 244))
                                two_in_one.paste(img, (0,0))
                                two_in_one.paste(img_buf, (244, 0))
                                kb.row(kb_button, buf)
                                bot.send_photo(message.chat.id, two_in_one, reply_markup=kb)
                        elif fl:
                            kb.row(kb_button)
                            bot.send_photo(message.chat.id, img, reply_markup=kb)
                        buf = kb_button
                        img_buf = img
                        fl = not fl
                else:
                    bot.send_message(message.chat.id, "Opps, something went wrong")

        bot.polling()
