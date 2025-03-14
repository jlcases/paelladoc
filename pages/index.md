---
layout: default
title: PAELLA DOC - Documentación con Sabor
description: Sistema de documentación interactivo impulsado por IA que hace que documentar sea tan satisfactorio como preparar una buena paella valenciana.
---

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
      <a href="projects/paellaSEO/00_index.html" class="primary-link">Documentación Principal</a>
      <a href="projects/paellaSEO/feature_documentation.html">Funcionalidades</a>
      <a href="projects/paellaSEO/quick_task_documentation.html">Tareas</a>
      <a href="projects/paellaSEO/bug_documentation.html">Errores</a>
    </div>
  </div>
</div>

<style>
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
</style>

# Paella Doc

Welcome to the Paella Doc documentation site. This site provides comprehensive information about the Paella Doc system, an AI-powered interactive documentation generator.

## Overview

Paella Doc is an advanced documentation system that uses natural language conversations to create, maintain, and organize project documentation efficiently.

## Features

- Interactive chat-based documentation generation
- Template-based document creation
- Automatic market research
- Architecture Decision Records (ADR) management
- Documentation completeness tracking
- MDC file generation for Cursor integration

## Getting Started

To get started with Paella Doc, follow these steps:

1. Initialize a new documentation project using the `PAELLA` command
2. Continue working on specific documents with the `CONTINUE` command
3. Generate Cursor MDC files with the `GENERATE_MDC` command

## Documentation Structure

Paella Doc organizes documentation in a structured way, following MECE principles (Mutually Exclusive, Collectively Exhaustive).

---

For more information, explore the documentation sections above. 