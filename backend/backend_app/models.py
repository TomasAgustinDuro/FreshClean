from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

class Usuario(models.Model):
    usuarioid = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    contrasenia = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)
    fecha_de_registro = models.DateTimeField(auto_now_add=True)

    @classmethod
    def registrar_usuario(cls, nombre, apellido, email, contrasenia, direccion, telefono):
        usuario = cls(
            nombre = nombre,
            apellido = apellido,
            email = email,
            contrasenia = make_password(contrasenia),
            direccion = direccion,
            telefono = telefono,
        )

        usuario.save()
        return usuario

    @classmethod
    def iniciar_sesion(cls, email, contrasenia):
        print(email)
        print(contrasenia)
        usuario = cls.objects.filter(email = email).first()
        
        print('este es el usuario' + str(usuario))

        if usuario and check_password(contrasenia, usuario.contrasenia):
            print('todo ok ')
            return usuario
        return None
    
    @classmethod
    def obtener_usuario(cls, usuario_id):
        return cls.objects.get(usuarioid=usuario_id)
    
    @classmethod
    def actualizar_perfil(cls, usuario_id, nombre, apellido, direccion, telefono):
        usuario = cls.objects.get(usuarioid=usuario_id)
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.direccion = direccion
        usuario.telefono = telefono
        usuario.save()
        return usuario
    
    @classmethod
    def listar_usuarios(cls):
        return cls.objects.all()
    
    @classmethod
    def mostrar_informacion(cls, usuario_id):
        usuario =  cls.objects.filter(usuarioid = usuario_id).first()
        return usuario
             
class Categoria(models.Model): 
    categoriaid = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=255)

    @classmethod
    def agregar_categoria(cls, nombre, descripcion):
        categoria = cls(
            nombre = nombre,
            descripcion = descripcion
        )

        categoria.save()
        return categoria
    
    @classmethod
    def obtener_categoria_por_id(cls, categoria_id):
        return cls.objects.get(categoriaid=categoria_id)

    @classmethod
    def obtener_categorias_por_nombre(cls, nombre):
        return cls.objects.filter(nombre=nombre)
    
    @classmethod
    def obtener_categorias(cls):
        return cls.objects.all()
    
class Subcategoria(models.Model):
    subcategoriaid = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=255)
    categoriaid = models.ForeignKey(Categoria, on_delete=models.CASCADE, to_field='categoriaid')

    @classmethod
    def agregar_subcategoria(cls, nombre, descripcion, categoria_id):
        categoria = Categoria.obtener_categoria_por_id(categoria_id)
        subcategoria = cls(
            nombre=nombre,
            descripcion=descripcion,
            categoriaid=categoria
        )

        subcategoria.save()
        return subcategoria


    @classmethod
    def obtener_subcategorias(cls):
        return cls.objects.all()
    
class Producto(models.Model):
    productoid = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=255)
    precio = models.FloatField()
    stock = models.IntegerField()
    subcategoriaid = models.ForeignKey(Subcategoria, on_delete=models.CASCADE, to_field='subcategoriaid')

    @classmethod
    def agregar_producto(cls, nombre, descripcion, precio, stock, subcategoria):
        producto= cls(
            nombre = nombre,
            descripcion = descripcion,
            precio = precio,
            stock = stock,
            subcategoria = subcategoria
        )

        producto.save()
        return producto
    
    @classmethod
    def eliminar_producto(cls, productoid):
        try:
            producto = cls.objects.get(productoid=productoid)
            producto.delete()
            return True  # Retorna True si se eliminó exitosamente
        except cls.DoesNotExist:
            return False  # Retorna False si el producto no existe
    
    @classmethod
    def editar_producto(cls, productoid, nombre, descripcion, precio, stock, subcategoria):
        try:
            producto = cls.objects.get(productoid=productoid)
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio = precio
            producto.stock = stock
            producto.subcategoriaid = subcategoria
            producto.save()
            return True  # Retorna True si se editó exitosamente
        except cls.DoesNotExist:
            return False  # Retorna False si el producto no existe
    @classmethod
    def listar_productos(cls):
        return cls.objects.all()

    @classmethod
    def obtener_producto(cls, producto_id):
        return cls.objects.get(productoid=producto_id)

    @classmethod
    def productos_por_categoria(cls, categoria_id):
        return cls.objects.filter(subcategoriaid__categoriaid=categoria_id)

    @classmethod
    def productos_por_subcategoria(cls, subcategoria_id):
        return cls.objects.filter(subcategoriaid=subcategoria_id)

