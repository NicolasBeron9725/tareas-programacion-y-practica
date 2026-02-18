require ("dotenv").config();
const clienteRoutes = require("./routes/cliente.routes");
const express = require("express");
const cors = require("cors");
require("dotenv").config();

const app = express();
const pool = require("./config/db");
const authRoutes = require("./routes/auth.routes");

app.use(cors());
app.use(express.json());
app.use("/api/auth", authRoutes);
app.use("/api/clientes", clienteRoutes);
app.get("/", async (req, res) => {
  try {
    const result = await pool.query("SELECT NOW()");
    res.json({
      message: "Servidor funcionando",
      databaseTime: result.rows[0],
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error de conexión a la base" });
  }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Servidor corriendo en puerto ${PORT}`);
});
