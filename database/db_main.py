from mysql.connector import cursor
import database
import numpy as np

if __name__ == '__main__':
    database = database.DataBase()
    #database._cursor.execute("DROP TABLE images")
    database.create_table()
    #database.delete_rows() # run it once to delete our test entries 

    array = np.array([ 0. ,  2.3,  4.6,  6.9,  9.2, 11.5, 13.8, 16.1, 18.4, 20.7, 23.])
    array1 = np.array([5.6, 8.9, 11.3])

    database.insert_into_table('https://blog.codinghorror.com/filesystem-paths-how-long-is-too-long/#:~:text=In%20the%20Windows%20API%20(with,and%20a%20terminating%20null%20character.', array, 'histogram')
    database.insert_into_table('https://blog.codinghorror.com/filesystem-paths-how-long-is-too-long/#:~:text=In%20the%20Windows%20API%20(with,and%20a%20terminating%20null%20character.', array1, 'dominant_color')
    database.insert_into_table('https://blog.codinghorror.com/filesystem-paths-how-long-is-too-long/#:~:text=In%20the%20Windows%20API%20(with,and%20a%20terminating%20null%20character.', array, 'average_color')

    #database._cursor.execute("SELECT * FROM images")
    #for x in database._cursor:
    #   print (x)

    #get images() function only works if the 3 feature vectors are inserted into the database
    output = database.get_images()
    print(output)
  
    print ("working fine!")