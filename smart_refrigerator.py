from datetime import datetime, date, timedelta
from decimal import Decimal

goods = {}

def add(items, title, amount, expiration_date=None):
    #Formato datetime.date para fecha de expiracion. - Формат datetime.date для даты истечения срока годности
    expiration_date = datetime.date(datetime.strptime(expiration_date, '%Y-%m-%d')) if expiration_date else None
    
    #lista para el valor dentro del diccionario - список для значения внутри словаря
    notes_list = [{'amount': Decimal(amount), 'expiration_date': expiration_date}]

    #Agregar al diccionario los pares clave:valor o solo valor a la clave existente. - 
    #Добавить в словарь пары ключ:значение или только значение к существующему ключу.
    items[title].append({'amount': Decimal(amount), 'expiration_date': expiration_date}) if title in items else dict.update(items, {title: notes_list})
    return items


def add_by_note(items, note):
    #Divide las notas separadas en espacio por comas - разделяет заметки, разделенные пробелами, запятыми
    notes = str.split(note, ' ' )
    # Dependiendo de la longitud de notes, se busca el titulo, amount y fecha de expiracion.
    #В зависимости от длины notes, ищется заголовок, сумма и дата истечения срока годности.
    if len(notes[-1]) > 3: 
        expiration_date = datetime.date(datetime.strptime(notes[-1], '%Y-%m-%d'))
        amount_format, title = Decimal(notes[-2]), (str.join(' ', notes[:-2]))   
    else:
        expiration_date = None
        amount_format, title = Decimal(notes[-1]), (str.join(' ', notes[:-1])) 

    notes_list = [{'amount': amount_format , 'expiration_date': expiration_date}]
    
    #se tiene un diccionario con clave : lista{clave:valor} - словарь с ключом : списком{ключ : значение}
    items[title].append({'amount': amount_format , 'expiration_date': expiration_date}) if title in items else dict.update(items, {title: notes_list})
    return items


def find(items, needle):
    #Se genera una lista con los productos disponibles. Lista indiferente a minusculas/mayusculas y fragmento de palabra
    #Генерируется список доступных продуктов. Список нечувствителен к регистру и позволяет находить фрагменты слов.
    product_list = [item for item in items if (item.lower()).find(needle.lower()) >= 0]
    return product_list

def amount(items, needle):
    product_amount_sum = 0
    for item, info in items.items():
        #Se empieza la iteracion con el primer item. Una vez termina, sigue con el siguiente item.        
        #Al final se suma todos los valores de amount en product amount list.
        if item.lower().find(needle.lower())>= 0:
            product_amount_sum += Decimal(sum([row['amount'] for row in info]))
    return product_amount_sum


def expire(items, in_advance_days=0):
    expire_date = datetime.now().date() + timedelta(days=in_advance_days)
    list_expired = []
    
    for item, info in items.items():
        product_amount_sum = 0
        product_amount_list = [value['amount'] for value in info if value['expiration_date'] is not None and value['expiration_date'] <= expire_date]
        product_amount_sum += Decimal(sum(product_amount_list))
            
# Esta condicion hace que evite agregar elementos a nuestra lista de caducados si es que el expiration date es None.
        if product_amount_sum > 0:
            list_expired.append((item, product_amount_sum))      
    return list_expired


def remove(items, title, unit):

    for item, info in items.items():
        product_amount_sum = 0

        if title.lower() == item.lower():
            #Crea una lista con las unidades disponibles del producto que se busca restar o eliminar
            #Cписок с доступными единицами продукта, который вы хотите вычесть или удалить
            product_amount_list = [values['amount'] for values in info]
            product_amount_sum += sum(product_amount_list)
            product_units = product_amount_sum - unit
            message = f'Продукт "{title}" в холодильнике всё ещё имеет {product_units} единиц'

            if product_units == 0: 
                product_remove = dict.pop(items, title)
                message = f'Продукт "{title}" был удален из словаря. Вы взяли все единицы продукта'
            elif product_units < 0:
                message = f'Продукт "{title}" не в достаточном количестве. Введите корректное значение'
                break  
        else:
            message = f'Продукта "{title}" нет в словаре холодильника'
        break      
    return message

#Add a good in dict goods:
add(goods, 'Яйца', Decimal('10'), '2023-9-30')
add(goods, 'Вода', Decimal('2.5'))
#Add by note a good in dict goods:
add_by_note(goods, 'Яйца гусиные 4 2023-07-15')
add_by_note(goods, 'Яйца гусиные 1.5 2024-02-21')
add_by_note(goods, 'Яйца 2.5')
print(goods)
#Find by keywords a good in dict goods:
print(find(goods, 'уси'))
print(find(goods, 'йц'))
print(find(goods, 'од'))
#Find by keywords the amount of a good in dict goods:
print(amount(goods, 'йца'))
print(amount(goods, 'Вода'))
#Find by number of days left to expire the good in dict goods:
print(expire(goods, 2))
#Remove a good in dict goods:
print(remove(goods, 'Яйца', Decimal('12.6')))
print(remove(goods, 'Яца', Decimal('13.5')))
