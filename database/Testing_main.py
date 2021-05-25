from mysql.connector import cursor
import Testing

if __name__ == '__main__':
    database = Testing.DataBase()
    #database._cursor.execute("DROP TABLE images")
    database.create_table()
    database.delete_rows()

    array = [ 0. ,  2.3,  4.6,  6.9,  9.2, 11.5, 13.8, 16.1, 18.4, 20.7, 23.]
    array1 = [5.6, 8.9, 11.3]
    database.insert_into_table('E:\DALIAA\DALIAA\photos', array, 'histogram')
    database.insert_into_table('E:\DALIAA\DALIAA\photos', array1, 'color_layout')
    database.insert_into_table('E:\DALIAA\DALIAA\photos', array, 'texture')

    #database._cursor.execute("SELECT * FROM images")
    #for x in database._cursor:
        #print (x)

    output = database.get_images()
    print (output)

    print ("working fine!")