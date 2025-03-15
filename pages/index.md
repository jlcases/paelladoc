---
layout: default
title: PAELLADOC - Interactive Documentation System
description: Bridge the gap between product and engineering teams with AI-powered documentation that evolves with your project in real-time.
---

<div class="hero-section">
  <div class="container">
    <h1 class="hero-title">🥘 PAELLADOC</h1>
    <p class="hero-description">Bridge the gap between product and engineering teams with AI-powered documentation that evolves with your project in real-time.</p>
    <div class="hero-buttons">
      <a href="https://github.com/jlcases/paelladoc" class="btn btn-primary" target="_blank">View on GitHub</a>
      <a href="#projects" class="btn btn-secondary">Explore Projects</a>
    </div>
  </div>
</div>

<div class="container">
  <section class="about-section">
    <h2>The Art of Product Development: A Paella Masterclass</h2>
    <p>Just as having all the ingredients for a paella isn't enough—only combining them in perfect proportions with a master chef's expertise creates an <strong>unforgettable paella</strong>—the same principle applies to product development.</p>
    
    <div class="paella-metaphor">
      <div class="metaphor-item">
        <h4>🍚 Ingredients</h4>
        <p>Having all the right tools, frameworks, and technologies</p>
      </div>
      <div class="metaphor-item">
        <h4>🔥 Heat</h4>
        <p>The pressure and timeline of development cycles</p>
      </div>
      <div class="metaphor-item">
        <h4>👨‍🍳 Expertise</h4>
        <p>The knowledge and experience of your team</p>
      </div>
      <div class="metaphor-item">
        <h4>📋 Recipe</h4>
        <p>The documentation that guides the entire process</p>
      </div>
    </div>
    
    <p>PAELLADOC is the master chef's recipe book that ensures your product development creates an <strong>unforgettable experience</strong>, combining all elements in perfect harmony.</p>
    
    <h3>Why Traditional Documentation Fails</h3>
    <ul>
      <li><strong>Disconnected tools</strong>: Product teams use Confluence while engineers use GitHub</li>
      <li><strong>Static documentation</strong>: Becomes outdated as soon as development begins</li>
      <li><strong>Implementation gaps</strong>: What's built often differs from what was specified</li>
      <li><strong>Knowledge silos</strong>: Critical context gets lost between teams</li>
    </ul>
    
    <h3>The PAELLADOC Advantage</h3>
    <p>Our integrated approach ensures documentation and implementation stay perfectly aligned:</p>
    
    <div class="advantage-grid">
      <div class="advantage-item">
        <h4>🔄 Real-Time Updates</h4>
        <p>Documentation evolves alongside your code, ensuring specs always reflect reality</p>
      </div>
      
      <div class="advantage-item">
        <h4>🤖 AI-Guided Implementation</h4>
        <p>Cursor follows documentation tasks, helping developers implement exactly what was specified</p>
      </div>
      
      <div class="advantage-item">
        <h4>🔗 Bidirectional Sync</h4>
        <p>Changes in code can update documentation and vice versa, maintaining perfect alignment</p>
      </div>
      
      <div class="advantage-item">
        <h4>👥 Cross-Team Collaboration</h4>
        <p>Product managers and developers work from the same source of truth</p>
      </div>
    </div>
    
    <pre><code>paelladoc/
├── .cursorrules              # The main recipe book
├── .cursor/
│   └── rules/
│       ├── templates/        # Our base recipes
│       ├── scripts/         # Kitchen utensils
│       └── paelladoc.mdc    # The master recipe
├── docs/                    # Our documentary paellas
└── .memory.json            # The chef's notebook</code></pre>
  </section>

  <section id="projects" class="projects-section">
    <h2>Documentation Projects</h2>
    <p>Explore our comprehensive documentation projects. Each project follows the MECE principle to ensure complete and non-redundant documentation.</p>
    
    <div class="projects-grid">
      {% assign projects = site.pages | where_exp: "item", "item.path contains 'projects/'" | where_exp: "item", "item.path != 'projects/index.md'" | group_by_exp: "item", "item.path | split: '/' | slice: 1 | first" %}
      
      {% for project in projects %}
        {% assign project_name = project.name %}
        {% if project_name != "RECUENCO" and project_name != "MALENIO" and project_name != "index" %}
          {% assign index = project.items | where_exp: "item", "item.name contains 'index'" | first %}
          {% if index %}
            <div class="project-card">
              <div class="project-card-header">
                <h3 class="project-card-title">{{ project_name | capitalize }}</h3>
              </div>
              <div class="project-card-body">
                <p class="project-card-description">{{ index.excerpt | strip_html | truncatewords: 25 }}</p>
                <a href="{{ index.url | relative_url }}" class="project-card-link">View Documentation →</a>
              </div>
            </div>
          {% endif %}
        {% endif %}
      {% endfor %}
    </div>
    
    {% assign public_project_count = 0 %}
    {% for project in projects %}
      {% assign project_name = project.name %}
      {% if project_name != "RECUENCO" and project_name != "MALENIO" and project_name != "index" %}
        {% assign public_project_count = public_project_count | plus: 1 %}
      {% endif %}
    {% endfor %}
    
    {% if public_project_count == 0 %}
      <div class="no-projects">
        <p>No hay proyectos públicos disponibles en este momento.</p>
      </div>
    {% endif %}
  </section>
  
  <section class="features-section">
    <h2>Key Features</h2>
    
    <div class="features-grid">
      <div class="feature">
        <h3>Product-Engineering Integration</h3>
        <ul>
          <li>Replace Confluence with living documentation</li>
          <li>Update user stories in real-time</li>
          <li>Track implementation against specifications</li>
          <li>Eliminate cross-team communication barriers</li>
        </ul>
      </div>
      
      <div class="feature">
        <h3>AI-Powered Development</h3>
        <ul>
          <li>Cursor follows documentation tasks automatically</li>
          <li>Contextual assistance based on project specs</li>
          <li>Intelligent implementation suggestions</li>
          <li>Continuous alignment with product vision</li>
        </ul>
      </div>
      
      <div class="feature">
        <h3>Comprehensive Documentation</h3>
        <ul>
          <li>Market research and product definition</li>
          <li>Technical architecture and specifications</li>
          <li>User stories and journey maps</li>
          <li>Architecture Decision Records (ADRs)</li>
        </ul>
      </div>
    </div>
  </section>
  
  <section class="getting-started-section">
    <h2>Getting Started</h2>
    <ol>
      <li><strong>Clone or Fork</strong>: Clone the repository or fork it to your GitHub account</li>
      <li><strong>Open with Cursor</strong>: Open the project with Cursor 0.47 or higher</li>
      <li><strong>Start Cooking</strong>: Simply type <code>PAELLA</code> and follow the interactive conversation</li>
    </ol>
    
    <div class="cta">
      <a href="https://github.com/jlcases/paelladoc" class="btn btn-primary" target="_blank">Get Started Now</a>
    </div>
  </section>
</div> 