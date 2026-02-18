const express = require("express");
const router = express.Router();
const pool = require("../config/db");
const authMiddleware = require("../middleware/auth.middleware");

// ==========================================
// 1. GESTIÓN DE CLIENTES Y ASIGNACIÓN
// ==========================================

router.get("/lista", authMiddleware, async (req, res) => {
    try {
        const resultado = await pool.query("SELECT * FROM clientes ORDER BY id DESC");
        res.json(resultado.rows);
    } catch (error) { res.status(500).json({ error: "Error al obtener clientes" }); }
});

router.post("/crear", authMiddleware, async (req, res) => {
    const { nombre, telefono, email } = req.body;
    try {
        await pool.query("INSERT INTO clientes (nombre, telefono, email, empresa_id) VALUES ($1, $2, $3, 1)", [nombre, telefono, email]);
        res.json({ message: "Cliente creado con éxito" });
    } catch (error) { res.status(500).json({ error: "Error al crear cliente" }); }
});

// IMPORTACIÓN MASIVA + REPARTO AUTOMÁTICO
router.post("/importar-masivo", authMiddleware, async (req, res) => {
    if (req.user.rol === 'vendedor') return res.status(403).json({ error: "No autorizado" });
    const { clientes } = req.body;
    if (!clientes || clientes.length === 0) return res.status(400).json({ error: "No hay datos" });

    const client = await pool.connect();
    try {
        await client.query('BEGIN');
        for (let c of clientes) {
            await client.query(
                "INSERT INTO clientes (nombre, telefono, email, empresa_id, estado) VALUES ($1, $2, $3, 1, 'NUEVO')",
                [c.nombre, c.telefono, c.email]
            );
        }
        const vendedores = await client.query("SELECT id FROM usuarios WHERE rol = 'vendedor'");
        const sinAsignar = await client.query("SELECT id FROM clientes WHERE asignado_a IS NULL");

        if (vendedores.rows.length > 0 && sinAsignar.rows.length > 0) {
            let vIndex = 0;
            for (let cRow of sinAsignar.rows) {
                await client.query("UPDATE clientes SET asignado_a = $1 WHERE id = $2", [vendedores.rows[vIndex].id, cRow.id]);
                vIndex = (vIndex + 1) % vendedores.rows.length;
            }
        }
        await client.query('COMMIT');
        res.json({ message: `¡Éxito! ${clientes.length} clientes importados y repartidos.` });
    } catch (error) {
        await client.query('ROLLBACK');
        res.status(500).json({ error: "Error en la carga masiva" });
    } finally { client.release(); }
});

router.put("/editar/:id", authMiddleware, async (req, res) => {
    const { id } = req.params;
    const { nombre, telefono, email } = req.body;
    if (req.user.rol === 'vendedor') return res.status(403).json({ error: "No autorizado" });
    try {
        await pool.query("UPDATE clientes SET nombre = $1, telefono = $2, email = $3 WHERE id = $4", [nombre, telefono, email, id]);
        res.json({ message: "Cliente actualizado" });
    } catch (error) { res.status(500).json({ error: "Error al actualizar" }); }
});

router.delete("/eliminar/:id", authMiddleware, async (req, res) => {
    try {
        await pool.query("DELETE FROM clientes WHERE id = $1", [req.params.id]);
        res.json({ message: "Cliente eliminado" });
    } catch (error) { res.status(500).json({ error: "Error de integridad" }); }
});

// ==========================================
// 2. AUTOMATIZACIÓN Y MONITOREO
// ==========================================

router.post("/reparto-automatico", authMiddleware, async (req, res) => {
    if (req.user.rol === 'vendedor') return res.status(403).json({ error: "No autorizado" });
    try {
        const vendedores = await pool.query("SELECT id FROM usuarios WHERE rol = 'vendedor'");
        const clientesSinAsignar = await pool.query("SELECT id FROM clientes WHERE asignado_a IS NULL");
        if (vendedores.rows.length === 0 || clientesSinAsignar.rows.length === 0) return res.json({ message: "Sin cambios" });

        let vIndex = 0;
        for (let cliente of clientesSinAsignar.rows) {
            await pool.query("UPDATE clientes SET asignado_a = $1 WHERE id = $2", [vendedores.rows[vIndex].id, cliente.id]);
            vIndex = (vIndex + 1) % vendedores.rows.length;
        }
        res.json({ message: "Reparto completado" });
    } catch (error) { res.status(500).json({ error: error.message }); }
});

