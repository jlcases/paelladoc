---
layout: default
title: PAELLADOC Commands
description: Complete guide to all commands available in PAELLADOC and how to use them
---

<div class="commands-container">
  <div class="commands-content">
    <section class="command-section">
      <h2>Main Commands</h2>
      
      <div class="command-card">
        <div class="command-name">PAELLA</div>
        <div class="command-description">
          <p>Initiates the documentation process and generates Cursor rules.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>PAELLA project_name</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>project_name</code> - Name of the project to document (required)</li>
              <li><code>generate_rules</code> - Whether to generate Cursor rules from documentation (default: true)</li>
              <li><code>ai_mode</code> - AI operation mode: "autonomous", "collaborative", or "advisory" (default: "collaborative")</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>PAELLA my_project</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">CONTINUE</div>
        <div class="command-description">
          <p>Continues with an existing project documentation.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>CONTINUE project_name</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>project_name</code> - Name of the project to continue with (required)</li>
              <li><code>update_rules</code> - Whether to update Cursor rules from documentation (default: true)</li>
              <li><code>sync_templates</code> - Whether to synchronize templates with current state (default: true)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>CONTINUE my_project</code>
          </div>
        </div>
      </div>
    </section>
    
    <section class="command-section">
      <h2>Project Management Commands</h2>
      
      <div class="command-card">
        <div class="command-name">ACHIEVEMENT</div>
        <div class="command-description">
          <p>Records an achievement in the project memory.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>ACHIEVEMENT description category [impact_level]</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>description</code> - Description of the achievement (required)</li>
              <li><code>category</code> - Category of the achievement (required): architecture, development, documentation, testing, security, performance, product, design, research</li>
              <li><code>impact_level</code> - Level of impact of the achievement (default: "medium"): high, medium, low</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>ACHIEVEMENT "Implemented responsive design" design high</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">ISSUE</div>
        <div class="command-description">
          <p>Records an issue in the project memory.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>ISSUE description severity area</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>description</code> - Description of the issue (required)</li>
              <li><code>severity</code> - Severity level of the issue (required): critical, high, medium, low</li>
              <li><code>area</code> - Area affected by the issue (required): product, technical, process, security, performance</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>ISSUE "Login page not responsive on mobile" high product</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">DECISION</div>
        <div class="command-description">
          <p>Records a technical decision in the project memory.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>DECISION description impact rationale</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>description</code> - Description of the decision (required)</li>
              <li><code>impact</code> - Areas impacted by the decision (required): architecture, development, documentation, testing, security, performance, product, design, process</li>
              <li><code>rationale</code> - Reasoning behind the decision (required)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>DECISION "Use React for frontend" "architecture,development" "Better component reusability and ecosystem"</code>
          </div>
        </div>
      </div>
    </section>
    
    <section class="command-section">
      <h2>Research and Verification Commands</h2>
      
      <div class="command-card">
        <div class="command-name">RESEARCH</div>
        <div class="command-description">
          <p>Performs automatic research for a specific topic.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>RESEARCH topic depth project_name</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>topic</code> - Topic to research (required)</li>
              <li><code>depth</code> - Research depth level (default: "standard"): basic, standard, exhaustive</li>
              <li><code>project_name</code> - Project to associate research with (required)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>RESEARCH "React state management" exhaustive my_project</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">VERIFY</div>
        <div class="command-description">
          <p>Verifies an information source.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>VERIFY source type [reliability]</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>source</code> - URL or reference of the source to verify (required)</li>
              <li><code>type</code> - Type of source (required): academic, technical, blog, documentation, market_research, user_research</li>
              <li><code>reliability</code> - Required reliability level (default: "high"): high, medium, low</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>VERIFY "https://reactjs.org/docs/hooks-intro.html" documentation high</code>
          </div>
        </div>
      </div>
    </section>
    
    <section class="command-section">
      <h2>Documentation Management Commands</h2>
      
      <div class="command-card">
        <div class="command-name">MEMORY</div>
        <div class="command-description">
          <p>Shows the development record.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>MEMORY [filter] [format]</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>filter</code> - Filter memory by category (default: "all"): all, achievements, issues, decisions, product, technical</li>
              <li><code>format</code> - Output format (default: "detailed"): detailed, summary, timeline</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>MEMORY decisions timeline</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">GENERATE_RULES</div>
        <div class="command-description">
          <p>Generates or updates Cursor rules from documentation.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>GENERATE_RULES project_name [rule_type]</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>project_name</code> - Name of the project (required)</li>
              <li><code>rule_type</code> - Types of rules to generate (default: ["all"]): product, technical, process, security, all</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>GENERATE_RULES my_project technical,security</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">TEMPLATE</div>
        <div class="command-description">
          <p>Manages documentation templates.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>TEMPLATE operation template_type [template_name]</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>operation</code> - Template operation to perform (required): create, update, delete, list, sync</li>
              <li><code>template_type</code> - Type of template (required): product, technical, process, simplified</li>
              <li><code>template_name</code> - Name of the template (optional)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>TEMPLATE list technical</code>
          </div>
        </div>
      </div>
    </section>
    
    <section class="command-section">
      <h2>Advanced Commands</h2>
      
      <div class="command-card">
        <div class="command-name">FORCE_RESEARCH</div>
        <div class="command-description">
          <p>Forces automatic deep research for a document without asking any questions.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>FORCE_RESEARCH project_name document [force_level]</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>project_name</code> - Name of the project (required)</li>
              <li><code>document</code> - Document to research (e.g., 01_market_research.md) (required)</li>
              <li><code>force_level</code> - Level of force to apply to research (default: "high"): normal, high, maximum</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>FORCE_RESEARCH my_project 01_market_research.md maximum</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">UPDATE_ADR</div>
        <div class="command-description">
          <p>Updates the Architecture Decision Record based on recent changes.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>UPDATE_ADR project_name [auto_detect] [update_status]</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>project_name</code> - Name of the project to update ADR for (required)</li>
              <li><code>auto_detect</code> - Whether to automatically detect architectural changes (default: true)</li>
              <li><code>update_status</code> - Whether to update status of existing decisions (default: true)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>UPDATE_ADR my_project true true</code>
          </div>
        </div>
      </div>
      
      <div class="command-card">
        <div class="command-name">GENERATE_MDC</div>
        <div class="command-description">
          <p>Generates a Cursor MDC file from project documentation for development.</p>
          <div class="command-usage">
            <h4>Usage:</h4>
            <code>GENERATE_MDC project_name [output_path] [include_rules]</code>
          </div>
          <div class="command-args">
            <h4>Arguments:</h4>
            <ul>
              <li><code>project_name</code> - Name of the project to generate MDC for (required)</li>
              <li><code>output_path</code> - Path where to save the MDC file (default: "docs/${project_name}/")</li>
              <li><code>include_rules</code> - Whether to extract development rules from documentation (default: true)</li>
            </ul>
          </div>
          <div class="command-example">
            <h4>Example:</h4>
            <code>GENERATE_MDC my_project "docs/my_project/" true</code>
          </div>
        </div>
      </div>
    </section>
  </div>
