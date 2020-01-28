import sqlite3


def connect():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    return cursor

# Запрос : вводим категорию, выводим сайты этой категории
def get_sites(category_input):
    cursor = connect()
    sql = "SELECT DISTINCT site.title FROM site INNER JOIN site_class ON site.Id=site_class.site_id WHERE site_class.class_id=?"
    sql1 = "SELECT DISTINCT site_class.class_id FROM classes INNER JOIN site_class ON classes.Id=site_class.class_id WHERE classes.title=? "
    cursor.execute(sql1, (category_input,))
    category_id = cursor.fetchall()[0][0]
    cursor.execute(sql, (category_id,))
    sites = cursor.fetchall()
    return sites

# Запрос : вводим cайт, выводим категории
def get_categories(site_input):
    cursor = connect()
    sql = "SELECT DISTINCT classes.title FROM classes INNER JOIN site_class ON classes.Id=site_class.class_id WHERE site_class.class_id=?"
    sql1 = "SELECT DISTINCT site_class.class_id FROM site INNER JOIN site_class ON site.Id=site_class.site_id WHERE site.title=? "
    cursor.execute(sql1, (site_input,))
    res = cursor.fetchall()
    sites = []
    if not res:
        print(res)
    else:
        category_id = res[0][0]
        cursor.execute(sql, (category_id,))
        sites = cursor.fetchall()
        print(sites)
    return sites

def add_site(site, category):
    # Запрос: добавить сайт в бд, если его там еще нет
    cursor = connect()
    sit = 'hse.ru'
    category = 'Наука,  Образование'
    find_class_id = "SELECT DISTINCT classes.Id FROM classes WHERE classes.title=?"
    cursor.execute(find_class_id, (category,))
    class_id = cursor.fetchall()[0][0]
    insert_site = "INSERT INTO site VALUES (?,?)"
    insert_site_class = "INSERT INTO site_class VALUES (?,?)"
    cursor.execute("SELECT EXISTS(SELECT 1 FROM site WHERE title=?)", (sit,))
    a = cursor.fetchall()[0][0]
    if (a != 1):
        cursor.execute("SELECT COUNT(*) FROM site")
        site_id = cursor.fetchall()[0][0] + 1
        cursor.execute(insert_site, (site_id, sit))
        cursor.execute(insert_site_class, (site_id, class_id))
