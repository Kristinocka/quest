import mysql.connector

db = mysql.connector.connect(user="root", password="kristi", host="127.0.0.1", database="kristinka", port="6969")

cursor = db.cursor()


def create_table(tb_name):
    cursor.execute('CREATE TABLE IF NOT EXISTS ' + tb_name + '(id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY )')
    add_column(tb_name, 'Q', 'VARCHAR(1000)')
    add_column(tb_name, 'V', 'VARCHAR(255)')
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()  ## zwraca wszystkie tabele, nie działa bez cursor.execute("SHOW TABLES")

    ## showing all the tables one by one
    print("Tabela stan: po dodaniu")
    for table in tables:
        print(table)


def check_if_column_exists(tb_name, cl_name):
    query = "SHOW COLUMNS FROM `" + tb_name + "` LIKE '" + cl_name + "'"
    cursor.execute(query)
    msg = cursor.fetchone()  ## zwraca wszystkie tabele, nie działa bez cursor.execute("SHOW TABLES")
    return msg


def add_column(tb_name, cl_name, cl_type, *args):
    check = check_if_column_exists(tb_name, cl_name)
    print(check)
    if check != None:
        print("Column '" + cl_name + "' already exists")
    else:
        list_of_args = []

        if not args:
            args = ''
        else:
            for arg in args:
                list_of_args.append(arg)

        query = cl_name + ' ' + cl_type + ' ' + ''.join(list_of_args)
        cursor.execute('ALTER TABLE ' + tb_name + ' ADD COLUMN ' + query + '')
        print('Column ' + cl_name + ' was succesfullly created')


def insert_data(tb_name, q, v):
    query = f'INSERT INTO {tb_name} (Q,V) VALUES ("{q}", "{v}")'
    cursor.execute(query)

    # to make final output we have to run the 'commit()' method of the database object
    db.commit()
    print(cursor.rowcount, "records inserted")


def get_data_from_table(tb_name):
    cursor.execute("Select Q,V from " + tb_name)
    data = cursor.fetchall()

    return data