</div>

<style>
  .commands-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 0;
  }
  
  .commands-content {
    text-align: center;
    margin-bottom: 3rem;
  }
  
  .paella-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
  }
  
  .commands-intro {
    max-width: 800px;
    margin: 0 auto;
    font-size: 1.2rem;
    color: #555;
  }
  
  .command-section {
    margin-bottom: 3rem;
    text-align: left;
  }
  
  .command-section h2 {
    border-bottom: 2px solid #f5821f;
    padding-bottom: 0.5rem;
    margin-bottom: 2rem;
    color: #333;
  }
  
  .command-card {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    margin-bottom: 2rem;
    display: flex;
    flex-direction: column;
  }
  
  @media (min-width: 768px) {
    .command-card {
      flex-direction: row;
    }
  }
  
  .command-name {
    background-color: #f5821f;
    color: white;
    font-weight: bold;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 1rem;
    font-family: monospace;
    font-size: 1.2rem;
    min-width: 150px;
    text-align: center;
  }
  
  @media (min-width: 768px) {
    .command-name {
      margin-right: 1.5rem;
      margin-bottom: 0;
    }
  }
  
  .command-description {
    flex: 1;
  }
  
  .command-description p {
    margin-bottom: 1rem;
    font-size: 1.1rem;
  }
  
  .command-usage, .command-args, .command-example {
    margin-bottom: 1rem;
  }
  
  .command-usage h4, .command-args h4, .command-example h4 {
    font-size: 1rem;
    color: #555;
    margin-bottom: 0.5rem;
  }
  
  .command-args ul {
    padding-left: 1.5rem;
  }
  
  .command-args li {
    margin-bottom: 0.5rem;
  }
  
  code {
    background-color: #f5f5f5;
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: monospace;
    font-size: 0.9rem;
  }
  
  .command-example code {
    display: block;
    padding: 0.5rem;
    background-color: #f5f5f5;
    border-left: 3px solid #f5821f;
  }
</style> 