from data import __all_models
from data.models import *
from data.db_session import *

VOWELS = "ёяыуаеиоюэ"
CONSONANTS = "йфцчвскмпнртгьшлщдзхъбж"
LETTERS = {VOWELS: 1, CONSONANTS: 0}
words = [
    "прожОрлива",
    "болтлИва",
    "монолОг",
    "некролОг",
    "аэропОрты",
    "бАнты",
    "бОроду",
    "бухгАлтеров",
    "вероисповЕдание",
    "граждАнство",
    "дефИс",
    "дешевИзна",
    "диспансЕр",
    "договорЁнность",
    "докумЕнт",
    "досУг",
    "еретИк",
    "жалюзИ",
    "знАчимость",
    "Иксы",
    "каталОг",
    "квартАл",
    "киломЕтр",
    "сантимЕтр",
    "кОнусы",
    "корЫсть",
    "крАны",
    "кремЕнь",
    "лЕкторы",
    "лыжнЯ",
    "мЕстностей",
    "мусоропровОд",
    "газопровОд",
    "намЕрение",
    "нарОст",
    "нЕдруг",
    "недУг",
    "некролОг",
    "нЕнависть",
    "нОвости",
    "нОготь",
    "Отрочество",
    "партЕр",
    "портфЕль",
    "пОручни",
    "придАное",
    "призЫв",
    "свЁкла",
    "сирОты",
    "срЕдства",
    "созЫв",
    "стАтуя",
    "столЯр",
    "доЯр",
    "тамОжня",
    "тОрты",
    "цемЕнт",
    "цЕнтнер",
    "цепОчка",
    "шАрфы",
    "шофЁр",
    "контролЁр…",
    "экспЕрт",
    "вернА",
    "знАчимый",
    "красИвее",
    "красИвейший",
    "кУхонный",
    "ловкА",
    "мозаИчный",
    "оптОвый",
    "прозорлИва",
    "Ива",
    "слИвовый",
    "Ива",
    "Глаголы",
    "бралА",
    "брАться",
    "бралАсь",
    "взялА",
    "взЯться",
    "взялАсь",
    "влИться",
    "влилАсь",
    "ворвАться",
    "ворвалАсь",
    "воспринЯть",
    "воспринялА",
    "воссоздалА",
    "вручИть",
    "вручИт",
    "гналА",
    "гнАться",
    "гналАсь",
    "добрАть",
    "добралА",
    "добрАться",
    "добралАсь",
    "дождАться",
    "дождалАсь",
    "дозвонИться",
    "дозвонИтся,",
    "дозвонЯтся",
    "дозИровать",
    "ждалА",
    "жИться",
    "жилОсь",
    "закУпорить",
    "занЯть",
    "зАнял",
    "зАняло",
    "заперЕть",
    "заперлА",
    "звалА",
    "звонИть",
    "звонИшь",
    "звонИм",
    "исчЕрпать",
    "клАсть",
    "клАла",
    "клЕить",
    "лгалА",
    "лилА",
    "лИться",
    "лилАсь",
    "наврАть",
    "навралА",
    "наделИть",
    "наделИт",
    "надорвАться",
    "надорвалАсь",
    "назвАться",
    "назвалАсь",
    "накренИться",
    "накренИтся",
    "налИть",
    "налилА",
    "нарвАть",
    "нарвалА",
    "насорИть",
    "насорИт",
    "начАть",
    "нАчал",
    "обзвонИть",
    "обзвонИт",
    "облегчИть",
    "облегчИт",
    "облИться",
    "облилАсь",
    "обнЯться",
    "обнялАсь",
    "обогнАть",
    "обогналА",
    "ободрАть",
    "ободралА",
    "ободрИть",
    "ободрИться",
    "ободрИшься",
    "обострИть",
    "одолжИть",
    "одолжИт",
    "озлОбить",
    "оклЕить",
    "окружИть",
    "окружИт",
    "опломбировАть",
    "формировАть",
    "премировАть…",
    "опОшлить",
    "освЕдомиться",
    "освЕдомишься",
    "отбЫть",
    "отбылА",
    "отдАть",
    "отдалА",
    "откУпорить",
    "откУпорил",
    "отозвАть",
    "отозвалА",
    "отозвАться",
    "отозвалАсь",
    "перезвонИть",
    "перезвонИт",
    "перелИть",
    "перелилА",
    "плодоносИть",
    "повторИть",
    "повторИт",
    "позвАть",
    "позвалА",
    "позвонИть",
    "позвонИшь",
    "полИть",
    "полилА",
    "положИть",
    "положИл",
    "понЯть",
    "понялА",
    "послАть",
    "послАла",
    "прибЫть",
    "прИбыл",
    "принЯть",
    "прИнял",
    "принУдить",
    "рвалА",
    "сверлИть",
    "сверлИшь",
    "снялА",
    "создАть",
    "создалА",
    "сорвАть",
    "сорвалА",
    "сорИть",
    "сорИт",
    "убрАть",
    "убралА",
    "убыстрИть",
    "углубИть",
    "укрепИть",
    "укрепИт",
    "чЕрпать",
    "щемИть",
    "щемИт",
    "щЁлкать",
    "Причастия",
    "балОванный",
    "включЁнный",
    "включЁн",
    "погружЁнный",
    "довезЁнный",
    "зАгнутый",
    "зАнятый",
    "занятА",
    "зАпертый",
    "запертА",
    "заселЁнный",
    "заселенА",
    "избалОванный",
    "кормЯщий",
    "кровоточАщий",
    "молЯщий",
    "нажИвший",
    "нАжитый",
    "нажитА",
    "налИвший",
    "налитА",
    "нанЯвшийся",
    "начАвший",
    "нАчатый",
    "начатА",
    "низведЁнный",
    "низведЁн",
    "ободрЁнный",
    "ободрЁн",
    "обострЁнный",
    "определЁнный",
    "определЁн",
    "отключЁнный",
    "повторЁнный",
    "поделЁнный",
    "понЯвший",
    "прИнятый",
    "приручЁнный",
    "прожИвший",
    "снЯтый",
    "снятА",
    "сОгнутый",
    "балУясь",
    "закУпорив",
    "начАв",
    "начАвшись",
    "отдАв ",
    "поднЯв",
    "понЯв",
    "прибЫв",
    "создАв",
    "вОвремя",
    "добелА",
    "дОверху",
    "донЕльзя",
    "дОнизу",
    "дОсуха",
    "завИдно",
    "зАгодя",
    "зАсветло",
    "зАтемно",
    "красИвее",
    "навЕрх",
    "надОлго",
    "ненадОлго",
]

global_init("db/gamers.db")


def get_word_structure(word):
    word_structure = ""
    for letter in word.lower():
        if letter in VOWELS:
            word_structure += "1"
        elif letter in CONSONANTS:
            word_structure += "0"
    return word_structure


def get_word_accent_position(word):
    for index, letter in enumerate(word):
        if letter.isupper():
            return index
    return -1


for word in words:
    if get_word_accent_position(word) == -1:
        words.remove(word)
print(words)

session = create_session()
for index, word in enumerate(words):
    word = Word(
        id=index,
        guesses_number=0,
        accent_position=get_word_accent_position(word),
        word_structure=get_word_structure(word),
        text=word.lower(),
    )
    session.add(word)
session.commit()
