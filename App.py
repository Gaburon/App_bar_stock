import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import json
import locale

class InventarioBarApp:

    def __init__(self, root): 
        self.root = root
        self.root.title("Inventario Bar App")
        self.root.geometry('1050x850')
        self.my_tree = ttk.Treeview(root)

        # Configurar formato de moneda colombiana (COP)
        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

        # Cargar inventario desde el archivo
        self.inventario = self.cargar_inventario()

        # Cargar ganancias del mes desde el archivo
        self.ganancias_mes_actual = self.cargar_ganancias_mes()

        # Variables para seguimiento de ganancias y costos
        self.ingresos_totales = 0
        self.costos_totales = 0

        # Varibla contador de ganancias
        self.ganancias_venta = 0
        self.ganancias_dia = 0
        self.ganancias_mes = 0

        # Interfaz de usuario
        # Manejo de inventario 
        self.lbl_header = tk.Label(root, text="Manejo Inventario", font= ("Arial", 14, "bold"), fg= "red")
        self.lbl_header.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_producto = tk.Label(root, text="Producto:")
        self.lbl_producto.grid(row=1, column=0, padx=10, pady=10)

        self.producto_var = tk.StringVar()
        self.cmb_producto = ttk.Combobox(root, textvariable=self.producto_var, values=list(self.inventario.keys()))
        self.cmb_producto.grid(row=1, column=1, padx=10, pady=10)
        self.cmb_producto.bind("<<ComboboxSelected>>", self.actualizar_precios)

        self.lbl_precio_compra = tk.Label(root, text="Precio de Compra:")
        self.lbl_precio_compra.grid(row=2, column=0, padx=10, pady=10)

        self.precio_compra_var = tk.StringVar()
        self.entry_precio_compra = tk.Entry(root, textvariable=self.precio_compra_var)
        self.entry_precio_compra.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_precio_venta = tk.Label(root, text="Precio de Venta:")
        self.lbl_precio_venta.grid(row=3, column=0, padx=10, pady=10)

        self.precio_venta_var = tk.StringVar()
        self.entry_precio_venta = tk.Entry(root, textvariable=self.precio_venta_var)
        self.entry_precio_venta.grid(row=3, column=1, padx=10, pady=10)

        # Nuevos campos para cantidad de stock
        self.lbl_cantidad_stock = tk.Label(root, text="Cantidad de Stock:")
        self.lbl_cantidad_stock.grid(row=4, column=0, padx=10, pady=10)

        self.cantidad_stock_var = tk.StringVar()
        self.entry_cantidad_stock = tk.Entry(root, textvariable=self.cantidad_stock_var)
        self.entry_cantidad_stock.grid(row=4, column=1, padx=10, pady=10)

        self.btn_agregar_stock = tk.Button(root, text="Agregar Stock", command=self.agregar_stock)
        self.btn_agregar_stock.grid(row=7, column=0, columnspan=2, pady=10)

        self.btn_agregar_producto = tk.Button(root, text="Agregar Producto", command=self.agregar_producto)
        self.btn_agregar_producto.grid(row=8, column=0, columnspan=2, pady=10)

        # GANANCIAS MESSSSSSS
        self.lbl_ganancias_mes_actual = tk.Label(root, text=f"Ganancias del mes actual: {locale.currency(int(self.ganancias_mes_actual), grouping=True, symbol=False)}")
        self.lbl_ganancias_mes_actual.grid(row=10, column=0, columnspan=2, pady=10)

        self.btn_limpiar_registro_mes = tk.Button(root, text="Limpiar Registro del Mes", command=self.limpiar_registro_mes)
        self.btn_limpiar_registro_mes.grid(row=11, column=0, columnspan=2, pady=10)
        
        # Interfas de ventas
        self.lbl_header = tk.Label(root, text="Ventas", font= ("Arial", 14, "bold"), fg= "red")
        self.lbl_header.grid(row=0, column=3, padx=10, pady=10)

        #1
        self.lbl_producto_venta1 = tk.Label(root, text="Producto de venta 1:")
        self.lbl_producto_venta1.grid(row=1, column=2, padx=10, pady=10)

        self.producto_venta1_var = tk.StringVar()
        self.cmb_producto_venta1 = ttk.Combobox(root, textvariable=self.producto_venta1_var, values=list(self.inventario.keys()))
        self.cmb_producto_venta1.grid(row=1, column=3, padx=10, pady=10)
        self.cmb_producto_venta1.bind("<<ComboboxSelected>>", self.actualizar_precios)

        self.lbl_cantidad_venta1 = tk.Label(root, text="Cantidad:")
        self.lbl_cantidad_venta1.grid(row=1, column=4, padx=10, pady=10)

        self.cantidad_venta1_var = tk.StringVar()
        self.entry_cantidad_venta1 = tk.Entry(root, textvariable=self.cantidad_venta1_var)
        self.entry_cantidad_venta1.grid(row=1, column=5, padx=10, pady=10)

        #2
        self.lbl_producto_venta2 = tk.Label(root, text="Producto de venta 2:")
        self.lbl_producto_venta2.grid(row=2, column=2, padx=10, pady=10)

        self.producto_venta2_var = tk.StringVar()
        self.cmb_producto_venta2 = ttk.Combobox(root, textvariable=self.producto_venta2_var, values=list(self.inventario.keys()))
        self.cmb_producto_venta2.grid(row=2, column=3, padx=10, pady=10)
        self.cmb_producto_venta2.bind("<<ComboboxSelected>>", self.actualizar_precios)

        self.lbl_cantidad_venta2 = tk.Label(root, text="Cantidad:")
        self.lbl_cantidad_venta2.grid(row=2, column=4, padx=10, pady=10)

        self.cantidad_venta2_var = tk.StringVar()
        self.entry_cantidad_venta2 = tk.Entry(root, textvariable=self.cantidad_venta2_var)
        self.entry_cantidad_venta2.grid(row=2, column=5, padx=10, pady=10)

        #3
        self.lbl_producto_venta3 = tk.Label(root, text="Producto de venta 3:")
        self.lbl_producto_venta3.grid(row=3, column=2, padx=10, pady=10)

        self.producto_venta3_var = tk.StringVar()
        self.cmb_producto_venta3 = ttk.Combobox(root, textvariable=self.producto_venta3_var, values=list(self.inventario.keys()))
        self.cmb_producto_venta3.grid(row=3, column=3, padx=10, pady=10)

        self.cmb_producto_venta3.bind("<<ComboboxSelected>>", self.actualizar_precios)
        self.lbl_cantidad_venta3 = tk.Label(root, text="Cantidad:")
        self.lbl_cantidad_venta3.grid(row=3, column=4, padx=10, pady=10)

        self.cantidad_venta3_var = tk.StringVar()
        self.entry_cantidad_venta3 = tk.Entry(root, textvariable=self.cantidad_venta3_var)
        self.entry_cantidad_venta3.grid(row=3, column=5, padx=10, pady=10)
        
        #4
        self.lbl_producto_venta4 = tk.Label(root, text="Producto de venta 4:")
        self.lbl_producto_venta4.grid(row=4, column=2, padx=10, pady=10)

        self.producto_venta4_var = tk.StringVar()
        self.cmb_producto_venta4 = ttk.Combobox(root, textvariable=self.producto_venta4_var, values=list(self.inventario.keys()))
        self.cmb_producto_venta4.grid(row=4, column=3, padx=10, pady=10)

        self.cmb_producto_venta4.bind("<<ComboboxSelected>>", self.actualizar_precios)
        self.lbl_cantidad_venta4 = tk.Label(root, text="Cantidad:")
        self.lbl_cantidad_venta4.grid(row=4, column=4, padx=10, pady=10)

        self.cantidad_venta4_var = tk.StringVar()
        self.entry_cantidad_venta4 = tk.Entry(root, textvariable=self.cantidad_venta4_var)
        self.entry_cantidad_venta4.grid(row=4, column=5, padx=10, pady=10)

        self.btn_registrar_venta = tk.Button(root, text="Registrar Venta", command=self.registrar_venta)
        self.btn_registrar_venta.grid(row=6, column=2, columnspan=2, pady=10)

        # Mostrar inventario
        style=ttk.Style()

        style.configure("Treeview.Heading", font=('Arial bold',15))

        self.my_tree['columns']=("Nombre", "Precio", "Cantidad")
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("Nombre", anchor=W, width=200)
        self.my_tree.column("Precio", anchor=W, width=150)
        self.my_tree.column("Cantidad", anchor=W, width=150)

        self.my_tree.heading("Nombre", text="Nombre", anchor=tk.W)
        self.my_tree.heading("Precio", text="Precio", anchor=tk.W)
        self.my_tree.heading("Cantidad", text="Cantidad", anchor=tk.W)

        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.my_tree.yview)
        scrollbar.grid(row=10, column=6, sticky="ns")

        self.mostrar_inventario()
        self.my_tree.tag_configure('orow', background="#EEEEEE", font=('Arial bold',15))
        self.my_tree.grid(row=10, column=2, columnspan=5, padx=10, pady=10)

        self.my_tree.heading("Nombre", text="Nombre", anchor = tk.W, command = lambda: 
                             self.organizar_nombres(self.my_tree, "Nombre", False))

        # Guardar inventario y ganancias del mes al cerrar la aplicación
        root.protocol("WM_DELETE_WINDOW", self.guardar_inventario_y_ganancias_mes_al_cerrar)

    #def eliminar_item(self):

    def organizar_nombres(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse = reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        
        tv.heading(col, command = lambda: self.organizar_nombres(tv, col, not reverse))
        
    def limpiar_registro_mes(self):
        self.ganancias_mes_actual = 0
        self.lbl_ganancias_mes_actual.config(text=f"Ganancias del mes actual: {locale.currency(int(self.ganancias_mes_actual), grouping=True, symbol=False)}")
        self.guardar_ganancias_mes()

    def cargar_ganancias_mes(self):
        try:
            with open("ganancias_mes.json", "r") as file:
                ganancias_mes = json.load(file)
            return ganancias_mes.get("ganancias_mes_actual", 0)
        except FileNotFoundError:
            return 0
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al cargar las ganancias del mes desde el archivo.")
            return 0

    def guardar_ganancias_mes(self):
        try:
            with open("ganancias_mes.json", "w") as file:
                json.dump({"ganancias_mes_actual": self.ganancias_mes_actual}, file)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar las ganancias del mes: {str(e)}")

    def actualizar_precios(self, event):
        producto_seleccionado = self.producto_var.get()
        if producto_seleccionado in self.inventario:
            precio_compra = self.inventario[producto_seleccionado]["precio_compra"]
            precio_venta = self.inventario[producto_seleccionado]["precio_venta"]
            self.precio_compra_var.set(locale.currency(int(precio_compra), grouping=True))
            self.precio_venta_var.set(locale.currency(int(precio_venta), grouping=True))
        
        self.mostrar_inventario()
            
    def registrar_venta(self):
        producto1 = self.producto_venta1_var.get()
        producto2 = self.producto_venta2_var.get()
        producto3 = self.producto_venta3_var.get()
        producto4 = self.producto_venta4_var.get()

        total_valor_producto1 = total_compra_producto1 = 0
        total_valor_producto2 = total_compra_producto2 = 0
        total_valor_producto3 = total_compra_producto3 = 0
        total_valor_producto4 = total_compra_producto4 = 0

        try:
            venta1 = int(self.entry_cantidad_venta1.get())

        except ValueError:
            venta1 = 0
        
        try:
            venta2 = int(self.entry_cantidad_venta2.get())

        except ValueError:
            venta2 = 0
        
        try:
            venta3 = int(self.entry_cantidad_venta3.get())

        except ValueError:
            venta3 = 0
        
        try:
            venta4 = int(self.entry_cantidad_venta4.get())

        except ValueError:
            venta4 = 0
        
        if producto1 not in self.inventario:
            producto1 = ""
            stock1 = -100
        else:
            stock1 = self.inventario[producto1]["stock"]


        if producto2 not in self.inventario:
            producto2 = ""
            stock2 = -100
        else:
            stock2 = self.inventario[producto2]["stock"]

        if producto3 not in self.inventario:
            producto3 = ""
            stock3 = -100
        else:
            stock3 = self.inventario[producto3]["stock"]
        
        if producto4 not in self.inventario:
            producto4 = ""
            stock4 = -100
        else:
            stock4 = self.inventario[producto4]["stock"]

        if venta1 >= stock1 and stock1 != -100:
                messagebox.showerror("Error", f"No hay suficientes unidades de {producto1} en el inventario.")
                return
        
        if stock1 == -100:
            total_valor_producto1 = 0
            total_compra_producto1 = 0
        else:
            valor_producto1 = float(self.inventario[producto1]["precio_venta"])
            compra_producto1 = float(self.inventario[producto1]["precio_compra"])
            total_compra_producto1 = compra_producto1 * venta1
            total_valor_producto1 = valor_producto1 * venta1

        if venta2 >= stock2 and stock2 != -100 :
                messagebox.showerror("Error", f"No hay suficientes unidades de {producto2} en el inventario.")
                return
        if stock2 == -100:
            total_valor_producto2 = 0
            total_compra_producto2 = 0
        else:
            valor_producto2 = float(self.inventario[producto2]["precio_venta"])
            compra_producto2 = float(self.inventario[producto2]["precio_compra"])
            total_compra_producto2 = compra_producto2 * venta2
            total_valor_producto2 = valor_producto2 * venta2
        
        if venta3 >= stock3 and stock3 != -100:
                messagebox.showerror("Error", f"No hay suficientes unidades de {producto3} en el inventario.")
                return
        if stock2 == -100:
            total_valor_producto2 = 0
            total_compra_producto2 = 0
        else:
            valor_producto3 = float(self.inventario[producto3]["precio_venta"])
            compra_producto3 = float(self.inventario[producto3]["precio_compra"])
            total_compra_producto3 = compra_producto3 * venta3
            total_valor_producto3 = valor_producto3 * venta3
        
        if venta4 >= stock4 and stock4 != -100:
                messagebox.showerror("Error", f"No hay suficientes unidades de {producto4} en el inventario.")
                return
        if stock4 == -100:
            total_valor_producto4 = 0
            total_compra_producto4 = 0
        else:
            valor_producto4 = float(self.inventario[producto4]["precio_venta"])
            compra_producto4 = float(self.inventario[producto4]["precio_compra"])
            total_compra_producto4 = compra_producto4 * venta4
            total_valor_producto4 = valor_producto4 * venta4
        
        ingresos_totales_total = total_valor_producto1 + total_valor_producto2 + total_valor_producto3 + total_valor_producto4
        costos_total = total_compra_producto1 +  total_compra_producto2 +  total_compra_producto3 +  total_compra_producto4

        ganancia_total = ingresos_totales_total - costos_total

        ganancias_venta = ganancia_total

        self.ganancias_mes_actual += ganancias_venta

        # Actualizar etiqueta de ganancias del mes actual con formato de moneda colombiana
        self.lbl_ganancias_mes_actual.config(text=f"Ganancias del mes actual: {locale.currency(int(self.ganancias_mes_actual), grouping=True, symbol=False)}")
        messagebox.showinfo("Venta Registrada", f"Cobrar : {locale.currency(int(ingresos_totales_total), grouping=True, symbol=False)}")
                
        self.mostrar_inventario()

    def agregar_stock(self):
        producto = self.producto_var.get()
        cantidad_stock = self.cantidad_stock_var.get()

        try:
            cantidad_stock = int(cantidad_stock)
            if cantidad_stock <= 0:
                raise ValueError("La cantidad de stock debe ser un número positivo.")
        except ValueError as e:
            messagebox.showerror("Error", f"Error en la cantidad de stock: {str(e)}")
            return

        if producto in self.inventario:
            self.inventario[producto]["stock"] += cantidad_stock
            messagebox.showinfo("Stock Actualizado", f"Se agregaron {cantidad_stock} unidades de {producto} al stock.")
        else:
            messagebox.showerror("Error", "Producto no encontrado en el inventario.")
        
        self.mostrar_inventario()

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
        
        self.mostrar_inventario()

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
        self.mostrar_inventario()

    def guardar_inventario_y_ganancias_mes_al_cerrar(self):
        self.guardar_inventario()
        self.guardar_ganancias_mes()
        self.root.destroy()

    def mostrar_inventario(self):
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

        producto_seleccionado = self.producto_var.get()
        for producto_seleccionado in self.inventario:
            precio_venta = self.inventario[producto_seleccionado]["precio_venta"]
            stock = self.inventario[producto_seleccionado]["stock"]

            self.my_tree.insert("", "end", values=(producto_seleccionado, locale.currency(int(precio_venta), grouping=True, symbol=False), stock), tags=('orow'))
    
if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioBarApp(root)
    root.mainloop()