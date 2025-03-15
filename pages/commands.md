---
layout: default
title: Comandos PAELLADOC
description: Guía completa de los comandos disponibles en PAELLADOC y cómo utilizarlos
---

<div class="commands-container">
  <div class="commands-header">
    <div class="paella-icon">🥘</div>
    <h1>Comandos PAELLADOC</h1>
    <p class="commands-intro">PAELLADOC ofrece una serie de comandos potentes para gestionar tu documentación de forma interactiva. Aquí encontrarás todos los comandos disponibles y cómo utilizarlos.</p>
  </div>

  <div class="commands-content">
    <section class="command-section">
      <h2>Comandos Principales</h2>
      
      <div class="command-card">
        <div class="command-name">PAELLA</div>
        <div class="command-description">
          <p>Inicia el proceso de documentación y genera las reglas de Cursor.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>PAELLA nombre_proyecto</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>nombre_proyecto</code> - Nombre del proyecto a documentar (requerido)</li>
              <li><code>generate_rules</code> - Si se deben generar reglas de Cursor desde la documentación (por defecto: true)</li>
              <li><code>ai_mode</code> - Modo de operación de la IA: "autonomous", "collaborative", o "advisory" (por defecto: "collaborative")</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>PAELLA mi_proyecto</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">CONTINUE</div>
        <div class="command-description">
          <p>Continúa con la documentación de un proyecto existente.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>CONTINUE nombre_proyecto</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>nombre_proyecto</code> - Nombre del proyecto a continuar (requerido)</li>
              <li><code>update_rules</code> - Si se deben actualizar las reglas de Cursor desde la documentación (por defecto: true)</li>
              <li><code>sync_templates</code> - Si se deben sincronizar las plantillas con el estado actual (por defecto: true)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>CONTINUE mi_proyecto</code>
          </div>
        </div>
      </div>
    </section>

    <section class="command-section">
      <h2>Comandos de Gestión de Proyectos</h2>
      
      <div class="command-card">
        <div class="command-name">ACHIEVEMENT</div>
        <div class="command-description">
          <p>Registra un logro en la memoria del proyecto.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>ACHIEVEMENT "descripción" categoría [nivel_impacto]</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>descripción</code> - Descripción del logro (requerido)</li>
              <li><code>categoría</code> - Categoría del logro: "architecture", "development", "documentation", "testing", "security", "performance", "product", "design", "research" (requerido)</li>
              <li><code>nivel_impacto</code> - Nivel de impacto: "high", "medium", "low" (por defecto: "medium")</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>ACHIEVEMENT "Implementación de autenticación segura" security high</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">ISSUE</div>
        <div class="command-description">
          <p>Registra un problema en la memoria del proyecto.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>ISSUE "descripción" severidad área</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>descripción</code> - Descripción del problema (requerido)</li>
              <li><code>severidad</code> - Nivel de severidad: "critical", "high", "medium", "low" (requerido)</li>
              <li><code>área</code> - Área afectada: "product", "technical", "process", "security", "performance" (requerido)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>ISSUE "Fallo en la validación de entrada" high security</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">DECISION</div>
        <div class="command-description">
          <p>Registra una decisión técnica en la memoria del proyecto.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>DECISION "descripción" impacto "razonamiento"</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>descripción</code> - Descripción de la decisión (requerido)</li>
              <li><code>impacto</code> - Áreas impactadas: ["architecture", "development", "documentation", "testing", "security", "performance", "product", "design", "process"] (requerido)</li>
              <li><code>razonamiento</code> - Razonamiento detrás de la decisión (requerido)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>DECISION "Usar arquitectura microservicios" ["architecture", "development"] "Mejora la escalabilidad y mantenibilidad"</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">MEMORY</div>
        <div class="command-description">
          <p>Muestra el registro de desarrollo.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>MEMORY [filtro] [formato]</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>filtro</code> - Filtrar memoria por categoría: "all", "achievements", "issues", "decisions", "product", "technical" (por defecto: "all")</li>
              <li><code>formato</code> - Formato de salida: "detailed", "summary", "timeline" (por defecto: "detailed")</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>MEMORY issues summary</code>
          </div>
        </div>
      </div>
    </section>

    <section class="command-section">
      <h2>Comandos de Investigación y Verificación</h2>
      
      <div class="command-card">
        <div class="command-name">RESEARCH</div>
        <div class="command-description">
          <p>Realiza investigación automática para un tema específico.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>RESEARCH "tema" [profundidad] nombre_proyecto</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>tema</code> - Tema a investigar (requerido)</li>
              <li><code>profundidad</code> - Nivel de profundidad: "basic", "standard", "exhaustive" (por defecto: "standard")</li>
              <li><code>nombre_proyecto</code> - Proyecto con el que asociar la investigación (requerido)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>RESEARCH "tendencias en microservicios" exhaustive mi_proyecto</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">VERIFY</div>
        <div class="command-description">
          <p>Verifica una fuente de información.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>VERIFY "fuente" tipo [fiabilidad]</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>fuente</code> - URL o referencia de la fuente a verificar (requerido)</li>
              <li><code>tipo</code> - Tipo de fuente: "academic", "technical", "blog", "documentation", "market_research", "user_research" (requerido)</li>
              <li><code>fiabilidad</code> - Nivel de fiabilidad requerido: "high", "medium", "low" (por defecto: "high")</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>VERIFY "https://example.com/research-paper" academic high</code>
          </div>
        </div>
      </div>
    </section>

    <section class="command-section">
      <h2>Comandos de Generación y Gestión</h2>
      
      <div class="command-card">
        <div class="command-name">GENERATE_RULES</div>
        <div class="command-description">
          <p>Genera o actualiza reglas de Cursor desde la documentación.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>GENERATE_RULES nombre_proyecto [tipo_regla]</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>nombre_proyecto</code> - Nombre del proyecto (requerido)</li>
              <li><code>tipo_regla</code> - Tipos de reglas a generar: ["product", "technical", "process", "security", "all"] (por defecto: ["all"])</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>GENERATE_RULES mi_proyecto ["technical", "security"]</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">TEMPLATE</div>
        <div class="command-description">
          <p>Gestiona plantillas de documentación.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>TEMPLATE operación tipo_plantilla [nombre_plantilla]</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>operación</code> - Operación a realizar: "create", "update", "delete", "list", "sync" (requerido)</li>
              <li><code>tipo_plantilla</code> - Tipo de plantilla: "product", "technical", "process", "simplified" (requerido)</li>
              <li><code>nombre_plantilla</code> - Nombre de la plantilla (requerido para algunas operaciones)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>TEMPLATE create technical arquitectura_microservicios</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">GENERATE_MDC</div>
        <div class="command-description">
          <p>Genera un archivo MDC de Cursor a partir de la documentación del proyecto para desarrollo.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>GENERATE_MDC nombre_proyecto [ruta_salida] [incluir_reglas]</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>nombre_proyecto</code> - Nombre del proyecto para generar MDC (requerido)</li>
              <li><code>ruta_salida</code> - Ruta donde guardar el archivo MDC (por defecto: "docs/${nombre_proyecto}/")</li>
              <li><code>incluir_reglas</code> - Si se deben extraer reglas de desarrollo de la documentación (por defecto: true)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>GENERATE_MDC mi_proyecto</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">UPDATE_ADR</div>
        <div class="command-description">
          <p>Actualiza el Registro de Decisiones de Arquitectura basado en cambios recientes.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>UPDATE_ADR nombre_proyecto [auto_detect] [update_status]</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>nombre_proyecto</code> - Nombre del proyecto para actualizar ADR (requerido)</li>
              <li><code>auto_detect</code> - Si se deben detectar automáticamente los cambios arquitectónicos (por defecto: true)</li>
              <li><code>update_status</code> - Si se debe actualizar el estado de las decisiones existentes (por defecto: true)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>UPDATE_ADR mi_proyecto</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">FORCE_RESEARCH</div>
        <div class="command-description">
          <p>Fuerza la investigación automática profunda para un documento sin hacer preguntas.</p>
          <div class="command-usage">
            <h4>Uso:</h4>
            <code>FORCE_RESEARCH nombre_proyecto documento [nivel_fuerza]</code>
          </div>
          <div class="command-args">
            <h4>Argumentos:</h4>
            <ul>
              <li><code>nombre_proyecto</code> - Nombre del proyecto (requerido)</li>
              <li><code>documento</code> - Documento a investigar (ej. 01_market_research.md) (requerido)</li>
              <li><code>nivel_fuerza</code> - Nivel de fuerza a aplicar: "normal", "high", "maximum" (por defecto: "high")</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Ejemplo:</h4>
            <code>FORCE_RESEARCH mi_proyecto 01_market_research.md maximum</code>
          </div>
        </div>
      </div>
    </section>
  </div>
