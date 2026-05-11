from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError, PyMongoError

def conectar():
    try:
        # 2) Instància del Client
        uri = "mongodb://localhost:27017/" 
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        
        # 4) Verificació (Ping)
        respuesta = client.admin.command('ping')
        
        # 5) Accés a la Base de Dades
        db = client["activitat_pymongo"]
        
        # 6) Accés a la Col·lecció
        col = db["pymongo_users"]
        
        print("Conectado con éxito a la base de datos y colección.")
        return client, db, col
        
    # 3) Control d'Errors
    except ConnectionFailure as e:
        print(f"Error de conexión: {e}")
        return None, None, None

if __name__ == "__main__":
    cliente, db, col = conectar()
    if cliente:
        # Llista d'usuaris a insertar
        usubd = [
            {
                "_id": 1,
                "username": "cacafina",
                "nomcomplet": "Dolores Fuertes de Barriga",
                "email": "barrigamal@insdanielblanxart.cat",
                "edat": "35",
            },
            {
                "_id": 2,
                "username": "fermin",
                "nomcomplet": "Fermín Galarga",
                "email": "yatusabes@insdanielblanxart.cat",
                "edat": "17",
            },
        ]
        
        # Utilitzem insert_many per insertar els usuaris de la llista
        print("\n--- Sección Inserts ---")
        try:
            res = col.insert_many(usubd)
            print(f"Registres insertats: {len(res.inserted_ids)}")
            #si els usuaris ja existien salta l'error DuplicateKeyError
        except DuplicateKeyError:
            print("Aviso: Los registros con ID 1 y 2 ya existen.")
        except PyMongoError as e:
            if "duplicate key error" in str(e):
                print("Aviso: Los registros con ID 1 y 2 ya existen.")
            else:
                print(f"Error: {e}")
            
        # Insertem un usuari únic
        usuario_unico = {
            "_id": 3,
            "username": "Kylian",
            "nomcomplet": "Kylian Mbappe",
            "email": "kiki@madrid.net",
            "edat": "27",
        }
        
        # Insertem l'usuari únic
        try:
            res_one = col.insert_one(usuario_unico)
            print(f"Registre insertat amb ID: {res_one.inserted_id}")
        except DuplicateKeyError:
            print("Aviso: El registro con ID 3 ya existe.")
        except PyMongoError as e:
            print(f"Error: {e}")
            
            
        print("\n--- Sección Update ---")
        #Modifiquem el camp edat del document amb _id = 1
        filtre = {"_id": 1}
        canvis = {"$set": {"edat": 35}}
        
        try:
            #Utilitzem update_one per modificar un document i retornem matched_count i modified_count
            res_update = col.update_one(filtre, canvis)
            print(f"Documents coincidents (matched_count): {res_update.matched_count}")
            print(f"Documents modificats (modified_count): {res_update.modified_count}")
        except PyMongoError as e:
            print(f"Error de conexión o de Mongo: {e}")
            
            
        print("\n--- Sección Research ---")
        #Mostrem el total de documents
        if col.count_documents({}) == 0:
            print("Error no hi ha llista que mostrar")
        else:
            print(f"Total de documentos: {col.count_documents({})}")
            
            # Recerca global
            print("\nLlistat de tots els usuaris:")
            cursor = col.find({})
            for documento in cursor:
                print(documento)
                
            # Modifiquem el camp edat del document amb _id = 2 i _id = 3
            col.update_one({"_id": 2}, {"$set": {"edat": 17}})
            col.update_one({"_id": 3}, {"$set": {"edat": 12}})
            
            #Mostrem els documents amb edat major que 15
            edad_limite = 15
            print(f"\nMostrem usuaris amb edat major que {edad_limite} ($gt):")
            usuedat = col.find({"edat": {"$gt": edad_limite}})
            for u in usuedat:
                print(u)
                
                
        print("\n--- Sección Delete ---")
        #Utilitzem delete_one per esborrar el document amb _id = 3
        id_a_borrar = 3
        try:
            res_delete = col.delete_one({"_id": id_a_borrar})
            print(f"Documents esborrats (deleted_count): {res_delete.deleted_count}")
            
            if res_delete.deleted_count == 0:
                print("No s'ha esborrat cap registre (tal vegada ja no existia).")
            else:
                print(f"Registre amb ID {id_a_borrar} esborrat amb èxit.")
                
        except PyMongoError as e:
            print(f"Error de conexión o de Mongo en el delete: {e}")
            
    else:
        print("No s'ha pogut conectar.")
