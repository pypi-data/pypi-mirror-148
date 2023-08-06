def showDatabases():
    # return '''
    # mysql -u root << MYSQL_SCRIPT
    # SHOW DATABASES;
    # MYSQL_SCRIPT
    # '''
    return '''sudo mysql -u root -e 'show databases';'''

def exportDatabase(dbName, dbPath):
    return f'''sudo mysqldump -u root {dbName} > '{dbPath}' --skip-dump-date; '''