const jwt = require("jsonwebtoken");

// Esta función es el "Guardia"
module.exports = (req, res, next) => {
  try {
    // 1. El cliente nos envía el Token en un apartado llamado 'Authorization'
    const authHeader = req.headers.authorization;

    // 2. Si el sobre no existe, el guardia no te deja pasar
    if (!authHeader) {
        return res.status(401).json({ error: "Acceso denegado. No hay token." });
    }

    // 3. El token suele venir como "Bearer [CÓDIGO]". Aquí le quitamos el "Bearer "
    const token = authHeader.split(" ")[1];

    // 4. Verificamos si el código es auténtico con nuestra clave secreta
    const verificado = jwt.verify(token, process.env.JWT_SECRET);
    
    // 5. Si es real, guardamos los datos del usuario en la petición (la mochila)
    req.user = verificado;

    // 6. ¡Todo en orden! El guardia te deja pasar a la siguiente función
    next();
  } catch (error) {
    // Si el token es falso o viejo (expirado), el guardia te rebota
    res.status(403).json({ error: "Token no válido o expirado" });
  }
};