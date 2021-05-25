import mysql.connector
import numpy as np

class DataBase:
    def __init__(self):
        self.connection =  mysql.connector.connect(host = "freedb.tech",
                                                user = "freedbtech_Team",
                                                password = "team",
                                                database="freedbtech_Multimedia"
                                                )
        self._cursor = self.connection.cursor()
        #self._cursor.execute("CREATE DATABASE IF NOT EXISTS testdatabase")                   

    def create_table(self):
        #self._cursor.execute("CREATE DATABASE testdatabase")
        self._cursor.execute("CREATE TABLE IF NOT EXISTS images (pth VARCHAR(1000), histogram VARCHAR(1000), dominant_color VARCHAR(1000), average_color VARCHAR(1000))")     
        self.connection.commit()

    def insert_into_table(self, image_path , feature_vector, algorithm):
        # to convert array to string #
        feature_string = '' 
        for i, j in zip(feature_vector, range(0, len(feature_vector))):           
            feature_string += str(i)
            if (j+1 == len(feature_vector)):
                continue
            feature_string +=  ',' 
        
        # check if the image_path doesn't exist then insert else update
        self._cursor.execute("""SELECT count(*) FROM images WHERE pth = %s""", (image_path,))
        data= self._cursor.fetchone()[0]
        if data == 0:
            if (algorithm == "histogram"):
                self._cursor.execute("INSERT INTO images (pth, histogram) VALUES (%s, %s)", (image_path, feature_string))
                self.connection.commit()

            elif (algorithm == "dominant_color"):
                self._cursor.execute("INSERT INTO images (pth, dominant_color) VALUES (%s, %s)", (image_path, feature_string))
                self.connection.commit()

            elif (algorithm == "average_color"):
                self._cursor.execute("INSERT INTO images (pth, average_color) VALUES (%s, %s)", (image_path, feature_string))
                self.connection.commit() 

        else:
            if (algorithm == "histogram"):
                self._cursor.execute("UPDATE images SET histogram = %s WHERE pth = %s", (feature_string, image_path))
                self.connection.commit()

            elif (algorithm == "dominant_color"):
                self._cursor.execute("UPDATE images SET dominant_color = %s WHERE pth = %s", (feature_string, image_path))
                self.connection.commit()

            elif (algorithm == "average_color"):
                self._cursor.execute("UPDATE images SET average_color = %s WHERE pth = %s", (feature_string, image_path))
                self.connection.commit()   


    def get_images(self):
        self._cursor.execute("SELECT * FROM images")
        image_list = []
        
        for x in self._cursor:
            # to convert string to array #
            feature_vector_1 = x[1].split(",")
            feature_vector_2 = x[2].split(",")
            feature_vector_3 = x[3].split(",")

            for i,j in zip (feature_vector_1,range(0,len(feature_vector_1))):
                feature_vector_1[j] = float(i)

            for i,j in zip (feature_vector_2,range(0,len(feature_vector_2))):
                feature_vector_2[j] = float(i)

            for i,j in zip (feature_vector_3,range(0,len(feature_vector_3))):
                feature_vector_3[j] = float(i)

            instance_image = []
            instance_image.append(x[0])
             
            instance_image.append(np.asarray(feature_vector_1))
            instance_image.append(np.asarray(feature_vector_2))
            instance_image.append(np.asarray(feature_vector_3))
            image_list.append(instance_image)

        return image_list

    def delete_rows(self):
        Delete_all_rows = """truncate table images"""
        self._cursor.execute(Delete_all_rows)
        self.connection.commit()