</div>

<style>
  .commands-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }
  
  .commands-header {
    text-align: center;
    margin-bottom: 3rem;
  }
  
  .paella-icon {
    font-size: 6rem;
    margin-bottom: 1rem;
    animation: steam 3s ease-in-out infinite;
  }
  
  @keyframes steam {
    0% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-10px) rotate(5deg); }
    100% { transform: translateY(0) rotate(0deg); }
  }
  
  .commands-intro {
    font-size: 1.2rem;
    max-width: 700px;
    margin: 0 auto;
  }
  
  .command-section {
    margin-bottom: 3rem;
  }
  
  .command-card {
    background-color: var(--gray-50);
    border-radius: var(--border-radius-md);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow-sm);
    border-left: 5px solid var(--paella-orange);
  }
  
  .command-name {
    font-family: monospace;
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--paella-orange);
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--gray-200);
  }
  
  .command-description p {
    margin-bottom: 1rem;
  }
  
  .command-usage, .command-args, .command-example {
    margin-bottom: 1rem;
  }
  
  .command-usage h4, .command-args h4, .command-example h4 {
    font-size: 1rem;
    margin-bottom: 0.5rem;
    color: var(--gray-700);
  }
  
  .command-args ul {
    list-style-type: disc;
    padding-left: 1.5rem;
  }
  
  .command-args li {
    margin-bottom: 0.5rem;
  }
  
  code {
    font-family: monospace;
    background-color: var(--gray-100);
    padding: 0.2rem 0.4rem;
    border-radius: var(--border-radius-sm);
    font-size: 0.9rem;
  }
  
  .command-example code {
    display: block;
    padding: 0.75rem;
    background-color: var(--gray-800);
    color: var(--gray-100);
    border-radius: var(--border-radius-md);
    overflow-x: auto;
  }
  
  @media (max-width: 768px) {
    .command-card {
      padding: 1rem;
    }
    
    .command-name {
      font-size: 1.3rem;
    }
  }
</style> 