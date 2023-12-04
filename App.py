import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import locale

class InventarioBarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario Bar App")

        # Configurar formato de moneda colombiana (COP)
        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

        # Cargar inventario desde el archivo
        self.inventario = self.cargar_inventario()

        # Variables para seguimiento de ganancias y costos
        self.ingresos_totales = 0
        self.costos_totales = 0

        # Interfaz de usuario
        self.lbl_producto = tk.Label(root, text="Producto:")
        self.lbl_producto.grid(row=0, column=0, padx=10, pady=10)

        self.producto_var = tk.StringVar()
        self.cmb_producto = ttk.Combobox(root, textvariable=self.producto_var, values=list(self.inventario.keys()))
        self.cmb_producto.grid(row=0, column=1, padx=10, pady=10)
        self.cmb_producto.bind("<<ComboboxSelected>>", self.actualizar_precios)

        self.lbl_precio_compra = tk.Label(root, text="Precio de Compra:")
        self.lbl_precio_compra.grid(row=1, column=0, padx=10, pady=10)

        self.precio_compra_var = tk.StringVar()
        self.entry_precio_compra = tk.Entry(root, textvariable=self.precio_compra_var)
        self.entry_precio_compra.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_precio_venta = tk.Label(root, text="Precio de Venta:")
        self.lbl_precio_venta.grid(row=2, column=0, padx=10, pady=10)

        self.precio_venta_var = tk.StringVar()
        self.entry_precio_venta = tk.Entry(root, textvariable=self.precio_venta_var)
        self.entry_precio_venta.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_cantidad = tk.Label(root, text="Cantidad:")
        self.lbl_cantidad.grid(row=3, column=0, padx=10, pady=10)

        self.cantidad_var = tk.StringVar()
        self.entry_cantidad = tk.Entry(root, textvariable=self.cantidad_var)
        self.entry_cantidad.grid(row=3, column=1, padx=10, pady=10)

        self.btn_registrar_venta = tk.Button(root, text="Registrar Venta", command=self.registrar_venta)
        self.btn_registrar_venta.grid(row=4, column=0, columnspan=2, pady=10)

        self.btn_agregar_stock = tk.Button(root, text="Agregar Stock", command=self.agregar_stock)
        self.btn_agregar_stock.grid(row=5, column=0, columnspan=2, pady=10)

        self.btn_agregar_producto = tk.Button(root, text="Agregar Producto", command=self.agregar_producto)
        self.btn_agregar_producto.grid(row=6, column=0, columnspan=2, pady=10)

        self.lbl_ganancias = tk.Label(root, text="Ganancias Totales: $0")
        self.lbl_ganancias.grid(row=7, column=0, columnspan=2, pady=10)

        # Guardar inventario al cerrar la aplicación
        root.protocol("WM_DELETE_WINDOW", self.guardar_inventario_al_cerrar)

    def actualizar_precios(self, event):
        producto_seleccionado = self.producto_var.get()
        if producto_seleccionado in self.inventario:
            precio_compra = self.inventario[producto_seleccionado]["precio_compra"]
            precio_venta = self.inventario[producto_seleccionado]["precio_venta"]
            self.precio_compra_var.set(locale.currency(int(precio_compra), grouping=True))
            self.precio_venta_var.set(locale.currency(int(precio_venta), grouping=True))

    def registrar_venta(self):
        producto = self.producto_var.get()
        cantidad = self.cantidad_var.get()

        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser un número positivo.")
        except ValueError as e:
            messagebox.showerror("Error", f"Error en la cantidad: {str(e)}")
            return

        if producto in self.inventario:
            if self.inventario[producto]["stock"] >= cantidad:
                # Eliminar símbolo de dólar y espacios antes de convertir a float
                precio_compra = float(self.precio_compra_var.get().replace('$', '').replace(',', ''))
                precio_venta = float(self.precio_venta_var.get().replace('$', '').replace(',', ''))

                costo_total = precio_compra * cantidad
                ingreso_total = precio_venta * cantidad

                self.inventario[producto]["stock"] -= cantidad
                self.costos_totales += costo_total
                self.ingresos_totales += ingreso_total

                # Calcular ganancia como ingreso total - costo total
                ganancia_total = ingreso_total - costo_total

                # Actualizar etiqueta de ganancias totales con formato de moneda colombiana
                self.lbl_ganancias.config(text=f"Ganancias Totales: {locale.currency(int(ganancia_total), grouping=True, symbol=False)}")

                messagebox.showinfo("Venta Registrada", f"Venta de {cantidad} unidades de {producto} registrada.\n"
                                                       f"Ganancia: {locale.currency(int(ganancia_total), grouping=True, symbol=False)}")
            else:
                messagebox.showerror("Error", "No hay suficiente stock para realizar la venta.")
        else:
            messagebox.showerror("Error", "Producto no encontrado en el inventario.")

    def agregar_stock(self):
        producto = self.producto_var.get()
        cantidad = self.cantidad_var.get()

        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser un número positivo.")
        except ValueError as e:
            messagebox.showerror("Error", f"Error en la cantidad: {str(e)}")
            return

        if producto in self.inventario:
            self.inventario[producto]["stock"] += cantidad
            messagebox.showinfo("Stock Actualizado", f"Se agregaron {cantidad} unidades de {producto} al stock.")
        else:
            messagebox.showerror("Error", "Producto no encontrado en el inventario.")

    def agregar_producto(self):
        producto = self.producto_var.get()
        if producto not in self.inventario:
            try:
                precio_compra = float(self.precio_compra_var.get().replace('$', '').replace(',', ''))
                precio_venta = float(self.precio_venta_var.get().replace('$', '').replace(',', ''))
                if precio_compra < 0 or precio_venta < 0:
                    raise ValueError("Los precios deben ser números no negativos.")
            except ValueError as e:
                messagebox.showerror("Error", f"Error en los precios: {str(e)}")
                return

            self.inventario[producto] = {"precio_compra": precio_compra, "precio_venta": precio_venta, "stock": 0}
            messagebox.showinfo("Producto Agregado", f"Se ha agregado el producto: {producto}")
            self.cmb_producto['values'] = list(self.inventario.keys())  # Actualizar las opciones del Combobox
        else:
            messagebox.showerror("Error", "El producto ya existe en el inventario.")

    def cargar_inventario(self):
        try:
            with open("inventario.json", "r") as file:
                inventario = json.load(file)
            return inventario
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al cargar el inventario desde el archivo.")
            return {}

    def guardar_inventario(self):
        with open("inventario.json", "w") as file:
            json.dump(self.inventario, file)

    def guardar_inventario_al_cerrar(self):
        self.guardar_inventario()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioBarApp(root)
    root.mainloop()
