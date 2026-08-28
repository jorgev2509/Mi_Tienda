# Mi Tienda ERP / POS

Primera base funcional de un ERP de ventas con FastAPI, Vue 3 + Vuetify y PostgreSQL.

## Puesta en marcha

1. Copia `.env.example` como `.env` y cambia las claves para un entorno real.
2. Ejecuta `docker compose up --build`.
3. Abre http://localhost:5173. La documentación de la API queda en http://localhost:8000/docs.

Usuario inicial: `admin@mitienda.local`  
Contraseña inicial: `Admin123!`

## Incluido

- Usuarios, roles y permisos.
- Productos con costo, precio e impuesto.
- Inventario auditable mediante entradas, ajustes y salidas.
- POS con validación y descuento transaccional de existencias.
- Historial de ventas y movimientos.
- Migración inicial y datos de arranque.

## Próximos módulos sugeridos

Clientes y proveedores, cajas/turnos y medios de pago, compras, devoluciones, bodegas, facturación, catálogo de cuentas y asientos contables automáticos.

