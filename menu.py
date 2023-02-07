"""
A menu - you need to add the database and fill in the functions. 
"""

from peewee import *

db = SqliteDatabase('menu.sqlite')

class Menu(Model):
    name = CharField()
    country = CharField()
    catches = IntegerField()

    class Meta:
        database = db
    
    def __str__(self):
        return f'{self.id}: {self.name:<20} {self.country:<15} {self.catches:<15}'


def database_data():
    db.connect()
    db.create_tables([Menu])
    Menu.delete().execute()
    
    janne = Menu(name='Janne Mustonen', country='Finland', catches=98)
    janne.save()

    ian = Menu(name='Ian Steward', country='Canada', catches=94)
    ian.save()

    aaron = Menu(name='Aaron Gregg', country='Canada', catches=88)
    aaron.save()

    chad = Menu(name='Chad Taylor', country='USA', catches=78)
    chad.save()


def main():
    database_data()
    menu_text = """
    1. Display all records
    2. Search by name
    3. Add new record
    4. Edit existing record
    5. Delete record 
    6. Quit
    """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_records()
        elif choice == '2':
            search_by_name()
        elif choice == '3':
            add_new_record()
        elif choice == '4':
            edit_existing_record()
        elif choice == '5':
            delete_record()
        elif choice == '6':
            break
        else:
            print('Not a valid selection, please try again')


def display_all_records():
    menus = Menu.select()
    for menu in menus:
        print(menu)


def search_by_name():
    try:
        name = input('Enter the name you want to search: ')
        search = Menu.select().where(fn.Lower(Menu.name) == name.lower()).get()

        if search:
            print(search)
        else:
            print('Name not found.')

    except DoesNotExist as ie:
        print(f'Error searching name: {ie}')


def add_new_record():
    try:
        new_name = input('Enter the person\'s name: ')
        new_country = input('Enter the country: ')
        new_catches = int(input('Enter amount of catches: '))

        new_record = Menu(name=new_name, country=new_country, catches=new_catches)
        new_record.save()
        
    except ValueError as ve:
        print(f'Error adding new record: {ve}')


def edit_existing_record():
    try:
        id_update = input('Enter the ID you want to edit: ')
        name_update = input('Enter new name: ')
        country_update = input('Enter new country: ')
        catches_update = int(input('Enter new catch: '))

        update_record = Menu.update(name=name_update, country=country_update, catches=catches_update).where(Menu.id == id_update).execute()

        if update_record:
            print(f'ID {id_update} has been edited')
        else:
            print('Record not found.')

    except ValueError as ve:
        print(f'Error editing existing record: {ve}')


def delete_record():
    try:
        id_delete = int(input('Enter the ID you want to delete: '))
        delete_row = Menu.delete().where(Menu.id == id_delete).execute()

        if delete_row:
            print(f'ID {id_delete} has been deleted.')
        else:
            print('Record not found.')

    except ValueError as ve:
        print(f'Error deleting record: {ve}')


if __name__ == '__main__':
    main()