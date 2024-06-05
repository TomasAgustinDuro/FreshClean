from django.shortcuts import render

from .models import Categoria, Producto, Usuario,Subcategoria,Pedido, Inventario, Carrito

# Categorias y subcategorias

def agregar_categoria(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        Categoria.agregar_categoria(nombre, descripcion)
        # Redirige para ver las categorias
        return redirect('obtener_categorias') 
    
    return render(request, 'agregar_categoria.html')

def obtener_categorias(request, categoria_id=None, nombre=None):
    if categoria_id:
        categoria = Categoria.obtener_categoria_por_id(categoria_id)
        return render(request, 'listar_categorias.html', {'categoria_por_id': categoria})
    elif nombre:
        categorias = Categoria.obtener_categorias_por_nombre(nombre)
        return render(request, 'lista_categorias.html', {'categorias_por_nombre': categorias})
    else:
        categorias = Categoria.obtener_categorias()
        return render(request, 'listar_categorias.html', {'categorias': categorias})

def obtener_subcategorias(request):
    subcategorias = Subcategoria.obtener_categorias()
    return render(request, 'listar_subcategorias.html', {'subcategorias': subcategorias})

# Producto
def agregar_producto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        stock = request.POST['stock']
        subcategoria = request.POST['subcategoria']
        Producto.agregar_producto(nombre, descripcion, precio, stock, subcategoria)
        return redirect('obtener_productos')
    
    return render(request, 'agregar_producto.html')

def eliminar_producto(request, producto_id ):
    Producto.eliminar_producto(producto_id)
    return render(request, 'obtener_productos.html')

def editar_producto (request, producto_id):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        stock = request.POST['stock']
        subcategoria = request.POST['subcategoria']
        Producto.editar_producto(producto_id, nombre, descripcion, precio, stock, subcategoria)
        return redirect('obtener_productos')
    
    return render (request, 'obtener_productos.html')

def obtener_productos(request):
    productos = Producto.listar_productos()
    return render(request, 'listar_productos.html', {'productos': productos})

def obtener_unidad_producto(request, producto_id):
    producto = Producto.obtener_producto(producto_id)
    return render (request, 'listar_producto.html',{'producto': producto} )

def productos_por_categoria(request, categoria_id):
    productos = Producto.productos_por_categoria(categoria_id)
    return render (request, 'listar_producto.html', {'productos': productos})

def productos_por_subcategoria(request, subcategoria_id):
    productos = Producto.productos_por_subcategoria(subcategoria_id)
    return render (request, 'listar_producto.html', {'productos': productos})

# Usuario
def registrar_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        contrasenia = request.POST['contrasenia']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        Usuario.registrar_usuario(nombre, apellido, email, contrasenia, direccion, telefono)
        return redirect('obtener_usuarios')
    
    return render(request, 'register')

def obtener_usuarios(request):
    usuarios = Usuario.listar_usuarios()
    return render (request, 'usuarios.html', {'usuarios': usuarios})

def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST['email']
        contrasenia = request.POST['contrasenia']
        Usuario.iniciar_sesion(email, contrasenia)
        return redirect('informacion_usuario')
    
    return render(request, 'informacion_usuario.html')

def informacion_usuario(request, usuario_id):
    usuario = Usuario.mostrar_informacion(usuario_id)
    return render (request, 'informacion_usuario.html', {'usuario': usuario})

def actualizar_perfil(request, usuario_id):
    usuario = Usuario.objects.get(pk=usuario_id)
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        contrasenia = request.POST['contrasenia']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        Usuario.actualizar_perfil(usuario_id, nombre, apellido, email, contrasenia, direccion, telefono)
        return redirect('mostrar_informacion_usuario', usuario_id=usuario_id)
    
    return render(request, 'informacion_usuario.html', {'usuario': usuario})

# Pedidos
def crear_pedido(request):
    if request.method == 'POST':
        metodo_de_pago = request.POST['metodo_de_pago']
        observaciones = request.POST['observaciones']

        Pedido.crear_pedido(metodo_de_pago, observaciones)
        return redirect ('obtener_pedido')
    
    return render (request, 'obtener_pedido.html')

def obtener_pedido(request):
    pedido = Pedido.obtener_pedido(pedido_id)
    return render (request, 'pedido.html', {'pedido': pedido})

def listar_pedidos_usuario(request, usuarioid):
    pedidos = Pedido.listar_pedidos_usuario(usuarioid)
    return render (request, 'lista_pedidos_usuarios.html', {'pedidos': pedidos})

# Inventario
def ver_inventario(request):
    inventario = Inventario.listar_inventario()
    return render (request, 'inventario.html', {'inventario': inventario})


# Carrito 
def ver_carrito(request):
    usuario_id = request.user.id
    carrito = Carrito.objects.filter(usuarioid=usuario_id).first()

    if carrito:
        detalles_carrito = carrito.detalle_carrito()
        total_carrito = sum(detalle['total_por_producto'] for detalle in detalles_carrito)
    else:
        detalles_carrito = []
        total_carrito = 0

    return render(request, 'ver_carrito.html', {'detalles_carrito': detalles_carrito, 'total_carrito': total_carrito})

def agregar_al_carrito(request, productoid, usuarioid, cantidad):
    if request.method == 'POST':
        cantidad = request.POST['cantidad']
        Carrito.agregar_articulo (productoid, usuarioid, cantidad)
        return redirect('carrito.html')
    
    return render (request, 'carrito.html')

def vaciar_carrito(request, usuarioid):
    Carrito.vaciar_carrito(usuarioid)
    return render (request, 'carrito.html')

def eliminar_producto(request, productoid, usuarioid):
    Carrito.eliminar_articulo(productoid, usuarioid)
    return render (request, 'carrito.html')

def agregar_unidad (request, productoid):
    Carrito.agregar_unidad(productoid)
    return render (request, 'carrito.html')

def quitar_unidad (request, productoid):
    Carrito.quitar_unidad(productoid)
    return render (request, 'carrito.html')

