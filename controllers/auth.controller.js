const pool = require("../config/db");
const jwt = require("jsonwebtoken");

// ==========================================
// FUNCIÓN AUXILIAR: Rastrear Actividad
// ==========================================
const registrarActividad = async (userId) => {
  try {
    await pool.query(
      "UPDATE usuarios SET ultima_conexion = CURRENT_TIMESTAMP WHERE id = $1",
      [userId]
    );
  } catch (error) {
    console.error("Error actualizando actividad:", error);
  }
};

// =======================
// REGISTER — Crear usuario
// =======================
exports.register = async (req, res) => {
  try {
    // Verificación de seguridad: Solo Admin
    if (req.user && req.user.rol !== 'admin') {
      return res.status(403).json({ error: "Solo el administrador puede crear usuarios" });
    }

    const { nombre_usuario, password, rol, empresa_id, empleado_id } = req.body;

    const result = await pool.query(
      `INSERT INTO usuarios (nombre_usuario, contrasena, rol, empresa_id, empleado_id)
       VALUES ($1, $2, $3, $4, $5)
       RETURNING id, nombre_usuario, rol`,
      [nombre_usuario, password, rol, empresa_id || 1, empleado_id]
    );

    res.status(201).json({
      message: "Usuario creado correctamente",
      user: result.rows[0]
    });

  } catch (error) {
    if (error.code === '23505') {
      return res.status(400).json({ error: "El nombre de usuario ya existe" });
    }
    res.status(500).json({ error: "Error al registrar usuario" });
  }
};

// =======================
// LOGIN — Iniciar sesión
// =======================
exports.login = async (req, res) => {
  try {
    const { nombre_usuario, contrasena } = req.body;

    const result = await pool.query(
      "SELECT * FROM usuarios WHERE nombre_usuario = $1",
      [nombre_usuario]
    );

    if (result.rows.length === 0) {
      return res.status(400).json({ error: "Usuario no encontrado" });
    }

    const user = result.rows[0];

    if (contrasena !== user.contrasena) {
      return res.status(400).json({ error: "Contraseña incorrecta" });
    }

    // Marcamos que acaba de entrar
    await registrarActividad(user.id);

    const token = jwt.sign(
      {
        id: user.id,
        nombre: user.nombre_usuario,
        rol: user.rol,
        empresa_id: user.empresa_id,
        empleado_id: user.empleado_id
      },
      process.env.JWT_SECRET || "secreto_de_respaldo",
      { expiresIn: "8h" }
    );

    res.json({
      message: "Login exitoso",
      token
    });

  } catch (error) {
    res.status(500).json({ error: "Error al iniciar sesión" });
  }
};

// ==========================================
// NUEVO: Perfil / Latido de conexión
// ==========================================
exports.perfil = async (req, res) => {
  try {
    // Cada vez que el dashboard pide el perfil, actualizamos su "Online"
    await registrarActividad(req.user.id);
    
    res.json({ 
      message: "Conexión activa", 
      usuario: req.user 
    });
  } catch (error) {
    res.status(500).json({ error: "Error de servidor" });
  }
};