router.post("/reciclar-base", authMiddleware, async (req, res) => {
    if (req.user.rol === 'vendedor') return res.status(403).json({ error: "No autorizado" });
    try {
        const result = await pool.query(`
            UPDATE clientes SET asignado_a = NULL, estado = 'NUEVO' 
            WHERE (estado = 'LLAMADO' OR estado = 'NO CONTESTA') AND ultima_gestion < NOW() - INTERVAL '48 hours'
        `);
        res.json({ message: `Se liberaron ${result.rowCount} clientes.` });
    } catch (error) { res.status(500).json({ error: error.message }); }
});

router.get("/status-vendedores", authMiddleware, async (req, res) => {
    try {
        const result = await pool.query(`
            SELECT u.nombre_usuario, u.ultima_conexion,
            (SELECT COUNT(*) FROM llamadas l WHERE l.empleado_id = u.id AND l.fecha::date = CURRENT_DATE) as llamadas_hoy
            FROM usuarios u WHERE u.rol = 'vendedor' ORDER BY u.ultima_conexion DESC
        `);
        res.json(result.rows);
    } catch (error) { res.status(500).json({ error: error.message }); }
});

// ==========================================
// 3. LLAMADAS, VENTAS Y AVISOS
// ==========================================

router.post("/llamada", authMiddleware, async (req, res) => {
    const { cliente_id, nota, nuevo_estado } = req.body;
    try {
        await pool.query("INSERT INTO llamadas (cliente_id, empleado_id, nota) VALUES ($1, $2, $3)", [cliente_id, req.user.id, nota]);
        await pool.query("UPDATE clientes SET estado = $1, ultima_gestion = CURRENT_TIMESTAMP WHERE id = $2", [nuevo_estado || 'LLAMADO', cliente_id]);
        res.json({ message: "Gestión guardada" });
    } catch (error) { res.status(500).json({ error: error.message }); }
});

router.post("/venta", authMiddleware, async (req, res) => {
    const { cliente_id, monto } = req.body;
    try {
        await pool.query("INSERT INTO ventas (cliente_id, empleado_id, monto, estado) VALUES ($1, $2, $3, 'Completado')", [cliente_id, req.user.id, monto]);
        await pool.query("UPDATE clientes SET estado = 'VENTA', ultima_gestion = CURRENT_TIMESTAMP WHERE id = $1", [cliente_id]);
        res.json({ message: "¡Venta exitosa!" });
    } catch (error) { res.status(500).json({ error: "Error al registrar venta" }); }
});

// ==========================================
// 4. NUEVO: MÓDULO DE ANALÍTICA (ADMIN)
// ==========================================

router.get("/stats-admin", authMiddleware, async (req, res) => {
    if (req.user.rol === 'vendedor') return res.status(403).json({ error: "Acceso denegado" });
    try {
        // 1. Ranking de Vendedores
        const ranking = await pool.query(`
            SELECT u.nombre_usuario, COUNT(v.id) as total_ventas, COALESCE(SUM(v.monto), 0) as monto_total
            FROM usuarios u
            LEFT JOIN ventas v ON u.id = v.empleado_id
            WHERE u.rol = 'vendedor'
            GROUP BY u.nombre_usuario
            ORDER BY monto_total DESC
        `);

        // 2. Estado del Embudo
        const funnel = await pool.query(`
            SELECT estado, COUNT(*) as cantidad FROM clientes GROUP BY estado
        `);

        // 3. Globales Rápidos
        const globales = await pool.query(`
            SELECT COUNT(*) as total_ventas, COALESCE(SUM(monto), 0) as facturacion FROM ventas
        `);

        res.json({
            ranking: ranking.rows,
            funnel: funnel.rows,
            globales: globales.rows[0]
        });
    } catch (error) { res.status(500).json({ error: "Error en estadísticas" }); }
});

module.exports = router;