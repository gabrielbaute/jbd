/**
 * Cliente de API generado dinámicamente según el entorno.
 */
import createClient from "openapi-fetch";
import type { paths } from "./schema";

// Vite expone las variables de entorno a través de import.meta.env
// Si VITE_API_URL está vacío (producción), el navegador usará la ruta relativa al host actual.
const apiBaseUrl = import.meta.env.VITE_API_URL || window.location.origin;

const client = createClient<paths>({ 
    baseUrl: apiBaseUrl 
});

export default client;