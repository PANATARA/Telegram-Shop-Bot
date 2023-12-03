from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db import shopDB


def MainKeyboard():#Кнопки главного меню
    
    buttons = [
        ['Каталог', 'Мои Избранные'],
        ['Корзина', 'Заказы'],
        ['Настройки', 'Помощь']
    ]

    
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True)

    
    for button_row in buttons:
        main_menu.row(*[KeyboardButton(button_text) for button_text in button_row])

    return main_menu


def INKB_BAG(num, totalPrice, quantity=1): #Кнопки для корзины товаров

    inline_bag_del = InlineKeyboardButton('❌', callback_data='deleteFromBag')

    inline_amount = InlineKeyboardButton(str(quantity), callback_data='amount')
    inline_plus = InlineKeyboardButton('+', callback_data='plus')
    inline_min = InlineKeyboardButton('-', callback_data='minus')

    inline_bag_previous = InlineKeyboardButton('⬅️', callback_data='previous')
    inline_bag_num = InlineKeyboardButton(num, callback_data='none')
    inline_bag_next = InlineKeyboardButton('➡️', callback_data='next')

    inline_bag_order = InlineKeyboardButton(str(totalPrice), callback_data='order')

    inline_kb4 = InlineKeyboardMarkup()
    inline_kb4.row(inline_bag_del,  inline_bag_previous,
               inline_bag_num, inline_bag_next)
    inline_kb4.row(inline_min, inline_amount, inline_plus)
    inline_kb4.row(inline_bag_order)

    
    return inline_kb4


def INKB_CARD(): #Кнопки для карточек товара
    inline_favorites = InlineKeyboardButton(
    'Добавить в избранное', callback_data='favorites')
    inline_buy = InlineKeyboardButton('Купить', callback_data='Bag')
    inline_link = InlineKeyboardButton('Подробнее', callback_data='link')

    inline_kb1 = InlineKeyboardMarkup(row_width=1).add(
                inline_link, inline_buy, inline_favorites)
    return inline_kb1


def INKB_FAV(): #Кнопки для избранных товаров
    inline_buy = InlineKeyboardButton('Купить', callback_data='Bag')
    inline_del_favorites = InlineKeyboardButton(
                        'Удалить из избранных', callback_data='delete_from_favorites')
    inline_kb2 = InlineKeyboardMarkup().add(inline_del_favorites, inline_buy)
    return inline_kb2


def makeInlineKeyboard(): #Кнопки каталога товаров
    ClientShop = shopDB.ClientShopDB('database.db')
    categories = ClientShop.get_all_categories()
    i = 0
    categories_list = []
    for item in categories:
        categories_list.append(InlineKeyboardButton(
            item[0], callback_data=item[0]))

        i += 1
    callback_data_values = [button.callback_data for button in categories_list]
    categories_keyboard = InlineKeyboardMarkup()
    for button in categories_list:
        categories_keyboard.add(button)
    return [categories_keyboard, callback_data_values]


def INKB_admin():
    pass