---
layout: default
title: PAELLA DOC - Español
permalink: /es/
redirect_from:
  - /es
  - /es/index.html
  - /es/home
---

# Bienvenido a PAELLA DOC

[English version](/en/)

<div class="language-selector">
  <a href="{{ site.baseurl }}/es/" class="active">Español</a>
  <a href="{{ site.baseurl }}/en/">English</a>
</div>

<div class="hero">
  <h1>PAELLA DOC</h1>
  <p class="tagline">Documentación con el sabor de la innovación</p>
</div>

<div class="projects-section">
  <h2>Proyectos</h2>
  
  <div class="project-card">
    <h3>paellaSEO</h3>
    <p>Extensión de Chrome para análisis SEO en tiempo real. Un ejemplo completo de documentación técnica.</p>
    <div class="project-links">
      <a href="/es/projects/paellaSEO/00_index.html" class="primary-link">Documentación Principal</a>
      <a href="/es/projects/paellaSEO/feature_documentation.html">Funcionalidades</a>
      <a href="/es/projects/paellaSEO/quick_task_documentation.html">Tareas</a>
      <a href="/es/projects/paellaSEO/bug_documentation.html">Errores</a>
    </div>
  </div>
</div>

<main>
  <article class="content">
    <div class="card fade-in">
      <h1>¿Qué es PAELLA DOC?</h1>
      <p>PAELLA DOC es un sistema de documentación interactivo impulsado por IA que hace que documentar sea tan satisfactorio como preparar una buena paella valenciana. Cada ingrediente (componente) tiene su momento y lugar, creando una documentación perfectamente equilibrada.</p>
    </div>

    <div class="card fade-in">
      <h2>Características Principales</h2>
      <div class="feature-grid">
        <div class="feature">
          <h3>🤖 Impulsado por IA</h3>
          <p>Generación inteligente de documentación que se adapta a tus necesidades.</p>
        </div>
        <div class="feature">
          <h3>🌟 Interactivo</h3>
          <p>Sistema de chat natural para crear y mantener tu documentación.</p>
        </div>
        <div class="feature">
          <h3>📚 Completo</h3>
          <p>Cubre todos los aspectos de tu proyecto, desde la arquitectura hasta la implementación.</p>
        </div>
        <div class="feature">
          <h3>🔄 Adaptable</h3>
          <p>Se ajusta a diferentes tipos de proyectos y metodologías.</p>
        </div>
      </div>
    </div>

    <div class="card fade-in">
      <h2>Empezar es Fácil</h2>
      <div class="quick-start">
        <pre><code>PAELLA mi-proyecto</code></pre>
        <p>Con un simple comando, comienza tu viaje de documentación.</p>
        <a href="{{ '/es/docs/inicio-rapido' | relative_url }}" class="button">Guía Rápida →</a>
      </div>
    </div>

    <div class="card fade-in">
      <h2>¿Por qué PAELLA DOC?</h2>
      <table>
        <tr>
          <th>Característica</th>
          <th>Beneficio</th>
        </tr>
        <tr>
          <td>Generación por IA</td>
          <td>Documentación consistente y profesional sin esfuerzo</td>
        </tr>
        <tr>
          <td>Interacción Natural</td>
          <td>Sin necesidad de aprender sintaxis compleja</td>
        </tr>
        <tr>
          <td>Plantillas Inteligentes</td>
          <td>Estructura probada para diferentes tipos de proyectos</td>
        </tr>
        <tr>
          <td>Integración con Cursor</td>
          <td>Perfecta integración con tu flujo de desarrollo</td>
        </tr>
      </table>
    </div>
  </article>
</main>

<style>
.language-selector {
  text-align: right;
  padding: 1rem;
}

.language-selector a {
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
  text-decoration: none;
  border-radius: 4px;
  color: var(--text-color, #1E1E24);
  border: 1px solid var(--border-color, #e1e4e8);
}

.language-selector a.active {
  background: var(--primary-color, #FFB800);
  color: white;
  border-color: var(--primary-color, #FFB800);
}

.hero {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #FFB800 0%, #CD9B1D 100%);
  color: white;
  margin-bottom: 3rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.hero h1 {
  font-size: 3rem;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.tagline {
  font-size: 1.5rem;
  margin-top: 1rem;
  opacity: 0.9;
}

.projects-section {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 2rem;
}

.project-card {
  background: var(--background-color, #ffffff);
  border: 1px solid var(--border-color, #e1e4e8);
  border-radius: 8px;
  padding: 2rem;
  margin: 2rem 0;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.project-card h3 {
  color: var(--primary-color, #FFB800);
  margin-top: 0;
}

.project-links {
  margin-top: 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.project-links a {
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.2s ease-in-out;
}

.primary-link {
  background: var(--primary-color, #FFB800);
  color: white;
}

.primary-link:hover {
  background: var(--secondary-color, #CD9B1D);
}

.project-links a:not(.primary-link) {
  border: 1px solid var(--border-color, #e1e4e8);
  color: var(--text-color, #1E1E24);
}

.project-links a:not(.primary-link):hover {
  background: var(--background-color, #f6f8fa);
  border-color: var(--primary-color, #FFB800);
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.feature {
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.feature:hover {
  transform: translateY(-4px);
}

.quick-start {
  text-align: center;
  padding: 2rem 0;
}

.quick-start pre {
  background: var(--code-bg);
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  overflow-x: auto;
}

.quick-start .button {
  display: inline-block;
  margin-top: 1rem;
}
</style>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "PAELLA DOC",
  "description": "Sistema de documentación interactivo impulsado por IA que hace que documentar sea tan satisfactorio como preparar una buena paella valenciana.",
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "All",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "author": {
    "@type": "Organization",
    "name": "PAELLA DOC Team",
    "url": "https://github.com/jlcases/paelladoc"
  },
  "inLanguage": "es",
  "availableLanguage": ["es", "en"]
}
</script>

{% include_relative projects/paellaSEO/00_index.md %} 