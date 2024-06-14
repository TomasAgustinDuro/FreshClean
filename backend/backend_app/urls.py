from django.urls import path
from backend_app import views

urlpatterns = [

    # Usuarios
    path('usuarios/registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('usuarios/iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('usuarios/obtener_usuario/<int:email>/', views.obtener_usuario, name='obtener_usuario'),   
    path('usuarios/cerrar_sesion', views.cerrar_sesion, name="cerrar_sesion"),
    path('usuarios/perfil/<str:email>/', views.informacion_usuario, name='perfil'),
    # path('usuarios/editar/<int:usuario_id>/', views.editar_perfil, name='editar_perfil'),

    # Productos
    # path('productos/', views.listar_productos, name='listar_productos'),
    path('admin/productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('admin/productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('admin/productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('productos/subcategoria/<int:subcategoria_id>/', views.productos_por_subcategoria, name='productos_por_subcategoria'),

    # Categorías y Subcategorías
    path('admin/categorias/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('categorias/', views.obtener_categorias, name="obtener_categorias"),
    path('categorias/<int:categoria_id>/', views.obtener_categorias, name="obtener_categoria_por_id"),
    path('categorias/<str:nombre>/', views.obtener_categorias, name="obtener_categoria_por_nombre"),
    # path('admin/subcategorias/agregar/', views.agregar_subcategoria, name='agregar_subcategoria'),
    path('subcategorias/', views.obtener_subcategorias, name="obtener_subcategorias"),

    # Pedidos
    path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),
    # path('pedidos/<int:pedido_id>/', views.ver_pedido, name='ver_pedido'),
    path('usuarios/<int:usuario_id>/pedidos/', views.listar_pedidos_usuario, name='listar_pedidos_usuario'),

    # Inventario
    path('inventario/', views.ver_inventario, name='ver_inventario'),

    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/vaciar/<int:usuarioid>/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/eliminar/<int:productoid>/<int:usuarioid>/', views.eliminar_producto, name='eliminar_producto'),
    path('carrito/agregar_unidad/<int:productoid>/', views.agregar_unidad, name='agregar_unidad'),
    path('carrito/quitar_unidad/<int:productoid>/', views.quitar_unidad, name='quitar_unidad'),
]
