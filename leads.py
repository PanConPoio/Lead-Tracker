import json
import matplotlib.pyplot as plt

# Archivo donde se guardarán los datos
DATA_FILE = "leads_data.json"

def load_data():
    """Carga los datos desde un archivo JSON."""
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """Guarda los datos en un archivo JSON."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_lead_data(date, received, converted):
    """Añade un nuevo registro de leads."""
    data = load_data()
    conversion_rate = (converted / received * 100) if received > 0 else 0
    data.append({"date": date, "received": received, "converted": converted, "rate": round(conversion_rate, 2)})
    save_data(data)
    print(f"Datos guardados para {date}: {converted}/{received} leads convertidos ({round(conversion_rate, 2)}%)")

# Historal de datos agregados
def display_data():
    """Muestra los datos almacenados en formato tabla."""
    data = load_data()
    if not data:
        print("No hay datos registrados aún.")
        return
    print("\nHistorial de Leads Convertidos:")
    print("ID | Fecha       | Leads Recibidos | Leads Convertidos | % Conversión")
    print("-" * 70)
    for i, entry in enumerate(data):
        print(f"{i:2} | {entry['date']} | {entry['received']:15} | {entry['converted']:16} | {entry['rate']:11}%")

# Genera el grafico de las estadisticas
def plot_data():
    """Genera un gráfico con la tendencia de conversión."""
    data = load_data()
    if not data:
        print("No hay datos para graficar.")
        return
    dates = [entry['date'] for entry in data]
    rates = [entry['rate'] for entry in data]
    
    plt.figure(figsize=(8, 4))
    plt.plot(dates, rates, marker='o', linestyle='-', color='b', label='Tasa de Conversión (%)')
    plt.xlabel("Fecha")
    plt.ylabel("% Conversión")
    plt.title("Tendencia de Conversión de Leads")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Nueva función para eliminar registros
def delete_lead_data():
    """Elimina un registro de leads existente."""
    data = load_data()
    if not data:
        print("No hay datos para eliminar.")
        return
    
    display_data()  # Muestra los datos con IDs para que el usuario pueda elegir
    try:
        index = int(input("\nIngrese el ID del registro que desea eliminar: "))
        if 0 <= index < len(data):
            deleted = data.pop(index)
            save_data(data)
            print(f"Registro del {deleted['date']} eliminado correctamente.")
        else:
            print("ID no válido. Operación cancelada.")
    except ValueError:
        print("Entrada no válida. Debe ingresar un número.")

# Nueva función para ver el total de leads recibidos
def view_total_leads():
    """Muestra el total de leads recibidos sin importar si se convirtieron."""
    data = load_data()
    if not data:
        print("No hay datos registrados aún.")
        return
    
    total_leads = sum(entry['received'] for entry in data)
    print(f"\nTotal de leads recibidos hasta la fecha: {total_leads}")
    
    # Graficar los leads recibidos por fecha
    plot_leads_received()

# Nueva función para graficar los leads recibidos
def plot_leads_received():
    """Genera un gráfico con los leads recibidos por fecha."""
    data = load_data()
    if not data:
        print("No hay datos para graficar.")
        return
    
    dates = [entry['date'] for entry in data]
    received = [entry['received'] for entry in data]
    
    plt.figure(figsize=(8, 4))
    plt.bar(dates, received, color='green', label='Leads Recibidos')
    plt.xlabel("Fecha")
    plt.ylabel("Cantidad de Leads")
    plt.title("Leads Recibidos por Fecha")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

# Formulario de entrada
if __name__ == "__main__":
    while True:
        print("\n1. Añadir datos de leads")
        print("2. Mostrar historial de leads")
        print("3. Mostrar gráfico de conversión")
        print("4. Eliminar registro de leads")
        print("5. Ver total de leads recibidos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            fecha = input("Ingrese la fecha (YYYY-MM-DD): ")
            recibidos = int(input("Ingrese la cantidad de leads recibidos: "))
            convertidos = int(input("Ingrese la cantidad de leads convertidos: "))
            add_lead_data(fecha, recibidos, convertidos)
        elif opcion == "2":
            display_data()
        elif opcion == "3":
            plot_data()
        elif opcion == "4":
            delete_lead_data()
        elif opcion == "5":
            view_total_leads()
        elif opcion == "6":
            break
        else:
            print("Opción no válida. Intente de nuevo.")