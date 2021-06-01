from mysql.connector import cursor
import database
import numpy as np

if __name__ == '__main__':
    database = database.DataBase()
    #database._cursor.execute("DROP TABLE images")
    #database.create_table()

    #database.delete_images_rows()
    
    database.delete_videos_rows()# run it once to delete our test entries 
    
    
    a = np.ones((2,100))
    #array = np.array([ 0. ,  2.3,  4.6,  6.9,  9.2, 11.5, 13.8, 16.1, 18.4, 20.7, 23.])
    #array1 = np.array([5.6, 8.9, 11.3])
    b=np.full((2, 10), 33333)
    #database.insert_video('https://blog.codinghorror.com/filesystem-paths-how-long-is-too-long/#:~:text=In%20the%20Windows%20API%20(with,and%20a%20terminating%20null%20character.', a)
    #database.insert_video('https://blog.codinghorror.com/filesystem-paths-how-long-is-too-long/', b)
    
    #database.insert_into_table('https://blog.codinghorror.com/filesystem-paths-how-long-is-too-long/#:~:text=In%20the%20Windows%20API%20(with,and%20a%20terminating%20null%20character.', array, 'average_color')
    #print(b)
    #database._cursor.execute("SELECT * FROM images")
    #for x in database._cursor:
    #   print (x)

    #get_videos() #function only works if the 3 feature vectors are inserted into the database
    output = database.get_videos()
    #print(output)
  
    print ("working fine!")