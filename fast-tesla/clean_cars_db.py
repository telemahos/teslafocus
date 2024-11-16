from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from add_cars_2db import Cars, Prices, Options, Photos  # Importiere deine Modelle

# Verbindung zur Datenbank herstellen
engine = create_engine('sqlite:///tesla_inventory.db')
Session = sessionmaker(bind=engine)

def delete_inactive_cars():
    try:
        with Session() as session:
            # Finde alle IDs von inaktiven Fahrzeugen
            inactive_cars = session.query(Cars).filter(Cars.active == False).all()
            inactive_car_ids = [car.id for car in inactive_cars]
            
            # Lösche alle verknüpften Einträge in den Tabellen Prices, Options, und Photos
            session.query(Prices).filter(Prices.car_id.in_(inactive_car_ids)).delete(synchronize_session=False)
            session.query(Options).filter(Options.car_id.in_(inactive_car_ids)).delete(synchronize_session=False)
            session.query(Photos).filter(Photos.car_id.in_(inactive_car_ids)).delete(synchronize_session=False)
            
            # Lösche die Einträge in der Cars-Tabelle
            session.query(Cars).filter(Cars.id.in_(inactive_car_ids)).delete(synchronize_session=False)
            
            # Änderungen speichern
            session.commit()
            print(f"{len(inactive_car_ids)} inaktive Fahrzeuge und alle verknüpften Daten erfolgreich gelöscht.")
            
            # Datenbankgröße reduzieren
            cleanup_database()
    
    except Exception as e:
        print(f"Fehler beim Löschen der inaktiven Fahrzeuge: {e}")

def cleanup_database():
    with engine.connect() as connection:
        # Führe das VACUUM-Kommando aus, um die Datenbankgröße zu reduzieren
        connection.execute(text("VACUUM;"))
        print("Datenbank bereinigt und ungenutzter Speicherplatz freigegeben.")

if __name__ == "__main__":
    delete_inactive_cars()