class Pedido(models.Model):
    pedidoid = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField(auto_now_add=True)
    metodo_de_pago = models.CharField(max_length=45)
    estado = models.CharField(max_length=45)
    observaciones=models.CharField(max_length=285)
    total = models.FloatField()
    usuarioid = models.ForeignKey(Usuario, on_delete=models.CASCADE, to_field='usuarioid')

    @classmethod
    def crear_pedido(cls, fecha_pedido, metodo_de_pago, observaciones):
        # busca los productos que aun no tengan pedido asignado
       detalles_pedido = DetallePedido.objects.filter(pedidoid=None)
        # suma dichos productos.     
       total = sum(detalle.calcular_total() for detalle in detalles_pedido)

       pedido = cls(
            fecha_pedido = fecha_pedido,
            metodo_de_pago=metodo_de_pago,
            estado= 'En proceso',
            observaciones = observaciones,
            total=total
       )
       
       pedido.save()
       return pedido
    
    def procesar_pedido(self):
        detalles_pedido = DetallePedido.objects.filter(pedidoid=self.pedidoid)
        for detalle in detalles_pedido:
             detalle.actualizar_inventario()


        asunto = 'Su pedido ha sido procesado'
        mensaje = 'Estimado cliente, su pedido ha sido procesado y esta en camino'
        remitente = 'micorreo@gmail.com'
        destinatario = self.usuarioid.email
        
        sendemail(asunto, mensaje, remitente, destinatario)

    @classmethod
    def obtener_pedido(cls, pedido_id):
        return cls.objects.get(pedidoid=pedido_id)

    @classmethod
    def listar_pedidos_usuario(cls, usuario_id):
        return cls.objects.filter(usuarioid=usuario_id)
    
class DetallePedido(models.Model):
    detalle_pedidoid = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()
    pedidoid = models.ForeignKey(Pedido, on_delete=models.CASCADE, to_field='pedidoid')
    productoid = models.ForeignKey(Producto, on_delete=models.CASCADE, to_field='productoid')

    def calcular_total(self):
        total = self.precio_unitario * self.cantidad
        return total

    def actualizar_inventario(self):
        producto = self.productoid
        producto.stock -= self.cantidad
        producto.save()
        return producto
   
class Inventario(models.Model):
    inventarioid = models.AutoField(primary_key=True)
    cantidad_actual = models.IntegerField()
    cantidad_minima = models.IntegerField()
    fecha_ultima_actualizacion = models.DateField(auto_now_add=True)
    productoid = models.ForeignKey(Producto, on_delete=models.CASCADE, to_field='productoid')

    @classmethod
    def listar_inventario(cls):
        return cls.objects.all()

