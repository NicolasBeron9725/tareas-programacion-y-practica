const express = require("express");
const router = express.Router();
const authController = require("../controllers/auth.controller");
const authMiddleware = require("../middleware/auth.middleware");

// Ruta abierta: Para entrar al sistema
router.post("/login", authController.login);

// Ruta PROTEGIDA: Solo el Admin (vía Dashboard) puede registrar nuevos empleados
// Agregamos authMiddleware para que req.user esté disponible en el controlador
router.post("/register", authMiddleware, authController.register);

// Ruta de prueba para verificar el perfil
router.get("/perfil", authMiddleware, (req, res) => {
    res.json({ 
        message: "¡Entraste al área secreta!", 
        usuario: req.user 
    });
});

module.exports = router;