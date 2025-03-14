---
layout: default
title: Proyectos PAELLA DOC
description: Colección de proyectos de ejemplo y documentación generada con PAELLA DOC
lang: es
---

<div class="projects-container">
  <h1>Proyectos de Ejemplo</h1>
  
  <div class="project-card">
    <h2>paellaSEO</h2>
    <p>Extensión de Chrome para análisis SEO en tiempo real. Un ejemplo completo de documentación técnica que incluye:</p>
    <ul>
      <li><a href="paellaSEO/00_index.html">Documentación Principal</a></li>
      <li><a href="paellaSEO/feature_documentation.html">Documentación de Funcionalidades</a></li>
      <li><a href="paellaSEO/quick_task_documentation.html">Tareas Rápidas</a></li>
      <li><a href="paellaSEO/bug_documentation.html">Registro de Errores</a></li>
    </ul>
  </div>
</div>

<style>
.projects-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.project-card {
  background: var(--background-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s ease-in-out;
}

.project-card:hover {
  transform: translateY(-2px);
}

.project-card h2 {
  color: var(--primary-color);
  margin-top: 0;
}

.project-card ul {
  list-style-type: none;
  padding-left: 0;
}

.project-card ul li {
  margin: 0.5rem 0;
}

.project-card ul li a {
  color: var(--link-color);
  text-decoration: none;
  display: inline-block;
  padding: 0.25rem 0;
  border-bottom: 2px solid transparent;
  transition: border-color 0.2s ease-in-out;
}

.project-card ul li a:hover {
  border-bottom-color: var(--link-color);
}
</style> 