class Pago(models.Model):
    pagoid = models.AutoField(primary_key=True)
    pedidoid = models.ForeignKey(Pedido, on_delete=models.CASCADE, to_field='pedidoid')
    usuarioid = models.ForeignKey(Usuario, on_delete=models.CASCADE, to_field='usuarioid')
    fecha_pago = models.DateField(auto_now_add=True)
    monto = models.FloatField()
    metodo_pago = models.CharField(max_length=45)

    def procesar_pago(self):
        # cambio de estado del pedido
        self.pedidoid.estado = 'Pagado'
        self.save()

        Transacciones.registrar_transaccion(
            pagoid= self,
            monto = self.monto,
            metodo_pago= self.metodo_pago,
            estado = self.pedidoid.estado
        )

        self.save()

        # notificacion via email del pago
        asunto = 'Su pago ha sido realizado'
        mensaje = 'Estimado cliente, su pago ha sido procesado y esta en camino'
        remitente = 'micorreo@gmail.com'
        destinatario = self.usuarioid.email
        
        sendemail(asunto, mensaje, remitente, destinatario)

    def metodo_pago(self):
    # Realizar alguna manipulación o validación del método de pago aquí
        metodo_pago = self.metodo_pago
    # Por ejemplo, formatear el método de pago en mayúsculas antes de devolverlo
        return metodo_pago.upper()
 
class Transacciones(models.Model):
    transaccionesid = models.AutoField(primary_key=True)
    pagoid = models.ForeignKey(Pago, on_delete=models.CASCADE, to_field='pagoid')
    monto = models.FloatField()
    fecha_y_hora = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=45)    
    metodo_pago = models.CharField(max_length=45)

    @classmethod
    def registrar_transaccion(cls, pagoid, monto, estado, metodo_pago):
        transacccion = cls(
            pagoid = pagoid,
            monto = monto,
            estado = estado,
            metodo_pago = metodo_pago
        )

        transacccion.save()
        return transacccion

class Carrito(models.Model):
    carritoid = models.AutoField(primary_key=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    usuarioid = models.ForeignKey(Usuario, on_delete=models.CASCADE, to_field='usuarioid')
    productoid = models.ForeignKey(Producto, on_delete=models.CASCADE, to_field='productoid')

    @classmethod
    def agregar_articulo(cls, usuarioid, productoid, cantidad):
        carrito, created = cls.objects.get_or_create(
            usuarioid= usuarioid,
            productoid= productoid,
        )
        if not created:
            # Si el artículo ya está en el carrito, incrementar la cantidad
            carrito.cantidad += cantidad
        else:
            carrito.cantidad = cantidad
        carrito.save()
        return carrito

    @classmethod
    def vaciar_carrito(cls, usuarioid):
        # Filtra dentro de los cls creados por cual tiene el usuario pasado y si hay coincidencia, lo borra
        cls.objects.filter(usuarioid=usuarioid).delete()

    @classmethod
    def eliminar_articulo(cls, usuarioid, productoid):
         # Filtra dentro de los cls creados por cual tiene el usuario pasado y el producto y si hay coincidencia, lo borra
        cls.objects.filter(usuarioid=usuarioid, productoid=productoid).delete()

    def agregar_unidad(self, productoid):
        detalle, created = DetalleCarrito.objects.get_or_create(carrito=self, productoid=productoid)
        if not created:
            detalle.cantidad += 1
            detalle.save()
        return detalle

    def quitar_unidad(self, productoid):
        try:
            detalle = DetalleCarrito.objects.get(carrito=self, productoid=productoid)
            if detalle.cantidad > 1:
                detalle.cantidad -= 1
                detalle.save()
            else:
                detalle.delete()
            return detalle
        except DetalleCarrito.DoesNotExist:
            return None
    
    def detalle_carrito(self):
        detalles = DetalleCarrito.objects.filter(carrito=self)
        lista_detalle = []

        for detalle in detalles:
            producto = detalle.productoid
            total_por_producto = detalle.calcular_total()
            lista_detalle.append({
                'nombre': producto.nombre,
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precio_unitario,
                'total_por_producto': total_por_producto
            })

        return lista_detalle
    
class DetalleCarrito(models.Model):
    detalle_carritoid = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, to_field='carritoid')
    productoid = models.ForeignKey(Producto, on_delete=models.CASCADE, to_field='productoid')

    def detalle(self): 
        self.precio_unitario = self.productoid.precio
        self.cantidad = self.carrito.cantidad

        if self.cantidad < 0:
            print('error')


    def calcular_total(self):
        return self.cantidad * self.precio_unitario